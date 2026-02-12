#!/usr/bin/env bash
#############################################################################
# Spec Crew Installer
# Interactive installer for Claude Code and OpenCode
#############################################################################

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'

# Configuration
REPO_URL="${REPO_URL:-https://raw.githubusercontent.com/victorgrein/spec-crew/main}"
REPO_API_TREE_URL="${REPO_API_TREE_URL:-https://api.github.com/repos/victorgrein/spec-crew/git/trees/main?recursive=1}"
REPO_ARCHIVE_URL="${REPO_ARCHIVE_URL:-https://codeload.github.com/victorgrein/spec-crew/tar.gz/refs/heads/main}"
INSTALL_DIR=""
PLATFORM=""
NON_INTERACTIVE=false
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REMOTE_BLOB_PATHS=""
REMOTE_ARCHIVE_SKILLS_DIR=""
REMOTE_ARCHIVE_TMP_DIR=""

# Package contents
# BEGIN GENERATED: TOOLKIT_PACKAGE_LISTS
PKG_SKILLS=(
    "core-build"
    "flows"
    "tools-expert"
    "orchestration-governance"
)

PKG_AGENTS=(
    "crewai/builder"
    "crewai/auditor"
    "crewai/flow"
    "crewai/docs"
)

PKG_COMMANDS=(
    "crew/init"
    "crew/inspect"
    "crew/fix"
    "crew/evolve"
    "crew/docs"
)
# END GENERATED: TOOLKIT_PACKAGE_LISTS





SKILL_ASSET_FILES=(
    "SKILL.md"
)

# Legacy skill directories from pre-consolidation releases.
# These are removed on install so OpenCode does not keep routing to stale packs.
LEGACY_SKILLS=(
    "crewai-agents"
    "crewai-tasks"
    "crewai-flows"
    "crewai-crews"
    "crewai-tools"
    "crewai-llms"
    "crewai-memory"
    "crewai-processes"
    "crewai-cli"
    "crewai-debugging"
    "crewai-optimization"
    "crewai-migration"
    "crewai-crew-creation"
    "crewai-code-quality"
    "crewai-project-structure"
)




#############################################################################
# Utility Functions
#############################################################################

