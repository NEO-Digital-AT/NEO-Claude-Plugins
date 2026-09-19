#!/usr/bin/env python3
"""Reads the source and finds cross-origin mistakes before anything runs.

Its companion cors-check.py measures a running source. This one works
when nothing is running yet - while the code is being written, which is
where the decision is actually made.

It reports two groups, and the difference between them matters:

    FINDING   certain. It cannot work, or it is a hole. Fix it.
    LOOK      a place where the answer depends on something this script
              cannot see. Somebody has to look. It is NOT a defect.

Mixing the two would make the output worthless, because a tool that
cries wolf gets ignored - and then the real finding is ignored with it.

    cors-scan.py src/
    cors-scan.py . --json
    cors-scan.py app/ tests/ --skip legacy

Exit code is 1 when a finding was found, 0 otherwise. A LOOK alone never
fails the run.

BLIND SPOTS - stated because a checker that hides them is a liar:
  - It does not know the server configuration. Whether an origin is on
    an allowlist is invisible here; measure that with cors-check.py.
  - It does not resolve variables, imports or build steps. An address
    assembled at runtime is not seen.
  - It cannot tell your own host from a foreign one. Absolute addresses
    are reported as something to look at, not as a defect.
  - It reads text, not meaning. A finding inside a comment or a test
    fixture still shows up. The one exception is this file itself, which
    is skipped - it holds every pattern as a literal.

No dependencies beyond the standard library.
"""

import argparse
import json
import os
import re
import sys

FINDING = 'FINDING'
LOOK = 'LOOK'

SKIP_DIRECTORIES = {
    '.git', '.hg', '.svn', 'node_modules', 'dist', 'build', 'out', 'target',
    'vendor', '.venv', 'venv', '__pycache__', 'coverage', '.next', '.nuxt',
    '.output', '.svelte-kit', 'bin', 'obj', '.gradle', '.idea', '.vscode',
}
READ_EXTENSIONS = {
    '.js', '.mjs', '.cjs', '.jsx', '.ts', '.tsx', '.vue', '.svelte', '.astro',
    '.html', '.htm', '.css', '.scss', '.sass', '.less',
    '.php', '.twig', '.py', '.rb', '.go', '.java', '.kt',
    '.cs', '.razor', '.cshtml',
    '.json', '.yml', '.yaml', '.toml', '.ini', '.conf', '.config',
    '.sh', '.bash', '.ps1', '.cmd',
}
MAXIMUM_BYTES = 2 * 1024 * 1024
MAXIMUM_LINE = 2000          # longer means generated or minified

# (level, name, pattern, explanation)
RULES = [
    (FINDING, 'browser security switched off',
     re.compile(r'--disable-web-security|--allow-file-access-from-files'
                r'|--disable-site-isolation-trials'
                r'|--disable-features=[^\s"\']*IsolateOrigins'),
     'What only runs with the browser guard removed does not run. A rig '
     'started this way measures an application that does not exist.'),

    (FINDING, 'public CORS forwarding service',
     re.compile(r'cors-anywhere|allorigins\.win|corsproxy\.io|thingproxy'
                r'|crossorigin\.me|codetabs\.com/v1/proxy'),
     'A foreign server in the middle: foreign availability, foreign '
     'insight into the data. With credentials it is a security incident.'),

    (FINDING, 'wildcard allowance together with credentials',
     re.compile(r'AllowAnyOrigin\s*\(\s*\)(?=[\s\S]{0,400}?AllowCredentials)'
                r'|AllowCredentials\s*\(\s*\)(?=[\s\S]{0,400}?AllowAnyOrigin)'),
     'The browser refuses this combination outright, so it does not work '
     'at all - and many frameworks throw at startup.'),

    (FINDING, 'any origin reflected together with credentials',
     re.compile(r'origin\s*:\s*true(?=[\s\S]{0,200}?credentials\s*:\s*true)'
                r'|credentials\s*:\s*true(?=[\s\S]{0,200}?origin\s*:\s*true)'),
     'Reflecting every origin while allowing credentials means any '
     'foreign page reads in the name of the signed-in user.'),

    (FINDING, 'worker script from a foreign address',
     re.compile(r'new\s+(?:Shared)?Worker\s*\(\s*[\'"`]https?://'),
     'A worker script is not loaded across origins at all. An allowance '
     'does not help; serve the script from your own origin.'),

    (FINDING, 'page loaded from the file system',
     re.compile(r'(?:goto|navigate|url|open)\s*\(\s*[\'"`]file://'),
     'A page from the file system has the origin null. Fonts, modules, '
     'fetches and every allowance fail against it. Serve it over http.'),

    (LOOK, 'canvas or WebGL reads pixels',
     re.compile(r'toDataURL|getImageData|captureStream|texImage2D|readPixels'
                r'|toBlob\s*\('),
     'Everything drawn in here must have been loaded with crossorigin, '
     'or the read throws. Check every source that reaches this surface.'),

    (LOOK, 'font from an absolute address',
     re.compile(r'@font-face[\s\S]{0,300}?url\s*\(\s*[\'"]?https?://'),
     'Fonts are always fetched with an origin check. A foreign font '
     'without an allowance falls back silently - nobody notices.'),

    (LOOK, 'module or script from an absolute address',
     re.compile(r'<script[^>]*type\s*=\s*[\'"]module[\'"][^>]*src\s*=\s*[\'"]https?://'
                r'|import\s*\(\s*[\'"`]https?://'),
     'Module scripts are always fetched with an origin check. Without an '
     'allowance nothing loads.'),

    (LOOK, 'request carries credentials',
     re.compile(r'credentials\s*:\s*[\'"]include[\'"]|withCredentials\s*=\s*true'),
     'Needs both halves: the allowance must name the origin and set '
     'allow-credentials, and the cookie itself must be allowed to travel '
     '(SameSite=None; Secure).'),

    (LOOK, 'allowance written in code',
     re.compile(r'[\'"]?Access-Control-Allow-Origin[\'"]?\s*[:,]'),
     'Origins belong in the configuration, not in the code - otherwise '
     'every environment needs its own build. If the value comes from the '
     'request, the allowlist has to be checked in the same place.'),

    (LOOK, 'media element in the markup',
     re.compile(r'<(?:img|video|audio)\b[^>]*src\s*=\s*[\'"]https?://'),
     'Display alone needs nothing. As soon as the content is evaluated - '
     'canvas, WebGL, Web Audio, a capture - it needs crossorigin and an '
     'allowance.'),
]

