# Prompt Archaeology

Extract and visualize your Claude Code conversation history.

**New to Claude Code?** Start with [GETTING-STARTED.md](./GETTING-STARTED.md) - a guide to setting up Claude Code properly (beyond just installation).

## What is this?

When you use [Claude Code](https://claude.com/claude-code), your conversations are saved in `~/.claude/projects/` as JSONL files. This tool extracts the prompts you've written—the raw material of building with AI.

## Quick Start

```bash
# Clone this repo
git clone https://github.com/dereklomas/promptknowledge.git
cd promptknowledge

# Edit the script to add your project folders
# Projects are stored in ~/.claude/projects/-Users-YOUR_USERNAME-PROJECT_NAME

# Run extraction
python3 extract_project_prompts.py
```

## What it does

1. Reads all JSONL files from your Claude Code project folders
2. Extracts user messages (your prompts)
3. Filters out noise (task notifications, system commands)
4. Redacts API keys and tokens
5. Outputs a JavaScript file for visualization

## Configuration

Edit `extract_project_prompts.py` to add your projects:

```python
projects = {
    "my-project": "-Users-yourusername-my-project",
    "another-project": "-Users-yourusername-another-project",
}
```

## Output

The script generates `/tmp/claude/project-prompts.js` with:
- Project name
- Prompt count
- Array of prompts with content and timestamp

## Live Demo

See [Prompt Archaeology](https://dereklomas.me/projects/promptarchaeology/) for a visualization of 10,497 prompts across 68 days.

## Privacy Notes

- Only extracts your own local conversation history
- Automatically redacts patterns matching API keys
- No data is sent anywhere—everything runs locally

## The Stack Behind This

This project emerged from 68 days of building with Claude Code. Here's what that stack looks like:

**Deployment**: Vercel, GitHub, Hetzner VPS
**AI Services**: Anthropic, Google Gemini, MuleRouter, ElevenLabs
**Frontend**: Next.js, D3.js, React Three Fiber
**Secrets**: [secret-lover](https://github.com/dereklomas/secret-lover) (macOS Keychain + Touch ID)
**Workflow**: Terse prompts, rapid iteration, 36-second avg project switching

See [GETTING-STARTED.md](./GETTING-STARTED.md) for how to replicate this setup.

## License

MIT
