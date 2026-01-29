#!/usr/bin/env bash
#############################################################################
# CrewAI Skills Installer
# Interactive TUI for Claude Code and OpenCode
#
# Usage:
#   bash <(curl -fsSL URL/install.sh)
#   curl -fsSL URL/install.sh | bash
#
#############################################################################

set -e

#############################################################################
# Colors & Styling
#############################################################################

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'

#############################################################################
# Configuration
#############################################################################

REPO_URL="https://raw.githubusercontent.com/victorgrein/cli-agents-config/main"

# Selected options (will be set by TUI)
PLATFORM=""
INSTALL_SCOPE=""
TARGET_DIR=""
INSTALL_MODE=""

# Package contents
PKG_SKILLS=(
    "crewai-agents"
    "crewai-tasks"
    "crewai-crews"
    "crewai-flows"
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
    "task-management"
)

PKG_AGENTS=(
    "crewai/crew-architect"
    "crewai/agent-designer"
    "crewai/task-designer"
    "crewai/flow-engineer"
    "crewai/tool-specialist"
    "crewai/debugger"
    "crewai/llm-optimizer"
    "crewai/migration-specialist"
    "crewai/performance-analyst"
    "crewai/crewai-documenter"
)

PKG_WORKFLOWS=(
    "create-crew"
    "debug-crew"
    "optimize-crew"
    "migrate-project"
    "create-flow"
)

PKG_COMMANDS=(
    "crew/create"
    "crew/analyze"
    "crew/debug"
    "crew/diagram"
    "crew/docs"
    "crew/migrate"
    "crew/optimize"
    "crew/review"
)

# What to install (set by scope selection)
INSTALL_SKILLS=true
INSTALL_AGENTS=true
INSTALL_WORKFLOWS=true
INSTALL_COMMANDS=true
INSTALL_SYSTEM=true

#############################################################################
# TUI Helper Functions
#############################################################################

clear_screen() {
    printf "\033[2J\033[H"
}

hide_cursor() {
    printf "\033[?25l"
}

show_cursor() {
    printf "\033[?25h"
}

move_cursor() {
    printf "\033[%d;%dH" "$1" "$2"
}

print_header() {
    echo -e "${CYAN}${BOLD}"
    echo "  ╔══════════════════════════════════════════════════════════╗"
    echo "  ║                                                          ║"
    echo "  ║            CrewAI Skills Installer                       ║"
    echo "  ║                                                          ║"
    echo "  ╚══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_step_header() {
    local step="$1"
    local title="$2"
    echo -e "\n  ${DIM}Step $step${NC}"
    echo -e "  ${WHITE}${BOLD}$title${NC}\n"
}

print_option() {
    local selected="$1"
    local label="$2"
    local description="$3"
    
    if [ "$selected" = true ]; then
        echo -e "    ${CYAN}${BOLD}▸ $label${NC}"
        if [ -n "$description" ]; then
            echo -e "      ${DIM}$description${NC}"
        fi
    else
        echo -e "    ${DIM}  $label${NC}"
    fi
}

print_success() {
    echo -e "  ${GREEN}✓${NC} $1"
}

print_info() {
    echo -e "  ${BLUE}ℹ${NC} $1"
}

print_warning() {
    echo -e "  ${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "  ${RED}✗${NC} $1"
}

#############################################################################
# TUI Menu System
#############################################################################

# Read a single keypress (from /dev/tty to work with curl pipe)
read_key() {
    local key
    IFS= read -rsn1 key </dev/tty 2>/dev/null || true
    
    # Handle arrow keys (escape sequences)
    if [[ $key == $'\x1b' ]]; then
        read -rsn2 -t 0.1 key </dev/tty 2>/dev/null || true
        case "$key" in
            '[A') echo "up" ;;
            '[B') echo "down" ;;
            *) echo "" ;;
        esac
    elif [[ $key == "" ]]; then
        echo "enter"
    else
        echo "$key"
    fi
}

# Generic menu selector
# Usage: select_menu "prompt" "option1" "option2" ...
# Returns: selected index (0-based)
select_menu() {
    local prompt="$1"
    shift
    local options=("$@")
    local selected=0
    local count=${#options[@]}
    
    hide_cursor
    
    while true; do
        # Clear and redraw
        clear_screen
        print_header
        print_step_header "$CURRENT_STEP" "$prompt"
        
        for i in "${!options[@]}"; do
            if [ $i -eq $selected ]; then
                print_option true "${options[$i]}"
            else
                print_option false "${options[$i]}"
            fi
            echo ""
        done
        
        echo -e "\n  ${DIM}↑/↓ Navigate  •  Enter Select${NC}"
        
        # Read input
        local key=$(read_key)
        
        case "$key" in
            up)
                ((selected--))
                [ $selected -lt 0 ] && selected=$((count - 1))
                ;;
            down)
                ((selected++))
                [ $selected -ge $count ] && selected=0
                ;;
            enter)
                show_cursor
                echo $selected
                return
                ;;
        esac
    done
}