print_header() {
    echo -e "${CYAN}${BOLD}"
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║                                                          ║"
    echo "║                Spec Crew Installer                       ║"
    echo "║                                                          ║"
    echo "╚══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_success() { echo -e "  ${GREEN}✓${NC} $1"; }
print_error() { echo -e "  ${RED}✗${NC} $1" >&2; }
print_info() { echo -e "  ${BLUE}ℹ${NC} $1"; }
print_warning() { echo -e "  ${YELLOW}⚠${NC} $1"; }
print_step() { echo -e "\n${CYAN}${BOLD}▶${NC} $1\n"; }

get_config_dir() {
    if [ "$PLATFORM" = "claude" ]; then
        echo ".claude"
    else
        echo ".opencode"
    fi
}

#############################################################################
# Check Interactive Mode
#############################################################################

check_interactive_mode() {
    if [ ! -t 0 ]; then
        print_header
        print_error "Interactive mode requires a terminal"
        echo ""
        echo "  You're running this script in a pipe (curl | bash)"
        echo "  For interactive mode, download the script first:"
        echo ""
        echo -e "  ${CYAN}# Download${NC}"
        echo "  curl -fsSL $REPO_URL/install.sh -o crewai-install.sh"
        echo ""
        echo -e "  ${CYAN}# Run interactively${NC}"
        echo "  bash crewai-install.sh"
        echo ""
        echo "  Or use quick install:"
        echo ""
        echo -e "  ${CYAN}# Install for Claude Code${NC}"
        echo "  curl -fsSL $REPO_URL/install.sh | bash -s claude"
        echo ""
        echo -e "  ${CYAN}# Install for OpenCode${NC}"
        echo "  curl -fsSL $REPO_URL/install.sh | bash -s opencode"
        echo ""
        exit 1
    fi
}

#############################################################################
# Installation Functions
#############################################################################

download_file() {
    local url="$1"
    local dest="$2"
    local max_retries=3
    local retry_count=0
    
    while [ $retry_count -lt $max_retries ]; do
        if curl -fsSL "$url" -o "$dest" 2>/dev/null; then
            # Verify file was actually created and has content
            if [ -f "$dest" ] && [ -s "$dest" ]; then
                return 0
            fi
        fi
        retry_count=$((retry_count + 1))
        sleep 1
    done
    
    return 1
}

install_template_file() {
    local rel_path="$1"
    local dest="$2"
    local local_source="$SCRIPT_DIR/$rel_path"

    if [ -f "$local_source" ]; then
        if cp "$local_source" "$dest" 2>/dev/null && [ -f "$dest" ] && [ -s "$dest" ]; then
            return 0
        fi
    fi

    download_file "$REPO_URL/$rel_path" "$dest"
}

load_remote_blob_paths() {
    local python_bin=""
    local tree_json=""

    if [ -n "$REMOTE_BLOB_PATHS" ]; then
        return 0
    fi

    tree_json=$(curl -fsSL "$REPO_API_TREE_URL" 2>/dev/null || true)
    if [ -z "$tree_json" ]; then
        return 1
    fi

    if command -v python3 >/dev/null 2>&1; then
        python_bin="python3"
    elif command -v python >/dev/null 2>&1; then
        python_bin="python"
    fi

    if [ -n "$python_bin" ]; then
        REMOTE_BLOB_PATHS=$(printf '%s' "$tree_json" | "$python_bin" -c '
import json
import sys

data = json.load(sys.stdin)
for entry in data.get("tree", []):
    if entry.get("type") == "blob":
        path = entry.get("path")
        if path:
            print(path)
' 2>/dev/null || true)
    fi

    if [ -z "$REMOTE_BLOB_PATHS" ]; then
        REMOTE_BLOB_PATHS=$(printf '%s' "$tree_json" | tr '{' '\n' | sed -n 's/.*"path":"\([^"]*\)".*"type":"blob".*/\1/p' || true)
    fi

    [ -n "$REMOTE_BLOB_PATHS" ]
}

get_remote_skill_files() {
    local skill="$1"

    if ! load_remote_blob_paths; then
        return 1
    fi

    awk -v prefix="templates/shared/skills/$skill/" 'index($0, prefix) == 1 { print }' <<< "$REMOTE_BLOB_PATHS"
}

install_remote_skill_package() {
    local skill="$1"
    local skills_dir="$2"
    local skill_files
    local rel_path
    local rel_dest
    local dest
    local failed_asset=0
    local copied_any=0

    skill_files=$(get_remote_skill_files "$skill")
    if [ -z "$skill_files" ]; then
        return 1
    fi

    if [ -d "$skills_dir/$skill" ] && ! rm -rf "$skills_dir/$skill"; then
        print_error "Failed to reset skill directory: $skill"
        return 1
    fi

    ensure_dir "$skills_dir/$skill"

    while IFS= read -r rel_path; do
        [ -z "$rel_path" ] && continue
        copied_any=1
        rel_dest="${rel_path#templates/shared/skills/$skill/}"
        dest="$skills_dir/$skill/$rel_dest"
        ensure_dir "$(dirname "$dest")"
        if ! install_template_file "$rel_path" "$dest"; then
            print_error "Failed to install skill asset: $skill/$rel_dest"
            failed_asset=1
        fi
    done <<< "$skill_files"

    if [ "$copied_any" -eq 0 ]; then
        return 1
    fi

    return $failed_asset
}

ensure_remote_archive_skills_dir() {
    local tmp_dir
    local archive_file
    local candidate

    if [ -n "$REMOTE_ARCHIVE_SKILLS_DIR" ] && [ -d "$REMOTE_ARCHIVE_SKILLS_DIR" ]; then
        return 0
    fi

    if ! command -v tar >/dev/null 2>&1; then
        return 1
    fi

    tmp_dir=$(mktemp -d 2>/dev/null || true)
    if [ -z "$tmp_dir" ] || [ ! -d "$tmp_dir" ]; then
        return 1
    fi

    archive_file="$tmp_dir/repo.tar.gz"
    if ! download_file "$REPO_ARCHIVE_URL" "$archive_file"; then
        rm -rf "$tmp_dir"
        return 1
    fi

    if ! tar -xzf "$archive_file" -C "$tmp_dir" 2>/dev/null; then
        rm -rf "$tmp_dir"
        return 1
    fi

    for candidate in "$tmp_dir"/*/templates/shared/skills; do
        if [ -d "$candidate" ]; then
            REMOTE_ARCHIVE_TMP_DIR="$tmp_dir"
            REMOTE_ARCHIVE_SKILLS_DIR="$candidate"
            return 0
        fi
    done

    rm -rf "$tmp_dir"
    return 1
}

install_remote_skill_package_from_archive() {
    local skill="$1"
    local skills_dir="$2"
    local source_skill_dir

    if ! ensure_remote_archive_skills_dir; then
        return 1
    fi

    source_skill_dir="$REMOTE_ARCHIVE_SKILLS_DIR/$skill"
    if [ ! -d "$source_skill_dir" ]; then
        return 1
    fi

    if [ -d "$skills_dir/$skill" ] && ! rm -rf "$skills_dir/$skill"; then
        print_error "Failed to reset skill directory: $skill"
        return 1
    fi

    ensure_dir "$skills_dir/$skill"
    if cp -R "$source_skill_dir/." "$skills_dir/$skill/"; then
        return 0
    fi

    print_error "Failed to copy archived remote skill package: $skill"
    return 1
}

cleanup_remote_archive_snapshot() {
    if [ -n "$REMOTE_ARCHIVE_TMP_DIR" ] && [ -d "$REMOTE_ARCHIVE_TMP_DIR" ]; then
        rm -rf "$REMOTE_ARCHIVE_TMP_DIR"
    fi
    REMOTE_ARCHIVE_TMP_DIR=""
    REMOTE_ARCHIVE_SKILLS_DIR=""
}

ensure_dir() {
    mkdir -p "$1" || {
        print_error "Failed to create directory: $1"
        return 1
    }
}

install_skill_assets() {
    local skill="$1"
    local skills_dir="$2"
    local failed_asset=0
    local rel
    local local_skill_dir="$SCRIPT_DIR/templates/shared/skills/$skill"
    local dest_skill_dir="$skills_dir/$skill"

    if [ -d "$local_skill_dir" ]; then
        if [ -d "$dest_skill_dir" ] && ! rm -rf "$dest_skill_dir"; then
            print_error "Failed to reset skill directory: $skill"
            return 1
        fi

        ensure_dir "$dest_skill_dir"
        if cp -R "$local_skill_dir/." "$dest_skill_dir/"; then
            return 0
        fi

        print_error "Failed to copy local skill package: $skill"
        return 1
    fi

    if install_remote_skill_package "$skill" "$skills_dir"; then
        return 0
    fi

    if install_remote_skill_package_from_archive "$skill" "$skills_dir"; then
        return 0
    fi

    for rel in "${SKILL_ASSET_FILES[@]}"; do
        local dest="$skills_dir/$skill/$rel"
        ensure_dir "$(dirname "$dest")"
        if ! install_template_file "templates/shared/skills/$skill/$rel" "$dest"; then
            print_error "Failed to install skill asset: $skill/$rel"
            failed_asset=1
        fi
    done

    return $failed_asset
}

cleanup_legacy_skills() {
    local skills_dir="$1"
    local removed=0
    local skill

    for skill in "${LEGACY_SKILLS[@]}"; do
        if [ -d "$skills_dir/$skill" ]; then
            if rm -rf "$skills_dir/$skill"; then
                removed=$((removed + 1))
            else
                print_error "Failed to remove legacy skill directory: $skill"
            fi
        fi
    done

    if [ "$removed" -gt 0 ]; then
        print_warning "Removed $removed legacy skill directories" >&2
    fi
}

install_skills() {
    local config_dir=$(get_config_dir)
    local skills_dir="$INSTALL_DIR/$config_dir/skills"
    local installed=0
    local failed=0

    ensure_dir "$skills_dir"
    cleanup_legacy_skills "$skills_dir"
    
    for skill in "${PKG_SKILLS[@]}"; do
        if install_skill_assets "$skill" "$skills_dir"; then
            installed=$((installed + 1))
        else
            print_error "Failed to install skill package: $skill"
            failed=$((failed + 1))
        fi
    done
    
    echo "$installed $failed"
}

transform_agent_for_opencode() {
    local input_file="$1"
    local output_file="$2"
    local agent_id="$3"
    local content
    local desc
    local tools_list
    local tool_name
    local read_enabled="false"
    local write_enabled="false"
    local edit_enabled="false"
    local grep_enabled="false"
    local glob_enabled="false"
    local bash_enabled="false"
    local skill_permissions
    local extra_permissions=""

    # Extract content after frontmatter
    content=$(awk '
        BEGIN { frontmatter_end = 0; delimiter_count = 0 }
        /^---$/ {
            delimiter_count++
            if (delimiter_count == 2) {
                frontmatter_end = 1
            }
            next
        }
        frontmatter_end { print }
    ' "$input_file")

    # Extract description from original file frontmatter
    desc=$(awk '
        BEGIN { in_frontmatter = 0 }
        /^---$/ {
            if (in_frontmatter == 0) {
                in_frontmatter = 1
                next
            }
            exit
        }
        in_frontmatter && /^description:/ {
            sub(/^description:[[:space:]]*/, "", $0)
            gsub(/"/, "", $0)
            print
            exit
        }
    ' "$input_file")

    if [ -z "$desc" ]; then
        desc="$agent_id specialist agent"
    fi

    # Extract tools from original frontmatter and map to OpenCode tool toggles
    tools_list=$(awk '
        BEGIN { in_frontmatter = 0; in_tools = 0 }
        /^---$/ {
            if (in_frontmatter == 0) {
                in_frontmatter = 1
                next
            }
            exit
        }
        in_frontmatter {
            if ($0 ~ /^tools:[[:space:]]*$/) {
                in_tools = 1
                next
            }
            if (in_tools == 1) {
                if ($0 ~ /^[[:space:]]*-[[:space:]]+/) {
                    tool = $0
                    sub(/^[[:space:]]*-[[:space:]]*/, "", tool)
                    gsub(/"/, "", tool)
                    if (length(tool) > 0) {
                        print tool
                    }
                    next
                }
                if ($0 ~ /^[A-Za-z0-9_-]+:/) {
                    in_tools = 0
                }
            }
        }
    ' "$input_file")

    while IFS= read -r tool_name; do
        case "$tool_name" in
            Read) read_enabled="true" ;;
            Write) write_enabled="true" ;;
            Edit) edit_enabled="true" ;;
            Grep) grep_enabled="true" ;;
            Glob) glob_enabled="true" ;;
            Bash) bash_enabled="true" ;;
            Skill) ;;
        esac
    done <<< "$tools_list"

    # Extract skills from original frontmatter and convert to OpenCode permission map
    skill_permissions=$(awk '
        BEGIN { in_frontmatter = 0; in_skills = 0 }
        /^---$/ {
            if (in_frontmatter == 0) {
                in_frontmatter = 1
                next
            }
            exit
        }
        in_frontmatter {
            if ($0 ~ /^skills:[[:space:]]*$/) {
                in_skills = 1
                next
            }
            if (in_skills == 1) {
                if ($0 ~ /^[[:space:]]*-[[:space:]]+/) {
                    skill = $0
                    sub(/^[[:space:]]*-[[:space:]]*/, "", skill)
                    gsub(/"/, "", skill)
                    if (length(skill) > 0) {
                        print "    \"" skill "\": allow"
                    }
                    next
                }
                if ($0 ~ /^[A-Za-z0-9_-]+:/) {
                    in_skills = 0
                }
            }
        }
    ' "$input_file")

    case "$agent_id" in
        auditor)
            extra_permissions=$(cat <<'EOF'
  write:
    "*": deny
  edit:
    "*": deny
  bash:
    "ls *": allow
    "cat *": allow
    "grep *": allow
    "find *": allow
    "tree *": allow
    "git status*": allow
    "git diff*": allow
    "git log*": allow
    "*": deny
EOF
)
            ;;
        docs)
            extra_permissions=$(cat <<'EOF'
  write:
    "**/*.md": allow
    "*": deny
  edit:
    "**/*.md": allow
    "*": deny
  bash:
    "ls *": allow
    "cat *": allow
    "grep *": allow
    "find *": allow
    "tree *": allow
    "git status*": allow
    "git diff*": allow
    "git log*": allow
    "*": deny
EOF
)
            ;;
    esac
    
    # Create OpenCode frontmatter (only valid fields per OpenCode docs)
    cat > "$output_file" << EOF
