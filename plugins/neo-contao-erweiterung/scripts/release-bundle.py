"""Builds the public release of a Contao extension (bundle) from its developer repository.

The developer repository holds everything used while building the bundle:
notes for agents, drafts, test benches, tools. The public repository and the
ZIP that customers upload in the Contao Manager hold only the package. This
script makes that copy and refuses when it is not clean:

1. Export: `git archive` of the given ref, so `.gitattributes` decides what
   stays out (`export-ignore`). Uncommitted changes are never released.
2. Hints: no CLAUDE.md, no .claude/ folder, no mention of an AI coding agent
   or its plugins, session links or co-author lines in any text file
   (--allow-word for terms the product itself uses, e.g. a crawler name).
3. Package: composer.json is valid, of type contao-bundle, has a licence, a
   Contao Manager plugin and no "version" (Packagist reads the git tag);
   contao/manager-plugin is a dev requirement with a conflict rule, as the
   Contao documentation asks; homepage and support point to the public
   repository (--repo-url).
4. Changelog: CHANGELOG.md has a section for the version and no non-empty
   "Unreleased" section.
5. bundle-check.py (next to this script) on the exported files, with the
   given --forbid and --allow.

When everything passes, it writes the ZIP for the Contao Manager (files at
the root, composer.json with the version added, which the Manager needs) to
--out, and with --target it replaces the working tree of a local clone of
the public repository by the export, commits it as "Release <version>" with
the given --author (author and committer) and tags it v<version>. It never
pushes; it prints the push command.

    release-bundle.py ../NEO-Contao-Basic --version 1.0.0 \\
        --repo-url https://github.com/acme/contao-basic-bundle --out ../dist
    release-bundle.py ../NEO-Contao-Basic --version 1.0.0 \\
        --repo-url https://github.com/acme/contao-basic-bundle --out ../dist \\
        --target ../contao-basic-bundle --author "Acme <noreply@example.com>" \\
        --forbid "Jane Doe" --allow public/credit.js

Exit code 0 when the release was built, 1 on findings, 2 on wrong use.
"""
from __future__ import annotations

import argparse
import io
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import zipfile

SEMVER = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$")
AUTHOR = re.compile(r"^(?P<name>[^<>]+?)\s*<(?P<email>[^<>@\s]+@[^<>\s]+)>$")
HINT_FILES = ("CLAUDE.md", "AGENTS.md")
HINT_DIRS = (".claude",)
HINTS = (
    re.compile(r"claude", re.IGNORECASE),
    re.compile(r"anthropic", re.IGNORECASE),
    re.compile(r"co-authored-by", re.IGNORECASE),
    re.compile(r"session_[0-9A-Za-z]{10,}"),
)
TEXT_SUFFIXES = {".php", ".twig", ".html", ".js", ".mjs", ".cjs", ".css", ".scss", ".yaml", ".yml", ".json", ".md", ".xlf", ".txt", ".svg", ".xml", ".neon", ".dist", ""}
MANAGER_PLUGIN = "contao/manager-plugin"
MANAGER_CONFLICT = "<2.0 || >=3.0"


def run(args: list[str], cwd: pathlib.Path, env: dict[str, str] | None = None) -> str:
    result = subprocess.run(args, cwd=cwd, env=env, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"{' '.join(args)} failed: {result.stderr.strip() or result.stdout.strip()}")

    return result.stdout


def export(source: pathlib.Path, ref: str, into: pathlib.Path) -> str:
    """Extracts `git archive <ref>` into `into` and returns the commit id."""
    commit = run(["git", "rev-parse", "--verify", f"{ref}^{{commit}}"], source).strip()
    archive = subprocess.run(["git", "archive", "--format=tar", commit], cwd=source, capture_output=True)

    if archive.returncode != 0:
        raise RuntimeError(f"git archive failed: {archive.stderr.decode(errors='replace').strip()}")

    with tarfile.open(fileobj=io.BytesIO(archive.stdout)) as tar:
        tar.extractall(into, filter="data")

    return commit