# Multi-select menu
# Usage: multiselect_menu "prompt" "option1" "option2" ...
# Returns: space-separated indices of selected items
multiselect_menu() {
    local prompt="$1"
    shift
    local options=("$@")
    local count=${#options[@]}
    local cursor=0
    
    # Initialize all as selected
    local selected=()
    for i in "${!options[@]}"; do
        selected[$i]=true
    done
    
    hide_cursor
    
    while true; do
        clear_screen
        print_header
        print_step_header "$CURRENT_STEP" "$prompt"
        
        for i in "${!options[@]}"; do
            local checkbox
            if [ "${selected[$i]}" = true ]; then
                checkbox="${GREEN}[✓]${NC}"
            else
                checkbox="${DIM}[ ]${NC}"
            fi
            
            if [ $i -eq $cursor ]; then
                echo -e "    ${CYAN}${BOLD}▸${NC} $checkbox ${WHITE}${options[$i]}${NC}"
            else
                echo -e "      $checkbox ${DIM}${options[$i]}${NC}"
            fi
        done
        
        echo -e "\n  ${DIM}↑/↓ Navigate  •  Space Toggle  •  Enter Confirm${NC}"
        
        local key=$(read_key)
        
        case "$key" in
            up)
                ((cursor--))
                [ $cursor -lt 0 ] && cursor=$((count - 1))
                ;;
            down)
                ((cursor++))
                [ $cursor -ge $count ] && cursor=0
                ;;
            " ")
                if [ "${selected[$cursor]}" = true ]; then
                    selected[$cursor]=false
                else
                    selected[$cursor]=true
                fi
                ;;
            enter)
                show_cursor
                local result=""
                for i in "${!selected[@]}"; do
                    if [ "${selected[$i]}" = true ]; then
                        result="$result $i"
                    fi
                done
                echo $result
                return
                ;;
        esac
    done
}

# Text input (from /dev/tty to work with curl pipe)
# Usage: text_input "prompt" "default"
text_input() {
    local prompt="$1"
    local default="$2"
    
    clear_screen
    print_header
    print_step_header "$CURRENT_STEP" "$prompt"
    
    echo -e "  ${DIM}Press Enter to use: ${NC}${CYAN}$default${NC}"
    echo ""
    echo -ne "  ${WHITE}Path:${NC} "
    
    local input
    read -r input </dev/tty
    
    if [ -z "$input" ]; then
        echo "$default"
    else
        # Expand ~ to home directory
        echo "${input/#\~/$HOME}"
    fi
}

#############################################################################
# Installation Functions
#############################################################################

get_config_dir() {
    if [ "$PLATFORM" = "claude" ]; then
        echo ".claude"
    else
        echo ".opencode"
    fi
}

download_file() {
    local url="$1"
    local dest="$2"
    curl -fsSL "$url" -o "$dest" 2>/dev/null
}

ensure_dir() {
    mkdir -p "$1" 2>/dev/null || true
}

install_skills() {
    local config_dir=$(get_config_dir)
    local skills_dir="$TARGET_DIR/$config_dir/skills"
    
    for skill in "${PKG_SKILLS[@]}"; do
        local source_url="$REPO_URL/templates/shared/skills/$skill/SKILL.md"
        local dest_file="$skills_dir/$skill/SKILL.md"
        
        ensure_dir "$(dirname "$dest_file")"
        download_file "$source_url" "$dest_file" || true
        
        # Try to download references
        local refs_url="$REPO_URL/templates/shared/skills/$skill/references"
        local refs_dir="$skills_dir/$skill/references"
        
        # Common reference file patterns
        for ref_name in "${skill}-reference.md" "reference.md"; do
            local ref_url="$refs_url/$ref_name"
            if curl -fsSL --head "$ref_url" 2>/dev/null | grep -q "200"; then
                ensure_dir "$refs_dir"
                download_file "$ref_url" "$refs_dir/$ref_name" || true
            fi
        done
    done
}