---
description: $desc
mode: subagent
temperature: 0.7
tools:
  read: $read_enabled
  edit: $edit_enabled
  write: $write_enabled
  grep: $grep_enabled
  glob: $glob_enabled
  bash: $bash_enabled
  task: false
  skill: true
permission:
$extra_permissions
  skill:
$skill_permissions
    "*": deny
---
$content
EOF
}

install_agents() {
    local config_dir=$(get_config_dir)
    local agents_dir
    local installed=0
    local failed=0
    
    if [ "$PLATFORM" = "claude" ]; then
        agents_dir="$INSTALL_DIR/$config_dir/agents"
    else
        # OpenCode agents go in .opencode/agents/ (flat structure, filename = agent name)
        agents_dir="$INSTALL_DIR/$config_dir/agents"
    fi
    
    for agent_path in "${PKG_AGENTS[@]}"; do
        local agent_name="${agent_path#*/}"
        local dest
        local temp_file="/tmp/agent_temp_$$.md"
        
        if [ "$PLATFORM" = "claude" ]; then
            dest="$agents_dir/$agent_name.md"
            ensure_dir "$(dirname "$dest")"
            if install_template_file "templates/shared/agents/$agent_path.md" "$dest"; then
                installed=$((installed + 1))
            else
                print_error "Failed to install agent: $agent_name"
                failed=$((failed + 1))
            fi
        else
            # For OpenCode, agents go in .opencode/agents/{name}.md
            dest="$agents_dir/$agent_name.md"
            ensure_dir "$agents_dir"
            # Download to temp, transform, then save
            if install_template_file "templates/shared/agents/$agent_path.md" "$temp_file"; then
                if transform_agent_for_opencode "$temp_file" "$dest" "$agent_name"; then
                    installed=$((installed + 1))
                else
                    print_error "Failed to transform agent: $agent_name"
                    failed=$((failed + 1))
                fi
                rm -f "$temp_file"
            else
                print_error "Failed to download agent: $agent_name"
                failed=$((failed + 1))
            fi
        fi
    done
    
    echo "$installed $failed"
}

