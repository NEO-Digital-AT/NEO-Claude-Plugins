#!/usr/bin/env python3
"""Measures whether a browser at ORIGIN may actually use a resource.

"The header is configured" is not a measurement. This script asks the
running source the same two questions a browser asks — the preflight and
the real request — reads every cross-origin header that comes back, and
reports the cases a browser will refuse.

It is deliberately one-sided: it never claims a resource works, only that
it found nothing that blocks it. What it cannot see is listed under
BLIND SPOTS below.

    cors-check.py https://api.example.at/v1/orders --origin https://app.example.at
    cors-check.py https://api.example.at/v1/orders --origin https://app.example.at \
                  --method POST --header content-type:application/json \
                  --header authorization --credentials
    cors-check.py https://media.example.at/photo.jpg \
                  --origin https://app.example.at --media
    cors-check.py <url> --origin <origin> --expect-header content-disposition --json

Exit code is 1 when a blocker was found, 0 otherwise, so the script works
as a gate in a pipeline.

SAFETY: a method other than GET, HEAD or OPTIONS is NOT sent unless
--send-actual is given. The preflight alone is harmless; the real request
may create or delete something. Without it the preflight is still
measured and the script says what it skipped.

BLIND SPOTS
  - It sees one source at one moment. A cache, a CDN node or a second
    server behind the same name may answer differently.
  - It cannot know whether the markup sets `crossorigin`. For media that
    is half the answer; the other half is in the page (browser.md).
  - It does not judge whether an origin SHOULD be allowed. An origin
    that is reflected without being checked looks correct here and is a
    security finding — see the reflection note in the output.

No dependencies beyond the standard library.
"""

import argparse
import json
import sys
import urllib.error
import urllib.request

BLOCKER = 'BLOCKER'
WARNING = 'WARNING'
NOTE = 'NOTE'

