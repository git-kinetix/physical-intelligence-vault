# Physical Intelligence Vault

A research knowledge base covering **60 papers** on physical intelligence — world models, joint-embedding architectures, vision-language-action models, physics-based character control, and video generation for planning.

**Live site:** [dxlrak3ky5x8b.cloudfront.net](https://dxlrak3ky5x8b.cloudfront.net)

## What's inside

| Content | Count |
|---------|-------|
| Papers | 60 |
| Embedded PDFs | 55 |
| Metric definitions | 64 |
| Dataset descriptions | 78 |
| Interactive explainers | 10 |

Every paper node includes a summary, architecture breakdown, reproduced results tables (with inline-linked metrics and datasets), and related paper connections.

## Papers by group

### JEPA Family
Le-World-Model · V-JEPA 2.1 · ACT-JEPA · Embodied AI Agents Modeling the World · JEPA-WMs · Le-JEPA · TD-JEPA · V-JEPA 2 · V-JEPA · I-JEPA

### World Models
Dream Dojo · Stable World Model · Hunyuan World 1.5 · PEVA · PLDM · DIAMOND · DINO-WM · Genie 2 · TD-MPC2 · DreamerV3 · Habitat 3.0 · IRIS · DreamerV2 · DreamerV1 · World Models

### Character Animation
CLoSD · LeVERB · PARC · Hierarchical Puppeteer · MaskedMimic · SuperPADL · CALM · MuscleVAE · Vid2Player3D · ASE · ControlVAE · PADL · PhysicsVAE · AMP · MVAE · MCP · DeepMimic · SFV · DeepLoco

### VLA Models
GR00T · Gemini Robotics · Pi0.5 · Pi0.6 · Octo · OpenVLA · Pi0 · ACT · RT-2

### Video Generation / Planning
Learning Latent Action World Models In The Wild · NVIDIA Cosmos · UniPi · UniSim

### Sim-to-Real & Reward Design
Eureka · Learning Agile Robotic Locomotion · Sim-to-Real Transfer

## Vault structure

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