install_commands() {
    local config_dir=$(get_config_dir)
    local commands_dir
    local installed=0
    local failed=0
    
    if [ "$PLATFORM" = "claude" ]; then
        commands_dir="$INSTALL_DIR/$config_dir/commands"
    else
        commands_dir="$INSTALL_DIR/$config_dir/command"
    fi
    
    for cmd in "${PKG_COMMANDS[@]}"; do
        local dest="$commands_dir/$cmd.md"
        ensure_dir "$(dirname "$dest")"
        if install_template_file "templates/shared/commands/$cmd.md" "$dest"; then
            installed=$((installed + 1))
        else
            print_error "Failed to install command: $cmd"
            failed=$((failed + 1))
        fi
    done
    
    echo "$installed $failed"
}

install_system() {
    local installed=0
    local failed=0
    
    if [ "$PLATFORM" = "claude" ]; then
        local config_dir="$INSTALL_DIR/.claude"
        ensure_dir "$config_dir"
        if install_template_file "templates/claude/CLAUDE.md" "$config_dir/CLAUDE.md"; then
            installed=$((installed + 1))
        else
            print_error "Failed to install CLAUDE.md"
            failed=$((failed + 1))
        fi
        if install_template_file "templates/claude/settings.json" "$config_dir/settings.json"; then
            installed=$((installed + 1))
        else
            print_error "Failed to install settings.json"
            failed=$((failed + 1))
        fi
    else
        # OpenCode: Install primary orchestrator agent to .opencode/agents/
        local agents_dir="$INSTALL_DIR/.opencode/agents"
        ensure_dir "$agents_dir"
        if install_template_file "templates/opencode/crewai-orchestrator.md" "$agents_dir/crewai-orchestrator.md"; then
            installed=$((installed + 1))
        else
            print_error "Failed to install orchestrator agent"
            failed=$((failed + 1))
        fi
    fi
    
    echo "$installed $failed"
}

