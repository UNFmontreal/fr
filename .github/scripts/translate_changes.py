"""
Called by sync-en.yml in GitHub Actions.
Reads changes.txt (git diff --name-status output), translates changed .md files,
writes results to /tmp/translated/ mirroring the repo structure.
Deleted files are recorded in /tmp/deleted_files.txt.
"""

import os
import pathlib
import sys
import anthropic

TRANSLATED_DIR = pathlib.Path("/tmp/translated")
DELETED_FILE = pathlib.Path("/tmp/deleted_files.txt")
REPO_ROOT = pathlib.Path(os.environ.get("GITHUB_WORKSPACE", "."))

SYSTEM_PROMPT = """You are a technical translator. Translate MyST Markdown documents from French to English.

Rules:
- Translate only human-readable French text (headings, paragraphs, table cells, link text, card titles/descriptions).
- Preserve ALL MyST directives exactly: :::, {image}, {grid}, {grid-item}, {grid-item-card}, {note}, etc.
- Preserve ALL YAML frontmatter keys (only translate values if they are human-readable text like title/description).
- Preserve ALL links, image paths, email addresses, URLs, and file references unchanged.
- Preserve ALL markdown formatting: bold, italic, tables, bullet lists, code blocks.
- Preserve ALL inline HTML exactly (iframes, etc.).
- Do NOT add or remove blank lines beyond what is necessary.
- Output ONLY the translated markdown. No preamble, no explanation."""


def translate_content(client: anthropic.Anthropic, content: str, filename: str) -> str:
    message = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=8192,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Translate this file ({filename}) from French to English:\n\n{content}",
            }
        ],
    )
    return message.content[0].text


def main():
    changes_file = pathlib.Path("changes.txt")
    if not changes_file.exists():
        print("No changes.txt found, nothing to translate.")
        return

    client = anthropic.Anthropic()
    TRANSLATED_DIR.mkdir(parents=True, exist_ok=True)
    deleted = []

    for line in changes_file.read_text().splitlines():
        line = line.strip()
        if not line:
            continue

        parts = line.split("\t", 1)
        if len(parts) != 2:
            continue
        status, filepath = parts[0], parts[1]

        # Handle renames: "R100\told_path\tnew_path"
        if status.startswith("R") and "\t" in filepath:
            old_path, new_path = filepath.split("\t", 1)
            deleted.append(old_path)
            filepath = new_path
            status = "A"

        if not filepath.endswith(".md"):
            continue

        abs_path = REPO_ROOT / filepath

        if status in ("A", "M"):
            if not abs_path.exists():
                print(f"  SKIP (not found): {filepath}")
                continue

            content = abs_path.read_text(encoding="utf-8")
            print(f"  Translating {filepath} ... ", end="", flush=True)
            translated = translate_content(client, content, filepath)

            out_path = TRANSLATED_DIR / filepath
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(translated, encoding="utf-8")
            print("done")

        elif status == "D":
            deleted.append(filepath)
            print(f"  Marked for deletion: {filepath}")

    if deleted:
        DELETED_FILE.write_text("\n".join(deleted) + "\n")

    print("Translation complete.")


if __name__ == "__main__":
    main()
