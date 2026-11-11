"""Checks a Contao extension (bundle) before it is released.

A bundle is sold to other agencies and their customers. Nothing in it may
point back to the people or the company that built it, every back-end
language must be complete, and the README must tell a stranger how to
install and use it. This script checks exactly that:

1. Neutrality: forbidden names (--forbid, repeatable or comma-separated; whole words, so
   "Erich" does not hit "Bericht"), e-mail addresses outside the reserved
   example domains (example.com/.org/.net), phone numbers. Put the
   author's domain into --forbid as well. The author may appear in LICENSE,
   the "authors" block of composer.json and the labels of its menu group
   ($GLOBALS['TL_LANG']['MOD'], ['FMD'] and ['CTE'] in
   contao/languages/*/modules.php). --allow
   names a file for the two exceptions of the rule in the shared base
   bundle: the credit line of the free edition and the address of the
   licence service; e-mail and phone checks still apply there.
2. Back-end languages: contao/languages/<lang>/ exists for every required
   language, with the same files and the same keys as the reference
   language (en).
3. Front-end texts: translations/<domain>.<lang>.yaml exists for every
   required language with the same keys as the English file.
4. Package: composer.json has type contao-bundle, a license, PSR-4
   autoloading and a Contao Manager plugin; README.md, CHANGELOG.md and
   LICENSE exist.
5. README: an English part first, then a German part; both describe the
   installation and link to the documentation (docs/en/, docs/de/).
6. Documentation shipped with the bundle: docs/en/ and docs/de/ with the
   required pages (installation, setup, permissions, usage, privacy,
   troubleshooting), the same file names in both languages, a README.md
   in every folder that links each page of the folder, and no local link
   or image that points to a missing file.

    bundle-check.py path/to/bundle
    bundle-check.py path/to/bundle --forbid "Jane Doe" --forbid "Acme Ltd"
    bundle-check.py path/to/bundle --forbid acme.example --allow public/credit.js
    bundle-check.py path/to/bundle --json

Exit code 0 when nothing was found, 1 on findings, 2 when the path is not
a bundle.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

LANGUAGES = ("en", "de", "fr", "nl", "it", "pl", "cs", "hu", "sl", "hr", "es")
REFERENCE = "en"
TEXT_SUFFIXES = {".php", ".twig", ".html", ".js", ".css", ".scss", ".yaml", ".yml", ".json", ".md", ".xlf", ".txt", ".svg"}
SKIP_DIRS = {".git", "vendor", "node_modules", "dev", "var", "tests"}
EXAMPLE_DOMAINS = ("example.com", "example.org", "example.net")
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@([A-Za-z0-9-]+\.)+[A-Za-z]{2,}")
PHONE = re.compile(r"(?<![\w.])(?:\+\d{2}[\s/-]?)?\(?0\d{2,4}\)?[\s/-]\d{3,}[\s-]?\d{2,}(?![\w.])")
# The menu group of the extension may carry the brand: lines that set a label of the back-end menu (MOD) or of the
# groups in the lists of front-end modules (FMD) and content elements (CTE).
MENU_LINE = re.compile(r"""\$GLOBALS\[\s*'TL_LANG'\s*\]\s*\[\s*'(?:MOD|FMD|CTE)'\s*\]""")
PHP_KEY = re.compile(r"""\[\s*'([^']+)'\s*\](?:\s*\[\s*'([^']+)'\s*\])?(?:\s*\[\s*'([^']+)'\s*\])?\s*=""")


def text_files(root: pathlib.Path):
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES and not (set(path.relative_to(root).parts[:-1]) & SKIP_DIRS):
            yield path


def is_example(domain: str) -> bool:
    domain = domain.lower().rstrip(".")
    return any(domain == d or domain.endswith("." + d) for d in EXAMPLE_DOMAINS)


def term_pattern(term: str) -> re.Pattern[str]:
    left = r"(?<!\w)" if term[:1].isalnum() else ""
    right = r"(?!\w)" if term[-1:].isalnum() else ""
    return re.compile(left + re.escape(term) + right, re.IGNORECASE)