perform_installation() {
    print_step "Installing components..."
    
    # Install system files
    local system_results=$(install_system)
    local system_installed=$(echo "$system_results" | awk 'END {print $1}')
    local system_failed=$(echo "$system_results" | awk 'END {print $2}')
    if [ "$PLATFORM" = "claude" ]; then
        print_success "System files ($system_installed installed, $system_failed failed)"
    else
        print_success "Orchestrator ($system_installed installed, $system_failed failed)"
    fi
    
    # Install skills
    local skills_results=$(install_skills)
    local skills_installed=$(echo "$skills_results" | awk 'END {print $1}')
    local skills_failed=$(echo "$skills_results" | awk 'END {print $2}')
    print_success "Skills ($skills_installed/${#PKG_SKILLS[@]} installed, $skills_failed failed)"
    
    # Install agents
    local agents_results=$(install_agents)
    local agents_installed=$(echo "$agents_results" | awk 'END {print $1}')
    local agents_failed=$(echo "$agents_results" | awk 'END {print $2}')
    print_success "Agents ($agents_installed/${#PKG_AGENTS[@]} installed, $agents_failed failed)"
    
    # Install commands
    local commands_results=$(install_commands)
    local commands_installed=$(echo "$commands_results" | awk 'END {print $1}')
    local commands_failed=$(echo "$commands_results" | awk 'END {print $2}')
    print_success "Commands ($commands_installed/${#PKG_COMMANDS[@]} installed, $commands_failed failed)"
    
    local config_dir=$(get_config_dir)
    
    # Calculate totals
    local total_failed=$((system_failed + skills_failed + agents_failed + commands_failed))
    local total_installed=$((system_installed + skills_installed + agents_installed + commands_installed))
    
    echo ""
    if [ $total_failed -gt 0 ]; then
        echo -e "  ${YELLOW}${BOLD}════════════════════════════════════════════════════════════${NC}"
        echo -e "  ${YELLOW}${BOLD}  Installation completed with warnings${NC}"
        echo -e "  ${YELLOW}${BOLD}════════════════════════════════════════════════════════════${NC}"
        print_warning "$total_failed components failed to install"
        echo "  Check your internet connection and REPO_URL: $REPO_URL"
    else
        echo -e "  ${GREEN}${BOLD}════════════════════════════════════════════════════════════${NC}"
        echo -e "  ${GREEN}${BOLD}  Installation complete!${NC}"
        echo -e "  ${GREEN}${BOLD}════════════════════════════════════════════════════════════${NC}"
    fi
    echo ""
    print_info "Installed to: $INSTALL_DIR/$config_dir"
    echo ""
    echo -e "  ${CYAN}Next steps:${NC}"
    if [ "$PLATFORM" = "claude" ]; then
        echo "    1. Open Claude Code in your project"
        echo "    2. Run /crew init"
    else
        echo "    1. Open OpenCode in your project"
        echo "    2. Run @crewai-orchestrator or /crew init"
    fi
    echo ""
}

