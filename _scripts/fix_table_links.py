#!/usr/bin/env python3
"""
Fix wikilinks inside markdown tables.
The pipe | in [[Name|Alias]] breaks table column parsing.
Solution: In table rows, replace [[Name|Alias]] with [[Name]] (drop the alias).
Outside tables, [[Name|Alias]] is fine and left alone.
"""

import re
from pathlib import Path

VAULT = Path("/home/omar/Repos/physical-intelligence-vault")

def is_table_line(line):
    """Check if a line is part of a markdown table."""
    stripped = line.strip()
    return stripped.startswith('|') or (stripped.startswith('|') and stripped.endswith('|'))

def is_separator_line(line):
    """Check if line is a table separator like |---|---|"""
    return bool(re.match(r'^\s*\|[\s\-:|]+\|', line))

def fix_table_links(line):
    """Replace [[Name|Alias]] with [[Name]] in a table line."""
    # Match [[anything|anything]] - the alias form
    # But we need to be careful: the | inside [[ ]] should not be treated as table delimiter
    # Fix: replace [[X|Y]] with [[X]] to remove the ambiguous pipe
    result = re.sub(r'\[\[([^\]|]+)\|([^\]]+)\]\]', r'[[\1]]', line)
    return result

def fix_table_column_count(lines):
    """Fix tables where the header/separator/data rows have mismatched column counts."""
    result = []
    i = 0
    while i < len(lines):
        line = lines[i]

        # Detect start of a table (header line)
        if is_table_line(line) and i + 1 < len(lines) and is_separator_line(lines[i + 1]):
            # Fix header
            fixed_header = fix_table_links(line)
            header_cols = len([c for c in fixed_header.split('|') if c.strip() != '']) if fixed_header.strip().startswith('|') else 0

            result.append(fixed_header)
            i += 1

            # Fix separator to match header column count
            if i < len(lines) and is_separator_line(lines[i]):
                sep_line = lines[i]
                # Rebuild separator with correct column count
                if header_cols > 0:
                    sep_parts = re.findall(r'[\s\-:]+', sep_line)
                    # Just pass through the separator but ensure it matches
                    result.append(sep_line)
                else:
                    result.append(sep_line)
                i += 1

            # Fix data rows
            while i < len(lines) and is_table_line(lines[i]) and not lines[i].strip() == '':
                fixed_row = fix_table_links(lines[i])
                result.append(fixed_row)
                i += 1
        else:
            result.append(line)
            i += 1

    return result

def process_file(filepath):
    """Process a single file, fixing table links."""
    with open(filepath, 'r') as f:
        content = f.read()

    lines = content.split('\n')

    # First pass: fix [[Name|Alias]] in table lines
    new_lines = []
    in_frontmatter = False
    fm_count = 0

    for line in lines:
        if line.strip() == '---':
            fm_count += 1
            if fm_count <= 2:
                in_frontmatter = fm_count == 1
                new_lines.append(line)
                if fm_count == 2:
                    in_frontmatter = False
                continue

        if in_frontmatter:
            new_lines.append(line)
            continue

        if is_table_line(line):
            new_lines.append(fix_table_links(line))
        else:
            new_lines.append(line)

    # Second pass: fix separator rows that have wrong column count
    final_lines = []
    i = 0
    while i < len(new_lines):
        line = new_lines[i]

        # If this is a table header, check column count matches separator
        if is_table_line(line) and i + 1 < len(new_lines) and is_separator_line(new_lines[i + 1]):
            header_cells = [c for c in line.split('|')]
            header_count = len(header_cells)

            sep_line = new_lines[i + 1]
            sep_cells = [c for c in sep_line.split('|')]
            sep_count = len(sep_cells)

            if header_count != sep_count:
                # Rebuild separator to match header
                new_sep_parts = []
                for j, cell in enumerate(header_cells):
                    if j == 0 or j == len(header_cells) - 1:
                        new_sep_parts.append(cell if cell.strip() == '' else ' ' + '-' * max(3, len(cell.strip())) + ' ')
                    else:
                        new_sep_parts.append(' ' + '-' * max(3, len(cell.strip())) + ' ')
                new_sep = '|'.join(new_sep_parts)
                final_lines.append(line)
                final_lines.append(new_sep)
                i += 2
                continue

        final_lines.append(line)
        i += 1

    new_content = '\n'.join(final_lines)

    if new_content != content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Fixed: {filepath.stem}")
        return True
    else:
        print(f"No changes: {filepath.stem}")
        return False

# Process all paper files
fixed = 0
for f in sorted((VAULT / "Papers").glob("*.md")):
    if process_file(f):
        fixed += 1

print(f"\nDone. Fixed {fixed} files.")
