#!/usr/bin/env python3
"""
compile_skill.py
Compiles an extracted SPEC.md into a production-grade Agent Skill (.agents/skills/<skill-name>/SKILL.md).
"""

import os
import sys
import re
import argparse

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

SKILL_TEMPLATE = """---
name: {skill_name}
description: {skill_description}
---

# {title}

{overview}

## Prerequisites & Environment Setup

{prerequisites}

## Core Workflow & Instructions

{workflow}

## Gotchas, Traps & Unstated Assumptions

{gotchas}

## Provenance
This skill was automatically compiled from an analyzed tutorial video via yT-tutorial-skill-extractor.
Reference spec is preserved at `SPEC.md`.
"""

def clean_text(text: str) -> str:
    return text.strip() if text else ""

def parse_spec(spec_content: str):
    sections = {
        "overview": "",
        "prerequisites": "",
        "workflow": "",
        "gotchas": "",
        "design": ""
    }
    
    parts = re.split(r'(?m)^#+\s+(?:\d+\.\s*)?', spec_content)
    
    for part in parts:
        lower_header = part[:60].lower()
        if "overview" in lower_header or "tool" in lower_header or "capability" in lower_header:
            sections["overview"] = part
        elif "prerequisite" in lower_header or "environment" in lower_header:
            sections["prerequisites"] = part
        elif "core workflow" in lower_header or "execution" in lower_header or "step" in lower_header:
            sections["workflow"] = part
        elif "gotcha" in lower_header or "assumption" in lower_header or "trap" in lower_header:
            sections["gotchas"] = part
        elif "agent skill" in lower_header or "design" in lower_header or "prompt" in lower_header:
            sections["design"] = part

    return sections

def compile_skill(spec_path: str, skill_name: str, target_dir: str = None):
    if not os.path.exists(spec_path):
        print(f"Error: Spec file not found at {spec_path}", file=sys.stderr)
        sys.exit(1)

    with open(spec_path, "r", encoding="utf-8") as f:
        spec_content = f.read()

    # Determine skill name if not provided
    if not skill_name:
        match = re.search(r'Name of the capability.*?:\s*(.+)', spec_content, re.IGNORECASE)
        if match:
            raw_name = match.group(1).strip()
            skill_name = re.sub(r'[^a-zA-Z0-9_-]', '-', raw_name).lower().strip('-')
        else:
            skill_name = "imported-video-skill"

    # Sanitize skill name
    skill_name = re.sub(r'[^a-zA-Z0-9_-]', '-', skill_name).lower().strip('-')

    # Resolve target directory
    if not target_dir:
        # Default to standard project .agents/skills/ in current working directory
        target_dir = os.path.join(os.getcwd(), ".agents", "skills", skill_name)

    os.makedirs(target_dir, exist_ok=True)
    os.makedirs(os.path.join(target_dir, "scripts"), exist_ok=True)

    sections = parse_spec(spec_content)

    desc_match = re.search(r'[-*]\s*Name[^\n]*\n[-*]\s*(.+)', sections.get("overview", ""))
    skill_desc = desc_match.group(1).strip() if desc_match else f"Automated workflow for {skill_name}."
    skill_desc = re.sub(r'[\r\n]+', ' ', skill_desc)[:160]

    title = skill_name.replace("-", " ").title()

    rendered_skill = SKILL_TEMPLATE.format(
        skill_name=skill_name,
        skill_description=skill_desc,
        title=title,
        overview=clean_text(sections.get("overview", "Workflow extracted from video.")),
        prerequisites=clean_text(sections.get("prerequisites", "None specified.")),
        workflow=clean_text(sections.get("workflow", "Follow standard execution.")),
        gotchas=clean_text(sections.get("gotchas", "None recorded.")),
    )

    skill_file = os.path.join(target_dir, "SKILL.md")
    with open(skill_file, "w", encoding="utf-8") as f:
        f.write(rendered_skill)

    # Save SPEC.md alongside SKILL.md for provenance
    provenance_file = os.path.join(target_dir, "SPEC.md")
    with open(provenance_file, "w", encoding="utf-8") as f:
        f.write(spec_content)

    print(f"[OK] Skill successfully compiled to: {skill_file}")
    print(f"[OK] Provenance spec saved to: {provenance_file}")
    print(f"[OK] Ready for live execution by Antigravity, Claude Code, Cursor, and Codex.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compile SPEC.md into an active Agent Skill.")
    parser.add_argument("--spec", default="SPEC.md", help="Path to input SPEC.md file")
    parser.add_argument("--name", default="", help="Name for the skill (e.g. docker-fastapi-deploy)")
    parser.add_argument("--target", default="", help="Target directory (defaults to .agents/skills/<name>)")
    args = parser.parse_args()

    compile_skill(args.spec, args.name, args.target)
