---
name: dialogue-archiver
description: "Archive full dialogue and all generated or modified files into a dedicated self-contained directory containing word-for-word markdown transcripts and copied assets. Make sure to use this skill whenever the user mentions archiving a chat, saving the dialogue, exporting the conversation, 'заархівуй діалог', 'архівуй розмову', 'збережи цей діалог', 'збережи розмову з файлами', 'full dialogue archive', 'export chat to md', or preserving session artifacts in a separate folder."
risk: low
source: custom
date_added: "2026-07-27"
---

# Dialogue Archiver Skill

## Overview

The **dialogue-archiver** skill creates a clean, human-readable archive of the current (or specified) conversation session. It extracts strictly the user requests and assistant responses (filtering out all technical noise, tool call JSONs, system XML tags, and internal logs), saves them as a clean Markdown document (`dialogue.md`), copies all created files and artifacts into a dedicated `files/` folder, and generates a clean `README.md` index.

---

## Key Features

1. **Clean Human-Readable Format**: Preserves only the user's explicit text and the assistant's natural language responses. Excludes technical noise, tool call dumps, system XML tags, and raw logs.
2. **Asset Preservation**: Copies all user-facing files (markdown, scripts, diagrams, documents, images) created during the session into the archive directory.
3. **Structured & Readable**: Generates `dialogue.md` (clean transcript with clickable file links) and `README.md` (overview and index of files).

---

## Workflow Steps

When the user asks to archive the dialogue or run this skill, perform the following steps:

### 1️⃣ Run the Automated Archiver Script

Run the bundled Python script `scripts/archive_dialogue.py` using `run_command`:

```bash
python c:/Users/taxco/Dev/Tomos/.agents/skills/dialogue-archiver/scripts/archive_dialogue.py
```

*Optional Arguments:*
- `--conv-id <ID>`: Specify a specific conversation ID if not archiving the current session.
- `--output-dir <PATH>`: Specify a custom archive directory location.
- `--title "<TITLE>"`: Custom title for the archived session.

### 2️⃣ Verify Archive Output

Verify that the output directory contains:
- `dialogue.md`: Clean transcript (Request — Response) in Markdown.
- `README.md`: Overview and index of created files.
- `metadata.json`: Machine-readable metadata.
- `files/`: Subfolder containing copies of all session files.

### 3️⃣ Present to User

Provide a summary to the user with clickable links (`file://...`) to:
- The archive folder path
- `dialogue.md`
- `README.md`
- List of archived files

---

## Archive Directory Structure

```
archives/archive_YYYY-MM-DD_HH-MM-SS_<conv_id>/
├── README.md           # Session overview and file directory
├── dialogue.md         # Clean Markdown transcript (User Request -> Assistant Response)
├── metadata.json       # Session metadata
└── files/              # Copies of all files created/modified during the session
    ├── artifact_1.md
    └── script.py
```
