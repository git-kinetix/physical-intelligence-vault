# Physical Intelligence Vault

55 papers on physical intelligence. Use this to answer cross-paper questions.

## Groups at a glance

**JEPA (8):** I-JEPA→V-JEPA→V-JEPA 2→V-JEPA 2.1 (video SSL). Le-JEPA (stable SSL via SIGReg). Le-World-Model (JEPA world model for control). TD-JEPA (TD learning + JEPA for zero-shot RL). ACT-JEPA (JEPA for policy learning).

**World Models / RL (11):** DreamerV1→V2→V3 (latent imagination, RSSM). IRIS (transformer tokens for Atari). DIAMOND (diffusion world model). Genie 2 (generative environments). TD-MPC2 (scalable model-based RL, SimNorm, MPPI planning). PLDM (reward-free latent planning). Stable World Model (benchmarking framework). Hunyuan World 1.5 (3D-consistent video WM). Dream Dojo (robot WM from human video).

**Character Animation — Adversarial (13, mostly Xue Bin Peng):** DeepLoco (2017, hierarchical locomotion) → DeepMimic (2018, motion imitation via RL) → SFV (2018, skills from video) → MCP (2019, compositional policies) → AMP (2021, adversarial motion priors — pivotal paper) → ASE (2022, skill embeddings at scale) → PADL (2022, language-directed) → CALM (2023, conditional adversarial) → Vid2Player3D (2023, tennis from broadcast) → SuperPADL (2024, scaled language control) → MaskedMimic (2024, unified inpainting) → PARC (2025, physics augmentation) → CLoSD (2025, diffusion + simulation loop).

**Character Animation — VAE (4):** MVAE (2020, latent action space, MoE decoder) → PhysicsVAE (2022, conditional prior) → ControlVAE (2022, learned world model) → MuscleVAE (2023, muscle actuation + fatigue).

**Humanoid Whole-Body:** Hierarchical Puppeteer (hierarchical visual humanoid control). LeVERB (language-conditioned humanoid via latent codes).

**VLA / Imitation Learning (9):** ACT (2023, action chunking + ALOHA). RT-2 (2023, VLM→VLA transfer). Octo (2024, open-source generalist). OpenVLA (2024, 7B open-source). Pi0 (2024, flow matching VLA) → Pi0.5 (heterogeneous co-training) → Pi0.6 (RL from experience). GR00T (2025, NVIDIA humanoid VLA). Gemini Robotics (2025, Gemini 2.0 for robots).

**Video Generation / Planning (5):** UniPi (video as planning). UniSim (neural simulator). NVIDIA Cosmos (world foundation model). PEVA (egocentric video prediction). Learning Latent Action WMs (latent actions from internet video).

**Sim-to-Real (3):** Sim-to-Real Transfer (dynamics randomization). Learning Agile Locomotion (quadruped from animal MoCap, RSS Best Paper). Eureka (LLM reward design).

## Key relationships

- AMP is the pivotal paper bridging DeepMimic→ASE/CALM/MaskedMimic (replaced hand-crafted rewards with learned discriminator)
- VAE vs Adversarial: two competing approaches to learning motor skills from MoCap. VAE gives smooth interpolation; adversarial scales better to diverse data
- Pi0 uses flow matching (like diffusion but ODE-based), ACT uses CVAE — both do action chunking
- V-JEPA 2-AC and Le-World-Model both do latent-space planning but V-JEPA 2-AC uses frozen features while LeWM trains end-to-end
- TD-MPC2 and DreamerV3 are the two main model-based RL approaches (MPC planning vs imagination)
- TD-JEPA combines TD-MPC2's TD learning with JEPA representations for zero-shot transfer

## Vault structure

- `Papers/` — 55 paper nodes with frontmatter (tags, year, arxiv, repo, importance, group)
- `Metrics/` — 64 metric definitions (Success Rate, LPIPS, Episode Return, etc.)
- `Datasets/` — 78 dataset descriptions (DMC, ImageNet, DROID, CMU MoCap, etc.)
- `Explainers/` — 5 interactive distill-style explainers (Le-World-Model, MVAE, Le-JEPA, TD-JEPA, TD-MPC2)
- `MOC.md` — main index organized by group
- Tags: `physics-simulation` (uses physics engine) vs `motion` (video/kinematic)

## Web app

- Site: https://dxlrak3ky5x8b.cloudfront.net
- Backend: DynamoDB API at https://zu6qahfn14.execute-api.eu-west-3.amazonaws.com (stores starred/read-by state)
- Built with Quartz v4, customized site repo at git-kinetix/physical-intelligence-site
