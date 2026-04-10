#!/usr/bin/env python3
"""
Replace ![[PDFs/file.pdf]] with HTML iframe embeds for Quartz web rendering.
Only modifies files in the Quartz content folder, not the vault source.
"""

import re
import sys
from pathlib import Path

target_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/home/omar/Repos/physical-intelligence-site/content/Papers")

count = 0
for f in sorted(target_dir.glob("*.md")):
    content = f.read_text()

    def replacer(m):
        pdf_path = m.group(1)
        # URL-encode the path for the web
        encoded = pdf_path.replace(' ', '%20')
        return f'<iframe src="/{encoded}" width="100%" height="800px" style="border: 1px solid #333; border-radius: 8px; margin-bottom: 1em;"></iframe>'

    new_content = re.sub(r'!\[\[(PDFs/[^\]]+\.pdf)\]\]', replacer, content)

    if new_content != content:
        f.write_text(new_content)
        count += 1
        print(f"  Updated: {f.name}")

print(f"\nConverted PDF embeds in {count} files")
