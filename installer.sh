#!/usr/bin/env bash
#############################################################################
# CrewAI Skills Installer
# Interactive TUI for Claude Code and OpenCode
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

# Selected options
PLATFORM=""
TARGET_DIR=""
INSTALL_MODE=""

# What to install
INSTALL_SKILLS=true
INSTALL_AGENTS=true
INSTALL_WORKFLOWS=true
INSTALL_COMMANDS=true
INSTALL_SYSTEM=true

# Package contents
PKG_SKILLS=(
    "crewai-agents" "crewai-tasks" "crewai-crews" "crewai-flows"
    "crewai-tools" "crewai-llms" "crewai-memory" "crewai-processes"
    "crewai-cli" "crewai-debugging" "crewai-optimization" "crewai-migration"
    "crewai-crew-creation" "crewai-code-quality" "crewai-project-structure"
    "task-management"
)

PKG_AGENTS=(
    "crewai/crew-architect" "crewai/agent-designer" "crewai/task-designer"
    "crewai/flow-engineer" "crewai/tool-specialist" "crewai/debugger"
    "crewai/llm-optimizer" "crewai/migration-specialist"
    "crewai/performance-analyst" "crewai/crewai-documenter"
)

PKG_WORKFLOWS=("create-crew" "debug-crew" "optimize-crew" "migrate-project" "create-flow")

PKG_COMMANDS=(
    "crew/create" "crew/analyze" "crew/debug" "crew/diagram"
    "crew/docs" "crew/migrate" "crew/optimize" "crew/review"
)

#############################################################################
# UI Helpers
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

print_header() {
    echo -e "${CYAN}${BOLD}"
    echo "  ╔══════════════════════════════════════════════════════════╗"
    echo "  ║                                                          ║"
    echo "  ║            CrewAI Skills Installer                       ║"
    echo "  ║                                                          ║"
    echo "  ╚══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_step() {
    local step="$1"
    local title="$2"
    echo -e "\n  ${DIM}Step $step${NC}"
    echo -e "  ${WHITE}${BOLD}$title${NC}\n"
}

print_success() {
    echo -e "  ${GREEN}✓${NC} $1"
}

print_info() {
    echo -e "  ${BLUE}ℹ${NC} $1"
}

print_error() {
    echo -e "  ${RED}✗${NC} $1"
}

#############################################################################
# Menu System
#############################################################################

select_option() {
    local prompt="$1"
    shift
    local options=("$@")
    local selected=0
    local count=${#options[@]}
    
    hide_cursor
    trap 'show_cursor' RETURN
    
    while true; do
        clear_screen
        print_header
        print_step "$CURRENT_STEP" "$prompt"
        
        for i in "${!options[@]}"; do
            if [ $i -eq $selected ]; then
                echo -e "    ${CYAN}${BOLD}▸ ${options[$i]}${NC}"
            else
                echo -e "    ${DIM}  ${options[$i]}${NC}"
            fi
        done
        
        echo -e "\n  ${DIM}↑/↓ Navigate  •  Enter Select${NC}"
        
        # Read single keypress
        IFS= read -rsn1 key
        
        case "$key" in
            $'\x1b')  # Escape sequence
                read -rsn2 -t 0.1 seq
                case "$seq" in
                    '[A') ((selected > 0)) && ((selected--)) ;;
                    '[B') ((selected < count-1)) && ((selected++)) ;;
                esac
                ;;
            '')  # Enter
                show_cursor
                return $selected
                ;;
        esac
    done
}

multiselect_option() {
    local prompt="$1"
    shift
    local options=("$@")
    local count=${#options[@]}
    local cursor=0
    
    # All selected by default
    local -a selected
    for ((i=0; i<count; i++)); do selected[$i]=1; done
    
    hide_cursor
    trap 'show_cursor' RETURN
    
    while true; do
        clear_screen
        print_header
        print_step "$CURRENT_STEP" "$prompt"
        
        for i in "${!options[@]}"; do
            local check
            [ "${selected[$i]}" -eq 1 ] && check="${GREEN}[✓]${NC}" || check="${DIM}[ ]${NC}"
            
            if [ $i -eq $cursor ]; then
                echo -e "    ${CYAN}▸${NC} $check ${WHITE}${options[$i]}${NC}"
            else
                echo -e "      $check ${DIM}${options[$i]}${NC}"
            fi
        done
        
        echo -e "\n  ${DIM}↑/↓ Navigate  •  Space Toggle  •  Enter Confirm${NC}"
        
        IFS= read -rsn1 key
        
        case "$key" in
            $'\x1b')
                read -rsn2 -t 0.1 seq
                case "$seq" in
                    '[A') ((cursor > 0)) && ((cursor--)) ;;
                    '[B') ((cursor < count-1)) && ((cursor++)) ;;
                esac
                ;;
            ' ')  # Space - toggle
                [ "${selected[$cursor]}" -eq 1 ] && selected[$cursor]=0 || selected[$cursor]=1
                ;;
            '')  # Enter
                show_cursor
                # Return space-separated list of selected indices
                local result=""
                for i in "${!selected[@]}"; do
                    [ "${selected[$i]}" -eq 1 ] && result="$result$i "
                done
                echo "$result"
                return
                ;;
        esac
    done
}

