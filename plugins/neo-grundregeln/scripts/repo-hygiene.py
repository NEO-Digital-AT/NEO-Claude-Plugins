#!/usr/bin/env python3
"""Finds what lies in a repository without being needed.

A repository is a working tool, not an archive. Everything lying in it
costs attention: somebody reads it, somebody believes it is current,
somebody keeps it alive. Screenshots from a debugging session, log files,
a script that was written once to try something out, a plan that was
finished half a year ago — none of it is a catastrophe on its own, and
together they make a repository that nobody trusts any more.

The script looks at the TRACKED files and reports four things:

    Secrets          files that must never be in a repository
    Leftovers        build output, logs, temporary and editor files
    Never mentioned  scripts and media no other file refers to
    Finished plans   plan and note files that have not moved in months

It DELETES NOTHING and proposes nothing silently: what goes is the
project owner's decision. The script prints the command for each finding,
it does not run it.

The last two sections are proposals, not verdicts. A file can be needed
without any other file naming it — a document for a human, a script
someone calls by hand. Read the list, do not execute it.

No dependencies beyond git, so the script runs in any CI.

    repo-hygiene.py
    repo-hygiene.py /pfad/zum/repo --age-months 6
    repo-hygiene.py --strict --report hygiene.json

Exit code 0 when nothing blocking was found, 1 on secrets or leftovers
(with --strict also on proposals), 2 when the repository cannot be read.
"""
from __future__ import annotations

import argparse
import datetime
import fnmatch
import json
import pathlib
import re
import subprocess
import sys

# --------------------------------------------------------------------------
# What must never be in a repository. A secret that was in it once counts
# as compromised: removing the file is not enough, it has to be replaced.
# --------------------------------------------------------------------------

SECRETS = (
    ".env", ".env.*", "*.pem", "*.key", "*.p12", "*.pfx", "*.jks",
    "*.keystore", "*.ppk", "id_rsa*", "id_ed25519*", "credentials.json",
    "service-account*.json", "secrets.*", "*secret*.json", ".npmrc",
    ".pypirc", "auth.json", "*.kdbx",
)
SECRETS_ALLOWED = ("*.example", "*.sample", "*.template", "*.dist", "*.md")

# Build output, caches, logs, editor and system leftovers.
LEFTOVERS = (
    "node_modules/*", "vendor/*", "dist/*", "build/*", "out/*", "bin/*",
    "obj/*", "target/*", "coverage/*", ".gradle/*", ".dart_tool/*",
    "__pycache__/*", ".venv/*", "venv/*", ".next/*", ".nuxt/*", ".cache/*",
    "Pods/*", "tmp/*", "temp/*", "scratch/*",
    "*.pyc", "*.pyo", "*.class", "*.log", "*.tmp", "*.temp", "*.bak",
    "*.orig", "*.rej", "*.swp", "*~", ".DS_Store", "Thumbs.db",
    "desktop.ini", "npm-debug.log*", "yarn-error.log", "nohup.out",
    "*.lcov",
)

# Names that only mean a leftover together with a picture: a rule file
# ABOUT screenshots is not a screenshot.
LEFTOVER_PICTURES = ("screenshot*", "bildschirmfoto*", "unbenannt*",
                     "untitled*", "bild *", "img_*", "foto*")
PICTURE_SUFFIXES = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp",
                    ".heic", ".pdf")

# Looks like a leftover and is not one. A dependency lock file belongs in
# the repository — it is what makes a build reproducible.
KEPT = (
    "package-lock.json", "yarn.lock", "pnpm-lock.yaml", "composer.lock",
    "pubspec.lock", "packages.lock.json", "poetry.lock", "Cargo.lock",
    "Gemfile.lock", "go.sum", "flake.lock",
)

