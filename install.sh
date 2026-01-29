#!/usr/bin/env bash
#############################################################################
# CrewAI Skills Installer for Claude Code and OpenCode
# Installs the complete CrewAI development toolkit
#
# Usage:
#   bash install.sh                           # Interactive mode
#   bash install.sh --platform claude
#   curl -fsSL URL/install.sh | bash -s --platform claude
#
# Compatible with:
#   macOS (bash 3.2+)
#   Linux (bash 3.2+)
#   Windows (Git Bash, WSL)
#############################################################################

set -e

# Detect platform
PLATFORM="$(uname -s)"
case "$PLATFORM" in
    Linux*)     PLATFORM="Linux";;
    Darwin*)    PLATFORM="macOS";;
    CYGWIN*|MINGW*|MSYS*) PLATFORM="Windows";;
    *)          PLATFORM="Unknown";;
esac

# Colors for output (disable on Windows if not supported)
if [ "$PLATFORM" = "Windows" ] && [ -z "$WT_SESSION" ] && [ -z "$ConEmuPID" ]; then
    RED=''
    GREEN=''
    YELLOW=''
    BLUE=''
    MAGENTA=''
    CYAN=''
    BOLD=''
    NC=''
else
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    BLUE='\033[0;34m'
    MAGENTA='\033[0;35m'
    CYAN='\033[0;36m'
    BOLD='\033[1m'
    NC='\033[0m' # No Color
fi

# Configuration
REPO_URL="https://raw.githubusercontent.com/victorgrein/cli-agents-config/main"
TEMP_DIR="/tmp/crewai-installer-$$"

# Default values
PLATFORM_TARGET=""
TARGET_DIR=""
DRY_RUN=false
NO_BACKUP=false
YES=false
UPDATE=false

# Cleanup temp directory on exit
trap 'rm -rf "$TEMP_DIR" 2>/dev/null || true' EXIT INT TERM

#############################################################################
# Package Contents (Single package with everything)
#############################################################################

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

#############################################################################
# Utility Functions
#############################################################################

print_header() {
    echo -e "${CYAN}${BOLD}"
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║                                                                ║"
    echo "║           CrewAI Skills Installer                              ║"
    echo "║                                                                ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_step() {
    echo -e "\n${MAGENTA}${BOLD}▶${NC} $1\n"
}

#############################################################################
# Platform & Path Handling
#############################################################################

check_bash_version() {
    local bash_version="${BASH_VERSION%%.*}"
    if [ "$bash_version" -lt 3 ]; then
        print_error "This script requires Bash 3.2 or higher"
        print_error "Current version: $BASH_VERSION"
        exit 1
    fi
}

check_dependencies() {
    print_step "Checking dependencies..."

    local missing_deps=()

    if ! command -v curl &> /dev/null; then
        missing_deps+=("curl")
    fi

    if [ ${#missing_deps[@]} -ne 0 ]; then
        print_error "Missing required dependencies: ${missing_deps[*]}"
        echo ""
        echo "Please install them:"
        case "$PLATFORM" in
            macOS)
                echo "  brew install ${missing_deps[*]}"
                ;;
            Linux)
                echo "  Ubuntu/Debian: sudo apt-get install ${missing_deps[*]}"
                echo "  Fedora/RHEL:   sudo dnf install ${missing_deps[*]}"
                echo "  Arch:          sudo pacman -S ${missing_deps[*]}"
                ;;
            Windows)
                echo "  Git Bash: Install via https://git-scm.com/"
                echo "  WSL:      sudo apt-get install ${missing_deps[*]}"
                ;;
        esac
        exit 1
    fi

    print_success "All dependencies found"
}