install_workflows() {
    local config_dir=$(get_config_dir)
    local skills_dir="$TARGET_DIR/$config_dir/skills"
    
    for workflow in "${PKG_WORKFLOWS[@]}"; do
        local source_url="$REPO_URL/templates/shared/workflows/$workflow/SKILL.md"
        local dest_file="$skills_dir/$workflow/SKILL.md"
        
        ensure_dir "$(dirname "$dest_file")"
        download_file "$source_url" "$dest_file" || true
    done
}

install_agents() {
    local config_dir=$(get_config_dir)
    local agents_dir
    
    if [ "$PLATFORM" = "claude" ]; then
        agents_dir="$TARGET_DIR/$config_dir/agents"
    else
        agents_dir="$TARGET_DIR/$config_dir/agent/subagents"
    fi
    
    for agent_path in "${PKG_AGENTS[@]}"; do
        local agent_name="${agent_path#*/}"
        local source_url="$REPO_URL/templates/shared/agents/$agent_path.md"
        local dest_file
        
        if [ "$PLATFORM" = "claude" ]; then
            dest_file="$agents_dir/$agent_name.md"
        else
            dest_file="$agents_dir/crewai/$agent_name.md"
        fi
        
        ensure_dir "$(dirname "$dest_file")"
        download_file "$source_url" "$dest_file" || true
    done
}

install_commands() {
    local config_dir=$(get_config_dir)
    local commands_dir
    
    if [ "$PLATFORM" = "claude" ]; then
        commands_dir="$TARGET_DIR/$config_dir/commands"
    else
        commands_dir="$TARGET_DIR/$config_dir/command"
    fi
    
    for cmd_path in "${PKG_COMMANDS[@]}"; do
        local source_url="$REPO_URL/templates/shared/commands/$cmd_path.md"
        local dest_file="$commands_dir/$cmd_path.md"
        
        ensure_dir "$(dirname "$dest_file")"
        download_file "$source_url" "$dest_file" || true
    done
}

install_system_prompt() {
    if [ "$PLATFORM" != "claude" ]; then
        return
    fi
    
    local config_dir="$TARGET_DIR/.claude"
    ensure_dir "$config_dir"
    
    download_file "$REPO_URL/templates/claude/CLAUDE.md" "$config_dir/CLAUDE.md" || true
    download_file "$REPO_URL/templates/claude/settings.json" "$config_dir/settings.json" || true
}

backup_existing() {
    local config_dir=$(get_config_dir)
    local existing_dir="$TARGET_DIR/$config_dir"
    
    if [ -d "$existing_dir" ]; then
        local timestamp=$(date +%Y%m%d_%H%M%S)
        local backup_dir="$TARGET_DIR/.crewai-backup-$timestamp"
        cp -r "$existing_dir" "$backup_dir"
        print_info "Backup created: $backup_dir"
    fi
}

#############################################################################
# Main TUI Flow
#############################################################################

