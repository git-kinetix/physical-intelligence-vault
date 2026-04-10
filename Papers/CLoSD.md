---
tags: [paper, world-model, physics-simulation]
title: "CLoSD: Closing the Loop between Simulation and Diffusion for Multi-Task Character Control"
authors: [Guy Tevet, Sigal Raab, Setareh Cohan, Daniele Reda, Zhengyi Luo, Xue Bin Peng, Amit H. Bermano, Michiel van de Panne]
year: 2025
arxiv: "https://arxiv.org/abs/2410.03441"
repo: "https://github.com/GuyTevet/CLoSD"
group: "World Models"
importance: 
aliases: [CLoSD, Closing the Loop between Simulation and Diffusion]
---

![[PDFs/CLoSD.pdf]]

# CLoSD: Closing the Loop between Simulation and Diffusion for Multi-Task Character Control

## Summary

CLoSD introduces a closed-loop framework that combines motion diffusion models with physics-based simulation for multi-task character control, published as an ICLR 2025 Spotlight paper. The key insight is that motion diffusion models and physics-based RL controllers have complementary strengths: diffusion models generate diverse, semantically rich motion plans from text but lack physical awareness, while RL tracking controllers produce physically plausible motion but struggle with generation errors and long-horizon planning. CLoSD unifies both by maintaining a continuous feedback loop between a Diffusion Planner (DiP) and a robust tracking controller.

The Diffusion Planner is a fast autoregressive diffusion model built on a transformer decoder architecture that generates short motion plans (40 frames) conditioned on text prompts, target locations, and the current character state. The tracking controller is based on PHC (Perpetual Humanoid Control), a single-primitive RL policy trained on the AMASS dataset. Crucially, the planner continuously receives feedback about the actual executed motion from the physics simulation, allowing it to adapt its plans in real time. This closed-loop interaction enables the system to handle multi-task scenarios including goal-directed navigation, object striking (with semantic awareness of which body part to use), sitting, and getting up from seated positions.

CLoSD achieves strong results across all evaluated tasks while maintaining text-motion semantic alignment (FID of 0.28 on HumanML3D) and near-perfect physical plausibility (ground penetration of only 0.022 mm, foot skating of 0.002). The diffusion planner operates at 3,500 fps (175x real-time), making the entire system suitable for interactive applications. CLoSD substantially outperforms baselines on tasks requiring physical interaction, such as object striking (0.9 vs 0.02 for UniHSI) and getting up (0.98 vs 0.08 for UniHSI).

## Key Contributions

- Proposes a closed-loop architecture coupling a fast autoregressive diffusion planner with a physics-based tracking controller, where simulation feedback continuously informs future motion plans
- Introduces DiP (Diffusion Planner), a real-time autoregressive diffusion model generating 40-frame motion plans at 3,500 fps (175x real-time) using only 10 diffusion steps
- Achieves state-of-the-art physical plausibility: 0.022 mm ground penetration and 0.002 foot skating ratio, dramatically lower than kinematic baselines
- Demonstrates multi-task character control spanning navigation, semantic object interaction, sitting, and getting up, all from text commands
- Maintains competitive text-motion alignment (FID 0.28 on HumanML3D) while operating in physics simulation with an SMPL-compatible humanoid

## Architecture / Method

**Diffusion Planner (DiP):**
- 8-layer transformer decoder with 512-dimensional latent space and 4 attention heads
- Text encoder: Frozen DistilBERT
- Input: text prompt, target location, prefix of 20 frames (executed motion feedback from simulation)
- Output: 40 frames of future motion plan
- 10 diffusion steps (reduced from 50 in standard MDM) for real-time performance
- Generates 22 seconds of reference motion in 11.4 ms (3,500 fps)
- Classifier-free guidance scale: 7.5 (tasks), 2.5 (closed-loop), 5.0 (text-to-motion)
- Training: 600K diffusion steps on NVIDIA RTX 3090, optimal checkpoint at 200K steps

**Tracking Controller:**
- Based on PHC (Perpetual Humanoid Control) single-primitive policy
- Pre-trained on AMASS dataset for 62K PPO epochs
- Fine-tuned for 4K additional epochs in closed-loop with DiP
- PD controller for humanoid actuation
- Training: 3,072 parallel environments on NVIDIA A100 GPU
- Humanoid: SMPL-compatible with 24 joints