normalize_path() {
    local input_path="$1"
    local normalized_path
    
    if [ -z "$input_path" ]; then
        echo ""
        return 1
    fi

    if [[ $input_path == ~* ]]; then
        normalized_path="${HOME}${input_path:1}"
    else
        normalized_path="$input_path"
    fi

    normalized_path="${normalized_path//\\//}"
    normalized_path="${normalized_path%/}"

    if [[ ! "$normalized_path" = /* ]] && [[ ! "$normalized_path" =~ ^[A-Za-z]: ]]; then
        normalized_path="$(pwd)/${normalized_path}"
    fi

    echo "$normalized_path"
    return 0
}

get_config_dir() {
    local platform=$1
    if [ "$platform" = "claude" ]; then
        echo ".claude"
    else
        echo ".opencode"
    fi
}

#############################################################################
# File Operations
#############################################################################

download_file() {
    local url="$1"
    local dest="$2"
    local silent="${3:-false}"

    if [ "$DRY_RUN" = true ]; then
        return 0
    fi

    if [ "$silent" = true ]; then
        curl -fsSL "$url" -o "$dest" 2>/dev/null || return 1
    else
        curl -fsSL "$url" -o "$dest" || return 1
    fi

    return 0
}

ensure_dir() {
    local dir="$1"
    if [ "$DRY_RUN" = false ]; then
        mkdir -p "$dir"
    fi
}

backup_existing() {
    local target_dir="$1"
    local platform="$2"
    local config_dir=$(get_config_dir "$platform")
    local existing_dir="$target_dir/$config_dir"

    if [ ! -d "$existing_dir" ]; then
        return 0
    fi

    local timestamp=$(date +%Y%m%d_%H%M%S)
    local backup_dir="$target_dir/.crewai-skills-backup/$timestamp"

    print_info "Creating backup at $backup_dir"

    if [ "$DRY_RUN" = false ]; then
        ensure_dir "$(dirname "$backup_dir")"
        cp -r "$existing_dir" "$backup_dir/$(basename "$config_dir")"
    fi
}

#############################################################################
# Content Adaptation
#############################################################################

adapt_agent_for_claude() {
    local content="$1"
    
    echo "$content" | sed -e '
        # Extract YAML frontmatter and body
        1,/^---$/ {
            /^---$/d
            # Extract name for tools conversion
            /^name:/s/^name:\s*/\nNAME:/
            # Extract tools and convert to comma-separated
            /^tools:/{
                s/^tools:\s*/\nTOOLS:/
                N
                s/\n\s*/\n/
                s/\n\s*/\n/g
                s/^\s*-//g
                s/\n/,/g
                s/^TOOLS:.*$/TOOLS:&/
            }
            # Extract skills
            /^skills:/{
                s/^skills:\s*/\nSKILLS:/
                N
                s/\n\s*/\n/
                s/\n\s*/\n/g
                s/^\s*-//g
                s/\n/,/g
                s/^SKILLS:.*$/SKILLS:&/
            }
        }
        # Remove YAML frontmatter markers
        /^---$/d
    ' | sed -e 's/^NAME: /name: /' -e 's/^TOOLS:/tools:/' -e 's/^SKILLS:/skills:/'
}

adapt_agent_for_opencode() {
    local content="$1"
    
    # Extract name from content
    local name=$(echo "$content" | grep -E "^name:" | sed 's/^name:\s*//' | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) substr($i,2)}1' | tr -d ' ')
    
    echo "$content" | sed -e "
        1,/^---$/ {
            # Transform to OpenCode format
            /^name:/s/^name:/id:/
            /^name:/a\\
name: $name\\
category: subagents/crewai\\
type: subagent\\
version: 1.0.0\\
author: crewai-skills\\
mode: subagent\\
temperature: 1.0
        }
        # Add tools dict
        /^tools:/a\\
tools:\\n  read: true\\n  write: true\\n  edit: true\\n  grep: true\\n  glob: true\\n  bash: true\\n  task: false\\npermission:\\n  bash:\\n    '*'*': deny\\n    'ls *': allow\\n    'cat *': allow\\n    'grep *': allow\\n    pwd: allow
        # Remove YAML markers
        /^---$/d
    "
}

