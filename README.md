# Physical Intelligence Vault

A research knowledge base covering **34 papers** on physical intelligence — world models, joint-embedding architectures, vision-language-action models, and video generation for planning.

**Live site:** [dxlrak3ky5x8b.cloudfront.net](https://dxlrak3ky5x8b.cloudfront.net)

## What's inside

| Content | Count |
|---------|-------|
| Papers | 34 |
| Embedded PDFs | 30 |
| Metric definitions | 64 |
| Dataset descriptions | 78 |

Every paper node includes a summary, architecture breakdown, reproduced results tables (with inline-linked metrics and datasets), and related paper connections.

## Papers by group

### JEPA Family
V-JEPA 2.1 · V-JEPA 2 · V-JEPA · I-JEPA · Le-World-Model · Le-JEPA · TD-JEPA · ACT-JEPA

### World Models
Dream Dojo · Stable World Model · PEVA · PLDM · Hierarchical Puppeteer · Hunyuan World 1.5 · DIAMOND · Genie 2 · IRIS · DreamerV3 · DreamerV2 · DreamerV1

### VLA Models
Pi0.5 · Pi0.6 · Pi0 · LeVERB · GR00T · Gemini Robotics · Octo · OpenVLA · RT-2

### Video Generation / Planning
Learning Latent Action World Models In The Wild · NVIDIA Cosmos · UniPi · UniSim

### Robotics
Eureka

## Vault structure

```
├── Papers/           # 34 paper nodes with embedded PDFs
├── Metrics/          # 64 metric definitions (Success Rate, LPIPS, FVD, ...)
├── Datasets/         # 78 dataset descriptions (ImageNet, DROID, DMC, ...)
├── PDFs/             # Arxiv PDFs for inline viewing
├── Canvases/         # Obsidian canvas with paper relationship graph
├── Templates/        # Paper, metric, and dataset templates
├── MOC.md            # Map of Content (main index)
├── Metrics Index.md  # All metrics by category
└── Datasets Index.md # All datasets by category
```

## How it works

- **Obsidian vault** — open this repo as a vault in [Obsidian](https://obsidian.md) for the full experience (graph view, backlinks, hover previews, PDF viewer)
- **Web app** — hosted on AWS (S3 + CloudFront) via [Quartz](https://quartz.jzhao.xyz), built automatically on push
- **Inline links** — metrics, datasets, and papers are `[[wikilinked]]` directly in tables and text, not just listed at the bottom
- **Graph view** — shows paper-to-paper connections (depth 2, local graph), excluding metrics and datasets for clarity

## Auto-deploy

Every push to `main` triggers a GitHub Action that:

1. Builds the vault into a static site with Quartz v4
2. Converts `![[PDF]]` embeds to `<iframe>` tags
3. Syncs to S3 and invalidates the CloudFront cache

Authentication uses GitHub OIDC federation (no static AWS keys).

## Adding a paper

1. Create `Papers/Paper Name.md` using the template in `Templates/Paper Template.md`
2. Download the PDF to `PDFs/Paper Name.pdf`
3. Add `![[PDFs/Paper Name.pdf]]` after the frontmatter
4. Use `[[Metric Name]]` and `[[Dataset Name]]` to link to existing nodes
5. Add the paper to `MOC.md` (ordered by year, most recent first)
6. Push to `main` — the site rebuilds automatically

## Graph view colors (Obsidian)

| Color | Tag |
|-------|-----|
| Cyan | `#jepa` |
| Red | `#world-model` |
| Green | `#vla` |
| Yellow | `#video-planning` |
| Magenta | `#metric` |
| Blue | `#dataset` |
