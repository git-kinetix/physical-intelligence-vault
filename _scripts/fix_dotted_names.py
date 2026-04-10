#!/usr/bin/env python3
"""
Fix broken references where the inline linker matched a prefix name
inside a longer dotted name. E.g.:
  - [[V-JEPA 2]].1 → V-JEPA 2.1 (in own file) or [[V-JEPA 2.1]] (in other files)
  - [[Pi0]].5 → Pi0.5 or [[Pi0.5]]
  - [[Pi0]].6 → Pi0.6 or [[Pi0.6]]
  - !PDFs/[[X]].Y.pdf → !PDFs/X.Y.pdf (always, embeds never need wikilinks)
  - !PDFs/[[V-JEPA]] 2.pdf → !PDFs/V-JEPA 2.pdf
"""

import re
from pathlib import Path

VAULT = Path("/home/omar/Repos/physical-intelligence-vault")

# Patterns: (broken pattern, what the full name should be)
FIXES = [
    (r'\[\[V-JEPA 2\]\]\.1', 'V-JEPA 2.1'),
    (r'\[\[V-JEPA 2\]\] \.1', 'V-JEPA 2.1'),
    (r'\[\[Pi0\]\]\.5', 'Pi0.5'),
    (r'\[\[Pi0\]\]\.6', 'Pi0.6'),
    (r'\[\[Pi0\.5\]\]\.6', 'Pi0.6'),  # just in case
]

count = 0
for f in sorted((VAULT / "Papers").glob("*.md")):
    content = f.read_text()
    original = content
    paper_name = f.stem

    # Fix PDF embed lines — always strip [[ ]] from inside !PDFs/ paths
    content = re.sub(r'!PDFs/\[\[([^\]]+)\]\](\S*\.pdf)', r'!PDFs/\1\2', content)
    # Also fix ![[...]] style if present
    content = re.sub(r'!\[\[PDFs/\[\[([^\]]+)\]\](\S*\.pdf)\]\]', r'![[PDFs/\1\2]]', content)

    # Fix broken dotted names in body text
    for broken_pat, full_name in FIXES:
        if paper_name == full_name:
            # Self-reference: replace with plain text
            content = re.sub(broken_pat, full_name, content)
        else:
            # Cross-reference: replace with proper wikilink
            content = re.sub(broken_pat, f'[[{full_name}]]', content)

    if content != original:
        f.write_text(content)
        count += 1
        print(f"  Fixed: {f.stem}")

print(f"\nFixed {count} files")
