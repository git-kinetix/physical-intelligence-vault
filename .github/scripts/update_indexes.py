#!/usr/bin/env python3
"""
Regenerate MOC.md, README.md, and CLAUDE.md from paper frontmatter.
Runs as a GitHub Action when new papers are added.
"""

import re
import yaml
from pathlib import Path

VAULT = Path(".")

# ── Parse all papers ──────────────────────────────────────────────

def parse_frontmatter(path):
    text = path.read_text()
    m = re.match(r'^---\n(.*?)\n---', text, re.DOTALL)
    if not m:
        return None
    try:
        fm = yaml.safe_load(m.group(1))
    except Exception:
        return None
    fm["_stem"] = path.stem
    return fm

papers = []
for f in sorted((VAULT / "Papers").glob("*.md")):
    fm = parse_frontmatter(f)
    if fm and "paper" in (fm.get("tags") or []):
        papers.append(fm)

# ── Group definitions ─────────────────────────────────────────────

# Map group names (from frontmatter) to MOC sections
GROUP_ORDER = [
    ("JEPA Family", "JEPA Family", "Joint-Embedding Predictive Architectures for video/image understanding and robot control."),
    ("World Models", "World Models", "Models that learn environment dynamics for planning, imagination, and control."),
    ("VLA Models", "VLA Models", "Vision-Language-Action models for generalist robot control via imitation learning."),
    ("Video Generation / Planning", "Video Generation / Planning", "Action-conditioned video generation and video-based planning for physical AI."),
]

# Papers with these tags go to character animation section (special handling)
CHAR_ANIM_PAPERS = {p["_stem"] for p in papers if "physics-simulation" in (p.get("tags") or []) and p.get("group") not in ("JEPA Family", "VLA Models", "Video Generation / Planning") and p.get("group") not in ("World Models",) or any(kw in p["_stem"] for kw in ["DeepMimic", "AMP", "ASE", "CALM", "Masked", "MVAE", "Physics", "Control", "Muscle", "PADL", "Super", "CLoSD", "PARC", "MCP", "SFV", "DeepLoco", "Vid2Player", "Puppet", "LeVERB"])}

def get_section(fm):
    stem = fm["_stem"]
    group = fm.get("group", "")
    tags = fm.get("tags") or []

    # Character animation papers
    if stem in CHAR_ANIM_PAPERS:
        return "Character Animation"

    # Sim-to-real
    if stem in ("Sim-to-Real Transfer", "Learning Agile Robotic Locomotion", "Eureka"):
        return "Sim-to-Real & Reward Design"

    # By group field
    for group_name, section_name, _ in GROUP_ORDER:
        if group == group_name:
            return section_name

    # Fallback: try tags
    if "jepa" in tags:
        return "JEPA Family"
    if "vla" in tags:
        return "VLA Models"
    if "world-model" in tags:
        return "World Models"
    if "video-planning" in tags:
        return "Video Generation / Planning"
    if "motion" in tags and "physics-simulation" not in tags:
        return "Video Generation / Planning"

    return "World Models"  # default bucket

# ── Build paper table rows ────────────────────────────────────────

def paper_row(fm):
    name = fm["_stem"]
    year = fm.get("year", "?")
    title = fm.get("title", name)
    # Generate a short key idea from title
    idea = title
    if len(idea) > 60:
        idea = idea[:57] + "..."
    return f"| [[{name}]] | {year} | {idea} |"

# Group papers by section, sort by year desc
sections = {}
for p in papers:
    sec = get_section(p)
    sections.setdefault(sec, []).append(p)

for sec in sections:
    sections[sec].sort(key=lambda p: -(p.get("year") or 0))

# ── Update README.md ──────────────────────────────────────────────

readme_papers = ", ".join(sorted(p["_stem"] for p in papers))
paper_count = len(papers)
metric_count = len(list((VAULT / "Metrics").glob("*.md")))
dataset_count = len(list((VAULT / "Datasets").glob("*.md")))
explainer_count = len(list((VAULT / "Explainers").iterdir())) if (VAULT / "Explainers").exists() else 0
pdf_count = len(list((VAULT / "PDFs").glob("*.pdf")))

readme = f"""# Physical Intelligence Vault

A research knowledge base covering **{paper_count} papers** on physical intelligence — world models, joint-embedding architectures, vision-language-action models, physics-based character control, and video generation for planning.

**Live site:** [dxlrak3ky5x8b.cloudfront.net](https://dxlrak3ky5x8b.cloudfront.net)

## What's inside

| Content | Count |
|---------|-------|
| Papers | {paper_count} |
| Embedded PDFs | {pdf_count} |
| Metric definitions | {metric_count} |
| Dataset descriptions | {dataset_count} |
| Interactive explainers | {explainer_count} |

Every paper node includes a summary, architecture breakdown, reproduced results tables (with inline-linked metrics and datasets), and related paper connections.

## Papers by group

"""

