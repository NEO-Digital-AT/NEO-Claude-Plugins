#!/bin/sh
# Installs the NEO plugins in a cloud environment (claude.ai/code).
#
# A cloud session does not add the marketplaces a repository lists under
# extraKnownMarketplaces, because that needs the workspace trust dialog,
# which a cloud session never shows. And a plugin whose only "true" is in
# the repository's .claude/settings.json is never fetched: Claude Code
# fetches only what user settings, settings.local.json, --settings or
# managed settings enable. So a repository cannot bring its own plugins
# into a cloud session, and the SessionStart hook with the core rules
# never runs either.
#
# This script closes that gap. It belongs in the cloud environment's setup
# script field, runs before Claude Code starts, and installs at USER scope
# — which is one of the scopes that are actually fetched and loaded.
#
# Enter it once per environment: Cloud environment > Edit > Setup script.
# Because the environment is cached, it takes effect in NEW sessions.
#
# It never exits non-zero. A setup script that fails takes the whole
# session with it, and no plugin is worth that.

export HOME="${HOME:-/root}"

CLAUDE=/opt/claude-code/bin/claude
[ -x "$CLAUDE" ] || CLAUDE="$(command -v claude)"
if [ -z "$CLAUDE" ]; then
  echo "NEO: claude CLI not found, plugins skipped"
  exit 0
fi

# The marketplaces to register. Add one line per marketplace repository.
for repo in \
  NEO-Digital-AT/NEO-Claude-Plugins \
  NEO-Digital-AT/NEO-Claude-GoogleAds-Plugin
do
  "$CLAUDE" plugin marketplace add "$repo" || true
done
"$CLAUDE" plugin marketplace update || true

# Install every plugin of every registered marketplace. Reading the
# catalogue instead of listing plugin names keeps the script correct when a
# plugin is added or renamed.
installed=0
for catalogue in "$HOME"/.claude/plugins/marketplaces/*/.claude-plugin/marketplace.json
do
  [ -f "$catalogue" ] || continue
  market="$(python3 -c "import json,sys
data = json.load(open(sys.argv[1]))
print(data.get('name', ''))" "$catalogue" 2>/dev/null)"
  [ -n "$market" ] || continue
  names="$(python3 -c "import json,sys
data = json.load(open(sys.argv[1]))
print(' '.join(p['name'] for p in data.get('plugins', []) if p.get('name')))" \
    "$catalogue" 2>/dev/null)"
  for plugin in $names; do
    if "$CLAUDE" plugin install "$plugin@$market" --scope user --yes; then
      installed=$((installed + 1))
    fi
  done
done

echo "NEO: $installed plugins installed at user scope"
exit 0