#############################################################################
# Interactive TUI
#############################################################################

show_platform_menu() {
    clear
    print_header
    
    echo -e "  ${BOLD}Step 1/3 - Choose platform:${NC}\n"
    echo "    1) Claude Code"
    echo "    2) OpenCode"
    echo ""
    read -r -p "  Enter choice [1-2]: " choice
    
    case $choice in
        1) PLATFORM="claude" ;;
        2) PLATFORM="opencode" ;;
        *) print_error "Invalid choice"; sleep 1; show_platform_menu ;;
    esac
}

show_location_menu() {
    clear
    print_header
    
    echo -e "  ${BOLD}Step 2/3 - Choose location:${NC}\n"
    echo "    1) Current directory ($(pwd))"
    echo "    2) Enter custom path"
    echo ""
    read -r -p "  Enter choice [1-2]: " choice
    
    case $choice in
        1) INSTALL_DIR="$(pwd)" ;;
        2) 
            echo ""
            read -r -p "  Enter path: " custom_path
            INSTALL_DIR="${custom_path/#\~/$HOME}"
            if [ ! -d "$INSTALL_DIR" ]; then
                mkdir -p "$INSTALL_DIR"
            fi
            ;;
        *) print_error "Invalid choice"; sleep 1; show_location_menu ;;
    esac
}