text_input() {
    local prompt="$1"
    local default="$2"
    
    clear_screen
    print_header
    print_step "$CURRENT_STEP" "$prompt"
    
    echo -e "  ${DIM}Press Enter for:${NC} ${CYAN}$default${NC}\n"
    echo -ne "  ${WHITE}Path:${NC} "
    
    read -r input
    
    [ -z "$input" ] && echo "$default" || echo "${input/#\~/$HOME}"
}

#############################################################################
# Installation Functions
#############################################################################

get_config_dir() {
    [ "$PLATFORM" = "claude" ] && echo ".claude" || echo ".opencode"
}

download_file() {
    curl -fsSL "$1" -o "$2" 2>/dev/null
}

ensure_dir() {
    mkdir -p "$1" 2>/dev/null || true
}

install_skills() {
    local config_dir=$(get_config_dir)
    local skills_dir="$TARGET_DIR/$config_dir/skills"
    
    for skill in "${PKG_SKILLS[@]}"; do
        local dest="$skills_dir/$skill/SKILL.md"
        ensure_dir "$(dirname "$dest")"
        download_file "$REPO_URL/templates/shared/skills/$skill/SKILL.md" "$dest" || true
    done
}

install_workflows() {
    local config_dir=$(get_config_dir)
    local skills_dir="$TARGET_DIR/$config_dir/skills"
    
    for workflow in "${PKG_WORKFLOWS[@]}"; do
        local dest="$skills_dir/$workflow/SKILL.md"
        ensure_dir "$(dirname "$dest")"
        download_file "$REPO_URL/templates/shared/workflows/$workflow/SKILL.md" "$dest" || true
    done
}

install_agents() {
    local config_dir=$(get_config_dir)
    local agents_dir
    
    [ "$PLATFORM" = "claude" ] && agents_dir="$TARGET_DIR/$config_dir/agents" || agents_dir="$TARGET_DIR/$config_dir/agent/subagents"
    
    for agent_path in "${PKG_AGENTS[@]}"; do
        local agent_name="${agent_path#*/}"
        local dest
        [ "$PLATFORM" = "claude" ] && dest="$agents_dir/$agent_name.md" || dest="$agents_dir/crewai/$agent_name.md"
        
        ensure_dir "$(dirname "$dest")"
        download_file "$REPO_URL/templates/shared/agents/$agent_path.md" "$dest" || true
    done
}

install_commands() {
    local config_dir=$(get_config_dir)
    local commands_dir
    
    [ "$PLATFORM" = "claude" ] && commands_dir="$TARGET_DIR/$config_dir/commands" || commands_dir="$TARGET_DIR/$config_dir/command"
    
    for cmd in "${PKG_COMMANDS[@]}"; do
        local dest="$commands_dir/$cmd.md"
        ensure_dir "$(dirname "$dest")"
        download_file "$REPO_URL/templates/shared/commands/$cmd.md" "$dest" || true
    done
}

install_system() {
    [ "$PLATFORM" != "claude" ] && return
    
    local config_dir="$TARGET_DIR/.claude"
    ensure_dir "$config_dir"
    
    download_file "$REPO_URL/templates/claude/CLAUDE.md" "$config_dir/CLAUDE.md" || true
    download_file "$REPO_URL/templates/claude/settings.json" "$config_dir/settings.json" || true
}

backup_existing() {
    local config_dir=$(get_config_dir)
    local existing="$TARGET_DIR/$config_dir"
    
    [ ! -d "$existing" ] && return
    
    local backup="$TARGET_DIR/.crewai-backup-$(date +%Y%m%d_%H%M%S)"
    cp -r "$existing" "$backup"
    print_info "Backup: $backup"
}

#############################################################################
# Main Flow
#############################################################################

