# Physical Intelligence Vault

56 papers on physical intelligence. Use this to answer cross-paper questions.

## Groups at a glance

**JEPA Family (9):** Le-World-Model, V-JEPA 2.1, ACT-JEPA, JEPA-WMs, Le-JEPA, TD-JEPA, V-JEPA 2, V-JEPA, I-JEPA
**World Models (12):** Dream Dojo, Stable World Model, Hunyuan World 1.5, PEVA, PLDM, DIAMOND, Genie 2, TD-MPC2, DreamerV3, IRIS, DreamerV2, DreamerV1
**Character Animation (19):** CLoSD, LeVERB, PARC, Hierarchical Puppeteer, MaskedMimic, SuperPADL, CALM, MuscleVAE, Vid2Player3D, ASE, ControlVAE, PADL, PhysicsVAE, AMP, MVAE, MCP, DeepMimic, SFV, DeepLoco
**VLA Models (9):** GR00T, Gemini Robotics, Pi0.5, Pi0.6, Octo, OpenVLA, Pi0, ACT, RT-2
**Video Generation / Planning (4):** Learning Latent Action World Models In The Wild, NVIDIA Cosmos, UniPi, UniSim
**Sim-to-Real & Reward Design (3):** Eureka, Learning Agile Robotic Locomotion, Sim-to-Real Transfer

## Key relationships

- AMP is the pivotal paper bridging DeepMimic→ASE/CALM/MaskedMimic (replaced hand-crafted rewards with learned discriminator)
- VAE vs Adversarial: two competing approaches to learning motor skills from MoCap. VAE gives smooth interpolation; adversarial scales better to diverse data
- Pi0 uses flow matching (like diffusion but ODE-based), ACT uses CVAE — both do action chunking
- V-JEPA 2-AC and Le-World-Model both do latent-space planning but V-JEPA 2-AC uses frozen features while LeWM trains end-to-end
- TD-MPC2 and DreamerV3 are the two main model-based RL approaches (MPC planning vs imagination)
- TD-JEPA combines TD-MPC2's TD learning with JEPA representations for zero-shot transfer

## Vault structure

- `Papers/` — 56 paper nodes with frontmatter (tags, year, arxiv, repo, importance, group)
- `Metrics/` — 64 metric definitions
- `Datasets/` — 78 dataset descriptions
- `Explainers/` — 10 interactive distill-style explainers
- `MOC.md` — main index organized by group
- Tags: `physics-simulation` (uses physics engine) vs `motion` (video/kinematic)

## Web app

- Site: https://dxlrak3ky5x8b.cloudfront.net
- Backend: DynamoDB API at https://zu6qahfn14.execute-api.eu-west-3.amazonaws.com (stores starred/read-by state)
- Built with Quartz v4, customized site repo at git-kinetix/physical-intelligence-site
