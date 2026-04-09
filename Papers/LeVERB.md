---
tags: [paper, vla]
title: "LeVERB: Humanoid Whole-Body Control with Latent Vision-Language Instruction"
authors: [Haoru Xue, Xiaoyu Huang, Dantong Niu, Qiayuan Liao, Thomas Kragerud, Jan Tommy Gravdahl, Xue Bin Peng, Guanya Shi, Trevor Darrell, Koushil Sreenath, Shankar Sastry]
year: 2025
arxiv: "https://arxiv.org/abs/2506.13751"
repo: ""
group: "VLA Models"
importance: 
aliases: [LeVERB, Latent Vision-Language Encoded Robot Behavior]
---

!PDFs/LeVERB.pdf

# LeVERB: Humanoid Whole-Body Control with Latent Vision-Language Instruction

## Summary

LeVERB introduces the first hierarchical latent instruction-following framework for humanoid vision-language whole-body control (WBC). Existing vision-language-action (VLA) systems assume an accurate low-level controller with hand-crafted action vocabularies (end-effector pose, root velocity), which confines them to quasi-static tasks and precludes the agile, dynamic whole-body behaviors required by humanoids. LeVERB addresses this through a dual-process hierarchy: a high-level vision-language policy (System 2, LeVERB-VL) that learns a structured latent action vocabulary from synthetically rendered kinematic demonstrations using a residual CVAE, and a low-level reinforcement-learned whole-body control policy (System 1, LeVERB-A) that consumes these latent codes to generate dynamics-level joint commands at 50 Hz.

The paper also introduces LeVERB-Bench, the first sim-to-real-ready, vision-language, closed-loop benchmark for humanoid WBC, comprising over 150 tasks across 10 categories including visual navigation, locomotion, sitting, and reaching. LeVERB achieves a 58.5% overall success rate, outperforming naive hierarchical whole-body VLA implementations by 7.8x, and demonstrates zero-shot sim-to-real transfer on a Unitree G1 humanoid robot. A key design insight is the use of a gradient reversal discriminator that enforces modality-invariant latent representations, preventing train/test distribution mismatch between privileged trajectory encodings and vision-language-only inference.

## Key Contributions

- First vision-language whole-body control framework for humanoid robots with latent action vocabulary
- Introduces LeVERB-Bench: 154 unique trajectories across 10 task categories with photorealistic rendering (17.1 hours of data)
- Dual-process hierarchy: high-level CVAE-based vision-language policy (10 Hz) + low-level RL whole-body controller (50 Hz)
- Gradient reversal discriminator for modality-invariant latent space alignment between training (privileged) and inference (vision-language only)
- Zero-shot sim-to-real transfer demonstrated on Unitree G1 humanoid
- 7.8x improvement over naive hierarchical VLA baselines (58.5% vs ~7.5% success rate)
- Trained on only 154 rendered trajectories with visual randomization

## Architecture / Method

### System 2: LeVERB-VL (High-Level Vision-Language Policy)

A residual Conditional Variational Autoencoder (CVAE) that produces structured latent action codes from vision-language inputs.

**Components:**
- **Vision Encoder:** Frozen ViT-B/16 SigLiP producing 768-dim image features
- **Text Encoder:** SigLiP text encoder producing 768-dim language features
- **Transformer Backbone:** ViT-Base architecture (ablated from ViT-Tiny to ViT-Base)
- **Kinematics Encoder $E_\psi$:** MLP encoding future privileged states $s_{t+1:t+M}$ (available only during training)
- **Kinematics Decoder $D_\psi$:** MLP reconstructing future states from latent codes
- **Discriminator $f_\psi$:** Gradient Reversal Layer (GRL) enforcing modality-invariant latent representations
- **Latent Dimension:** 256-D

**Training Objective:**

$$\mathcal{L} = \mathcal{L}_{recon} + \beta_1 \mathcal{L}_{KL} + \beta_2 \mathcal{L}_{disc}$$

where $\mathcal{L}_{recon}$ is MSE trajectory reconstruction, $\mathcal{L}_{KL}$ ($\beta_1 = 0.1$) is KL divergence for distribution alignment, and $\mathcal{L}_{disc}$ ($\beta_2 = 5 \times 10^{-4}$) is adversarial classification via GRL ensuring the latent space cannot distinguish between privileged and vision-language-only inputs.

### System 1: LeVERB-A (Low-Level Whole-Body Control Policy)