run_tui() {
    # Check if /dev/tty is available
    if [ ! -e /dev/tty ]; then
        print_error "This installer requires a terminal"
        exit 1
    fi
    
    trap 'show_cursor; exit' INT TERM
    
    # Step 1: Platform Selection
    CURRENT_STEP="1/4"
    local platform_idx=$(select_menu "Which platform are you using?" \
        "Claude Code" \
        "OpenCode")
    
    case $platform_idx in
        0) PLATFORM="claude" ;;
        1) PLATFORM="opencode" ;;
    esac
    
    # Step 2: Installation Scope
    CURRENT_STEP="2/4"
    local scope_idx=$(select_menu "What would you like to install?" \
        "Everything (Recommended)" \
        "Let me choose specific components")
    
    if [ "$scope_idx" -eq 1 ]; then
        CURRENT_STEP="2/4"
        local components=$(multiselect_menu "Select components to install:" \
            "Skills (16 CrewAI knowledge modules)" \
            "Agents (10 specialist assistants)" \
            "Workflows (5 guided processes)" \
            "Commands (8 slash commands)" \
            "System Prompt (CLAUDE.md orchestrator)")
        
        INSTALL_SKILLS=false
        INSTALL_AGENTS=false
        INSTALL_WORKFLOWS=false
        INSTALL_COMMANDS=false
        INSTALL_SYSTEM=false
        
        for idx in $components; do
            case $idx in
                0) INSTALL_SKILLS=true ;;
                1) INSTALL_AGENTS=true ;;
                2) INSTALL_WORKFLOWS=true ;;
                3) INSTALL_COMMANDS=true ;;
                4) INSTALL_SYSTEM=true ;;
            esac
        done
    fi
    
    # Step 3: Target Directory
    CURRENT_STEP="3/4"
    local location_idx=$(select_menu "Where do you want to install?" \
        "Current directory ($(pwd))" \
        "Different location")
    
    if [ "$location_idx" -eq 0 ]; then
        TARGET_DIR="$(pwd)"
    else
        CURRENT_STEP="3/4"
        TARGET_DIR=$(text_input "Enter the project path:" "$(pwd)")
        
        # Create if doesn't exist
        if [ ! -d "$TARGET_DIR" ]; then
            mkdir -p "$TARGET_DIR" 2>/dev/null || {
                print_error "Could not create directory: $TARGET_DIR"
                exit 1
            }
        fi
    fi
    
    # Step 4: Check for existing installation
    local config_dir=$(get_config_dir)
    if [ -d "$TARGET_DIR/$config_dir" ]; then
        CURRENT_STEP="4/4"
        local mode_idx=$(select_menu "Found existing $config_dir folder. What would you like to do?" \
            "Add new files (keep your customisations)" \
            "Overwrite everything (fresh install)")
        
        if [ "$mode_idx" -eq 1 ]; then
            INSTALL_MODE="overwrite"
        else
            INSTALL_MODE="add"
        fi
    else
        INSTALL_MODE="new"
    fi
    
    # Show summary and confirm
    clear_screen
    print_header
    
    echo -e "  ${WHITE}${BOLD}Installation Summary${NC}\n"
    echo -e "  ${CYAN}Platform:${NC}    $PLATFORM"
    echo -e "  ${CYAN}Location:${NC}    $TARGET_DIR"
    echo -e "  ${CYAN}Mode:${NC}        $INSTALL_MODE"
    echo ""
    echo -e "  ${CYAN}Components:${NC}"
    [ "$INSTALL_SKILLS" = true ] && echo "    ✓ Skills (16)"
    [ "$INSTALL_AGENTS" = true ] && echo "    ✓ Agents (10)"
    [ "$INSTALL_WORKFLOWS" = true ] && echo "    ✓ Workflows (5)"
    [ "$INSTALL_COMMANDS" = true ] && echo "    ✓ Commands (8)"
    [ "$INSTALL_SYSTEM" = true ] && [ "$PLATFORM" = "claude" ] && echo "    ✓ System Prompt"
    echo ""
    
    echo -ne "  ${WHITE}Proceed with installation? ${NC}${DIM}[Y/n]${NC} "
    read -r confirm </dev/tty
    
    if [[ "$confirm" =~ ^[Nn]$ ]]; then
        echo ""
        print_info "Installation cancelled"
        exit 0
    fi
    
    # Perform installation
    echo ""
    echo -e "  ${WHITE}${BOLD}Installing...${NC}\n"
    
    # Backup if overwriting
    if [ "$INSTALL_MODE" = "overwrite" ]; then
        backup_existing
        rm -rf "$TARGET_DIR/$config_dir"
    fi
    
    # Install components
    if [ "$INSTALL_SYSTEM" = true ] && [ "$PLATFORM" = "claude" ]; then
        install_system_prompt
        print_success "System prompt"
    fi
    
    if [ "$INSTALL_SKILLS" = true ]; then
        install_skills
        print_success "Skills (${#PKG_SKILLS[@]})"
    fi
    
    if [ "$INSTALL_WORKFLOWS" = true ]; then
        install_workflows
        print_success "Workflows (${#PKG_WORKFLOWS[@]})"
    fi
    
    if [ "$INSTALL_AGENTS" = true ]; then
        install_agents
        print_success "Agents (${#PKG_AGENTS[@]})"
    fi
    
    if [ "$INSTALL_COMMANDS" = true ]; then
        install_commands
        print_success "Commands (${#PKG_COMMANDS[@]})"
    fi
    
    # Done!
    echo ""
    echo -e "  ${GREEN}${BOLD}════════════════════════════════════════════════════════════${NC}"
    echo -e "  ${GREEN}${BOLD}  Installation complete!${NC}"
    echo -e "  ${GREEN}${BOLD}════════════════════════════════════════════════════════════${NC}"
    echo ""
    print_info "Installed to: $TARGET_DIR/$config_dir"
    echo ""
    
    if [ "$PLATFORM" = "claude" ]; then
        echo -e "  ${CYAN}Next steps:${NC}"
        echo "    1. Open Claude Code in your project"
        echo "    2. Run ${WHITE}/crew create${NC} to build your first crew"
        echo "    3. Or just ask Claude about CrewAI"
    else
        echo -e "  ${CYAN}Next steps:${NC}"
        echo "    1. Open OpenCode in your project"
        echo "    2. Run ${WHITE}/crew create${NC} to build your first crew"
    fi
    echo ""
}

#############################################################################
# Entry Point
#############################################################################

run_tui
