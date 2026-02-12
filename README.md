# Spec Crew

### Spec-driven CrewAI development toolkit for Claude Code & OpenCode.

[![Connect with me on LinkedIn](https://img.shields.io/badge/Let's_Connect-LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/victorgrein/)

---

## Why I Built This

CrewAI is still new. A framework that's growing fast and changing how we think about AI systems.

I discovered it over a year ago and something just clicked. I've always believed in vertical AI agents. Specialists. Focused. Built to do one thing exceptionally well. CrewAI made that vision real.

So I went deep. Really deep.

And then something interesting started happening. People began reaching out.

*"How do I build an agent that does X?"*  
*"Why isn't my flow working?"*  
*"Can you help me structure this crew?"*

Most of them had already asked an AI for help before coming to me. And the answers they got?

That's what AI gives you without proper skills and a professional workflow. Generic templates that miss the point. Overcomplicated solutions nobody asked for. Code that looks fine but falls apart the moment you run it.

The AI simply didn't understand CrewAI. Not the patterns. Not the pitfalls. Not the way things actually work in practice.

That's why I built this.

A toolkit that gives your AI assistant real knowledge about CrewAI. The skills. The proper way to build things.

So when you ask for help, you finally get answers that work.

---

## What's Inside

Everything you need to build crews properly:

<!-- BEGIN GENERATED: TOOLKIT_WHATS_INSIDE -->
- **4 Skill Packs**
- **4 Core Agents**
- **5 Canonical Commands**
<!-- END GENERATED: TOOLKIT_WHATS_INSIDE -->






One install. Your AI becomes a Spec Crew expert.

### Toolkit Index (Generated)

<!-- BEGIN GENERATED: TOOLKIT_INDEX -->
- **Canonical commands (5):** `/crew init`, `/crew inspect`, `/crew fix`, `/crew evolve`, `/crew docs`
- **Canonical agents (4):** `builder`, `auditor`, `flow`, `docs`
- **Canonical skill packs (4):** `core-build`, `flows`, `tools-expert`, `orchestration-governance`
<!-- END GENERATED: TOOLKIT_INDEX -->






Maintainer sync:

- Source manifest: `toolkit/manifest.json`
- Regenerate generated assets: `python3 scripts/sync_toolkit_manifest.py`
- Validate manifest + generated assets: `python3 scripts/validate_toolkit_manifest.py`


---

## Installation

### macOS

**Interactive installer:**
```bash
curl -fsSL https://raw.githubusercontent.com/victorgrein/cli-agents-config/main/install.sh -o /tmp/i.sh && bash /tmp/i.sh
```

**Quick install:**
```bash
# Claude Code
curl -fsSL https://raw.githubusercontent.com/victorgrein/cli-agents-config/main/install.sh | bash -s claude

# OpenCode
curl -fsSL https://raw.githubusercontent.com/victorgrein/cli-agents-config/main/install.sh | bash -s opencode
```

### Linux

**Interactive installer:**
```bash
curl -fsSL https://raw.githubusercontent.com/victorgrein/cli-agents-config/main/install.sh -o /tmp/i.sh && bash /tmp/i.sh
```

**Quick install:**
```bash
# Claude Code
curl -fsSL https://raw.githubusercontent.com/victorgrein/cli-agents-config/main/install.sh | bash -s claude

# OpenCode
curl -fsSL https://raw.githubusercontent.com/victorgrein/cli-agents-config/main/install.sh | bash -s opencode
```

> **Note:** If you don't have curl, install it first:
> - Ubuntu/Debian: `sudo apt install curl`
> - Fedora: `sudo dnf install curl`
> - Arch: `sudo pacman -S curl`

### Windows

**Option 1: Git Bash (recommended)**

Install [Git for Windows](https://git-scm.com/download/win), then open Git Bash and run:

```bash
curl -fsSL https://raw.githubusercontent.com/victorgrein/cli-agents-config/main/install.sh -o ~/i.sh && bash ~/i.sh
```

**Option 2: WSL (Windows Subsystem for Linux)**

Open your WSL terminal and run:

```bash
curl -fsSL https://raw.githubusercontent.com/victorgrein/cli-agents-config/main/install.sh -o /tmp/i.sh && bash /tmp/i.sh
```

**Option 3: PowerShell (quick install only)**

```powershell
# Claude Code
irm https://raw.githubusercontent.com/victorgrein/cli-agents-config/main/install.sh | bash -s claude
```

> **Note:** PowerShell requires Git Bash or WSL to be installed for bash commands.

### What the installer does

The interactive installer will ask for your **platform** (Claude Code or OpenCode), **installation location**, and confirmation before installing:

<!-- BEGIN GENERATED: TOOLKIT_INSTALLER_COUNTS -->
- 4 Skills
- 4 Agents
- 5 Commands
<!-- END GENERATED: TOOLKIT_INSTALLER_COUNTS -->





Also installs the system prompt for Claude Code.

---

## Commands

Quick actions when you need them:

| Command | What it does |
|---------|--------------|
| `/crew init` | Set up project context or create from natural language spec |
| `/crew inspect` | Inspect architecture and performance |
| `/crew fix` | Debug failures and optimize runtime behavior |
| `/crew evolve` | Migrate or refactor project structure |
| `/crew docs` | Create documentation |

Just type the command. The AI handles the rest.

---

## Agents

Canonical specialists:

| Agent | What they do |
|-------|--------------|
| **builder** | Builds crews, agents, tasks, and tools |
| **auditor** | Runs read-only investigations, audits, and validation |
| **flow** | Designs flows and handles migration/refactoring |
| **docs** | Produces docs, diagrams, and standards summaries |

You don't call them directly. The orchestrator brings in whoever you need.

---

## Skills

Knowledge the AI loads when it needs it:

**Canonical Skill Packs**
- `core-build` - Crews, agents, tasks, and process design
- `flows` - Flow orchestration, state, and routing
- `tools-expert` - Tool selection, custom tooling, and integration patterns
- `orchestration-governance` - Routing, delegation contracts, and validation policy

---

## Recommended Workflow

Here's how I use it:

**1. Start with init**
```
/crew init --spec="A research crew that analyses AI trends and writes reports"
```
The AI walks you through everything. Agent roles. Task structure. The lot.

**2. Build iteratively**  
Don't try to do everything at once. Start simple. Add complexity as you need it.

**3. Inspect before changing**
```
/crew inspect ./my_crew --focus="full"
```
Get architecture and runtime findings before making edits.

**4. Fix what matters most**
```
/crew fix ./my_crew --target="stability"
```
Resolve failures first, then target cost, latency, or quality.

**5. Evolve and document**
```
/crew evolve ./my_crew --to="flow"
/crew docs
```
Future you will thank present you.

---

## Project Structure

```
spec-crew/
├── README.md              # This documentation
├── install.sh             # Installation script
├── scripts/               # Toolkit validation & sync scripts
├── templates/             # Agent, skill, and workflow prompts
│   ├── shared/            # Core prompts (commands, agents, skills)
│   ├── claude/            # Claude Code-specific configuration
│   └── opencode/          # OpenCode-specific configuration
└── toolkit/               # Toolkit metadata & validation data
    ├── manifest.json      # Source of truth for all toolkit assets
    ├── registry.json      # Runtime registry (generated)
    └── cases/             # Validation test cases
        ├── agent-routing.json
        ├── command-smoke.json
        └── e2e-scenarios.json
```

---

## Questions?

Connect with me on [LinkedIn](https://www.linkedin.com/in/victorgrein/). Always happy to chat about CrewAI and Spec Crew.

---

MIT Licence