# Files that are an entry point by convention: nobody names them, everybody
# needs them.
ENTRY_POINTS = (
    "README*", "LICENSE*", "CHANGELOG*", "CONTRIBUTING*", "SECURITY*",
    "CODE_OF_CONDUCT*", "CLAUDE.md", "AGENTS.md", ".gitignore",
    ".gitattributes", ".editorconfig", ".github/*", ".claude/*",
    "Dockerfile*", "docker-compose*", "Makefile", "package.json",
    "composer.json", "pubspec.yaml", "pyproject.toml", "setup.py",
    "requirements*.txt", "go.mod", "Cargo.toml", "*.csproj", "*.sln",
    "*.props", "*.targets", "index.*", "main.*", "__init__.py",
    "conftest.py",
)

# Only these are proposed when no other file mentions them. Documents are
# deliberately not in this list: a document can be needed without any file
# referring to it — the documentation of an external interface, for
# instance, which is exactly what one keeps a repository for.
ORPHAN_CANDIDATES = (
    ".py", ".sh", ".bash", ".zsh", ".ps1", ".bat", ".cmd", ".js", ".mjs",
    ".ts", ".php", ".rb", ".pl", ".sql", ".png", ".jpg", ".jpeg", ".gif",
    ".webp", ".bmp", ".svg", ".mp4", ".zip", ".tar", ".gz",
)

# Scaffolding: it carries a task, not a decision. A finished plan either
# becomes a decision record or goes.
PLANS = (
    "plan*.md", "*-plan.md", "*_plan.md", "todo*.md", "TODO*", "notes*.md",
    "notizen*.md", "scratch*.md", "entwurf*.md", "draft*.md", "wip*.md",
    "plan/*", "plans/*", "planung/*",
)

BINARY = re.compile(rb"\x00")
MAX_READ = 512 * 1024


def matches(path: str, patterns) -> bool:
    name = pathlib.PurePosixPath(path).name
    return any(fnmatch.fnmatch(path, p) or fnmatch.fnmatch(name, p)
               for p in patterns)


def git(root, *args):
    result = subprocess.run(("git", "-C", str(root)) + args,
                            capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "git failed")
    return result.stdout


def tracked_files(root):
    return [f for f in git(root, "ls-files", "-z").split("\0") if f]


def last_changed(root):
    """One pass through the history: which file was last touched when."""
    dates = {}
    try:
        out = git(root, "log", "--no-renames", "--name-only",
                  "--pretty=format:%x01%cs")
    except RuntimeError:
        return dates
    date = None
    for line in out.splitlines():
        if line.startswith("\x01"):
            date = line[1:].strip()
        elif line.strip() and date:
            dates.setdefault(line.strip(), date)
    return dates


def months_since(date):
    """How many months ago, counted from today — not from the last commit:
    a repository whose newest commit carries an old date would otherwise
    make every file look young."""
    today = datetime.date.today()
    try:
        year, month, _ = (int(part) for part in date.split("-"))
    except (ValueError, AttributeError):
        return 0
    return max(0, (today.year - year) * 12 + (today.month - month))


def read_texts(root, files):
    """The content of every readable text file, for the mention check."""
    texts = {}
    for name in files:
        path = pathlib.Path(root) / name
        try:
            raw = path.read_bytes()[:MAX_READ]
        except OSError:
            continue
        if BINARY.search(raw[:8192]):
            continue
        try:
            texts[name] = raw.decode("utf-8", errors="replace")
        except ValueError:
            continue
    return texts


def mentioned(name, texts):
    """Is the file named anywhere else? Its stem counts too: a script is
    often called without its extension."""
    base = pathlib.PurePosixPath(name).name
    stem = pathlib.PurePosixPath(base).stem
    for other, text in texts.items():
        if other == name:
            continue
        if base in text or (len(stem) > 3 and stem in text):
            return True
    return False