**Teacher Policies $T_\xi$:**
- Trained with PPO on motion tracking rewards
- 3-layer MLP (512 → 256 → 128 hidden dims)
- Domain randomization for sim-to-real transfer
- Inputs: proprioceptive observations + reference motion commands

**Student Policy $\tau_{\theta_A}$:**
- Transformer-based: 2 layers, 4 attention heads, 128 hidden dim
- Trained via DAgger with Huber loss to imitate teacher policies
- Inputs: proprioceptive observations + latent code $z_t$ from LeVERB-VL
- Output: joint position delta actions at 50 Hz

**Execution Frequencies:**
- LeVERB-VL: 10 Hz (vision-language inference)
- LeVERB-A: 50 Hz (low-level control)
- Latent resampling: every 5 low-level steps (100 ms)

**Deployment:** System 1 runs onboard via ONNX runtime on CPU at 50 Hz; System 2 runs on external RTX 4090 GPU at ~10 Hz; communication via ROS2 topics.

## Results

### Table 1: LeVERB-Bench Task Distribution

| Category | # Motions | Total Duration [s] | Avg Duration [s] |
|----------|-----------|--------------------|--------------------|
| **Vision-Language Tasks** | | | |
| Navigation | 101 | 465.6 | 4.61 |
| — Towards | 80 | 372.0 | 4.65 |
| — Around | 21 | 93.6 | 4.46 |
| Locomotion | 20 | 64.4 | 3.22 |
| Sitting | 23 | 74.4 | 3.23 |
| Reaching | 10 | 17.4 | 1.74 |
| **VL Total** | **154** | **621.7** | **4.04** |
| **Language-Only Tasks** | | | |
| Locomotion | 399 | 1052.8 | 2.6 |
| Reaching | 61 | 101.6 | 1.7 |
| **Language Total** | **460** | **1154.5** | **2.5** |

LeVERB-Bench comprises 154 vision-language trajectories and 460 language-only trajectories totaling over 29 minutes of motion data. Navigation tasks dominate the VL split (101/154), reflecting the importance of visually-guided locomotion for humanoid robots.

### Table 2: LeVERB Performance and Ablation ([[Success Rate]] %)

| Task | LeVERB | ND | NE | NVL | NLS | NS |
|------|--------|----|----|-----|-----|-----|
| **Vision-Language Tasks** | | | | | | |
| VNF Objective | 80 | 75 | 75 | 15 | 0 | 0 |
| VNR Objective | 30 | 10 | 45 | 10 | 5 | 0 |
| VNF Distractor | 75 | 55 | 60 | 0 | 0 | 0 |
| VNR Distractor | 30 | 10 | 25 | 15 | 10 | 0 |
| VNF Cluttered | 50 | 5 | 25 | 15 | 5 | 0 |
| VNR Cluttered | 25 | 0 | 5 | 5 | 5 | 0 |
| VNS | 5 | 0 | 5 | 0 | 0 | 0 |
| **Language-Only Tasks** | | | | | | |
| Sit | 100 | 0 | 100 | 40 | 5 | 10 |
| Stand | 90 | 75 | 90 | 55 | 10 | 15 |
| Locomotion | 100 | 100 | 100 | 100 | 25 | 50 |
| **All (Average)** | **58.5** | **33.0** | **53.0** | **25.5** | **6.5** | **7.5** |

**Ablation Legend:** ND = No Discriminator; NE = No Kinematics Encoder; NVL = No Vision-Language Module; NLS = No Low-level Sampling; NS = No Sampling (deterministic). **Task Legend:** VNF = Visual Navigation Front; VNR = Visual Navigation Rear; VNS = Visual Navigation Sit.

The full LeVERB system achieves 58.5% average success rate. Removing the discriminator (ND) causes a 43% relative drop (33.0%), confirming the GRL is critical for bridging the train/test distribution gap. Removing vision-language (NVL) drops to 25.5%, with vision-dependent tasks (VNF/VNR) collapsing near 0-15%. The no-sampling ablations (NLS, NS) demonstrate that stochastic latent sampling is essential for robust execution.

### Table 3: Data Mixture Strategy