def check_neutrality(root: pathlib.Path, forbid: list[str], allow: list[str] | None = None) -> list[str]:
    findings = []
    # Files named with --allow may carry the names (only the exceptions of the rule); e-mail and phone checks still apply.
    allowed = {pathlib.PurePosixPath(value.strip()).as_posix() for value in (allow or []) if value.strip()}
    # "--forbid 'A, B'" is two names: a single option with commas was read as one name before and found nothing.
    terms = [term.strip() for value in forbid for term in value.split(",")]
    patterns = [(term, term_pattern(term)) for term in terms if term]

    for path in text_files(root):
        rel = path.relative_to(root).as_posix()

        if rel == "LICENSE":
            continue

        text = path.read_text(encoding="utf-8", errors="replace")

        if rel == "composer.json":
            try:
                data = json.loads(text)
            except json.JSONDecodeError:
                findings.append("composer.json: not valid JSON")
                continue
            data.pop("authors", None)
            text = json.dumps(data, ensure_ascii=False, indent=1)

        menu = re.fullmatch(r"contao/languages/[^/]+/modules\.php", rel) is not None

        for number, line in enumerate(text.splitlines(), 1):
            for term, pattern in patterns:
                if rel in allowed or (menu and MENU_LINE.search(line)):
                    continue
                if pattern.search(line):
                    findings.append(f"{rel}:{number}: forbidden name \"{term}\"")
            for match in EMAIL.finditer(line):
                domain = match.group(0).split("@", 1)[1].lower()
                if not is_example(domain) and not domain.endswith((".png", ".svg", ".jpg", ".webp")):
                    findings.append(f"{rel}:{number}: e-mail address \"{match.group(0)}\" outside the example domains (use name@example.com)")
            if path.suffix in {".php", ".yaml", ".yml", ".md", ".twig"} and PHONE.search(line):
                findings.append(f"{rel}:{number}: looks like a real phone number \"{PHONE.search(line).group(0).strip()}\"")

    return findings


def php_keys(path: pathlib.Path) -> set[str]:
    keys = set()
    for match in PHP_KEY.finditer(path.read_text(encoding="utf-8", errors="replace")):
        keys.add(".".join(part for part in match.groups() if part))
    return keys


def check_backend_languages(root: pathlib.Path) -> list[str]:
    base = root / "contao" / "languages"
    if not base.is_dir():
        return []

    findings = []
    reference = base / REFERENCE
    if not reference.is_dir():
        return [f"contao/languages/{REFERENCE}/ missing (reference language)"]

    ref_files = {p.name: php_keys(p) for p in reference.glob("*.php")}

    for lang in LANGUAGES:
        folder = base / lang
        if not folder.is_dir():
            findings.append(f"contao/languages/{lang}/ missing")
            continue
        for name, keys in ref_files.items():
            other = folder / name
            if not other.is_file():
                findings.append(f"contao/languages/{lang}/{name} missing")
                continue
            missing = sorted(keys - php_keys(other))
            for key in missing[:10]:
                findings.append(f"contao/languages/{lang}/{name}: key \"{key}\" missing")
            if len(missing) > 10:
                findings.append(f"contao/languages/{lang}/{name}: {len(missing) - 10} more keys missing")

    return findings


def yaml_keys(path: pathlib.Path) -> set[str]:
    """Key paths of a plain YAML mapping file (block style, any indent width)."""
    keys, stack, block_indent = set(), [], None
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        indent = len(raw) - len(raw.lstrip())
        if block_indent is not None:
            # inside a block scalar (| or >): its lines are text, not keys
            if not raw.strip() or indent > block_indent:
                continue
            block_indent = None
        if not raw.strip() or raw.lstrip().startswith("#") or raw.lstrip().startswith("- "):
            continue
        match = re.match(r"^(\s*)([^\s:#'\"][^:]*?|'[^']*'|\"[^\"]*\"):(\s+(.*))?$", raw)
        if not match:
            continue
        while stack and stack[-1][0] >= indent:
            stack.pop()
        stack.append((indent, match.group(2).strip("'\"")))
        keys.add(".".join(key for _, key in stack))
        if re.match(r"^[|>][-+0-9]*\s*(#.*)?$", (match.group(4) or "").strip()):
            block_indent = indent
    return keys


