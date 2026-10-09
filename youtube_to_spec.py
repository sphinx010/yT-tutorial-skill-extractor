#!/usr/bin/env python3
"""
youtube_to_spec.py
Streamlined YouTube tutorial extractor powered by Gemini native multimodal video understanding.
"""

import os
import sys
import argparse

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from google import genai
from google.genai import types

EXTRACTION_PROMPT = """
You are an expert systems engineer and technical curriculum compiler. 
Analyze this video tutorial thoroughly and output a production-grade Implementation Spec for an AI Coding Agent.

Format your output strictly with these sections:

# 1. TOOL / CAPABILITY OVERVIEW
- Name of the capability / workflow taught in the video.
- Exact stack, libraries, CLI tools, and runtime versions required.

# 2. PREREQUISITES & ENVIRONMENT SETUP
- System prerequisites (OS packages, global CLIs, Docker, API keys).
- Installation commands verbatim as executed on screen.

# 3. CORE WORKFLOW & EXECUTION STEPS
- Step-by-step procedure in chronological order.
- Exact commands typed in the terminal (with all flags and parameters).
- Exact file paths created or edited, accompanied by the complete code snippets shown on screen.
- Exact expected stdout / output indicators of success.

# 4. GOTCHAS, UNSTATED ASSUMPTIONS & TRAPS
- Any silent prerequisites the presenter assumed you had installed.
- Subtle bugs, breaking changes, or workarounds mentioned verbally.
- Platform-specific caveats (Windows vs Linux/macOS).

# 5. AGENT SKILL DESIGN (PROMPT & TOOL DEFINITION)
- When should a coding agent trigger this skill? (Exact trigger phrases & scenarios).
- What parameters does the agent need to ask the user for, or derive automatically?
- What helper script(s) should be scaffolded inside the skill's `scripts/` directory?
"""

def extract_spec(video_source: str, focus: str = "", output_file: str = "SPEC.md"):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY is not set in your environment.", file=sys.stderr)
        print("Tip: Get a free key at https://aistudio.google.com/apikey and run:", file=sys.stderr)
        print("  export GEMINI_API_KEY='your-key' (or set it in your environment variables)", file=sys.stderr)
        sys.exit(1)

    client = genai.Client(api_key=api_key)
    
    prompt = EXTRACTION_PROMPT
    if focus:
        prompt += f"\n\nSPECIAL INSTRUCTION: Focus specifically on this aspect or timestamp range: {focus}"

    # Determine whether it's a URL or local file
    is_url = video_source.startswith("http://") or video_source.startswith("https://")
    
    if is_url:
        print(f"[*] Ingesting video via Gemini Cloud Bridge: {video_source}...")
        video_part = types.Part.from_uri(file_uri=video_source, mime_type="video/mp4")
    else:
        if not os.path.exists(video_source):
            print(f"Error: Local file not found: {video_source}", file=sys.stderr)
            sys.exit(1)
        print(f"[*] Uploading local video file to Gemini Files API: {video_source}...")
        uploaded_file = client.files.upload(file=video_source)
        video_part = uploaded_file

    # Fast models fall forward automatically
    models = ["gemini-2.5-flash", "gemini-3.8-flash", "gemini-flash-latest"]
    
    response = None
    for model_name in models:
        try:
            print(f"[*] Requesting extraction using {model_name}...")
            response = client.models.generate_content(
                model=model_name,
                contents=[
                    video_part,
                    prompt,
                ],
            )
            if response and response.text:
                print(f"[OK] Extraction succeeded with {model_name}.")
                break
        except Exception as e:
            print(f"[-] {model_name} failed: {e}. Trying fallback...")

    if not response or not response.text:
        print("[-] Extraction failed across all models.", file=sys.stderr)
        sys.exit(1)

    output_dir = os.path.dirname(output_file)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(response.text)

    print(f"[OK] Spec generated successfully and written to: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract an agent build spec from a YouTube URL or video file.")
    parser.add_argument("url", help="YouTube video URL or local video path")
    parser.add_argument("--focus", default="", help="Specific topic or timestamp range to focus on")
    parser.add_argument("--output", default="SPEC.md", help="Output file path (default: SPEC.md)")
    args = parser.parse_args()

    extract_spec(args.url, args.focus, args.output)
