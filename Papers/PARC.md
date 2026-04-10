---
tags: [paper, world-model, physics-simulation]
title: "PARC: Physics-based Augmentation with Reinforcement Learning for Character Controllers"
authors: [Michael Xu, Yi Shi, KangKang Yin, Xue Bin Peng]
year: 2025
arxiv: "https://arxiv.org/abs/2505.04002"
repo: "https://github.com/mshoe/PARC"
group: "World Models"
importance: 
aliases: [PARC, Physics-based Augmentation with RL for Character Controllers]
---

!PDFs/PARC.pdf

# PARC: Physics-based Augmentation with Reinforcement Learning for Character Controllers

## Summary
PARC introduces an iterative framework that jointly trains a kinematic motion generator and a physics-based tracking controller to progressively expand both the diversity of a motion dataset and the capabilities of terrain traversal controllers. Starting from a small initial parkour motion capture dataset (approximately 14 minutes), the system uses a diffusion-based motion generator to synthesize new motions for unseen terrains, then deploys a reinforcement learning tracking controller in Isaac Gym to execute and physically correct those motions, and finally feeds the corrected motions back into the dataset to retrain the generator. This self-augmenting loop bridges the scarcity of terrain-traversal motion data with the need for versatile character controllers.

The motion generator is a transformer-encoder-based diffusion model conditioned on local terrain heightmaps and target direction. It produces full-body kinematic motion sequences including root position/rotation, joint rotations/positions, and contact labels. The tracking controller follows the [[DeepMimic]] paradigm, using PPO in Isaac Gym at 120 Hz simulation with 30 Hz policy queries. Key technical contributions include a terrain penetration loss during diffusion training, blended denoising (mixing unconditional and conditional score estimates to balance diversity and terrain compliance), kinematic optimization for post-generation refinement, and prioritized state initialization for the tracker. Over four iterations, the framework dramatically improves both generator quality and tracker success rate, producing complex parkour behaviors such as climbing, vaulting, and jumping across diverse procedural and hand-designed terrains.

Published at SIGGRAPH 2025, this work from Simon Fraser University and NVIDIA demonstrates a practical pipeline for scaling physics-based character animation beyond the limits of available motion capture data.

## Key Contributions
- Proposes an iterative self-augmenting framework where a diffusion-based motion generator and a physics-based tracking controller mutually improve each other across training rounds
- Demonstrates that physics-based correction of kinematic artifacts (penetrations, floating, jerk) produces higher-quality synthetic data than uncorrected kinematic generation alone
- Introduces blended denoising for terrain-conditioned diffusion, mixing unconditional and conditional score estimates to balance motion diversity with terrain compliance
- Shows progressive improvement across four iterations: tracker success rate rises from 27% to 68%, and generator terrain penetration drops by two orders of magnitude
- Enables agile terrain traversal (parkour) from only ~14 minutes of initial motion capture data by iteratively generating and correcting motions for increasingly complex terrains

## Architecture / Method
PARC consists of two alternating components trained in an iterative loop:

**Motion Generator (Diffusion Model):**
- Architecture: Transformer encoder backbone operating on per-frame tokens
- Conditioning: Local terrain heightmap (sampled around the character root) and a target travel direction
- Output: Full kinematic motion sequence including root position/rotation, joint rotations/positions, and binary contact labels per foot
- Training losses: Standard diffusion denoising loss plus a terrain penetration loss that penalizes generated joint positions below the terrain surface
- Inference technique: Blended denoising with coefficient s=0.65, mixing unconditional denoising (s=0, more diverse but terrain-ignoring) with fully conditional denoising (s=1, terrain-compliant but higher jerk), followed by kinematic optimization that refines generated motions via gradient-based post-processing

**Tracking Controller (RL Policy):**
- Framework: [[DeepMimic]]-style imitation learning using PPO
- Simulator: Isaac Gym at 120 Hz simulation frequency, 30 Hz policy query
- Objective: Track the kinematic reference motion in physics simulation, correcting artifacts such as terrain penetrations, floating feet, and unphysical jerk
- Technique: Prioritized state initialization that biases episode start states toward difficult segments where the tracker previously failed, improving convergence on challenging terrain transitions

**Iterative Loop:**
1. Train motion generator on current dataset
2. Generate synthetic motions for new terrain configurations
3. Train tracking controller to imitate generated motions in physics simulation
4. Collect corrected (physically valid) motions from successful tracking episodes
5. Add corrected motions to the dataset; repeat from step 1

**Terrain Generation Strategies:**
- Iterations 1-2: Random boxes terrain generation
- Iterations 3-4: Random terrain slices from a 100x100 manually designed terrain
- Evaluation: Random walk terrain generation producing 100 test terrains

## Results

### Table 1: Motion Generator Performance Across PARC Iterations
| Iteration | FWD ↓ | TPL ↓ | TCL ↓ | %HJF ↓ |
|-----------|-------|-------|-------|---------|
| 1 | 1.908 | 2093 | 114.1 | 10.70 |
| 2 | 1.586 | 705.5 | 9.761 | 4.387 |
| 3 | 0.747 | 448.2 | 8.070 | 3.238 |
| 4 | 0.596 | 179.6 | 9.763 | 2.730 |
| No physics correction | 1.572 | 547.3 | 17.44 | 18.68 |

