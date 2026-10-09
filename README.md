# yT-tutorial-skill-extractor ⚡

> **Turn YouTube tutorials into executable AI coding agent skills in 30 seconds using Gemini native multimodal video understanding.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Gemini 2.0 Flash](https://img.shields.io/badge/Model-Gemini%20Flash-orange.svg)](https://aistudio.google.com/)
[![Disk Footprint](https://img.shields.io/badge/Disk%20Downloaded-0%20MB-green.svg)](#how-it-works)
[![Agent Compatibility](https://img.shields.io/badge/Agents-Antigravity%20%7C%20Claude%20%7C%20Cursor-purple.svg)](#universal-agent-compatibility)

Most people watch a build tutorial, take notes they never open again, then rebuild from memory three weeks later and get stuck on an unstated assumption.

**yT-tutorial-skill-extractor** ends that. It turns any technical YouTube tutorial or conference talk into an **executable skill (`SKILL.md`)** that lives inside your AI coding agents—ready to execute the workflow on demand, forever.

---

## 🚀 Why This Exists (And Why It’s 10x Faster)

Previous approaches downloaded gigabytes of video, sliced hundreds of image frames with `ffmpeg`, ran local Whisper transcribers, and required wrestling with heavy diff tools.

**This engine replaces all of that with Gemini's cloud-native multimodal bridge:**

```
[ YouTube Tutorial URL ]
           │
           ▼
[ Gemini 2.0 Flash Cloud Bridge ] ──► Ingests Video + Audio natively (0 MB disk, ~20s)
           │
           ▼
[ Structured Spec: SPEC.md ] ───────► Verbatim commands, code snippets, traps & unstated assumptions
           │
           ▼
[ compile_skill.py / Agent ] ───────► Compiles into .agents/skills/<skill-name>/
           │
           ▼
[ Universal SKILL.md + Scripts ] ───► Executable by Antigravity, Claude Code, Cursor, Codex
```

* **0 MB Downloaded to Disk:** Google ingests the public YouTube stream directly on their cloud.
* **Synchronized Vision & Audio:** Gemini simultaneously inspects the visual screen (terminal typing, IDE edits) and hears spoken explanations.
* **Unstated Assumptions Extracted:** The prompt explicitly forces Gemini to catch the unspoken prerequisites, flags, and silent gotchas that tutorials usually gloss over.
* **Universal Agent Skills Standard:** Compiles into the open `SKILL.md` format recognized by Antigravity, Claude Code, Cursor, and Codex.
* **100% Free:** Runs on the Google AI Studio free tier (no credit card required).

---

## 📦 Quickstart

### 1. Prerequisites & Setup

Clone the repo and install dependencies:

```bash
git clone https://github.com/sphinx010/yT-tutorial-skill-extractor.git
cd yT-tutorial-skill-extractor
pip install -r requirements.txt
```

Get a free Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey) and export it:

```bash
# Linux / macOS
export GEMINI_API_KEY="your-api-key-here"

# Windows (PowerShell)
$env:GEMINI_API_KEY="your-api-key-here"
```

---

### 2. Extract the Build Spec from YouTube

Run the extractor on any public YouTube tutorial:

```bash
python youtube_to_spec.py "https://www.youtube.com/watch?v=VIDEO_ID" --output SPEC.md
```

#### Optional: Focus on a specific section or timestamp window:
```bash
python youtube_to_spec.py "https://www.youtube.com/watch?v=VIDEO_ID" \
  --focus "hands-on coding and config from minute 12 to 18" \
  --output SPEC.md
```

This generates `SPEC.md` with:
1. Tool / Capability Overview
2. Prerequisites & Environment Setup
3. Verbatim Execution Steps & Code Blocks
4. Gotchas, Unstated Assumptions & Traps
5. Agent Skill Design Specifications

---

### 3. Compile to an Executable Agent Skill

Compile `SPEC.md` into your project's `.agents/skills/` directory:

```bash
python compile_skill.py --spec SPEC.md --name my-new-skill
```

This creates:
```
.agents/skills/my-new-skill/
├── SKILL.md         <-- Master executable agent skill definition
├── SPEC.md          <-- Full provenance and reference specification
└── scripts/         <-- Directory for any companion automation scripts
```

---

### 4. Tell Your Agent to Run the Dry Run

Ask your coding agent:
> *"Run the new `my-new-skill` skill once on a test case to verify that all commands and scripts execute cleanly."*

Once verified, the skill is **permanently available** to your entire agent workforce.

---

## 🤖 Universal Agent Compatibility

Because the output conforms to the open **Agent Skills Specification** (`SKILL.md` with YAML frontmatter):

| Agent | Skill Discovery Path | How It Uses It |
| :--- | :--- | :--- |
| **Antigravity (AGY)** | `.agents/skills/<skill-name>/` | Discovers natively; executes commands via shell tools. |
| **Claude Code** | `.claude/skills/<skill-name>/` or `.agents/skills/` | Scans YAML frontmatter; executes commands in terminal. |
| **Cursor / Copilot / Codex** | `.cursor/skills/` or `.agents/skills/` | Ingests instructions when related prompts or files are opened. |

---

## 💡 Expert Moves

### 1. Window Scoping (Save Time on Long Talks)
If a 45-minute video only has 6 minutes of actual hands-on build, don't make the model digest the preamble:
```bash
python youtube_to_spec.py "https://youtu.be/..." --focus "hands-on coding between 12:30 and 18:45"
```
Gemini uses its internal temporal grounding to jump straight to the relevant segment.

### 2. Private or Local Video Files
Public YouTube URLs are ingested directly without downloading. If you have a private or unlisted recording stored locally:
```bash
python youtube_to_spec.py "path/to/local_tutorial.mp4" --output SPEC.md
```
The script will automatically upload it to Google's Files API, process the frames remotely, and generate the spec.

---

## ⚙️ How Gemini Ingests Video Under the Hood

Gemini does **not** simply read a transcript. It processes video frames natively:
1. **Frame Sampling (1 FPS):** Google's backend samples the video at 1 frame per second.
2. **Visual Tokens:** Each sampled frame is passed into Gemini's vision transformer encoder (~258 tokens per frame).
3. **Synchronized Audio Tokens:** The audio stream is simultaneously tokenized (~32 tokens/sec) and temporally aligned with the frames.
4. **Context Retrieval:** Gemini correlates what is visible on screen (terminal commands, IDE lines) with spoken commentary simultaneously.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
