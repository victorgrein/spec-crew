#!/bin/bash
set -e

echo "🔍 Verifying OpenCode Read-Only Orchestrator Setup..."
echo ""

CONFIG_FILE="$HOME/.opencode/opencode.json"

# Check opencode.json exists
if [ ! -f "$CONFIG_FILE" ]; then
    echo "❌ Missing: $CONFIG_FILE"
    exit 1
fi
echo "✅ opencode.json found"

# Verify permissions are set
if grep -q '"bash": "deny"' "$CONFIG_FILE"; then
    echo "✅ Bash access denied"
else
    echo "❌ Bash not denied in permissions"
    exit 1
fi

if grep -q '"edit": "deny"' "$CONFIG_FILE"; then
    echo "✅ Edit access denied"
else
    echo "❌ Edit not denied in permissions"
    exit 1
fi

if grep -q '"write": "deny"' "$CONFIG_FILE"; then
    echo "✅ Write access denied"
else
    echo "❌ Write not denied in permissions"
    exit 1
fi

if grep -q '"patch": "deny"' "$CONFIG_FILE"; then
    echo "✅ Patch access denied"
else
    echo "❌ Patch not denied in permissions"
    exit 1
fi

if grep -q '"multiedit": "deny"' "$CONFIG_FILE"; then
    echo "✅ Multiedit access denied"
else
    echo "❌ Multiedit not denied in permissions"
    exit 1
fi

if grep -q '"todowrite": "deny"' "$CONFIG_FILE"; then
    echo "✅ Todowrite access denied"
else
    echo "❌ Todowrite not denied in permissions"
    exit 1
fi

# Check orchestrator agent defined
if grep -q '"orchestrator"' "$CONFIG_FILE"; then
    echo "✅ Orchestrator agent configured"
else
    echo "❌ Orchestrator agent not found"
    exit 1
fi

# Check question tool is available
if grep -q '"question"' "$CONFIG_FILE"; then
    echo "✅ Question tool available for orchestrator"
else
    echo "❌ Question tool not found in config"
    exit 1
fi

# Verify existing config preserved
if grep -q '"zai-coding-plan"' "$CONFIG_FILE"; then
    echo "✅ Existing providers preserved"
else
    echo "⚠️  Warning: Provider config may be missing"
fi

if grep -q '"zread"' "$CONFIG_FILE"; then
    echo "✅ Existing MCP servers preserved"
else
    echo "⚠️  Warning: MCP config may be missing"
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "🎉 All checks passed! Read-Only Orchestrator is properly configured."
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "📋 Configuration Summary:"
echo "   - Orchestrator has read-only access only"
echo "   - Bash, edit, write, patch, multiedit, todowrite: DENIED"
echo "   - Allowed tools: question, skill, read, glob, grep, todoread, webfetch, websearch"
echo ""
echo "🚀 Next Steps:"
echo "   1. Restart opencode to apply changes"
echo "   2. Test orchestrator by asking it to create a file"
echo "   3. Verify it asks questions instead of implementing directly"
