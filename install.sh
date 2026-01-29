#!/usr/bin/env bash
# CrewAI Skills Installer Bootstrap
set -e
REPO="https://raw.githubusercontent.com/victorgrein/cli-agents-config/main"
TMP="/tmp/crewai-installer-$$.sh"
cleanup() { rm -f "$TMP" 2>/dev/null; }
trap cleanup EXIT
curl -fsSL "$REPO/installer.sh" -o "$TMP"
chmod +x "$TMP"
bash "$TMP" < /dev/tty
