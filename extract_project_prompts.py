#!/usr/bin/env python3
"""Extract all user prompts from a Claude project folder."""

import json
import os
from pathlib import Path
from datetime import datetime

def extract_prompts(project_path: Path) -> list[dict]:
    """Extract all user prompts from JSONL files in a project folder."""
    prompts = []

    for jsonl_file in project_path.glob("*.jsonl"):
        with open(jsonl_file, 'r') as f:
            for line in f:
                try:
                    data = json.loads(line)
                    if data.get("type") == "user":
                        content = data.get("message", {}).get("content", "")
                        timestamp = data.get("timestamp", "")
                        # Filter out noise
                        if content and isinstance(content, str):
                            # Skip task notifications, command messages, etc.
                            if any(skip in content for skip in [
                                "<task-notification>",
                                "<command-name>",
                                "<local-command-",
                                "<bash-notification>",
                                "Caveat: The messages below",
                                "This session is being continued from a previous"
                            ]):
                                continue
                            # Redact potential API keys/tokens
                            import re
                            content = re.sub(r'sk-ant-[a-zA-Z0-9_-]+', '[REDACTED_API_KEY]', content)
                            content = re.sub(r're_[a-zA-Z0-9_]+', '[REDACTED_TOKEN]', content)
                            content = re.sub(r'[a-f0-9]{32,}', '[REDACTED_KEY]', content)

                            prompts.append({
                                "content": content,
                                "timestamp": timestamp,
                                "session": jsonl_file.stem
                            })
                except json.JSONDecodeError:
                    continue

    # Sort by timestamp
    prompts.sort(key=lambda x: x.get("timestamp", ""))
    return prompts

def format_for_html(prompts: list[dict], project_name: str) -> str:
    """Format prompts as HTML for display."""
    html_parts = [f'<div class="prompt-log" data-project="{project_name}">']
    html_parts.append(f'<h3>{project_name}</h3>')
    html_parts.append(f'<p class="prompt-count">{len(prompts)} prompts</p>')
    html_parts.append('<div class="prompts">')

    for p in prompts:
        ts = p.get("timestamp", "")
        if ts:
            try:
                dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                time_str = dt.strftime("%b %d, %H:%M")
            except:
                time_str = ""
        else:
            time_str = ""

        content = p["content"].replace("<", "&lt;").replace(">", "&gt;")
        # Truncate very long prompts for display
        display = content[:500] + "..." if len(content) > 500 else content

        html_parts.append(f'''<div class="prompt">
    <span class="time">{time_str}</span>
    <span class="text">{display}</span>
</div>''')

    html_parts.append('</div></div>')
    return '\n'.join(html_parts)

def format_as_json(prompts: list[dict], project_name: str) -> dict:
    """Format prompts as JSON for JavaScript consumption."""
    return {
        "project": project_name,
        "count": len(prompts),
        "prompts": [
            {
                "content": p["content"],
                "timestamp": p.get("timestamp", ""),
            }
            for p in prompts
        ]
    }

if __name__ == "__main__":
    import sys

    claude_projects = Path.home() / ".claude" / "projects"

    # Projects to extract
    projects = {
        "xwhysi": "-Users-dereklomas-xwhysi",
        "milo": "-Users-dereklomas-milo",
        "seliger": "-Users-dereklomas-Seliger",
        "designtherapy": "-Users-dereklomas-julika-designtherapy",
        "fractalviewer": "-Users-dereklomas-fractalviewer",
        "morniplus": "-Users-dereklomas-oura",
        "solidsleep": "-Users-dereklomas-sleep",
    }

    all_data = {}

    for name, folder in projects.items():
        project_path = claude_projects / folder
        if project_path.exists():
            prompts = extract_prompts(project_path)
            all_data[name] = format_as_json(prompts, name)
            print(f"{name}: {len(prompts)} prompts")
        else:
            print(f"{name}: folder not found at {project_path}")

    # Output as JavaScript data file
    output_path = Path("/tmp/claude/project-prompts.js")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        f.write("// Auto-generated prompt data for specific projects\n")
        f.write(f"const PROJECT_PROMPTS = {json.dumps(all_data, indent=2)};\n")

    print(f"\nWritten to {output_path}")