#############################################################################
# Installation Functions
#############################################################################

install_skills() {
    local platform="$1"
    local target_dir="$2"
    local config_dir=$(get_config_dir "$platform")
    local results=()
    
    local skills_dir="$target_dir/$config_dir/skills"
    
    for skill in "${PKG_SKILLS[@]}"; do
        local skill_path="templates/shared/skills/$skill"
        
        # Install SKILL.md and all subdirectories
        local source_url="$REPO_URL/$skill_path/SKILL.md"
        local dest_file="$skills_dir/$skill/SKILL.md"
        
        if download_file "$source_url" /tmp/skill_check 2>/dev/null; then
            ensure_dir "$(dirname "$dest_file")"
            
            if download_file "$source_url" "$dest_file"; then
                results+=("skills/$skill/SKILL.md: created")
            else
                print_warning "Failed to download: $skill"
            fi
            
            # Also download references directory if it exists
            local refs_source="$REPO_URL/$skill_path/references"
            if download_file "$refs_source" /tmp/refs_check 2>/dev/null; then
                local refs_dest="$skills_dir/$skill/references"
                ensure_dir "$refs_dest"
                
                # Try to download known reference files
                local ref_files=$(curl -fsSL "$refs_source/" 2>/dev/null | grep -oE 'href="[^"]*\.md"' | sed 's/href="//;s/"//' || true)
                for ref in $ref_files; do
                    download_file "$refs_source/$ref" "$refs_dest/$ref"
                done
            fi
        else
            print_warning "Skill not found: $skill"
        fi
    done
    
    echo "${results[@]}"
}

