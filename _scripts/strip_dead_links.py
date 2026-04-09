#!/usr/bin/env python3
"""
Remove [[ ]] from wikilinks that point to non-existent pages.
Keeps the display text, just removes the link syntax.
"""

import re
from pathlib import Path

VAULT = Path("/home/omar/Repos/physical-intelligence-vault")

# Collect all existing page names (stems of .md files)
existing = set()
for folder in ["Papers", "Metrics", "Datasets"]:
    for f in (VAULT / folder).glob("*.md"):
        existing.add(f.stem)
# Root-level pages
for f in VAULT.glob("*.md"):
    existing.add(f.stem)

# Also collect aliases
aliases = set()
for folder in ["Papers", "Metrics", "Datasets"]:
    for f in (VAULT / folder).glob("*.md"):
        content = f.read_text()
        m = re.search(r'^aliases:\s*\[([^\]]*)\]', content, re.MULTILINE)
        if m:
            for alias in m.group(1).split(','):
                alias = alias.strip().strip('"').strip("'")
                if alias:
                    aliases.add(alias)

all_valid = existing | aliases
print(f"Valid targets: {len(existing)} pages + {len(aliases)} aliases = {len(all_valid)} total")

def strip_dead_links(content, filename):
    """Replace [[target]] or [[target|display]] with plain text if target doesn't exist."""
    changes = 0

    def replacer(m):
        nonlocal changes
        full = m.group(0)
        inner = m.group(1)

        if '|' in inner:
            target, display = inner.split('|', 1)
        else:
            target = inner
            display = inner

        target = target.strip()

        # Check if target exists
        if target in all_valid:
            return full  # Keep the link

        changes += 1
        return display.strip()

    result = re.sub(r'\[\[([^\]]+)\]\]', replacer, content)
    return result, changes

total_changes = 0
for folder in ["Papers", "Metrics", "Datasets"]:
    for f in sorted((VAULT / folder).glob("*.md")):
        content = f.read_text()
        new_content, changes = strip_dead_links(content, f.name)
        if changes > 0:
            f.write_text(new_content)
            total_changes += changes
            print(f"  Fixed {changes:3d} dead links in {folder}/{f.stem}")

print(f"\nTotal: stripped {total_changes} dead links")
