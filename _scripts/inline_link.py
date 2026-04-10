#!/usr/bin/env python3
"""
Inline-link metrics, datasets, and papers throughout all paper .md files.
Replaces plain-text mentions with [[Name]] Obsidian wikilinks.
Skips frontmatter, already-linked text, and PDF embeds.
"""

import os
import re
from pathlib import Path

VAULT = Path("/home/omar/Repos/physical-intelligence-vault")

def get_names(folder):
    """Get all .md filenames (without extension) from a folder."""
    names = []
    for f in (VAULT / folder).glob("*.md"):
        names.append(f.stem)
    return names

def get_aliases(folder):
    """Get aliases from frontmatter of files in a folder."""
    alias_map = {}  # alias -> canonical name
    for f in (VAULT / folder).glob("*.md"):
        canonical = f.stem
        with open(f, 'r') as fh:
            content = fh.read()
        # Extract aliases from frontmatter
        m = re.search(r'^aliases:\s*\[([^\]]*)\]', content, re.MULTILINE)
        if m:
            aliases = [a.strip().strip('"').strip("'") for a in m.group(1).split(',') if a.strip()]
            for alias in aliases:
                if alias and alias != canonical:
                    alias_map[alias] = canonical
    return alias_map

# Collect all linkable names
metrics = get_names("Metrics")
datasets = get_names("Datasets")
papers = get_names("Papers")

# Collect aliases
metric_aliases = get_aliases("Metrics")
dataset_aliases = get_aliases("Datasets")
paper_aliases = get_aliases("Papers")

# Build a single lookup: name -> name (canonical), sorted longest first to avoid partial matches
all_names = {}
for n in metrics:
    all_names[n] = n
for n in datasets:
    all_names[n] = n
for n in papers:
    all_names[n] = n
for alias, canonical in metric_aliases.items():
    if alias not in all_names:  # Don't override canonical names
        all_names[alias] = canonical
for alias, canonical in dataset_aliases.items():
    if alias not in all_names:
        all_names[alias] = canonical
for alias, canonical in paper_aliases.items():
    if alias not in all_names:
        all_names[alias] = canonical

# Sort by length descending so longer names match first
sorted_names = sorted(all_names.keys(), key=len, reverse=True)

# Pre-filter: remove very short names that cause false positives
sorted_names = [n for n in sorted_names if len(n) >= 3]

# Names that need special handling (they're common words or substrings)
SKIP_NAMES = {"AVA", "COIN", "MVP", "FPS", "DMLab"}  # Too short / common

def process_line(line, own_paper_name):
    """Replace plain-text mentions with [[links]] in a single line."""
    # Skip lines that are frontmatter, embeds, or PDF embed lines
    if line.startswith('![[') or line.startswith('---') or line.startswith('!PDFs/'):
        return line

    for name in sorted_names:
        if name in SKIP_NAMES:
            continue
        canonical = all_names[name]

        # Don't self-link
        if canonical == own_paper_name:
            continue

        # Build pattern: match the name NOT already inside [[ ]]
        escaped = re.escape(name)

        # Build negative lookahead for longer names that start with this one
        # e.g. "V-JEPA" should not match when followed by " 2" (→ "V-JEPA 2")
        # e.g. "V-JEPA 2" should not match when followed by ".1" (→ "V-JEPA 2.1")
        # e.g. "Pi0" should not match when followed by ".5" or ".6"
        suffix_lookaheads = []
        for longer_name in sorted_names:
            if longer_name != name and longer_name.startswith(name) and len(longer_name) > len(name):
                suffix = re.escape(longer_name[len(name):])
                suffix_lookaheads.append(suffix)

        lookahead = ""
        if suffix_lookaheads:
            # Combine all suffix lookaheads: (?!\.1|\.5|\.6| 2)
            lookahead = "(?!" + "|".join(suffix_lookaheads) + ")"

        pattern = r'(?<!\[\[)(?<!\|)\b' + escaped + r'\b(?!\]\])(?!\|)' + lookahead

        def replacer(m):
            # Check if we're inside a [[ ]] block by scanning backwards
            start = m.start()
            prefix = line[:start]
            # Count [[ and ]] to see if we're inside a link
            open_count = prefix.count('[[')
            close_count = prefix.count(']]')
            if open_count > close_count:
                return m.group(0)  # Inside a link, don't replace
            if canonical != name:
                return f'[[{canonical}|{name}]]'
            return f'[[{canonical}]]'

        line = re.sub(pattern, replacer, line)

    return line

def process_file(filepath):
    """Process a single paper file."""
    paper_name = filepath.stem

    with open(filepath, 'r') as f:
        content = f.read()

    lines = content.split('\n')
    result = []
    in_frontmatter = False
    frontmatter_count = 0
    changed = False

    for line in lines:
        if line.strip() == '---':
            frontmatter_count += 1
            if frontmatter_count <= 2:
                in_frontmatter = frontmatter_count == 1
                result.append(line)
                if frontmatter_count == 2:
                    in_frontmatter = False
                continue

        if in_frontmatter:
            result.append(line)
            continue

        new_line = process_line(line, paper_name)
        if new_line != line:
            changed = True
        result.append(new_line)

    if changed:
        with open(filepath, 'w') as f:
            f.write('\n'.join(result))
        print(f"Updated: {paper_name}")
    else:
        print(f"No changes: {paper_name}")

# Process all paper files
for f in sorted((VAULT / "Papers").glob("*.md")):
    process_file(f)

print(f"\nDone. Processed {len(list((VAULT / 'Papers').glob('*.md')))} files.")
print(f"Linkable names: {len(sorted_names)} (metrics: {len(metrics)}, datasets: {len(datasets)}, papers: {len(papers)}, aliases: {len(metric_aliases) + len(dataset_aliases) + len(paper_aliases)})")
