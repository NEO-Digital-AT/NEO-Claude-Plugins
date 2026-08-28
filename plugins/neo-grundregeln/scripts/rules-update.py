#!/usr/bin/env python3
"""Keeps the installed NEO rule plugins level with the marketplace.

Runs from the SessionStart hook. It refreshes the marketplace and then
runs `claude plugin update` for every plugin of this marketplace that is
behind. Both are the commands Claude itself offers — the script never
edits Claude's own bookkeeping, because a half-written registry leaves a
plugin that no longer loads at all.

It cannot update the session it runs in: the hook lives inside a plugin,
so the plugins are already loaded by the time it starts. What it changes
takes effect from the next session — `claude plugin update` says the same
("restart required to apply").

The script is quiet while everything is level. It prints only when
something changed, and then it names what:

    NEO rules updated - active from the next session
      neo-grundregeln  2.4.0 -> 2.5.0
      neo-design       1.8.0 -> 1.9.0

Offline or with an unreadable registry it does nothing and says nothing.
A session start is never blocked by a failure here.

    rules-update.py              refresh and update
    rules-update.py --check      report only, change nothing
    rules-update.py --interval 0 ignore the throttle

Two environment variables steer it: NEO_RULES_UPDATE=off switches the
whole thing off, NEO_RULES_INTERVAL sets the minutes between two network
calls.

No dependencies, standard library only.
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import subprocess
import sys
import time

STAMP = ".neo-rules-checked"
DEFAULT_INTERVAL = 10      # minutes between two network calls
REFRESH_TIMEOUT = 60       # seconds for the marketplace refresh
UPDATE_TIMEOUT = 60        # seconds per plugin


def read_json(path: pathlib.Path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def plugins_dir(plugin_root: pathlib.Path) -> pathlib.Path | None:
    """The directory holding installed_plugins.json, found from this plugin."""
    for parent in plugin_root.parents:
        if (parent / "installed_plugins.json").exists():
            return parent
    fallback = pathlib.Path(
        os.environ.get("CLAUDE_CONFIG_DIR") or (pathlib.Path.home() / ".claude")
    ) / "plugins"
    return fallback if (fallback / "installed_plugins.json").exists() else None


def marketplace_name(plugin_root: pathlib.Path, plugins: pathlib.Path) -> str | None:
    """The marketplace this plugin came from.

    Claude keeps a plugin in one of two places, and both occur:

        <plugins>/cache/<marketplace>/<plugin>/<version>
        <plugins>/marketplaces/<marketplace>/plugins/<plugin>

    In both the marketplace name is the second path element.
    """
    try:
        parts = plugin_root.relative_to(plugins).parts
    except ValueError:
        return None
    if len(parts) >= 2 and parts[0] in ("cache", "marketplaces"):
        return parts[1]
    return None


def claude(arguments: list[str], timeout: int) -> bool:
    """Runs a claude subcommand quietly. A failure is not an error here."""
    try:
        done = subprocess.run(["claude", *arguments], timeout=timeout,
                              stdin=subprocess.DEVNULL,
                              stdout=subprocess.DEVNULL,
                              stderr=subprocess.DEVNULL)
        return done.returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


def refresh(marketplace: str) -> None:
    """Fetches the newest marketplace state."""
    claude(["plugin", "marketplace", "update", marketplace], REFRESH_TIMEOUT)


def offered(clone: pathlib.Path) -> dict[str, str]:
    """Version of every plugin the marketplace currently offers."""
    manifest = read_json(clone / ".claude-plugin" / "marketplace.json", {})
    versions: dict[str, str] = {}
    for entry in manifest.get("plugins") or []:
        name, source = entry.get("name"), entry.get("source")
        if not name or not isinstance(source, str):
            continue
        own = read_json(clone / source / ".claude-plugin" / "plugin.json", {})
        if own.get("version"):
            versions[name] = own["version"]
    return versions


def pinned(registry: dict, marketplace: str) -> dict[str, str]:
    """Version of every plugin installed from this marketplace."""
    versions: dict[str, str] = {}
    for key, entries in (registry.get("plugins") or {}).items():
        name, _, source = key.partition("@")
        if source != marketplace or not entries:
            continue
        versions[name] = entries[0].get("version", "?")
    return versions


def update(marketplace: str, names: list[str]) -> list[str]:
    """Updates the named plugins and returns those that went through.

    Uses `claude plugin update`, which also copies the new files into
    place. Editing the registry by hand would set the version but leave
    the files behind, and the plugin would silently stop loading.
    """
    return [name for name in names
            if claude(["plugin", "update", f"{name}@{marketplace}", "-y"],
                      UPDATE_TIMEOUT)]


def throttled(plugins: pathlib.Path, minutes: int) -> bool:
    """True while the last check is younger than the interval."""
    if minutes <= 0:
        return False
    stamp = plugins / STAMP
    try:
        return (time.time() - stamp.stat().st_mtime) < minutes * 60
    except OSError:
        return False


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Keep the installed NEO rule plugins level with the marketplace.")
    parser.add_argument("--check", action="store_true",
                        help="report only, change nothing")
    parser.add_argument("--interval", type=int,
                        default=int(os.environ.get("NEO_RULES_INTERVAL",
                                                   DEFAULT_INTERVAL)),
                        help=f"minutes between two network calls "
                             f"(default {DEFAULT_INTERVAL}, 0 disables the throttle)")
    args = parser.parse_args(argv)

    if os.environ.get("NEO_RULES_UPDATE", "").strip().lower() == "off":
        return 0

    root = os.environ.get("CLAUDE_PLUGIN_ROOT")
    if not root:
        return 0
    plugin_root = pathlib.Path(root).resolve()

    plugins = plugins_dir(plugin_root)
    if plugins is None:
        return 0
    marketplace = marketplace_name(plugin_root, plugins)
    if marketplace is None:
        return 0

    if not args.check and throttled(plugins, args.interval):
        return 0

    known = read_json(plugins / "known_marketplaces.json", {})
    location = (known.get(marketplace) or {}).get("installLocation")
    if not location:
        return 0
    clone = pathlib.Path(location)

    if not args.check:
        refresh(marketplace)
        try:
            (plugins / STAMP).touch()
        except OSError:
            pass

    registry = read_json(plugins / "installed_plugins.json", {})
    have, there = pinned(registry, marketplace), offered(clone)

    behind = sorted(name for name, version in have.items()
                    if name in there and there[name] != version)
    if not behind:
        return 0

    if args.check:
        width = max(len(name) for name in behind)
        print(f"NEO rules: {len(behind)} plugin(s) behind the marketplace")
        for name in behind:
            print(f"    {name:<{width}}  {have[name]} -> {there[name]}")
        return 1

    done = update(marketplace, behind)
    if not done:
        return 0
    width = max(len(name) for name in done)
    print("NEO rules updated - active from the next session")
    for name in done:
        print(f"    {name:<{width}}  {have[name]} -> {there[name]}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        # A session start is never blocked by a failure here.
        sys.exit(0)
