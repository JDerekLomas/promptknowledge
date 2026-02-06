# Getting Started with Claude Code (Beyond Installation)

You installed Claude Code. Now what?

This guide covers the setup that makes Claude Code actually powerful: the tools, the workflow patterns, and the configuration that turns "AI assistant" into "AI collaborator."

## The Basics You Need

### 1. Essential CLIs

Claude Code works best when it can use real tools. Install these:

```bash
# On macOS with Homebrew
brew install gh jq node

# Then authenticate GitHub
gh auth login
```

**Why these matter:**
- `gh` - Claude can create repos, PRs, issues directly
- `jq` - Parse JSON (API responses, config files)
- `node` - Run JavaScript, use npm packages

### 2. A Deployment Target

Claude Code shines when it can deploy what it builds. Pick one:

```bash
# Vercel (recommended for beginners)
npm install -g vercel
vercel login

# Or Netlify
npm install -g netlify-cli
netlify login
```

Now you can say "deploy this" and watch it happen.

### 3. Your First CLAUDE.md

Create a `CLAUDE.md` file in your home directory or project root. This is Claude's instruction manual for working with you.

```bash
# Global preferences (applies everywhere)
mkdir -p ~/.claude
touch ~/.claude/CLAUDE.md
```

Start simple:

```markdown
# My Preferences

## Style
- Be concise
- No emojis unless I ask
- Explain what you're doing before doing it

## Project Defaults
- Deploy to Vercel with `vercel --prod`
- Use TypeScript when possible

## Things to Remember
- My GitHub username is: YOUR_USERNAME
- Preferred test command: `npm test`
```

Claude reads this automatically and adapts.

---

## The Secret to Secrets

**Never put API keys in .env files when using AI tools.**

Claude Code can read your files. Your API keys end up in conversation history. Instead:

### Option 1: Environment Variables (Quick)
```bash
# Add to ~/.zshrc or ~/.bashrc
export OPENAI_API_KEY="sk-..."
```

Then restart your terminal. Claude can use `$OPENAI_API_KEY` without seeing the value.

### Option 2: secret-lover (Recommended)

A tool that stores secrets in macOS Keychain with Touch ID protection:

```bash
# Install
curl -sL https://secret-lover.dev/install.sh | bash

# Add a secret
secret-lover add OPENAI_API_KEY

# Run commands with secrets injected
secret-lover run -- npm run dev
```

Create a `.secrets.json` in your project to tell Claude what secrets exist (without exposing values):

```json
{
  "project": "my-app",
  "secrets": {
    "OPENAI_API_KEY": "OpenAI API key for completions",
    "DATABASE_URL": "PostgreSQL connection string"
  }
}
```

Claude sees what you need, suggests the right commands, but never sees the actual keys.

---

## Folder Structure That Works

Claude Code creates a `.claude/` folder in your home directory:

```
~/.claude/
├── CLAUDE.md          # Your global preferences
├── settings.json      # Permissions, hooks, plugins
├── projects/          # Conversation history (your prompt archaeology!)
├── skills/            # Custom skills (reusable prompts)
└── handoffs/          # Session summaries for continuity
```

### Skills: Reusable Prompt Patterns

Create skills for things you do repeatedly:

```bash
mkdir -p ~/.claude/skills/my-skill
```

Create `~/.claude/skills/my-skill/skill.md`:

```markdown
---
name: my-skill
description: Describe when to use this skill
---

# My Skill

Instructions for Claude when this skill is invoked...
```

Invoke with `/my-skill` in conversation.

### Handoffs: Don't Lose Context

Before ending a complex session:

```
Save a handoff summary to .claude/handoffs/
```

Resume later:

```
Continue from @.claude/handoffs/2024-01-15-project-name.md
```

---

## Workflow Patterns

### The Vibe Coding Flow

1. **Start loose**: "I want to build X"
2. **Iterate fast**: "try again", "no, more like Y", "yes, that direction"
3. **Deploy early**: "push to vercel" (even if incomplete)
4. **Refine live**: "the button doesn't work on mobile"

### Context Management

Claude Code has limited context. Manage it:

- `/compact` - Summarize and compress at ~75% context
- `/clear` - Fresh start when switching projects
- Be specific: "look at src/components/Header.tsx" not "look at the header"

### The Terse Prompt Style

Once Claude understands your project, you can be brief:

```
# These all work:
"vercel"           → deploys to Vercel
"push it"          → git push
"try again"        → retry the last failed thing
"mobile"           → fix mobile responsiveness
"darker"           → adjust colors
```

---

## Your First Real Project

Try this sequence:

```
1. "create a simple landing page for [your idea]"
2. "deploy it to vercel"
3. "add a contact form"
4. "make it look more professional"
5. "add dark mode"
```

You'll have a deployed website in minutes.

---

## Common Gotchas

### "Permission denied" errors
Claude runs in a sandbox. Some operations need approval:
- Say "yes" or approve in the UI
- Or add to allowed commands in settings

### "I don't have access to X"
- Make sure you're in the right directory
- Check if the file/folder exists: "ls the current directory"

### Context window full
- Use `/compact` to summarize
- Or `/clear` and start fresh with key context

### Claude keeps making the same mistake
- Be more specific about what's wrong
- Show the error message
- Say "stop and think about this differently"

---

## Level Up: Power User Setup

Once comfortable, add:

### MCP Servers
Connect Claude to external tools:
```json
// ~/.claude/mcp_servers.json
{
  "chrome-devtools": { ... },
  "your-database": { ... }
}
```

### Custom Hooks
Auto-run commands on certain events:
```json
// in settings.json
"hooks": {
  "PreCommit": ["npm test"],
  "PostDeploy": ["notify-slack"]
}
```

### Multiple AI Services
```bash
secret-lover add ANTHROPIC_API_KEY "..."
secret-lover add GEMINI_API_KEY "..."
secret-lover add MULEROUTER_API_KEY "..."  # For image generation
```

---

## Resources

- [Claude Code Documentation](https://docs.anthropic.com/claude-code)
- [secret-lover](https://github.com/dereklomas/secret-lover) - Secure secrets management
- [Prompt Archaeology](https://dereklomas.me/projects/promptarchaeology/) - See real Claude Code usage patterns
- [CodeVibing](https://codevibing.com) - Community of Claude Code users

---

## The Most Important Thing

Claude Code isn't about typing less. It's about **thinking at a higher level**.

Instead of:
- "Write a function that validates email addresses"

Try:
- "I need user signup - handle validation, error states, and success feedback"

Let Claude figure out the implementation. You focus on what you're building.

Welcome to vibe coding.