install_agents() {
    local platform="$1"
    local target_dir="$2"
    local results=()
    
    local agents_dir
    
    if [ "$platform" = "claude" ]; then
        agents_dir="$target_dir/.claude/agents"
    else
        agents_dir="$target_dir/.opencode/agent/subagents"
    fi
    
    for agent_path in "${PKG_AGENTS[@]}"; do
        local parts=(${agent_path//\// })
        local category="${parts[0]}"
        local agent_name="${parts[1]}"
        
        local source_url="$REPO_URL/templates/shared/agents/$category/$agent_name.md"
        local dest_file
        
        if [ "$platform" = "claude" ]; then
            dest_file="$agents_dir/$agent_name.md"
        else
            dest_file="$agents_dir/$category/$agent_name.md"
        fi
        
        if download_file "$source_url" /tmp/agent_check 2>/dev/null; then
            ensure_dir "$(dirname "$dest_file")"
            
            # Download and adapt content
            local temp_file="/tmp/agent_content_$$"
            if download_file "$source_url" "$temp_file"; then
                local content
                content=$(cat "$temp_file")
                
                # Adapt for platform
                if [ "$platform" = "claude" ]; then
                    content=$(adapt_agent_for_claude "$content")
                else
                    content=$(adapt_agent_for_opencode "$content")
                fi
                
                echo "$content" > "$dest_file"
                results+=("agents/$agent_path.md: created")
            fi
            rm -f "$temp_file"
        else
            print_warning "Agent not found: $agent_path"
        fi
    done
    
    echo "${results[@]}"
}

install_workflows() {
    local platform="$1"
    local target_dir="$2"
    local config_dir=$(get_config_dir "$platform")
    local results=()
    
    local skills_dir="$target_dir/$config_dir/skills"
    
    for workflow in "${PKG_WORKFLOWS[@]}"; do
        local workflow_path="templates/shared/workflows/$workflow"
        
        # Install as skill
        local source_url="$REPO_URL/$workflow_path/SKILL.md"
        local dest_file="$skills_dir/$workflow/SKILL.md"
        
        if download_file "$source_url" /tmp/workflow_check 2>/dev/null; then
            ensure_dir "$(dirname "$dest_file")"
            
            if download_file "$source_url" "$dest_file"; then
                results+=("workflows/$workflow/SKILL.md: created")
            fi
        else
            print_warning "Workflow not found: $workflow"
        fi
    done
    
    echo "${results[@]}"
}

install_commands() {
    local platform="$1"
    local target_dir="$2"
    local results=()
    
    local commands_dir
    
    if [ "$platform" = "claude" ]; then
        commands_dir="$target_dir/.claude/commands"
    else
        commands_dir="$target_dir/.opencode/command"
    fi
    
    for cmd_path in "${PKG_COMMANDS[@]}"; do
        local parts=(${cmd_path//\// })
        local cmd_name="${parts[1]}"
        
        local source_url="$REPO_URL/templates/shared/commands/$cmd_path.md"
        local dest_file="$commands_dir/$cmd_path.md"
        
        if download_file "$source_url" /tmp/command_check 2>/dev/null; then
            ensure_dir "$(dirname "$dest_file")"
            
            if download_file "$source_url" "$dest_file"; then
                results+=("commands/$cmd_path.md: created")
            fi
        else
            print_warning "Command not found: $cmd_path"
        fi
    done
    
    echo "${results[@]}"
}

install_system_prompt() {
    local platform="$1"
    local target_dir="$2"
    local results=()
    
    # Only for Claude Code
    if [ "$platform" != "claude" ]; then
        echo "${results[@]}"
        return
    fi
    
    local config_dir="$target_dir/.claude"
    
    # Install CLAUDE.md
    local claude_url="$REPO_URL/templates/claude/CLAUDE.md"
    local claude_dest="$config_dir/CLAUDE.md"
    
    if download_file "$claude_url" /tmp/claude_check 2>/dev/null; then
        ensure_dir "$config_dir"
        
        if download_file "$claude_url" "$claude_dest"; then
            results+=("CLAUDE.md: created")
        fi
    fi
    
    # Install settings.json
    local settings_url="$REPO_URL/templates/claude/settings.json"
    local settings_dest="$config_dir/settings.json"
    
    if download_file "$settings_url" /tmp/settings_check 2>/dev/null; then
        if download_file "$settings_url" "$settings_dest"; then
            results+=("settings.json: created")
        fi
    fi
    
    echo "${results[@]}"
}

#############################################################################
# Interactive Menus
#############################################################################

check_interactive_mode() {
    if [ ! -t 0 ]; then
        print_error "Interactive mode requires a terminal"
        echo ""
        echo "For non-interactive mode, use:"
        echo "  curl -fsSL $REPO_URL/install.sh | bash -s --platform claude"
        exit 1
    fi
}

prompt_platform() {
    check_interactive_mode
    
    echo -e "${BOLD}Select platform:${NC}"
    echo "  [1] Claude Code"
    echo "  [2] OpenCode"
    echo ""
    
    while true; do
        read -p "Enter choice (1 or 2): " choice
        case "$choice" in
            1) echo "claude"; return ;;
            2) echo "opencode"; return ;;
            *) print_error "Invalid choice. Please enter 1 or 2." ;;
        esac
    done
}

prompt_target_directory() {
    check_interactive_mode
    
    echo -e "\n${BOLD}Enter project folder:${NC}"
    echo -e "  ${CYAN}Where do you want to install CrewAI skills?${NC}"
    echo "  (Press Enter to use current directory: $(pwd))"
    echo ""
    
    while true; do
        read -p "Project folder path: " user_input
        
        if [ -z "$user_input" ]; then
            echo "$(pwd)"
            return
        fi
        
        local path=$(normalize_path "$user_input")
        
        if [ -d "$path" ]; then
            echo "$path"
            return
        else
            read -p "  Directory '$path' does not exist. Create it? [y/N]: " create
            if [[ "$create" =~ ^[Yy]$ ]]; then
                if mkdir -p "$path" 2>/dev/null; then
                    print_success "Created directory: $path"
                    echo "$path"
                    return
                else
                    print_error "Could not create directory"
                fi
            fi
        fi
    done
}

prompt_install_mode() {
    check_interactive_mode
    
    local platform="$1"
    local config_dir=$(get_config_dir "$platform")
    
    echo -e "\n${YELLOW}Existing installation detected ($config_dir)${NC}"
    echo -e "\n${BOLD}Choose action:${NC}"
    echo "  [1] ${GREEN}Add${NC} - Add new files, keep customized files"
    echo "  [2] ${CYAN}Update${NC} - Overwrite all files with latest versions"
    echo ""
    
    while true; do
        read -p "Enter choice (1 or 2): " choice
        case "$choice" in
            1) echo "add"; return ;;
            2) echo "update"; return ;;
            *) print_error "Invalid choice. Please enter 1 or 2." ;;
        esac
    done
}

