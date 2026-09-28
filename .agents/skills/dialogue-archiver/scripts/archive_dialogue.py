import os
import sys
import json
import shutil
import re
import argparse
from datetime import datetime

def sanitize_filename(name):
    return re.sub(r'[^\w\-. ]', '_', name)

def parse_transcript(transcript_path):
    steps = []
    if not os.path.exists(transcript_path):
        return steps
    
    with open(transcript_path, 'r', encoding='utf-8', errors='replace') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                steps.append(data)
            except Exception as e:
                continue
    return steps

def find_created_files(app_data_dir, conv_id, workspace_dir, steps):
    created_files = set()
    
    # 1. Check brain artifact directory for user artifacts/scratch files
    brain_dir = os.path.join(app_data_dir, "brain", conv_id)
    if os.path.exists(brain_dir):
        for root, dirs, files in os.walk(brain_dir):
            # Exclude internal system, git, and hidden directories
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            if ".system_generated" in root or ".git" in root or "\\git\\" in root or "/git/" in root:
                continue
            for file in files:
                if file.startswith("."):
                    continue
                full_path = os.path.join(root, file)
                created_files.add(full_path)
                
    # 2. Parse tool calls from transcript steps for written/modified files
    for step in steps:
        tool_calls = step.get("tool_calls", [])
        for tc in tool_calls:
            name = tc.get("name", "")
            args = tc.get("args", {})
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except:
                    args = {}
            
            target = None
            if name in ["write_to_file", "replace_file_content", "multi_replace_file_content"]:
                target = args.get("TargetFile") or args.get("target_file")
            elif name == "generate_image":
                img_name = args.get("ImageName") or args.get("image_name")
                if img_name:
                    pass
            
            if target and os.path.exists(target):
                abs_t = os.path.abspath(target)
                # Avoid archiving files inside archives directory
                if not abs_t.startswith(os.path.abspath(os.path.join(workspace_dir, "archives"))):
                    created_files.add(abs_t)
                
    return sorted(list(created_files))

def clean_user_prompt(content):
    if not content:
        return ""
    # Extract text inside <USER_REQUEST> if present
    match = re.search(r'<USER_REQUEST>\s*(.*?)\s*</USER_REQUEST>', content, re.DOTALL)
    if match:
        text = match.group(1).strip()
    else:
        # Strip system metadata blocks if tag missing
        text = re.sub(r'<ADDITIONAL_METADATA>.*?</ADDITIONAL_METADATA>', '', content, flags=re.DOTALL)
        text = re.sub(r'<USER_SETTINGS_CHANGE>.*?</USER_SETTINGS_CHANGE>', '', text, flags=re.DOTALL)
        text = text.strip()
    return text

def is_internal_tool_output(text):
    if not text:
        return True
    lines = text.strip().split("\n")
    first_line = lines[0].strip()
    
    # Common system/tool log outputs injected into content
    if first_line.startswith("Created At:") or first_line.startswith("Completed At:"):
        return True
    if first_line.startswith("Created file file://") or "with requested content." in first_line:
        return True
    if first_line.startswith("The following changes were made by") or first_line.startswith("[diff_block_start]"):
        return True
    if first_line.startswith("The command completed successfully") or first_line.startswith("Output:"):
        return True
    if first_line.startswith("File Path: `file://") or first_line.startswith("Total Lines:"):
        return True
    if first_line.startswith("{\"name\":") or first_line.startswith("Summary:"):
        return True
    if first_line.startswith("Archiving conversation ID") or first_line.startswith("Dialogue archived"):
        return True
    return False

def clean_assistant_response(content):
    if not content:
        return ""
    text = content.strip()
    if is_internal_tool_output(text):
        return ""
    return text

def generate_markdown(steps, conv_id, created_files_map, title):
    md = []
    md.append(f"# 📜 Архів Діалогу: {title}\n")
    md.append(f"- **ID Сесії**: `{conv_id}`")
    md.append(f"- **Дата архівування**: `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`\n")
    md.append("---\n")
    
    if created_files_map:
        md.append("## 📁 Файли, створені в процесі діалогу\n")
        for orig_path, rel_path in created_files_map.items():
            fname = os.path.basename(orig_path)
            md.append(f"- 📄 [{fname}]({rel_path})")
        md.append("\n---\n")

    md.append("## 💬 Історія Запитів та Відповідей\n")
    
    turns = []
    current_turn = None

    for step in steps:
        source = step.get("source", "")
        stype = step.get("type", "")
        content = step.get("content", "")

        # Skip system messages, checkpoints, and tool outputs
        if stype in ["CONVERSATION_HISTORY", "CHECKPOINT", "VIEW_FILE", "COMMAND_OUTPUT", "TOOL_RESPONSE"] or source == "SYSTEM":
            continue

        if stype in ["USER_INPUT", "USER_EXPLICIT"] or source in ["USER", "USER_EXPLICIT"]:
            clean_text = clean_user_prompt(content)
            if not clean_text:
                continue
            if current_turn:
                turns.append(current_turn)
            current_turn = {
                "user": clean_text,
                "assistant": []
            }
            
        elif (stype == "PLANNER_RESPONSE" or source == "MODEL") and current_turn is not None:
            clean_resp = clean_assistant_response(content)
            if clean_resp:
                current_turn["assistant"].append(clean_resp)

    if current_turn:
        turns.append(current_turn)

    for i, turn in enumerate(turns, 1):
        md.append(f"### 👤 Запит #{i}\n")
        md.append(turn["user"])
        md.append("\n")
        
        if turn["assistant"]:
            md.append(f"### 🤖 Відповідь #{i}\n")
            assistant_full = "\n\n".join(turn["assistant"])
            md.append(assistant_full)
            md.append("\n")
        
        md.append("---\n")

    return "\n".join(md)