def files_of(root: pathlib.Path) -> list[pathlib.Path]:
    return sorted(p for p in root.rglob("*") if p.is_file())


def check_hints(root: pathlib.Path, allow_words: list[str]) -> list[str]:
    findings = []
    allowed = [re.compile(re.escape(w), re.IGNORECASE) for w in allow_words if w.strip()]

    for path in files_of(root):
        rel = path.relative_to(root)

        if rel.name in HINT_FILES:
            findings.append(f"{rel.as_posix()}: notes for agents are not part of the package (add it to .gitattributes with export-ignore)")
            continue

        if set(rel.parts[:-1]) & set(HINT_DIRS):
            findings.append(f"{rel.as_posix()}: folder for agents is not part of the package")
            continue

        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue

        text = path.read_text(encoding="utf-8", errors="replace")

        for number, line in enumerate(text.splitlines(), 1):
            cleaned = line
            for word in allowed:
                cleaned = word.sub("", cleaned)

            for hint in HINTS:
                if hint.search(cleaned):
                    findings.append(f"{rel.as_posix()}:{number}: hint of the development tooling ({hint.pattern}): {line.strip()[:120]}")
                    break

    return findings


def load_composer(root: pathlib.Path) -> tuple[dict | None, list[str]]:
    path = root / "composer.json"

    if not path.is_file():
        return None, ["composer.json: missing"]

    try:
        return json.loads(path.read_text(encoding="utf-8")), []
    except json.JSONDecodeError as error:
        return None, [f"composer.json: invalid JSON ({error})"]


def same_url(a: str | None, b: str) -> bool:
    return (a or "").rstrip("/").removesuffix(".git").lower() == b.rstrip("/").removesuffix(".git").lower()


def check_composer(data: dict, repo_url: str | None) -> list[str]:
    findings = []

    if not re.fullmatch(r"[a-z0-9]([_.-]?[a-z0-9]+)*/[a-z0-9](([_.]|-{1,2})?[a-z0-9]+)*", str(data.get("name", ""))):
        findings.append("composer.json: name missing or not a valid package name (vendor/package, lower case)")
    if data.get("type") != "contao-bundle":
        findings.append("composer.json: type is not contao-bundle (the Contao Manager lists only contao-bundle and contao-module)")
    if not data.get("license"):
        findings.append("composer.json: license missing")
    if not data.get("description"):
        findings.append("composer.json: description missing (shown on Packagist and in the Contao Manager)")
    if "version" in data:
        findings.append("composer.json: remove \"version\"; Packagist reads the version from the git tag, the ZIP gets it from this script")
    if not (data.get("extra") or {}).get("contao-manager-plugin"):
        findings.append("composer.json: extra.contao-manager-plugin missing (the Contao Manager lists only packages with a plugin)")
    if MANAGER_PLUGIN in (data.get("require") or {}):
        findings.append(f"composer.json: {MANAGER_PLUGIN} belongs into require-dev, not require (Contao documentation, Manager Plugin)")
    if MANAGER_PLUGIN not in (data.get("require-dev") or {}):
        findings.append(f"composer.json: require-dev needs {MANAGER_PLUGIN}")
    if (data.get("conflict") or {}).get(MANAGER_PLUGIN) != MANAGER_CONFLICT:
        findings.append(f"composer.json: conflict needs \"{MANAGER_PLUGIN}\": \"{MANAGER_CONFLICT}\"")
    for key, value in (data.get("require") or {}).items():
        if key != "php" and not key.startswith("ext-") and value.strip() in {"*", "dev-main", "dev-master"}:
            findings.append(f"composer.json: require {key} has no version range ({value})")
    if any(r.get("type") in {"path", "vcs", "artifact"} for r in (data.get("repositories") or []) if isinstance(r, dict)):
        findings.append("composer.json: repositories must not be set in a package (Composer only reads them from the project)")

    if repo_url:
        if not same_url(data.get("homepage"), repo_url):
            findings.append(f"composer.json: homepage is not the public repository ({data.get('homepage')})")
        support = data.get("support") or {}
        if not same_url(support.get("source"), repo_url):
            findings.append(f"composer.json: support.source is not the public repository ({support.get('source')})")
        if not same_url(support.get("issues"), repo_url.rstrip("/") + "/issues"):
            findings.append(f"composer.json: support.issues is not the issue list of the public repository ({support.get('issues')})")

    return findings