#############################################################################
# Installation Execution
#############################################################################

perform_installation() {
    local platform="$1"
    local target_dir="$2"
    local force_update="$3"
    
    local config_dir=$(get_config_dir "$platform")
    local existing_dir="$target_dir/$config_dir"
    local has_existing=false
    
    if [ -d "$existing_dir" ]; then
        has_existing=true
        
        if [ "$force_update" = true ]; then
            print_info "Mode: Update (overwrite existing files)"
        else
            local install_mode=$(prompt_install_mode "$platform")
            if [ "$install_mode" = "update" ]; then
                force_update=true
            else
                print_info "Mode: Add (keep customized files)"
            fi
        fi
    fi
    
    # Summary
    echo -e "\n${BOLD}Installation Summary:${NC}"
    echo "  Platform:  $platform"
    echo "  Target:    $target_dir"
    echo "  Skills:    ${#PKG_SKILLS[@]}"
    echo "  Agents:    ${#PKG_AGENTS[@]}"
    echo "  Workflows: ${#PKG_WORKFLOWS[@]}"
    echo "  Commands:  ${#PKG_COMMANDS[@]}"
    
    if [ "$DRY_RUN" = true ]; then
        print_warning "\nDRY RUN - No changes will be made"
    fi
    
    # Confirm
    if [ "$YES" = false ] && [ "$DRY_RUN" = false ]; then
        echo ""
        read -p "Proceed with installation? [y/N]: " confirm
        if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
            print_info "Installation cancelled"
            exit 0
        fi
    fi
    
    # Backup if needed
    if [ "$has_existing" = true ] && [ "$force_update" = true ] && [ "$NO_BACKUP" = false ] && [ "$DRY_RUN" = false ]; then
        backup_existing "$target_dir" "$platform"
    fi
    
    # Create temp directory
    mkdir -p "$TEMP_DIR"
    
    # Install components
    print_step "Installing components..."
    
    local all_results=()
    
    # Install system prompt first
    if [ "$platform" = "claude" ]; then
        local results=($(install_system_prompt "$platform" "$target_dir"))
        all_results+=("${results[@]}")
    fi
    
    # Install skills
    local results=($(install_skills "$platform" "$target_dir"))
    all_results+=("${results[@]}")
    
    # Install workflows
    local results=($(install_workflows "$platform" "$target_dir"))
    all_results+=("${results[@]}")
    
    # Install agents
    local results=($(install_agents "$platform" "$target_dir"))
    all_results+=("${results[@]}")
    
    # Install commands
    local results=($(install_commands "$platform" "$target_dir"))
    all_results+=("${results[@]}")
    
    # Print results
    echo ""
    print_step "Results"
    
    local created=0
    local skipped=0
    
    for result in "${all_results[@]}"; do
        if [[ "$result" == *"created"* ]]; then
            ((created++))
        fi
        if [[ "$result" == *"skipped"* ]]; then
            ((skipped++))
        fi
    done
    
    print_success "Installed: $created files"
    if [ $skipped -gt 0 ]; then
        print_info "Skipped: $skipped files"
    fi
    
    # Final message
    echo ""
    print_success "Installation complete!"
    echo ""
    print_info "Files installed to: $target_dir/$config_dir"
    echo ""
    
    if [ "$platform" = "claude" ]; then
        echo -e "${CYAN}Next steps:${NC}"
        echo "  1. Start Claude Code in your project"
        echo "  2. Use /crew create to create your first crew"
        echo "  3. Or ask Claude to help with CrewAI development"
    else
        echo -e "${CYAN}Next steps:${NC}"
        echo "  1. Start OpenCode in your project"
        echo "  2. Use /crew create to create your first crew"
        echo "  3. The orchestrator will guide you through the process"
    fi
    
    echo ""
}