main() {
    trap 'show_cursor; exit' INT TERM
    
    # Step 1: Platform
    CURRENT_STEP="1/4"
    select_option "Which platform are you using?" "Claude Code" "OpenCode"
    [ $? -eq 0 ] && PLATFORM="claude" || PLATFORM="opencode"
    
    # Step 2: Scope
    CURRENT_STEP="2/4"
    select_option "What would you like to install?" "Everything (Recommended)" "Choose specific components"
    
    if [ $? -eq 1 ]; then
        CURRENT_STEP="2/4"
        local components=$(multiselect_option "Select components:" \
            "Skills (16 knowledge modules)" \
            "Agents (10 specialists)" \
            "Workflows (5 guides)" \
            "Commands (8 actions)" \
            "System Prompt (orchestrator)")
        
        INSTALL_SKILLS=false
        INSTALL_AGENTS=false
        INSTALL_WORKFLOWS=false
        INSTALL_COMMANDS=false
        INSTALL_SYSTEM=false
        
        [[ "$components" == *"0"* ]] && INSTALL_SKILLS=true
        [[ "$components" == *"1"* ]] && INSTALL_AGENTS=true
        [[ "$components" == *"2"* ]] && INSTALL_WORKFLOWS=true
        [[ "$components" == *"3"* ]] && INSTALL_COMMANDS=true
        [[ "$components" == *"4"* ]] && INSTALL_SYSTEM=true
    fi
    
    # Step 3: Location
    CURRENT_STEP="3/4"
    select_option "Where to install?" "Current directory ($(pwd))" "Different location"
    
    if [ $? -eq 0 ]; then
        TARGET_DIR="$(pwd)"
    else
        CURRENT_STEP="3/4"
        TARGET_DIR=$(text_input "Enter project path:" "$(pwd)")
        [ ! -d "$TARGET_DIR" ] && mkdir -p "$TARGET_DIR"
    fi
    
    # Step 4: Existing config?
    local config_dir=$(get_config_dir)
    if [ -d "$TARGET_DIR/$config_dir" ]; then
        CURRENT_STEP="4/4"
        select_option "Found existing $config_dir. What to do?" "Add new files (keep customisations)" "Overwrite (fresh install)"
        [ $? -eq 0 ] && INSTALL_MODE="add" || INSTALL_MODE="overwrite"
    else
        INSTALL_MODE="new"
    fi
    
    # Confirmation
    clear_screen
    print_header
    
    echo -e "  ${WHITE}${BOLD}Ready to install${NC}\n"
    echo -e "  Platform:  ${CYAN}$PLATFORM${NC}"
    echo -e "  Location:  ${CYAN}$TARGET_DIR${NC}"
    echo -e "  Mode:      ${CYAN}$INSTALL_MODE${NC}\n"
    
    echo -e "  Components:"
    [ "$INSTALL_SKILLS" = true ] && echo "    ✓ Skills (16)"
    [ "$INSTALL_AGENTS" = true ] && echo "    ✓ Agents (10)"
    [ "$INSTALL_WORKFLOWS" = true ] && echo "    ✓ Workflows (5)"
    [ "$INSTALL_COMMANDS" = true ] && echo "    ✓ Commands (8)"
    [ "$INSTALL_SYSTEM" = true ] && [ "$PLATFORM" = "claude" ] && echo "    ✓ System Prompt"
    
    echo ""
    echo -ne "  ${WHITE}Install now?${NC} ${DIM}[Y/n]${NC} "
    read -r confirm
    
    [[ "$confirm" =~ ^[Nn]$ ]] && { print_info "Cancelled"; exit 0; }
    
    # Install
    echo -e "\n  ${WHITE}${BOLD}Installing...${NC}\n"
    
    [ "$INSTALL_MODE" = "overwrite" ] && { backup_existing; rm -rf "$TARGET_DIR/$config_dir"; }
    
    [ "$INSTALL_SYSTEM" = true ] && [ "$PLATFORM" = "claude" ] && { install_system; print_success "System prompt"; }
    [ "$INSTALL_SKILLS" = true ] && { install_skills; print_success "Skills (${#PKG_SKILLS[@]})"; }
    [ "$INSTALL_WORKFLOWS" = true ] && { install_workflows; print_success "Workflows (${#PKG_WORKFLOWS[@]})"; }
    [ "$INSTALL_AGENTS" = true ] && { install_agents; print_success "Agents (${#PKG_AGENTS[@]})"; }
    [ "$INSTALL_COMMANDS" = true ] && { install_commands; print_success "Commands (${#PKG_COMMANDS[@]})"; }
    
    # Done
    echo ""
    echo -e "  ${GREEN}${BOLD}════════════════════════════════════════════════════════════${NC}"
    echo -e "  ${GREEN}${BOLD}  Done!${NC}"
    echo -e "  ${GREEN}${BOLD}════════════════════════════════════════════════════════════${NC}"
    echo ""
    print_info "Installed to: $TARGET_DIR/$config_dir"
    echo ""
    
    echo -e "  ${CYAN}Next steps:${NC}"
    if [ "$PLATFORM" = "claude" ]; then
        echo "    1. Open Claude Code in your project"
        echo "    2. Run /crew create"
    else
        echo "    1. Open OpenCode in your project"
        echo "    2. Run /crew create"
    fi
    echo ""
}

main
