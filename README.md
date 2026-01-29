# CrewAI Development Toolkit

### Build AI crews that actually work. Pre-built skills, agents, and workflows for Claude Code & OpenCode.

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

A toolkit that gives your AI assistant real knowledge about CrewAI. The skills. The workflows. The proper way to build things.

So when you ask for help, you finally get answers that work.

---

## What's Inside

Everything you need to build crews properly:

- **16 Skills** that teach your AI how CrewAI actually works
- **10 Specialist Agents** ready to help with specific tasks
- **8 Commands** for quick actions when you need them
- **5 Workflows** that guide you step by step

One install. Your AI becomes a CrewAI expert.

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

The interactive installer will ask you:
1. **Platform** - Claude Code or OpenCode?
2. **Location** - Current folder or custom path?
3. **Confirm** - Review before installing

Then it downloads and installs:
- 16 Skills
- 10 Agents  
- 5 Workflows
- 8 Commands
- System prompt (Claude Code only)

---

## Commands

Quick actions when you need them:

| Command | What it does |
|---------|--------------|
| `/crew create` | Start a new crew from scratch |
| `/crew analyze` | Understand your crew's architecture |
| `/crew debug` | Find and fix issues |
| `/crew diagram` | Generate visual diagrams |
| `/crew docs` | Create documentation |
| `/crew migrate` | Move to a better structure |
| `/crew optimise` | Make it faster and cheaper |
| `/crew review` | Get feedback on your code |

Just type the command. The AI handles the rest.

---

## Agents

Your specialist team. Each one knows their craft:

| Agent | What they do |
|-------|--------------|
| **crew-architect** | Designs how your crew fits together |
| **agent-designer** | Creates agents with proper roles and goals |
| **task-designer** | Builds tasks that get results |
| **flow-engineer** | Handles flows and state management |
| **tool-specialist** | Creates custom tools that work |
| **debugger** | Finds problems and fixes them |
| **llm-optimizer** | Picks the right model, saves you money |
| **migration-specialist** | Moves projects to better patterns |
| **performance-analyst** | Makes everything run faster |
| **crewai-documenter** | Writes docs that make sense |

You don't call them directly. The orchestrator brings in whoever you need.

---

## Skills

Knowledge the AI loads when it needs it:

**Core Concepts**
- `crewai-agents` - How to build agents properly
- `crewai-tasks` - Task configuration that works
- `crewai-crews` - Putting it all together
- `crewai-flows` - State management and routing
- `crewai-tools` - Custom and built-in tools
- `crewai-llms` - Model selection and setup
- `crewai-memory` - Memory systems
- `crewai-processes` - Sequential vs hierarchical
- `crewai-cli` - Command line reference

**Process Skills**
- `crewai-debugging` - Troubleshooting crews
- `crewai-optimisation` - Cost and speed improvements
- `crewai-migration` - Moving to better patterns
- `crewai-crew-creation` - Step by step guidance

**Standards**
- `crewai-code-quality` - Writing clean code
- `crewai-project-structure` - Organising your project

---

## Recommended Workflow

Here's how I use it:

**1. Start with create**
```
/crew create
```
The AI walks you through everything. Agent roles. Task structure. The lot.

**2. Build iteratively**  
Don't try to do everything at once. Start simple. Add complexity as you need it.

**3. Debug when stuck**
```
/crew debug
```
Something not working? The debugger agent finds the issue.

**4. Optimise when ready**
```
/crew optimise
```
Once it works, make it efficient. Better models. Faster execution. Lower costs.

**5. Document before you forget**
```
/crew docs
```
Future you will thank present you.

---

## Questions?

Connect with me on [LinkedIn](https://www.linkedin.com/in/victorgrein/). Always happy to chat about CrewAI.

---

MIT Licence
