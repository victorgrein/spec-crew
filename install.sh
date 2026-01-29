#!/usr/bin/env bash
#############################################################################
# CrewAI Skills Installer - Bootstrap
# Downloads and runs the interactive installer
#############################################################################

set -e

REPO_URL="https://raw.githubusercontent.com/victorgrein/cli-agents-config/main"
INSTALLER_URL="$REPO_URL/installer.sh"
TEMP_INSTALLER="/tmp/crewai-installer-$$.sh"

# Cleanup on exit
trap 'rm -f "$TEMP_INSTALLER" 2>/dev/null' EXIT

# Download the real installer
curl -fsSL "$INSTALLER_URL" -o "$TEMP_INSTALLER" || {
    echo "Failed to download installer"
    exit 1
}

# Make executable and run with terminal access
chmod +x "$TEMP_INSTALLER"
exec bash "$TEMP_INSTALLER"