Across four iterations, the motion generator improves substantially on all metrics. Final Waypoint Distance (FWD) drops from 1.908 to 0.596, indicating the generator increasingly produces motions that successfully traverse terrains end-to-end. Terrain Penetration Loss (TPL) decreases by over an order of magnitude from 2093 to 179.6, demonstrating the physics correction loop's effectiveness at eliminating ground intersections. The "no physics correction" ablation (training on uncorrected kinematic data from iteration 1) shows substantially worse TPL and %HJF, confirming that the physics-based correction is essential for producing clean training data.

### Table 2: Motion Tracker Performance Across Iterations
| Iteration | [[Success Rate]] (%) ↑ | Joint Tracking Error (m) ↓ |
|-----------|-------------------|---------------------------|
| 1 | 27 | 0.08294 |
| 2 | 44 | 0.05851 |
| 3 | 60 | 0.05321 |
| 4 | 68 | 0.05167 |

The tracker's success rate more than doubles from iteration 1 (27%) to iteration 4 (68%), while joint tracking error steadily decreases. This improvement is driven by two factors: the generator produces cleaner, more physically plausible reference motions as iterations progress, and the tracker itself benefits from re-initialization with the prior iteration's weights plus training on the expanded dataset.

### Table 3: Blended Denoising Coefficient Analysis (Iteration 4)
| Blending Coefficient (s) | FWD ↓ | TPL ↓ | TCL ↓ | %HJF ↓ |
|--------------------------|-------|-------|-------|---------|
| 0 | 0.908 | 40796 | 185.3 | 1.479 |
| 0.25 | 0.776 | 7411 | 44.93 | 1.113 |
| 0.5 | 0.571 | 4872 | 32.58 | 1.017 |
| 0.65 | 0.596 | 179.6 | 9.763 | 2.730 |
| 0.75 | 0.574 | 132.2 | 7.718 | 8.434 |
| 1 | 0.537 | 129.8 | 6.751 | 54.82 |

The blending coefficient s controls the trade-off between diversity and terrain compliance. At s=0 (fully unconditional), motions are smooth (low %HJF of 1.479) but massively penetrate terrain (TPL of 40796). At s=1 (fully conditional), terrain compliance is excellent (TPL 129.8) but motions become extremely jerky (%HJF of 54.82). The chosen value of s=0.65 provides a practical sweet spot with strong terrain compliance (TPL 179.6), reasonable jerk (%HJF 2.730), and good waypoint accuracy (FWD 0.596).

## Metrics Used
- **Final Waypoint Distance (FWD)** — measures distance between the character's final root position and the target endpoint; lower indicates better terrain traversal completion
- **Terrain Penetration Loss (TPL)** — quantifies the extent of body part intersections with the ground surface; lower means fewer physically implausible ground penetrations
- **Terrain Contact Loss (TCL)** — measures consistency between generated contact labels and actual terrain contact; lower indicates better contact prediction
- **Percentage of High Jerk Frames (%HJF)** — fraction of frames exceeding the maximum joint jerk observed in the original mocap data (~11666 m/s^3); lower indicates smoother motion
- [[Success Rate]] — percentage of tracking episodes where the controller successfully reaches the final reference motion frame
- **Joint Tracking Error** — average Euclidean distance between simulated and reference joint positions during tracking

## Datasets Used
- **Parkour Motion Capture Dataset** — 14 minutes 7 seconds of initial mocap data covering vaulting, climbing, jumping, running on flat/bumpy ground, platforms, and stairs; 5.5 seconds sourced from Unreal Engine Game Animation Sample Project; terrains manually reconstructed and contact labels manually annotated
- **Terrain Variation Expansion** — 50 spatial variations per motion clip generated via heuristic terrain adaptation plus physics correction
- **Random Walk Test Terrains** — 100 procedurally generated evaluation terrains

## Related Papers
- [[DeepMimic]] — foundational framework for the tracking controller; PARC's RL-based tracker directly builds on [[DeepMimic]]'s reference state initialization and imitation reward
- [[ASE]] — adversarial skill embeddings for physics-based characters by the same senior author (Xue Bin Peng); PARC's iterative augmentation provides an alternative to [[ASE]]'s large-scale pre-training approach
- [[CALM]] — conditional adversarial latent models for directable characters; related GAN-based approach to motion generation that PARC replaces with diffusion models
- [[MaskedMimic]] — unified physics-based control via masked motion inpainting; cited as concurrent work on versatile physics-based character controllers
- [[MVAE]] — VAE-based motion generation and RL-based control; PARC extends the idea of learned motion priors but uses diffusion models and iterative physics correction instead of VAEs
- [[MuscleVAE]] — model-based controllers with muscle actuation; related work on combining learned motion models with physics-based simulation