CROSSORIGIN_PRESENT = re.compile(r'crossorigin|crossOrigin', re.IGNORECASE)


def readable_files(roots, skip_names):
    # This script carries every pattern it looks for as a literal, so it
    # would always find itself. A checker that reports itself on every
    # run teaches people to ignore it.
    own = os.path.abspath(__file__)
    for root in roots:
        if os.path.isfile(root):
            if os.path.abspath(root) != own:
                yield root
            continue
        for directory, subdirectories, names in os.walk(root):
            subdirectories[:] = [name for name in subdirectories
                                 if name not in SKIP_DIRECTORIES
                                 and name not in skip_names
                                 and not name.startswith('.')]
            for name in sorted(names):
                if os.path.splitext(name)[1].lower() not in READ_EXTENSIONS:
                    continue
                if '.min.' in name:
                    continue
                path = os.path.join(directory, name)
                if os.path.abspath(path) == own:
                    continue
                yield path


def scan_file(path):
    """Returns (list of hits, skipped reason or None)."""
    try:
        if os.path.getsize(path) > MAXIMUM_BYTES:
            return [], 'larger than %d bytes' % MAXIMUM_BYTES
        with open(path, 'r', encoding='utf-8', errors='replace') as handle:
            text = handle.read()
    except OSError as error:
        return [], str(error)

    lines = text.split('\n')
    if lines and max(len(line) for line in lines) > MAXIMUM_LINE:
        return [], 'looks generated or minified'

    file_has_crossorigin = bool(CROSSORIGIN_PRESENT.search(text))
    hits = []
    for level, name, pattern, explanation in RULES:
        for match in pattern.finditer(text):
            # A canvas read in a file that already sets crossorigin
            # everywhere is the normal, correct case - do not nag.
            if name == 'canvas or WebGL reads pixels' and file_has_crossorigin:
                continue
            if name == 'media element in the markup' and file_has_crossorigin:
                continue
            line_number = text.count('\n', 0, match.start()) + 1
            line = lines[line_number - 1].strip()
            hits.append({
                'level': level, 'rule': name, 'file': path,
                'line': line_number,
                'source': line[:160],
                'explanation': explanation,
            })
            break                     # one hit per rule and file is enough
    return hits, None


def main():
    parser = argparse.ArgumentParser(
        description='Finds cross-origin mistakes in the source.')
    parser.add_argument('paths', nargs='+')
    parser.add_argument('--skip', action='append', default=[],
                        metavar='NAME', help='directory name to skip; repeatable')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()

    hits = []
    skipped = []
    counted = 0
    for path in readable_files(args.paths, set(args.skip)):
        counted += 1
        found, reason = scan_file(path)
        hits.extend(found)
        if reason:
            skipped.append({'file': path, 'reason': reason})

    findings = [hit for hit in hits if hit['level'] == FINDING]
    looks = [hit for hit in hits if hit['level'] == LOOK]

    if args.json:
        print(json.dumps({'files': counted, 'findings': findings,
                          'look': looks, 'skipped': skipped}, indent=2))
    else:
        print('cors-scan: %d files read' % counted)
        print()
        if not hits:
            print('Nothing found. No certain mistake, nothing to look at - as '
                  'far as source text can show it.')
        if findings:
            print('FINDINGS - certain, these do not work or are a hole:')
            for hit in findings:
                print('  %s:%d  %s' % (hit['file'], hit['line'], hit['rule']))
                print('      %s' % hit['source'])
                print('      %s' % hit['explanation'])
            print()
        if looks:
            print('LOOK - depends on something this script cannot see. '
                  'Not a defect:')
            for hit in looks:
                print('  %s:%d  %s' % (hit['file'], hit['line'], hit['rule']))
                print('      %s' % hit['source'])
                print('      %s' % hit['explanation'])
            print()
        if skipped:
            print('Skipped: %d file(s) (generated, minified or too large).'
                  % len(skipped))
        print('%d finding(s), %d place(s) to look at.'
              % (len(findings), len(looks)))
        print('What this cannot see is listed at the top of this script - '
              'the server configuration is measured with cors-check.py.')

    return 1 if findings else 0


if __name__ == '__main__':
    sys.exit(main())