**Closed-Loop Interaction:**
- DiP generates a 40-frame motion plan from text + target + current state
- The tracking controller executes the plan frame-by-frame in physics simulation
- After the plan is consumed, the last 20 executed frames are fed back to DiP as the new prefix
- This feedback loop allows DiP to correct for tracking errors, environmental constraints, and physical interactions
- The system naturally handles multi-task sequences by changing text prompts between planning steps

## Results

### Table 1: Multi-Task Success Rates

| Task | CLoSD | UniHSI | Open-Loop |
|------|-------|--------|-----------|
| Goal reaching | **1.00** | 0.96 | **1.00** |
| Object striking | **0.90** | 0.02 | 0.80 |
| Sitting | **0.88** | 0.85 | 0.19 |
| Getting up | **0.98** | 0.08 | 0.23 |

CLoSD achieves the highest success rates across all tasks. The advantage is most pronounced on tasks requiring physical interaction: object striking (0.90 vs 0.02 for UniHSI) and getting up (0.98 vs 0.08), where the closed-loop feedback and semantic planning are critical.

### Table 2: DiP Ablation Study

| Configuration | R-[[Precision]] (top-3) | FID | Runtime (ms) | Speed (fps) |
|---------------|---------------------|-----|-------------|-------------|
| **10 steps (default)** | **0.78** | **0.28** | **11.4** | **3,500** |
| 5 steps | 0.76 | 0.32 | 6.1 | 6,600 |
| 20 steps | 0.80 | 0.28 | 23.0 | 1,700 |
| Np=40 (longer prefix) | 0.74 | 0.70 | 13.0 | 3,100 |
| Ng=20 (shorter generation) | 0.78 | 0.26 | 11.4 | 1,700 |
| Ng=80 (longer generation) | 0.74 | 1.18 | 16.0 | 5,000 |

The default configuration (10 diffusion steps, 20-frame prefix, 40-frame generation) balances quality and speed. Fewer steps trade slight quality loss for 2x speedup; longer generation windows degrade FID substantially.

### Table 3: Text-to-Motion Evaluation (HumanML3D)

| Metric | DiP (kinematic) | CLoSD (physics) | MoConVQ | MDM |
|--------|-----------------|-----------------|---------|-----|
| R-[[Precision]] (top-3) | 0.777 | 0.689 | 0.614 | 0.719 |
| FID | 0.28 | 0.28 | 3.279 | 0.423 |
| Ground penetration (mm) | 0.083 | **0.022** | 0.249 | 0.147 |
| Floating (mm) | 23.6 | **20.0** | 32.0 | 28.6 |
| Foot skating (mm) | 629e-3 | **0.002** | 294e-3 | 330e-3 |

CLoSD maintains the same FID as its kinematic DiP counterpart (0.28) while dramatically improving physical plausibility metrics. Ground penetration drops from 0.083 mm to 0.022 mm, and foot skating is reduced by over 300x (from 0.629 to 0.002), demonstrating the value of the physics simulation loop.

## Metrics Used

- [[Success Rate]] — task completion rate across goal reaching, object striking, sitting, and getting up
- R-[[Precision]] (top-3) — text-motion retrieval accuracy on HumanML3D
- FID (Frechet Inception Distance) — distributional similarity between generated and reference motions
- Ground penetration (mm) — physical plausibility metric measuring body-ground interpenetration
- Floating (mm) — distance of feet above ground during contact phases
- Foot skating (mm) — foot displacement during supposed ground contact phases
- [[Motion Naturalness]] — qualitative assessment of generated motion quality

## Datasets Used

- HumanML3D — text-to-motion benchmark used for evaluation of motion quality and text alignment
- AMASS — large-scale motion capture dataset used for training the PHC tracking controller

## Related Papers

- [[DeepMimic]] — foundational physics-based motion imitation; CLoSD's tracking controller follows this paradigm
- [[ASE]] — adversarial skill embeddings for physics-based characters; related approach to reusable motion skills
- [[CALM]] — conditional adversarial latent models; related controllable physics-based animation
- [[PADL]] — language-directed physics-based control using CLIP + adversarial RL; CLoSD offers an alternative via diffusion planning
- [[SuperPADL]] — scales [[PADL]] to thousands of motions; CLoSD takes a different approach using diffusion models as planners
- [[MaskedMimic]] — unified physics-based control through masked inpainting; complementary approach to multi-task control