# Headers a browser sends without asking permission first.
SAFELISTED_REQUEST_HEADERS = {
    'accept', 'accept-language', 'content-language', 'content-type', 'range',
}
SIMPLE_CONTENT_TYPES = {
    'application/x-www-form-urlencoded', 'multipart/form-data', 'text/plain',
}
SIMPLE_METHODS = {'GET', 'HEAD', 'POST'}
# Response headers JavaScript may read without Access-Control-Expose-Headers.
SAFELISTED_RESPONSE_HEADERS = {
    'cache-control', 'content-language', 'content-length', 'content-type',
    'expires', 'last-modified', 'pragma',
}
UNSAFE_METHODS = {'POST', 'PUT', 'PATCH', 'DELETE'}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    """Keeps redirects visible instead of silently following them."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def parse_header_argument(raw):
    """"name" or "name:value" -> (lowercase name, value or None)."""
    if ':' in raw:
        name, value = raw.split(':', 1)
        return name.strip().lower(), value.strip()
    return raw.strip().lower(), None


def needs_preflight(method, headers):
    """Tells whether the browser would ask permission before the request."""
    reasons = []
    if method.upper() not in SIMPLE_METHODS:
        reasons.append('method %s is not GET, HEAD or POST' % method.upper())
    for name, value in headers:
        if name not in SAFELISTED_REQUEST_HEADERS:
            reasons.append('header %s is not safelisted' % name)
        elif name == 'content-type':
            if value is None:
                reasons.append(
                    'content-type given without a value - assuming a type '
                    'that triggers a preflight; pass '
                    '--header content-type:<value> to be exact')
            elif value.split(';')[0].strip().lower() not in SIMPLE_CONTENT_TYPES:
                reasons.append('content-type %s is not a simple type' % value)
    return reasons


def request(url, method, headers, timeout):
    """Performs one request and returns (status, headers, error or None)."""
    opener = urllib.request.build_opener(NoRedirect)
    req = urllib.request.Request(url, method=method)
    for name, value in headers.items():
        req.add_header(name, value)
    try:
        with opener.open(req, timeout=timeout) as response:
            return response.status, response.headers, None
    except urllib.error.HTTPError as error:
        # 3xx and 4xx still carry the headers we want to look at.
        return error.code, error.headers, None
    except Exception as error:                      # noqa: BLE001 - reported
        return None, None, '%s: %s' % (type(error).__name__, error)


def values(headers, name):
    """All values of a header, split on commas, lowercase names kept intact."""
    if headers is None:
        return []
    raw = headers.get_all(name) or []
    out = []
    for entry in raw:
        out.extend(part.strip() for part in entry.split(',') if part.strip())
    return out


def check_allow_origin(headers, origin, credentials, stage, findings):
    """The core rule: exactly one allowed origin, and it must match."""
    raw = headers.get_all('Access-Control-Allow-Origin') or []
    if not raw:
        findings.append((BLOCKER, '%s: no Access-Control-Allow-Origin - the '
                                  'browser discards this response' % stage))
        return None
    if len(raw) > 1:
        findings.append((BLOCKER, '%s: Access-Control-Allow-Origin sent %d '
                                  'times (%s) - a duplicate header is invalid; '
                                  'usually the application and a proxy both '
                                  'set it' % (stage, len(raw), ', '.join(raw))))
        return None
    allowed = raw[0].strip()
    if ',' in allowed:
        findings.append((BLOCKER, '%s: Access-Control-Allow-Origin carries a '
                                  'list (%s) - only one origin or * is valid'
                                  % (stage, allowed)))
        return None
    if allowed == '*':
        if credentials:
            findings.append((BLOCKER, '%s: Access-Control-Allow-Origin is * and '
                                      'the request carries credentials - the '
                                      'browser refuses this combination'
                                      % stage))
    elif allowed != origin:
        findings.append((BLOCKER, '%s: Access-Control-Allow-Origin is %s, the '
                                  'page runs on %s - no match, the browser '
                                  'discards the response'
                                  % (stage, allowed, origin)))
    return allowed


def check_vary(headers, allowed, origin, stage, findings):
    """A reflected origin without Vary breaks behind any shared cache."""
    if allowed is None or allowed == '*' or allowed != origin:
        return
    vary = [value.lower() for value in values(headers, 'Vary')]
    if '*' in vary or 'origin' in vary:
        return
    findings.append((WARNING, '%s: the origin is reflected but Vary: Origin is '
                              'missing - a shared cache or CDN will hand the '
                              'wrong allowance to the next visitor' % stage))


def check_credentials(headers, credentials, stage, findings):
    if not credentials:
        return
    allow = values(headers, 'Access-Control-Allow-Credentials')
    if not allow or allow[0].strip().lower() != 'true':
        findings.append((BLOCKER, '%s: the request carries credentials but '
                                  'Access-Control-Allow-Credentials: true is '
                                  'missing - the browser discards the response'
                                  % stage))


def check_preflight(headers, status, method, request_headers, credentials,
                    findings):
    if status is None or not 200 <= status < 300:
        if status is not None and 300 <= status < 400:
            findings.append((BLOCKER, 'preflight: answered with a redirect '
                                      '(%d) - a preflight may not redirect'
                                      % status))
        else:
            findings.append((BLOCKER, 'preflight: answered with %s - it must '
                                      'be 2xx. A 401 or 403 means the '
                                      'OPTIONS request runs through the '
                                      'authentication filter; a 405 means it '
                                      'is not routed at all'
                                      % (status if status else 'no response')))
        return
    allowed_methods = {value.upper() for value in
                       values(headers, 'Access-Control-Allow-Methods')}
    if '*' in allowed_methods and credentials:
        findings.append((BLOCKER, 'preflight: Access-Control-Allow-Methods is '
                                  '* while credentials are used - with '
                                  'credentials the * is taken literally, so '
                                  'name every method'))
    elif '*' not in allowed_methods and method.upper() not in allowed_methods:
        findings.append((BLOCKER, 'preflight: %s is not in '
                                  'Access-Control-Allow-Methods (%s)'
                                  % (method.upper(),
                                     ', '.join(sorted(allowed_methods)) or 'empty')))
    allowed_headers = {value.lower() for value in
                       values(headers, 'Access-Control-Allow-Headers')}
    for name, _ in request_headers:
        if name in allowed_headers:
            continue
        if '*' in allowed_headers and not credentials:
            continue
        if '*' in allowed_headers and credentials:
            findings.append((BLOCKER, 'preflight: Access-Control-Allow-Headers '
                                      'is * while credentials are used - the '
                                      '* is taken literally then; name %s'
                                      % name))
            continue
        findings.append((BLOCKER, 'preflight: header %s is not in '
                                  'Access-Control-Allow-Headers (%s)'
                                  % (name, ', '.join(sorted(allowed_headers))
                                     or 'empty')))
    if not values(headers, 'Access-Control-Max-Age'):
        findings.append((NOTE, 'preflight: no Access-Control-Max-Age - every '
                               'single request pays for a second round trip'))


def check_expose(headers, expected, credentials, findings):
    exposed = {value.lower() for value in
               values(headers, 'Access-Control-Expose-Headers')}
    for name in expected:
        if name in SAFELISTED_RESPONSE_HEADERS or name in exposed:
            continue
        if '*' in exposed and not credentials:
            continue
        findings.append((BLOCKER, 'response: %s is not exposed - the value is '
                                  'null in JavaScript even though the '
                                  'developer tools show it' % name))


def check_media(headers, findings):
    """Extra rules for a resource that ends up in a canvas, WebGL or audio."""
    corp = values(headers, 'Cross-Origin-Resource-Policy')
    if corp and corp[0].strip().lower() in ('same-origin', 'same-site'):
        findings.append((WARNING, 'media: Cross-Origin-Resource-Policy is %s - '
                                  'this blocks embedding independently of '
                                  'CORS, and always under '
                                  'Cross-Origin-Embedder-Policy: require-corp'
                                  % corp[0].strip()))
    if not values(headers, 'Timing-Allow-Origin'):
        findings.append((NOTE, 'media: no Timing-Allow-Origin - load timings '
                               'stay hidden from any measurement in the page'))
    findings.append((NOTE, 'media: the allowance above is only half of it - '
                           'the element must also carry crossorigin, set '
                           'BEFORE src, or the canvas is tainted anyway'))


def check_reflection_hint(allowed, origin, findings):
    if allowed is not None and allowed == origin:
        findings.append((NOTE, 'the source returned exactly the origin that '
                               'was asked for. That is correct behaviour for '
                               'a checked allowlist and identical on the wire '
                               'to reflecting any origin unchecked - this '
                               'script cannot tell the two apart. Verify the '
                               'allowlist in the configuration'))


def main():
    parser = argparse.ArgumentParser(
        description='Measures the cross-origin allowance of one resource.')
    parser.add_argument('url')
    parser.add_argument('--origin', required=True,
                        help='origin the page runs under, e.g. https://app.example.at')
    parser.add_argument('--method', default='GET',
                        help='method the code uses (default GET)')
    parser.add_argument('--header', action='append', default=[],
                        metavar='NAME[:VALUE]',
                        help='request header the code sends; repeatable')
    parser.add_argument('--credentials', action='store_true',
                        help='the request carries cookies or credentials')
    parser.add_argument('--media', action='store_true',
                        help='the resource is used in a canvas, WebGL or Web Audio')
    parser.add_argument('--expect-header', action='append', default=[],
                        metavar='NAME',
                        help='response header the code must read; repeatable')
    parser.add_argument('--send-actual', action='store_true',
                        help='also send a non-GET request (it may change data)')
    parser.add_argument('--timeout', type=float, default=10.0)
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()

    origin = args.origin.rstrip('/')
    method = args.method.upper()
    headers = [parse_header_argument(entry) for entry in args.header]
    expected = [name.strip().lower() for name in args.expect_header]
    findings = []
    steps = []

    preflight_reasons = needs_preflight(method, headers)
    if preflight_reasons:
        request_headers = {
            'Origin': origin,
            'Access-Control-Request-Method': method,
        }
        if headers:
            request_headers['Access-Control-Request-Headers'] = ', '.join(
                name for name, _ in headers)
        status, response_headers, error = request(
            args.url, 'OPTIONS', request_headers, args.timeout)
        steps.append({'step': 'preflight', 'status': status, 'error': error,
                      'reasons': preflight_reasons})
        if error:
            findings.append((BLOCKER, 'preflight: request failed - %s' % error))
        else:
            allowed = check_allow_origin(response_headers, origin,
                                         args.credentials, 'preflight',
                                         findings)
            check_vary(response_headers, allowed, origin, 'preflight', findings)
            check_credentials(response_headers, args.credentials, 'preflight',
                              findings)
            check_preflight(response_headers, status, method, headers,
                            args.credentials, findings)
    else:
        steps.append({'step': 'preflight', 'status': None, 'error': None,
                      'reasons': ['not needed - this is a simple request']})

    probe_method = method
    skipped = None
    if method in UNSAFE_METHODS and not args.send_actual:
        probe_method = 'GET'
        skipped = ('the real %s was not sent because it may change data; '
                   'a GET was used to read the response headers. Pass '
                   '--send-actual to send the real method' % method)

    request_headers = {'Origin': origin}
    for name, value in headers:
        if value is not None:
            request_headers[name] = value
    status, response_headers, error = request(
        args.url, probe_method, request_headers, args.timeout)
    steps.append({'step': 'request', 'method': probe_method, 'status': status,
                  'error': error, 'skipped': skipped})

    if error:
        findings.append((BLOCKER, 'request: failed - %s' % error))
    else:
        if 300 <= status < 400:
            findings.append((WARNING, 'request: answered with a redirect (%d) '
                                      '- the target of the redirect needs the '
                                      'allowance as well' % status))
        allowed = check_allow_origin(response_headers, origin,
                                     args.credentials, 'response', findings)
        check_vary(response_headers, allowed, origin, 'response', findings)
        check_credentials(response_headers, args.credentials, 'response',
                          findings)
        check_expose(response_headers, expected, args.credentials, findings)
        if args.media:
            check_media(response_headers, findings)
        check_reflection_hint(allowed, origin, findings)

    blockers = [text for level, text in findings if level == BLOCKER]

    if args.json:
        print(json.dumps({
            'url': args.url, 'origin': origin, 'method': method,
            'steps': steps,
            'findings': [{'level': level, 'message': text}
                         for level, text in findings],
            'blockers': len(blockers),
        }, indent=2))
    else:
        print('cors-check: %s' % args.url)
        print('  origin  %s' % origin)
        print('  method  %s%s' % (method, '' if not skipped else '  (probed with GET)'))
        for step in steps:
            detail = step.get('reasons') or []
            print('  %-9s %s%s' % (
                step['step'],
                step['status'] if step['status'] is not None else '-',
                '   ' + '; '.join(detail) if detail else ''))
        if skipped:
            print('  note      %s' % skipped)
        print()
        if not findings:
            print('Nothing found that a browser would refuse.')
        for level, text in findings:
            print('  [%s] %s' % (level, text))
        print()
        print('%d blocker(s), %d warning(s), %d note(s).' % (
            len(blockers),
            len([1 for level, _ in findings if level == WARNING]),
            len([1 for level, _ in findings if level == NOTE])))

    return 1 if blockers else 0


if __name__ == '__main__':
    sys.exit(main())