def examine(root, age_months):
    files = tracked_files(root)
    dates = last_changed(root)
    texts = read_texts(root, files)

    secrets, leftovers, orphans, plans = [], [], [], []

    for name in files:
        base = pathlib.PurePosixPath(name).name
        age = months_since(dates.get(name))

        if matches(name, SECRETS) and not matches(base, SECRETS_ALLOWED):
            secrets.append((name, "must never be in a repository"))
            continue
        if base in KEPT:
            continue
        if matches(name, LEFTOVERS):
            leftovers.append((name, "build output, log or temporary file"))
            continue
        if (pathlib.PurePosixPath(name).suffix.lower() in PICTURE_SUFFIXES
                and matches(base.lower(), LEFTOVER_PICTURES)):
            leftovers.append((name, "picture from a session, not a document"))
            continue
        if matches(name, ENTRY_POINTS):
            continue

        if matches(name, PLANS):
            if age >= age_months:
                plans.append((name, f"unchanged for {age} months — finished?"))
            continue

        if (pathlib.PurePosixPath(name).suffix.lower() in ORPHAN_CANDIDATES
                and not mentioned(name, texts)):
            note = "no other file mentions it"
            if age:
                note += f", unchanged for {age} months"
            orphans.append((name, note))

    return files, secrets, leftovers, orphans, plans


def section(title, findings, command, hint=None):
    if not findings:
        return
    print(f"{title} ({len(findings)})")
    if hint:
        print(f"  {hint}")
    for name, reason in findings:
        print(f"  {name}")
        print(f"      {reason}")
    print(f"  → {command}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Reports what lies in a repository without being "
                    "needed. Deletes nothing.")
    parser.add_argument("path", nargs="?", default=".",
                        help="path inside the repository (default: .)")
    parser.add_argument("--age-months", type=int, default=6,
                        help="from how many months a plan counts as old "
                             "(default 6)")
    parser.add_argument("--strict", action="store_true",
                        help="let the proposals fail the run as well")
    parser.add_argument("--report", help="write the findings as JSON")
    args = parser.parse_args()

    root = pathlib.Path(args.path)
    try:
        files, secrets, leftovers, orphans, plans = examine(
            root, args.age_months)
    except (RuntimeError, FileNotFoundError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    print(f"repo-hygiene: {len(files)} tracked files\n")

    section("Secrets — out, and replace them", secrets,
            "git rm --cached <file>, add the pattern to .gitignore, "
            "then rotate the secret",
            "A secret that was in the repository once counts as "
            "compromised. Removing it is not enough.")
    section("Leftovers — do not belong in a repository", leftovers,
            "git rm --cached <file> and add the pattern to .gitignore")
    section("Never mentioned — proposal, not a verdict", orphans,
            "check, then git rm <file> if nobody needs it",
            "A file can be needed without another file naming it. Read "
            "the list, do not execute it.")
    section("Plans that have not moved — finished?", plans,
            "make it a decision record, or git rm <file>",
            "A plan carries a task, not a decision. What is worth keeping "
            "belongs in a decision record (Skill neo-doku).")

    blocking = len(secrets) + len(leftovers)
    proposals = len(orphans) + len(plans)
    if not blocking and not proposals:
        print("Nothing found. The repository holds only what is needed —"
              " as far as this can be measured.")
    else:
        print(f"{blocking} blocking, {proposals} for a decision.")
        print("Nothing was deleted. What goes is the project owner's call.")

    if args.report:
        pathlib.Path(args.report).write_text(
            json.dumps({"tracked": len(files),
                        "secrets": [{"file": f, "reason": r}
                                    for f, r in secrets],
                        "leftovers": [{"file": f, "reason": r}
                                      for f, r in leftovers],
                        "orphans": [{"file": f, "reason": r}
                                    for f, r in orphans],
                        "plans": [{"file": f, "reason": r}
                                  for f, r in plans]},
                       ensure_ascii=False, indent=2), encoding="utf-8")

    if blocking or (args.strict and proposals):
        return 1
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.stderr.close()
        sys.exit(0)
