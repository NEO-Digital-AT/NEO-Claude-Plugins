#!/usr/bin/env python3
"""Keeps the installed NEO rule plugins level with the marketplace.

Runs from the SessionStart hook. It refreshes the marketplace clone and
then removes the version pins of this marketplace from Claude's plugin
registry, so the next session installs the current state.

It cannot update the session it runs in: the hook lives inside a plugin,
so the plugins are already loaded by the time it starts. What it changes
takes effect from the next session — `claude plugin update` says the same
("restart required to apply").

The script is quiet while everything is level. It prints only when
something changed, and then it names what:

    NEO rules updated - active from the next session
      neo-grundregeln  2.4.0 -> 2.5.0
      neo-design       1.8.0 -> 1.9.0

Offline, without git, or with an unreadable registry it does nothing and
says nothing. A session start is never blocked by a failure here.

    rules-update.py              refresh and unpin
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
GIT_TIMEOUT = 20           # seconds


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

    Installed plugins live at <plugins>/cache/<marketplace>/<plugin>/<version>.
    """
    try:
        parts = plugin_root.relative_to(plugins).parts
    except ValueError:
        return None
    return parts[1] if len(parts) >= 2 and parts[0] == "cache" else None


def refresh(clone: pathlib.Path, marketplace: str) -> None:
    """Fetches the newest marketplace state. Failures are not an error."""
    if (clone / ".git").exists():
        command = ["git", "-C", str(clone), "pull", "--quiet", "--ff-only"]
    else:
        command = ["claude", "plugin", "marketplace", "update", marketplace]
    try:
        subprocess.run(command, timeout=GIT_TIMEOUT, stdin=subprocess.DEVNULL,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (OSError, subprocess.SubprocessError):
        pass


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


def unpin(path: pathlib.Path, registry: dict, marketplace: str,
          names: list[str]) -> bool:
    """Drops the pins of the named plugins, so the next session reinstalls.

    Only entries of this marketplace are touched; plugins from elsewhere
    keep their pin.
    """
    plugins = registry.get("plugins") or {}
    for name in names:
        plugins.pop(f"{name}@{marketplace}", None)
    try:
        path.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
        return True
    except OSError:
        return False


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
        refresh(clone, marketplace)
        try:
            (plugins / STAMP).touch()
        except OSError:
            pass

    registry_path = plugins / "installed_plugins.json"
    registry = read_json(registry_path, {})
    have, there = pinned(registry, marketplace), offered(clone)

    behind = sorted(name for name, version in have.items()
                    if name in there and there[name] != version)
    if not behind:
        return 0

    width = max(len(name) for name in behind)
    lines = [f"    {name:<{width}}  {have[name]} -> {there[name]}"
             for name in behind]

    if args.check:
        print(f"NEO rules: {len(behind)} plugin(s) behind the marketplace")
        print("\n".join(lines))
        return 1

    if not unpin(registry_path, registry, marketplace, behind):
        return 0
    print("NEO rules updated - active from the next session")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        # A session start is never blocked by a failure here.
        sys.exit(0)
