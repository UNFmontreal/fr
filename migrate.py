#!/usr/bin/env python3
"""
Migrate Hugo FR content to MyST/JB format.
- Strips Hugo-specific frontmatter fields
- Renames _index.md → index.md
- Converts YouTube shortcodes to MyST directives
- Copies resulting files to target locations
"""

import re
import shutil
from pathlib import Path

SRC = Path("/home/lune/git/unf-montreal.ca/content/fr")
DST = Path("/home/lune/git/unf-montreal.ca-fr")

# Hugo frontmatter keys to drop
DROP_KEYS = {
    "draft", "bg_image", "image", "type", "linkTitle",
    "icon", "link", "contact", "interest", "course", "bio",
}

# Section mapping: src subpath → dst subpath (None = skip)
SECTION_MAP = {
    "documentation/facility": "facility",
    "documentation/your_study": "your_study",
    "documentation/your_data": "your_data",
    "documentation/covid": "documents/covid",
    "documentation/welcome": "welcome",  # will merge into about or keep
    "documentation": "documentation_root",  # _index.md only → skip (content in intro)
    "course": "course",
    "documents": "documents",
    "team": None,  # handled separately as team.md gallery
    "news": "news",
    "seminars": "seminars",
    "about": None,  # placeholder, write manually
    "contact": None,  # placeholder, write manually
    "rate": None,  # write manually (already done)
    "history": None,
    "researchers": None,
    "author": None,
    "event": None,
    "research": None,
    "scholarship": None,
}

KEEP_FRONTMATTER = {"title", "date", "description"}


def strip_frontmatter(text: str) -> str:
    """Keep only whitelisted frontmatter keys, drop Hugo-specific ones."""
    if not text.startswith("---"):
        return text

    end = text.find("---", 3)
    if end == -1:
        return text

    fm_block = text[3:end].strip()
    body = text[end + 3:].lstrip("\n")

    kept_lines = []
    skip_multiline = False
    for line in fm_block.splitlines():
        # Detect multiline value continuation (indented)
        if skip_multiline:
            if line.startswith(" ") or line.startswith("\t"):
                continue
            else:
                skip_multiline = False

        # Parse key
        m = re.match(r'^(\w+)\s*:', line)
        if m:
            key = m.group(1)
            if key not in KEEP_FRONTMATTER:
                # Check if this is a multiline block value
                if line.rstrip().endswith(">") or line.rstrip().endswith("|"):
                    skip_multiline = True
                continue
        kept_lines.append(line)

    if kept_lines:
        new_fm = "---\n" + "\n".join(kept_lines) + "\n---\n\n"
    else:
        new_fm = ""

    return new_fm + body


def convert_shortcodes(text: str) -> str:
    """Convert Hugo shortcodes to MyST directives."""
    # YouTube: {{< youtube ID >}} → MyST raw html iframe
    text = re.sub(
        r'\{\{<\s*youtube\s+(\S+)\s*>\}\}',
        lambda m: (
            "```{raw} html\n"
            f'<iframe width="560" height="315" '
            f'src="https://www.youtube.com/embed/{m.group(1)}" '
            'frameborder="0" allowfullscreen></iframe>\n'
            "```"
        ),
        text,
    )
    return text


def migrate_file(src: Path, dst: Path):
    dst.parent.mkdir(parents=True, exist_ok=True)
    text = src.read_text(encoding="utf-8")
    text = strip_frontmatter(text)
    text = convert_shortcodes(text)
    dst.write_text(text, encoding="utf-8")
    print(f"  {src.relative_to(SRC)} → {dst.relative_to(DST)}")


def migrate_section(src_rel: str, dst_rel: str):
    src_dir = SRC / src_rel
    dst_dir = DST / dst_rel
    if not src_dir.exists():
        print(f"  [skip] {src_rel} not found")
        return
    for src_file in sorted(src_dir.rglob("*.md")):
        rel = src_file.relative_to(src_dir)
        # Rename _index.md → index.md
        parts = list(rel.parts)
        parts = ["index.md" if p == "_index.md" else p for p in parts]
        dst_file = dst_dir / Path(*parts)
        migrate_file(src_file, dst_file)


def build_team_page() -> str:
    """Build a single MyST grid page from all team member files."""
    lines = ["# Notre Équipe\n\n"]
    lines.append("::::{grid} 1 2 3 3\n:gutter: 3\n\n")

    team_dir = SRC / "team"
    for md in sorted(team_dir.glob("*.md")):
        if md.name == "_index.md":
            continue
        text = md.read_text(encoding="utf-8")
        title = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', text, re.M)
        course = re.search(r'^course:\s*["\']?(.+?)["\']?\s*$', text, re.M)
        bio = re.search(r'^bio:\s*["\']?(.+?)["\']?\s*$', text, re.M)
        email_m = re.search(r'mailto:([^\s"]+)', text)

        name = title.group(1) if title else md.stem
        role = course.group(1) if course else ""
        bio_text = bio.group(1) if bio else ""
        email = email_m.group(1) if email_m else None

        lines.append(":::{grid-item-card} " + name + "\n")
        if role:
            lines.append(f"**{role}**\n\n")
        if bio_text:
            lines.append(bio_text + "\n\n")
        if email:
            lines.append(f"[{email}](mailto:{email})\n")
        lines.append(":::\n\n")

    lines.append("::::\n")
    return "".join(lines)


if __name__ == "__main__":
    print("=== Migrating content sections ===")
    for src_rel, dst_rel in [
        ("documentation/facility", "facility"),
        ("documentation/your_study", "your_study"),
        ("documentation/your_data", "your_data"),
        ("documentation/covid", "documents/covid"),
        ("documentation/welcome", "welcome"),
        ("course", "course"),
        ("documents", "documents"),
        ("news", "news"),
        ("seminars", "seminars"),
    ]:
        print(f"\n[{src_rel}]")
        migrate_section(src_rel, dst_rel)

    print("\n[team] → team.md (grid)")
    team_page = build_team_page()
    (DST / "team.md").write_text(team_page, encoding="utf-8")
    print("  team/* → team.md")

    # Migrate documentation _index as the documentation landing (skip, already have intro)
    doc_index = SRC / "documentation" / "_index.md"
    if doc_index.exists():
        migrate_file(doc_index, DST / "documentation_index.md")

    print("\nDone.")