show_confirm_menu() {
    local config_dir=$(get_config_dir)
    
    clear
    print_header
    
    echo -e "  ${BOLD}Step 3/3 - Confirm installation:${NC}\n"
    echo -e "  Platform:  ${CYAN}$PLATFORM${NC}"
    echo -e "  Location:  ${CYAN}$INSTALL_DIR${NC}"
    echo -e "  Config:    ${CYAN}$config_dir${NC}"
    echo ""
    echo "  Components:"
    echo "    • Skills (${#PKG_SKILLS[@]})"
    echo "    • Agents (${#PKG_AGENTS[@]})"
    echo "    • Commands (${#PKG_COMMANDS[@]})"
    if [ "$PLATFORM" = "claude" ]; then
        echo "    • System prompt (CLAUDE.md)"
    else
        echo "    • Orchestrator agent"
    fi
    echo ""
    
    # Check existing
    if [ -d "$INSTALL_DIR/$config_dir" ]; then
        print_warning "Existing $config_dir found - files will be added/updated"
        echo ""
    fi
    
    read -r -p "  Proceed? [Y/n]: " confirm
    if [[ "$confirm" =~ ^[Nn]$ ]]; then
        print_info "Cancelled"
        exit 0
    fi
}

run_interactive() {
    check_interactive_mode
    show_platform_menu
    show_location_menu
    show_confirm_menu
    perform_installation
}

#############################################################################
# Non-Interactive Mode
#############################################################################

run_non_interactive() {
    print_header
    print_success "Platform: $PLATFORM"
    print_success "Location: $INSTALL_DIR"
    perform_installation
}

#############################################################################
# Main
#############################################################################

main() {
    # Parse arguments
    while [ $# -gt 0 ]; do
        case "$1" in
            claude|--claude)
                PLATFORM="claude"
                NON_INTERACTIVE=true
                shift
                ;;
            opencode|--opencode)
                PLATFORM="opencode"
                NON_INTERACTIVE=true
                shift
                ;;
            --dir=*)
                INSTALL_DIR="${1#*=}"
                shift
                ;;
            --help|-h)
                print_header
                echo "Usage: install.sh [PLATFORM] [OPTIONS]"
                echo ""
                echo "Platforms:"
                echo "  claude      Install for Claude Code"
                echo "  opencode    Install for OpenCode"
                echo ""
                echo "Options:"
                echo "  --dir=PATH  Custom installation directory"
                echo "  --help      Show this help"
                echo ""
                echo "Examples:"
                echo "  # Interactive mode"
                echo "  bash install.sh"
                echo ""
                echo "  # Quick install for Claude Code"
                echo "  curl -fsSL URL/install.sh | bash -s claude"
                echo ""
                echo "  # Install to custom directory"
                echo "  bash install.sh claude --dir=~/my-project"
                echo ""
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                exit 1
                ;;
        esac
    done
    
    # Set default install dir if not specified
    if [ -z "$INSTALL_DIR" ]; then
        INSTALL_DIR="$(pwd)"
    fi
    
    if [ "$NON_INTERACTIVE" = true ]; then
        run_non_interactive
    else
        run_interactive
    fi
}

trap cleanup_remote_archive_snapshot EXIT
main "$@"