def generate_readme(conv_id, title, created_files_map):
    md = []
    md.append(f"# 📖 Архів Розмови: {title}\n")
    md.append(f"Ця папка містить чистий архів діалогу (Запит — Відповідь) та створених під час нього файлів.\n")
    md.append("## 📄 Повний діалог:")
    md.append("- 📖 [dialogue.md](./dialogue.md) — Запити користувача та відповіді асистента у форматі Markdown\n")
    
    md.append("## 📂 Створені файли:")
    if created_files_map:
        for orig_path, rel_path in created_files_map.items():
            fname = os.path.basename(orig_path)
            md.append(f"- 📄 [{fname}]({rel_path})")
    else:
        md.append("- *Під час цієї сесії не було створено додаткових файлів.*")
        
    return "\n".join(md)

def main():
    parser = argparse.ArgumentParser(description="Archive dialogue cleanly (user request + assistant response + files).")
    parser.add_argument("--conv-id", help="Conversation ID to archive", default=None)
    parser.add_argument("--app-data-dir", help="Path to Antigravity appDataDir", default=r"C:\Users\taxco\.gemini\antigravity")
    parser.add_argument("--workspace-dir", help="Workspace root directory", default=r"c:\Users\taxco\Dev\Tomos")
    parser.add_argument("--output-dir", help="Destination folder for archive", default=None)
    parser.add_argument("--title", help="Title / topic of conversation", default="Dialogue Archive")

    args = parser.parse_args()

    app_data_dir = os.path.abspath(args.app_data_dir)
    workspace_dir = os.path.abspath(args.workspace_dir)
    
    # Auto-detect conv-id if not supplied
    conv_id = args.conv_id
    if not conv_id:
        brain_dir = os.path.join(app_data_dir, "brain")
        if os.path.exists(brain_dir):
            subdirs = [d for d in os.listdir(brain_dir) if os.path.isdir(os.path.join(brain_dir, d))]
            if subdirs:
                subdirs.sort(key=lambda d: os.path.getmtime(os.path.join(brain_dir, d)), reverse=True)
                conv_id = subdirs[0]

    if not conv_id:
        print("Error: Could not determine Conversation ID.")
        sys.exit(1)

    print(f"Archiving conversation ID cleanly: {conv_id}")
    
    # Path to transcript
    logs_dir = os.path.join(app_data_dir, "brain", conv_id, ".system_generated", "logs")
    transcript_full = os.path.join(logs_dir, "transcript_full.jsonl")
    transcript_norm = os.path.join(logs_dir, "transcript.jsonl")
    
    transcript_file = transcript_full if os.path.exists(transcript_full) else transcript_norm
    if not os.path.exists(transcript_file):
        print(f"Warning: Transcript file not found at {transcript_file}")
        steps = []
    else:
        steps = parse_transcript(transcript_file)

    # Extract title from user input if default
    inferred_title = args.title
    for s in steps:
        if s.get("type") in ["USER_INPUT", "USER_EXPLICIT"]:
            c = s.get("content", "")
            match = re.search(r'<USER_REQUEST>\s*(.*?)\s*</USER_REQUEST>', c, re.DOTALL)
            if match:
                clean_req = match.group(1).split("\n")[0][:60]
                inferred_title = clean_req
            elif c:
                inferred_title = c.strip().split("\n")[0][:60]
            break

    # Set output dir
    timestamp_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    if not args.output_dir:
        output_dir = os.path.join(workspace_dir, "archives", f"archive_{timestamp_str}_{conv_id[:8]}")
    else:
        output_dir = os.path.abspath(args.output_dir)

    os.makedirs(output_dir, exist_ok=True)
    files_dir = os.path.join(output_dir, "files")
    os.makedirs(files_dir, exist_ok=True)

    # Find created files
    created_files = find_created_files(app_data_dir, conv_id, workspace_dir, steps)
    
    created_files_map = {}
    for filepath in created_files:
        if not os.path.isfile(filepath):
            continue
        if os.path.abspath(output_dir) in os.path.abspath(filepath):
            continue
            
        rel_dest = os.path.join("files", os.path.basename(filepath))
        dest_full = os.path.join(output_dir, rel_dest)
        
        counter = 1
        base, ext = os.path.splitext(os.path.basename(filepath))
        while os.path.exists(dest_full):
            rel_dest = os.path.join("files", f"{base}_{counter}{ext}")
            dest_full = os.path.join(output_dir, rel_dest)
            counter += 1
            
        shutil.copy2(filepath, dest_full)
        created_files_map[filepath] = rel_dest.replace("\\", "/")

    # Build dialogue.md
    dialogue_md = generate_markdown(steps, conv_id, created_files_map, inferred_title)
    dialogue_file = os.path.join(output_dir, "dialogue.md")
    with open(dialogue_file, "w", encoding="utf-8") as f:
        f.write(dialogue_md)

    # Build README.md
    readme_md = generate_readme(conv_id, inferred_title, created_files_map)
    readme_file = os.path.join(output_dir, "README.md")
    with open(readme_file, "w", encoding="utf-8") as f:
        f.write(readme_md)

    # Build metadata.json
    meta = {
        "conversation_id": conv_id,
        "title": inferred_title,
        "archived_at": datetime.now().isoformat(),
        "copied_files_count": len(created_files_map),
        "files_mapping": created_files_map
    }
    meta_file = os.path.join(output_dir, "metadata.json")
    with open(meta_file, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    print(f"Dialogue archived cleanly!")
    print(f"Archive location: {output_dir}")
    print(f"Dialogue MD: {dialogue_file}")
    print(f"Copied {len(created_files_map)} files.")

if __name__ == "__main__":
    main()