def check_changelog(root: pathlib.Path, version: str) -> list[str]:
    path = root / "CHANGELOG.md"

    if not path.is_file():
        return ["CHANGELOG.md: missing"]

    text = path.read_text(encoding="utf-8")
    findings = []

    heading = re.search(rf"^##\s+\[?{re.escape(version)}\]?(\s.*)?$", text, re.MULTILINE)
    if not heading:
        findings.append(f"CHANGELOG.md: no section \"## [{version}] - YYYY-MM-DD\"")
    elif "unreleased" in heading.group(0).lower() or not re.search(r"\d{4}-\d{2}-\d{2}", heading.group(0)):
        findings.append(f"CHANGELOG.md: the section of {version} needs its release date (\"## [{version}] - YYYY-MM-DD\"): {heading.group(0).strip()}")

    unreleased = re.search(r"^##\s+\[?Unreleased\]?\s*$(.*?)(?=^##\s|\Z)", text, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    if unreleased and unreleased.group(1).strip():
        findings.append("CHANGELOG.md: the \"Unreleased\" section still has entries; move them into the version section")

    return findings


def check_bundle(root: pathlib.Path, forbid: list[str], allow: list[str]) -> list[str]:
    script = pathlib.Path(__file__).with_name("bundle-check.py")
    args = [sys.executable, str(script), str(root), "--json"]
    for term in forbid:
        args += ["--forbid", term]
    for path in allow:
        args += ["--allow", path]

    result = subprocess.run(args, capture_output=True, text=True)

    if result.returncode == 2:
        return [f"bundle-check: {result.stderr.strip() or result.stdout.strip()}"]

    try:
        report = json.loads(result.stdout)
    except json.JSONDecodeError:
        return [f"bundle-check: unreadable output: {result.stdout.strip()[:200]}"]

    items = report.items() if isinstance(report, dict) else []
    return [f"bundle-check {check}: {finding}" for check, found in items for finding in (found or [])]


def write_zip(root: pathlib.Path, data: dict, version: str, out: pathlib.Path) -> pathlib.Path:
    """ZIP for the Contao Manager: package files at the root, composer.json with the version."""
    manifest = {}
    for key, value in data.items():
        manifest[key] = value
        if key == "name":
            manifest["version"] = version

    out.mkdir(parents=True, exist_ok=True)
    target = out / f"{data['name'].split('/')[-1]}-{version}.zip"

    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in files_of(root):
            rel = path.relative_to(root).as_posix()
            info = zipfile.ZipInfo(rel, date_time=(2020, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            if rel == "composer.json":
                archive.writestr(info, json.dumps(manifest, indent=4, ensure_ascii=False) + "\n")
            else:
                archive.writestr(info, path.read_bytes())

    return target


def check_target(target: pathlib.Path, version: str) -> list[str]:
    """The public clone must be a clean git clone without the tag of this version."""
    if not (target / ".git").exists():
        return [f"{target}: not a git clone of the public repository"]
    if run(["git", "status", "--porcelain"], target).strip():
        return [f"{target}: has uncommitted changes"]
    if run(["git", "tag", "--list", f"v{version}"], target).strip():
        return [f"{target}: already has the tag v{version}"]
    return []


def publish(root: pathlib.Path, target: pathlib.Path, version: str, author: str) -> None:
    """Replaces the working tree of the public clone by the export, commits and tags it."""
    for entry in target.iterdir():
        if entry.name == ".git":
            continue
        if entry.is_dir() and not entry.is_symlink():
            shutil.rmtree(entry)
        else:
            entry.unlink()

    for path in files_of(root):
        destination = target / path.relative_to(root)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, destination)

    match = AUTHOR.match(author)
    env = {
        **os.environ,
        "GIT_AUTHOR_NAME": match["name"], "GIT_AUTHOR_EMAIL": match["email"],
        "GIT_COMMITTER_NAME": match["name"], "GIT_COMMITTER_EMAIL": match["email"],
    }
    run(["git", "add", "--all"], target)
    if not run(["git", "status", "--porcelain"], target).strip():
        raise RuntimeError("nothing changed compared with the last release")
    run(["git", "-c", "commit.gpgsign=false", "commit", "--quiet", "-m", f"Release {version}"], target, env)
    run(["git", "-c", "tag.gpgsign=false", "tag", "-a", f"v{version}", "-m", f"Version {version}"], target, env)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("source", help="developer repository of the bundle (a git clone)")
    parser.add_argument("--version", required=True, help="version to release, e.g. 1.0.0")
    parser.add_argument("--ref", default="HEAD", help="git ref to release (default HEAD; uncommitted changes never count)")
    parser.add_argument("--repo-url", help="URL of the public repository; homepage and support of composer.json must point there")
    parser.add_argument("--out", required=True, help="folder for the ZIP (outside the repositories or ignored by git)")
    parser.add_argument("--target", help="local clone of the public repository: replace, commit and tag (never pushed)")
    parser.add_argument("--author", help="author and committer of the release commit, \"Name <address>\"; required with --target")
    parser.add_argument("--forbid", action="append", default=[], help="passed to bundle-check.py; repeatable")
    parser.add_argument("--allow", action="append", default=[], help="passed to bundle-check.py; repeatable")
    parser.add_argument("--allow-word", action="append", default=[], help="term that may appear although it looks like a hint, e.g. a crawler name the product checks; repeatable")
    parser.add_argument("--json", action="store_true", help="print the result as JSON")
    args = parser.parse_args()

    source = pathlib.Path(args.source).resolve()
    if not SEMVER.match(args.version):
        parser.error(f"--version {args.version!r} is not a semantic version like 1.0.0")
    if args.target and not (args.author and AUTHOR.match(args.author)):
        parser.error("--target needs --author \"Name <address>\"")
    if not (source / ".git").exists():
        parser.error(f"{source} is not a git repository")

    with tempfile.TemporaryDirectory(prefix="release-bundle-") as tmp:
        root = pathlib.Path(tmp) / "package"
        root.mkdir()
        try:
            commit = export(source, args.ref, root)
        except RuntimeError as error:
            print(error, file=sys.stderr)
            return 2

        data, findings = load_composer(root)
        findings += check_hints(root, args.allow_word)
        if data is not None:
            findings += check_composer(data, args.repo_url)
        findings += check_changelog(root, args.version)
        findings += check_bundle(root, args.forbid, args.allow)
        target = pathlib.Path(args.target).resolve() if args.target else None
        if target:
            findings += check_target(target, args.version)

        result = {"source": str(source), "commit": commit, "version": args.version, "files": len(files_of(root)), "findings": findings}

        if not findings:
            result["zip"] = str(write_zip(root, data, args.version, pathlib.Path(args.out).resolve()))
            if target:
                try:
                    publish(root, target, args.version, args.author)
                except RuntimeError as error:
                    result["findings"] = [str(error)]
                else:
                    result["target"] = str(target)
                    result["push"] = f"git -C {target} push origin HEAD && git -C {target} push origin v{args.version}"

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"{result['source']} @ {commit[:12]}: version {args.version}, {result['files']} files")
        for finding in result["findings"]:
            print(f"  - {finding}")
        if "zip" in result:
            print(f"ZIP: {result['zip']}")
        if "push" in result:
            print(f"Committed and tagged in {result['target']}; publish with:\n  {result['push']}")
        if not result["findings"]:
            print("No findings.")

    return 1 if result["findings"] else 0


if __name__ == "__main__":
    sys.exit(main())
