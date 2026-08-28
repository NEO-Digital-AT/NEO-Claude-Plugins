#!/bin/sh
# Runs rules-update.py with whatever Python the machine has.
#
# Claude Code runs hooks through Git Bash on Windows, which brings a shell
# but no Python. Without Python this does nothing and says nothing - a
# session start is never blocked by the update check.
for python in python3 python py; do
  if command -v "$python" >/dev/null 2>&1; then
    "$python" "${CLAUDE_PLUGIN_ROOT}/scripts/rules-update.py" 2>/dev/null
    exit 0
  fi
done
exit 0