for sec_name in ["JEPA Family", "World Models", "Character Animation", "VLA Models", "Video Generation / Planning", "Sim-to-Real & Reward Design", "Other"]:
    if sec_name not in sections:
        continue
    readme += f"### {sec_name}\n"
    names = [p["_stem"] for p in sections[sec_name]]
    readme += " · ".join(names) + "\n\n"

readme += """## Vault structure

```
├── Papers/           # Paper nodes with embedded PDFs
├── Metrics/          # Metric definitions
├── Datasets/         # Dataset descriptions
├── PDFs/             # Arxiv PDFs for inline viewing
├── Explainers/       # Interactive distill-style explorations
├── Canvases/         # Obsidian canvas with paper relationship graph
├── Templates/        # Paper, metric, and dataset templates
├── MOC.md            # Map of Content (main index)
├── Metrics Index.md  # All metrics by category
└── Datasets Index.md # All datasets by category
```

## Auto-deploy

Every push to `main` that adds papers triggers a GitHub Action that updates MOC.md, README.md, and CLAUDE.md.

## Adding a paper

1. Create `Papers/Paper Name.md` using the template in `Templates/Paper Template.md`
2. Download the PDF to `PDFs/Paper Name.pdf`
3. Add `![[PDFs/Paper Name.pdf]]` after the frontmatter
4. Use `[[Metric Name]]` and `[[Dataset Name]]` to link to existing nodes
5. Push to `main` — indexes update automatically

## Graph view colors (Obsidian)

| Color | Tag |
|-------|-----|
| Cyan | `#jepa` |
| Red | `#world-model` |
| Green | `#vla` |
| Yellow | `#video-planning` |
| Magenta | `#metric` |
| Blue | `#dataset` |
"""

(VAULT / "README.md").write_text(readme)
print(f"Updated README.md ({paper_count} papers)")

# ── Update CLAUDE.md ──────────────────────────────────────────────

def group_summary(sec_name, papers_list):
    count = len(papers_list)
    names = ", ".join(p["_stem"] for p in papers_list)
    return f"**{sec_name} ({count}):** {names}"

claude_sections = []
for sec_name in ["JEPA Family", "World Models", "Character Animation", "VLA Models", "Video Generation / Planning", "Sim-to-Real & Reward Design"]:
    if sec_name in sections:
        claude_sections.append(group_summary(sec_name, sections[sec_name]))

claude = f"""# Physical Intelligence Vault

{paper_count} papers on physical intelligence. Use this to answer cross-paper questions.

## Groups at a glance

{chr(10).join(claude_sections)}

## Key relationships

- AMP is the pivotal paper bridging DeepMimic→ASE/CALM/MaskedMimic (replaced hand-crafted rewards with learned discriminator)
- VAE vs Adversarial: two competing approaches to learning motor skills from MoCap. VAE gives smooth interpolation; adversarial scales better to diverse data
- Pi0 uses flow matching (like diffusion but ODE-based), ACT uses CVAE — both do action chunking
- V-JEPA 2-AC and Le-World-Model both do latent-space planning but V-JEPA 2-AC uses frozen features while LeWM trains end-to-end
- TD-MPC2 and DreamerV3 are the two main model-based RL approaches (MPC planning vs imagination)
- TD-JEPA combines TD-MPC2's TD learning with JEPA representations for zero-shot transfer

## Vault structure

- `Papers/` — {paper_count} paper nodes with frontmatter (tags, year, arxiv, repo, importance, group)
- `Metrics/` — {metric_count} metric definitions
- `Datasets/` — {dataset_count} dataset descriptions
- `Explainers/` — {explainer_count} interactive distill-style explainers
- `MOC.md` — main index organized by group
- Tags: `physics-simulation` (uses physics engine) vs `motion` (video/kinematic)

## Web app

- Site: https://dxlrak3ky5x8b.cloudfront.net
- Backend: DynamoDB API at https://zu6qahfn14.execute-api.eu-west-3.amazonaws.com (stores starred/read-by state)
- Built with Quartz v4, customized site repo at git-kinetix/physical-intelligence-site
"""

(VAULT / "CLAUDE.md").write_text(claude)
print(f"Updated CLAUDE.md")

print("Done.")