#############################################################################
# Argument Parsing
#############################################################################

usage() {
    cat << EOF
Usage: $0 [OPTIONS]

CrewAI Skills Installer for Claude Code and OpenCode
Installs the complete CrewAI development toolkit.

Options:
  -p, --platform PLATFORM   Target platform (claude or opencode)
  -t, --target PATH         Target directory (default: current directory)
  -n, --dry-run             Show what would be installed without making changes
  --no-backup               Skip backup of existing installation
  -y, --yes                 Skip confirmation prompt
  -u, --update              Update mode: overwrite all existing files
  -h, --help                Show this help message

Examples:
  # Interactive mode
  $0

  # Non-interactive mode
  $0 --platform claude

  # Install to specific directory
  $0 --platform opencode --target /path/to/project

  # Dry run to see what would be installed
  $0 --platform claude --dry-run

  # Install via curl
  curl -fsSL $REPO_URL/install.sh | bash -s --platform claude

Package Contents:
  Skills (16):    crewai-agents, crewai-tasks, crewai-crews, crewai-flows,
                  crewai-tools, crewai-llms, crewai-memory, crewai-processes,
                  crewai-cli, crewai-debugging, crewai-optimization,
                  crewai-migration, crewai-crew-creation, crewai-code-quality,
                  crewai-project-structure, task-management

  Agents (10):    crew-architect, agent-designer, task-designer, flow-engineer,
                  tool-specialist, debugger, llm-optimizer, migration-specialist,
                  performance-analyst, crewai-documenter

  Workflows (5):  create-crew, debug-crew, optimize-crew, migrate-project,
                  create-flow

  Commands (8):   /crew create, /crew analyze, /crew debug, /crew diagram,
                  /crew docs, /crew migrate, /crew optimize, /crew review
EOF
}

parse_args() {
    while [ $# -gt 0 ]; do
        case "$1" in
            -p|--platform)
                PLATFORM_TARGET="$2"
                shift 2
                ;;
            -t|--target)
                TARGET_DIR="$2"
                shift 2
                ;;
            -n|--dry-run)
                DRY_RUN=true
                shift
                ;;
            --no-backup)
                NO_BACKUP=true
                shift
                ;;
            -y|--yes)
                YES=true
                shift
                ;;
            -u|--update)
                UPDATE=true
                shift
                ;;
            -h|--help)
                usage
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                usage
                exit 1
                ;;
        esac
    done
}

#############################################################################
# Main
#############################################################################

main() {
    parse_args "$@"
    
    print_header
    
    # Check dependencies
    check_bash_version
    check_dependencies
    
    # Get platform
    if [ -z "$PLATFORM_TARGET" ]; then
        PLATFORM_TARGET=$(prompt_platform)
    fi
    
    print_success "Platform: $PLATFORM_TARGET"
    
    # Get target directory
    if [ -z "$TARGET_DIR" ]; then
        # If not interactive (piped), use current directory
        if [ ! -t 0 ]; then
            TARGET_DIR="$(pwd)"
        else
            TARGET_DIR=$(prompt_target_directory)
        fi
    else
        TARGET_DIR=$(normalize_path "$TARGET_DIR")
    fi
    
    print_success "Target: $TARGET_DIR"
    
    # Perform installation
    perform_installation "$PLATFORM_TARGET" "$TARGET_DIR" "$UPDATE"
}

main "$@"
