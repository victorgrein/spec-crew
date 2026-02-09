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
REPO_URL="https://raw.githubusercontent.com/victorgrein/cli-agents-config/main"
INSTALL_DIR=""
PLATFORM=""
NON_INTERACTIVE=false

# Package contents
# BEGIN GENERATED: TOOLKIT_PACKAGE_LISTS
PKG_SKILLS=(
    "core-build"
    "flows"
    "runtime"
    "tools"
    "migration"
    "governance"
)

PKG_AGENTS=(
    "crewai/builder"
    "crewai/runtime"
    "crewai/flow"
    "crewai/docs"
)

PKG_WORKFLOWS=(
    "create-crew"
    "debug-crew"
    "optimize-crew"
    "migrate-project"
    "create-flow"
)

PKG_COMMANDS=(
    "crew/init"
    "crew/inspect"
    "crew/fix"
    "crew/evolve"
    "crew/docs"
)
# END GENERATED: TOOLKIT_PACKAGE_LISTS






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
print_error() { echo -e "  ${RED}✗${NC} $1"; }
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

ensure_dir() {
    mkdir -p "$1" || {
        print_error "Failed to create directory: $1"
        return 1
    }
}

install_skills() {
    local config_dir=$(get_config_dir)
    local skills_dir="$INSTALL_DIR/$config_dir/skills"
    local installed=0
    local failed=0
    
    for skill in "${PKG_SKILLS[@]}"; do
        local dest="$skills_dir/$skill/SKILL.md"
        ensure_dir "$(dirname "$dest")"
        if download_file "$REPO_URL/templates/shared/skills/$skill/SKILL.md" "$dest"; then
            installed=$((installed + 1))
        else
            print_error "Failed to install skill: $skill"
            failed=$((failed + 1))
        fi
    done
    
    echo "$installed $failed"
}

install_workflows() {
    local config_dir=$(get_config_dir)
    local skills_dir="$INSTALL_DIR/$config_dir/skills"
    local installed=0
    local failed=0
    
    for workflow in "${PKG_WORKFLOWS[@]}"; do
        local dest="$skills_dir/$workflow/SKILL.md"
        ensure_dir "$(dirname "$dest")"
        if download_file "$REPO_URL/templates/shared/workflows/$workflow/SKILL.md" "$dest"; then
            installed=$((installed + 1))
        else
            print_error "Failed to install workflow: $workflow"
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
    local skill_permissions

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
    
    # Create OpenCode frontmatter (only valid fields per OpenCode docs)
    cat > "$output_file" << EOF
---
description: $desc
mode: subagent
temperature: 0.7
tools:
  read: true
  edit: true
  write: true
  grep: true
  glob: true
  bash: true
  task: true
  skill: true
permission:
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
            if download_file "$REPO_URL/templates/shared/agents/$agent_path.md" "$dest"; then
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
            if download_file "$REPO_URL/templates/shared/agents/$agent_path.md" "$temp_file"; then
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
        if download_file "$REPO_URL/templates/shared/commands/$cmd.md" "$dest"; then
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
        if download_file "$REPO_URL/templates/claude/CLAUDE.md" "$config_dir/CLAUDE.md"; then
            installed=$((installed + 1))
        else
            print_error "Failed to install CLAUDE.md"
            failed=$((failed + 1))
        fi
        if download_file "$REPO_URL/templates/claude/settings.json" "$config_dir/settings.json"; then
            installed=$((installed + 1))
        else
            print_error "Failed to install settings.json"
            failed=$((failed + 1))
        fi
    else
        # OpenCode: Install primary orchestrator agent to .opencode/agents/
        local agents_dir="$INSTALL_DIR/.opencode/agents"
        ensure_dir "$agents_dir"
        if download_file "$REPO_URL/templates/opencode/crewai-orchestrator.md" "$agents_dir/crewai-orchestrator.md"; then
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
    local system_installed=$(echo "$system_results" | awk '{print $1}')
    local system_failed=$(echo "$system_results" | awk '{print $2}')
    if [ "$PLATFORM" = "claude" ]; then
        print_success "System files ($system_installed installed, $system_failed failed)"
    else
        print_success "Orchestrator ($system_installed installed, $system_failed failed)"
    fi
    
    # Install skills
    local skills_results=$(install_skills)
    local skills_installed=$(echo "$skills_results" | awk '{print $1}')
    local skills_failed=$(echo "$skills_results" | awk '{print $2}')
    print_success "Skills ($skills_installed/${#PKG_SKILLS[@]} installed, $skills_failed failed)"
    
    # Install workflows
    local workflows_results=$(install_workflows)
    local workflows_installed=$(echo "$workflows_results" | awk '{print $1}')
    local workflows_failed=$(echo "$workflows_results" | awk '{print $2}')
    print_success "Workflows ($workflows_installed/${#PKG_WORKFLOWS[@]} installed, $workflows_failed failed)"
    
    # Install agents
    local agents_results=$(install_agents)
    local agents_installed=$(echo "$agents_results" | awk '{print $1}')
    local agents_failed=$(echo "$agents_results" | awk '{print $2}')
    print_success "Agents ($agents_installed/${#PKG_AGENTS[@]} installed, $agents_failed failed)"
    
    # Install commands
    local commands_results=$(install_commands)
    local commands_installed=$(echo "$commands_results" | awk '{print $1}')
    local commands_failed=$(echo "$commands_results" | awk '{print $2}')
    print_success "Commands ($commands_installed/${#PKG_COMMANDS[@]} installed, $commands_failed failed)"
    
    local config_dir=$(get_config_dir)
    
    # Calculate totals
    local total_failed=$((system_failed + skills_failed + workflows_failed + agents_failed + commands_failed))
    local total_installed=$((system_installed + skills_installed + workflows_installed + agents_installed + commands_installed))
    
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
    echo "    • Workflows (${#PKG_WORKFLOWS[@]})"
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

main "$@"