def check_frontend_texts(root: pathlib.Path) -> list[str]:
    base = root / "translations"
    if not base.is_dir():
        return []

    findings = []
    domains = sorted({p.name.rsplit(".", 2)[0] for p in base.glob("*.yaml")})

    for domain in domains:
        reference = base / f"{domain}.{REFERENCE}.yaml"
        if not reference.is_file():
            findings.append(f"translations/{domain}.{REFERENCE}.yaml missing (reference language)")
            continue
        keys = yaml_keys(reference)
        for lang in LANGUAGES:
            other = base / f"{domain}.{lang}.yaml"
            if not other.is_file():
                findings.append(f"translations/{domain}.{lang}.yaml missing")
                continue
            missing = sorted(keys - yaml_keys(other))
            for key in missing[:10]:
                findings.append(f"translations/{domain}.{lang}.yaml: key \"{key}\" missing")
            if len(missing) > 10:
                findings.append(f"translations/{domain}.{lang}.yaml: {len(missing) - 10} more keys missing")

    return findings


def check_package(root: pathlib.Path) -> list[str]:
    findings = []
    for name in ("README.md", "CHANGELOG.md", "LICENSE", "composer.json"):
        if not (root / name).is_file():
            findings.append(f"{name} missing")

    try:
        data = json.loads((root / "composer.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return findings

    if data.get("type") != "contao-bundle":
        findings.append("composer.json: \"type\" must be \"contao-bundle\"")
    if not data.get("license"):
        findings.append("composer.json: \"license\" missing")
    if not data.get("autoload", {}).get("psr-4"):
        findings.append("composer.json: PSR-4 autoloading missing")
    if not data.get("extra", {}).get("contao-manager-plugin"):
        findings.append("composer.json: \"extra.contao-manager-plugin\" missing")
    if not data.get("description"):
        findings.append("composer.json: \"description\" missing")

    return findings


def check_readme(root: pathlib.Path) -> list[str]:
    path = root / "README.md"
    if not path.is_file():
        return []

    text = path.read_text(encoding="utf-8", errors="replace")
    findings = []
    english = re.search(r"^#{1,2} .*\binstall", text, re.IGNORECASE | re.MULTILINE)
    german = re.search(r"^#{1,2} .*(installation|einrichten|einrichtung)\b", text, re.IGNORECASE | re.MULTILINE)
    german_part = re.search(r"^# .*(deutsch|\(de\))", text, re.IGNORECASE | re.MULTILINE)

    if not english:
        findings.append("README.md: no English installation section (## Installation)")
    if not german_part:
        findings.append("README.md: no German part (a top-level heading containing \"Deutsch\" after the English part)")
    elif english and english.start() > german_part.start():
        findings.append("README.md: the German part comes before the English one (English first, then German)")
    if german_part and not re.search(r"^#{2} .*(installation|einrichten|einrichtung)", text[german_part.start():], re.IGNORECASE | re.MULTILINE):
        findings.append("README.md: the German part has no installation section")

    english_text = text[: german_part.start()] if german_part else text
    german_text = text[german_part.start():] if german_part else ""
    if not re.search(r"\]\((\./)?docs/en/", english_text):
        findings.append("README.md: the English part does not link to the documentation (docs/en/README.md)")
    if german_part and not re.search(r"\]\((\./)?docs/de/", german_text):
        findings.append("README.md: the German part does not link to the documentation (docs/de/README.md)")

    return findings


# Pages every bundle documents, in docs/<lang>/ ("usage" may be a folder with a README.md).
REQUIRED_PAGES = ("installation", "setup", "permissions", "usage", "privacy", "troubleshooting")
DOC_LANGUAGES = ("en", "de")
LINK = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")


def local_target(link: str) -> str | None:
    """The file part of a relative link, None for web addresses, mail links and anchors."""
    if re.match(r"^[a-z][a-z0-9+.-]*:", link, re.IGNORECASE) or link.startswith("#") or link.startswith("/"):
        return None
    return link.split("#", 1)[0].split("?", 1)[0] or None


def check_docs(root: pathlib.Path) -> list[str]:
    docs = root / "docs"
    findings = []
    if not (docs / "README.md").is_file():
        findings.append("docs/README.md missing (entry point: languages, where to start)")

    pages: dict[str, set[str]] = {}
    for lang in DOC_LANGUAGES:
        base = docs / lang
        if not base.is_dir():
            findings.append(f"docs/{lang}/ missing")
            continue

        pages[lang] = {str(path.relative_to(base)) for path in base.rglob("*.md")}
        for page in REQUIRED_PAGES:
            if f"{page}.md" not in pages[lang] and f"{page}/README.md" not in pages[lang]:
                findings.append(f"docs/{lang}/{page}.md missing")

        # Every folder has a README.md that links each page in it.
        for folder in sorted({base, *(path.parent for path in base.rglob("*.md"))}):
            index = folder / "README.md"
            rel = folder.relative_to(docs)
            if not index.is_file():
                findings.append(f"docs/{rel}/README.md missing (table of contents)")
                continue
            linked = {local_target(link) for link in LINK.findall(index.read_text(encoding="utf-8", errors="replace"))}
            linked = {pathlib.PurePosixPath(link).as_posix().removeprefix("./") for link in linked if link}
            for page in sorted(folder.glob("*.md")):
                if page.name != "README.md" and page.name not in linked:
                    findings.append(f"docs/{rel}/README.md does not link {page.name}")
            for sub in sorted(path for path in folder.iterdir() if path.is_dir() and (path / "README.md").is_file()):
                if f"{sub.name}/README.md" not in linked and f"{sub.name}/" not in linked:
                    findings.append(f"docs/{rel}/README.md does not link {sub.name}/README.md")

    if len(pages) == len(DOC_LANGUAGES):
        reference = pages[DOC_LANGUAGES[0]]
        for lang in DOC_LANGUAGES[1:]:
            for missing in sorted(reference - pages[lang]):
                findings.append(f"docs/{lang}/{missing} missing (exists in docs/{DOC_LANGUAGES[0]}/)")
            for extra in sorted(pages[lang] - reference):
                findings.append(f"docs/{DOC_LANGUAGES[0]}/{extra} missing (exists in docs/{lang}/)")

    # Local links and images must point to existing files.
    if docs.is_dir():
        for path in sorted(docs.rglob("*.md")):
            for link in LINK.findall(path.read_text(encoding="utf-8", errors="replace")):
                target = local_target(link)
                if target and not (path.parent / target).exists():
                    findings.append(f"{path.relative_to(root)}: link to missing file {target}")

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("path", help="root folder of the bundle (where composer.json is)")
    parser.add_argument("--forbid", action="append", default=[], help="name that must not appear (person, company, domain); repeatable, or several separated by commas")
    parser.add_argument("--allow", action="append", default=[], help="file (relative to the bundle) where the forbidden names may appear; only for the exceptions of the rule (credit line of the free edition, address of the licence service); repeatable")
    parser.add_argument("--json", action="store_true", help="print the findings as JSON")
    args = parser.parse_args()

    root = pathlib.Path(args.path).resolve()
    if not (root / "composer.json").is_file():
        print(f"{root}: no composer.json, not a bundle", file=sys.stderr)
        return 2

    groups = {
        "neutrality": check_neutrality(root, args.forbid, args.allow),
        "backend_languages": check_backend_languages(root),
        "frontend_texts": check_frontend_texts(root),
        "package": check_package(root),
        "readme": check_readme(root),
        "docs": check_docs(root),
    }

    if args.json:
        print(json.dumps(groups, indent=2, ensure_ascii=False))
    else:
        for group, findings in groups.items():
            print(f"{group}: {'ok' if not findings else f'{len(findings)} finding(s)'}")
            for finding in findings:
                print(f"  {finding}")
            if group == "neutrality" and args.allow:
                print("  allowed by --allow: " + ", ".join(args.allow))

    return 1 if any(groups.values()) else 0


if __name__ == "__main__":
    sys.exit(main())
