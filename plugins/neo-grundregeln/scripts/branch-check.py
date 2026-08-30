"""Reports branches that were opened and never merged.

One task, one branch: open it, finish it, merge it, delete it. Only then
the next one. Branches piled on half-finished branches end in cherry-picks,
and after a cherry-pick nobody knows what is really in the tree.

The script names the branches that are not merged into the integration
branch, how old they are, and which of them are already merged and only
need deleting.

    branch-check.py
    branch-check.py --into dev
    branch-check.py --remote --max-open 1

Exit code 0 when at most --max-open branches are open, 1 above that or on
branches that are merged but still lying around, 2 when the repository
cannot be read.
"""
from __future__ import annotations

import argparse
import datetime
import json
import pathlib
import re
import subprocess
import sys

PROTECTED = ("main", "master", "dev", "develop", "HEAD")


def git(root, *args):
    result = subprocess.run(("git", "-C", str(root)) + args,
                            capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "git failed")
    return result.stdout


def integration_branch(root, wanted):
    """Which branch the work is merged into: dev where it exists, else the
    branch the repository itself points at."""
    if wanted:
        return wanted
    branches = git(root, "branch", "-a", "--format=%(refname:short)").split()
    for name in ("dev", "develop"):
        if name in branches or f"origin/{name}" in branches:
            return name
    head = git(root, "symbolic-ref", "--quiet", "--short", "HEAD").strip()
    return "main" if "main" in branches else (head or "master")


def branches(root, remote):
    fmt = "%(refname:short)\t%(committerdate:short)\t%(authorname)"
    args = ["branch", "--format=" + fmt]
    if remote:
        args.append("-a")
    out = []
    for line in git(root, *args).splitlines():
        parts = line.split("\t")
        if len(parts) != 3:
            continue
        name = parts[0].removeprefix("remotes/")
        if name.split("/")[-1] in PROTECTED or "->" in name:
            continue
        out.append((name, parts[1], parts[2]))
    return out


def merged_into(root, target, remote):
    args = ["branch", "--format=%(refname:short)", "--merged", target]
    if remote:
        args.append("-a")
    try:
        return {n.removeprefix("remotes/") for n in git(root, *args).split()}
    except RuntimeError:
        return set()


def days_since(date):
    try:
        year, month, day = (int(p) for p in date.split("-"))
    except (ValueError, AttributeError):
        return 0
    return max(0, (datetime.date.today() - datetime.date(year, month, day)).days)


def main():
    parser = argparse.ArgumentParser(
        description="Reports branches that were opened and never merged.")
    parser.add_argument("path", nargs="?", default=".")
    parser.add_argument("--into", help="integration branch (default: dev if "
                                       "it exists, otherwise main)")
    parser.add_argument("--remote", action="store_true",
                        help="include remote branches")
    parser.add_argument("--max-open", type=int, default=1,
                        help="how many open branches are allowed (default 1)")
    parser.add_argument("--report", help="write the findings as JSON")
    args = parser.parse_args()

    root = pathlib.Path(args.path)
    try:
        target = integration_branch(root, args.into)
        alle = branches(root, args.remote)
        fertig = merged_into(root, target, args.remote)
    except (RuntimeError, FileNotFoundError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    offen = [(n, d, a) for n, d, a in alle if n not in fertig]
    liegen = [(n, d, a) for n, d, a in alle if n in fertig]

    print(f"branch-check: integration branch \"{target}\"\n")

    if liegen:
        print(f"Merged and still lying around ({len(liegen)}) — delete them:")
        for name, date, author in liegen:
            print(f"  {name:<44} {date}  {author}")
        print(f"  → git branch -d <branch>"
              f"{' / git push origin --delete <branch>' if args.remote else ''}\n")

    if offen:
        print(f"Open, not merged into {target} ({len(offen)}):")
        for name, date, author in sorted(offen, key=lambda b: b[1]):
            age = days_since(date)
            print(f"  {name:<44} {date}  {age:>4} d  {author}")
        print()

    if len(offen) > args.max_open:
        print(f"{len(offen)} open branches — allowed are {args.max_open}.")
        print("One task, one branch: finish and merge the oldest one before "
              "opening the next.")
    elif not offen and not liegen:
        print("Nothing open, nothing lying around.")

    if args.report:
        pathlib.Path(args.report).write_text(
            json.dumps({"into": target, "max_open": args.max_open,
                        "open": [{"branch": n, "date": d, "author": a,
                                  "days": days_since(d)} for n, d, a in offen],
                        "merged_not_deleted": [{"branch": n, "date": d,
                                                "author": a}
                                               for n, d, a in liegen]},
                       ensure_ascii=False, indent=2), encoding="utf-8")

    return 1 if (len(offen) > args.max_open or liegen) else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.stderr.close()
        sys.exit(0)