| Category | Count | % | Unique Traj | Description |
|----------|-------|---|-------------|-------------|
| **Total Demos** | **5,996** | **100%** | **614** | |
| Vision-Language | 3,696 | 61.6% | 154 | Rendered with images |
| Language Only | 2,300 | 38.4% | 460 | Kinematic only |
| **Environments (with Images)** | | | | |
| Brown Stone | 456 | 12.3% | 19 | Kitchens and living rooms |
| Living Room | 408 | 11.0% | 12 | Small living room |
| Modern House | 1,872 | 50.6% | 89 | Multi-room large house |
| Kitchens | 960 | 26.0% | 34 | Small kitchens |
| **Sources (without Images)** | | | | |
| Whole Body (AMASS) | 425 | 18.5% | 85 | Reaching and sitting |
| Walk (LAFAN) | 520 | 22.6% | 104 | Egocentric navigation |
| Run (LAFAN) | 1,115 | 48.5% | 219 | Running trajectories |
| RL Motions (In-House) | 240 | 10.4% | 52 | Egocentric trajectories |

The training data totals 5,996 demonstrations from 614 unique trajectories, with a 62/38 split between vision-language and language-only data. Visual data is rendered across 4 indoor environments with randomization, while language-only data draws from AMASS, LAFAN, and in-house RL motion sources.

### Table 4: Teacher Policy Reward Terms

| Reward Term | Weight | Formulation | σ |
|-------------|--------|-------------|---|
| Global Torso Position | 0.5 | $\exp(-\lVert\mathbf{p}_{motion} - \mathbf{p}_{robot}\rVert^2 / \sigma^2)$ | $\sqrt{0.25}$ |
| Global Torso Orientation | 0.3 | $\exp(-\text{quat\_error}^2 / \sigma^2)$ | $\sqrt{0.5}$ |
| Global Body Position | 0.5 | $\exp(-\lVert\mathbf{x}_{motion} - \mathbf{x}_{robot}\rVert^2 / \sigma^2)$ | $\sqrt{0.25}$ |
| Joint [[Tdist]] | -1.0 | $-\lVert\theta_{motion} - \theta_{robot}\rVert$ | — |
| Joint Velocity Error | -0.1 | $-\lVert\dot{\theta}_{motion} - \dot{\theta}_{robot}\rVert$ | — |
| Action Rate L2 | -0.001 | $-\lVert\mathbf{a}_t - \mathbf{a}_{t-1}\rVert^2$ | — |
| Joint Limit Violation | -100.0 | $-\mathbb{1}_{\text{violate\_limit}}$ | — |
| Termination Signal | -200.0 | $-\mathbb{1}_{\text{done}}$ | — |

The teacher policy reward function combines Gaussian-kernel tracking rewards (torso position/orientation, body position) with penalty terms for joint errors, action smoothness, joint limit violations, and early termination. Heavy penalties (-100, -200) on constraint violations ensure safe motion generation.

## Metrics Used

- [[Success Rate]] — primary metric; percentage of successful task completions over 20 evaluation runs per task/environment combination
- Trajectory Reconstruction Loss — MSE loss for CVAE objective measuring how well latent codes reconstruct future kinematic trajectories
- Validation Loss — used for System 2 transformer backbone architecture selection (ViT-Tiny to ViT-Base)

## Datasets Used

- LeVERB-Bench — custom benchmark with 154 vision-language tasks and 460 language-only tasks across 10 categories; 17.1 hours of photorealistic motion rollouts rendered via IsaacSim ray-tracing; 15,400 VL samples from 154 trajectories x 100 randomizations
- AMASS — large-scale human motion capture dataset; provides 85 unique whole-body reaching and sitting trajectories for language-only training
- LAFAN — locomotion and action dataset; provides 323 walk/run trajectories for language-only egocentric navigation training
- IsaacSim — NVIDIA simulation platform used for physics simulation, domain randomization, and photorealistic rendering of training environments

## Related Papers

- [[GR00T]] — NVIDIA humanoid foundation model; LeVERB addresses a similar humanoid control problem but with vision-language-conditioned latent actions rather than direct action prediction
- [[Pi0]] — VLA model; LeVERB extends the VLA paradigm to whole-body humanoid control with a hierarchical latent action space
- [[V-JEPA 2]] — self-supervised video model; LeVERB's vision encoder (SigLiP) and latent representation learning share conceptual parallels with JEPA's latent prediction
- [[V-JEPA 2.1]] — adds planning to [[V-JEPA]]; related to LeVERB's hierarchical planning through latent action codes
- [[DreamerV3]] — world model with latent dynamics; LeVERB's CVAE-based latent space relates to [[DreamerV3]]'s RSSM latent dynamics model
- [[Le-World-Model]] — JEPA-based world model; shares the idea of structured latent representations for embodied control
- [[Le-JEPA]] — theoretical JEPA foundations; LeVERB's latent representation learning benefits from similar principles of structured embedding spaces
