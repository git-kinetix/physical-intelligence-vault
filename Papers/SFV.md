---
tags: [paper, world-model, physics-simulation]
title: "SFV: Reinforcement Learning of Physical Skills from Videos"
authors: [Xue Bin Peng, Angjoo Kanazawa, Jitendra Malik, Pieter Abbeel, Sergey Levine]
year: 2018
arxiv: "https://arxiv.org/abs/1810.03599"
repo: "https://github.com/akanazawa/motion_reconstruction"
group: "World Models"
importance: 
aliases: [SFV, Skills from Videos, Reinforcement Learning of Physical Skills from Videos]
---

![[PDFs/SFV.pdf]]

# SFV: Reinforcement Learning of Physical Skills from Videos

## Summary
SFV (Skills from Videos) presents a three-stage framework that enables physically simulated characters to learn motor skills directly from monocular video, eliminating the dependence on motion capture data that constrained prior work like [[DeepMimic]]. The key insight is that recent advances in deep pose estimation (OpenPose for 2D, HMR for 3D) can extract sufficiently accurate reference motions from ordinary video clips -- including YouTube videos -- which can then be refined and used as imitation targets for physics-based reinforcement learning. This opens the door to leveraging the vast abundance of publicly available video on the web as a source of motion data for character animation.

The framework operates in three stages: (1) pose estimation, where OpenPose predicts 2D joint positions and HMR (Human Mesh Recovery) predicts 3D joint rotations in axis-angle form from each video frame; (2) motion reconstruction, where an optimization in HMR's latent space consolidates per-frame predictions into a temporally smooth 3D kinematic trajectory that reconciles 2D and 3D predictions while enforcing physical consistency; and (3) motion imitation, where a simulated character is trained via PPO to reproduce the reconstructed reference motion using a [[DeepMimic]]-style multi-component imitation reward. A critical innovation is Adaptive State Initialization (ASI), which dynamically adjusts the initial state distribution during RL training based on the agent's current performance along the reference trajectory, substantially outperforming both fixed and uniform (RSI) initialization strategies.

Published at SIGGRAPH Asia 2018 (ACM Transactions on Graphics, Vol. 37, No. 6) by UC Berkeley researchers, SFV demonstrated over 20 dynamic skills learned from video clips including backflips, cartwheels, frontflips, handsprings, kicks, spins, dance moves (Gangnam Style), and vaulting. The learned controllers also generalize to perturbation recovery, irregular terrain traversal, and morphology retargeting (Atlas robot), establishing video as a viable alternative to motion capture for physics-based animation.

## Key Contributions
- Introduces the first complete pipeline for learning physics-based character skills from monocular video rather than motion capture data, bridging computer vision and physics-based animation
- Proposes a motion reconstruction optimization stage that operates in HMR's latent space to produce temporally smooth, physically consistent reference trajectories from noisy per-frame pose estimates
- Introduces Adaptive State Initialization (ASI), which dynamically adjusts the initial state distribution during RL training by sampling from states where the policy currently transitions from success to failure, outperforming both fixed and reference state initialization
- Demonstrates that rotation-augmented pose estimator fine-tuning is critical for predicting inverted poses (backflips, handsprings) that standard pose estimators fail on
- Shows successful imitation of over 20 dynamic skills from video clips including acrobatics, martial arts, dance, and locomotion, with transfer to the Atlas robot morphology

## Architecture / Method
The SFV framework consists of three sequential stages: pose estimation, motion reconstruction, and motion imitation.

**Stage 1: Pose Estimation**
- 2D joint detection: OpenPose (fine-tuned with rotation augmentation for inverted poses)
- 3D pose/shape estimation: HMR (Human Mesh Recovery) predicting SMPL body model parameters (axis-angle joint rotations)
- Rotation augmentation: Training data augmented with random rotations so pose estimators can handle upside-down frames (critical for acrobatic skills)
- Per-frame predictions are noisy and temporally inconsistent

**Stage 2: Motion Reconstruction**
- Optimization in HMR's latent encoding space (not raw joint angles)
- Objective: minimize discrepancy between predicted and reconstructed poses while enforcing:
  - 2D reprojection consistency with OpenPose detections
  - 3D pose consistency with HMR predictions
  - Temporal smoothness between adjacent frames
- Produces a clean kinematic trajectory suitable as an RL reference motion
- Mitigates jitter, foot sliding, and physically impossible poses from raw estimation

**Stage 3: Motion Imitation**
- Physics engine: Bullet at 1.2 kHz simulation frequency
- Control frequency: 30 Hz via PD controllers at each joint
- RL algorithm: Proximal Policy Optimization (PPO)
- Policy network: 2 fully-connected hidden layers with 1024 and 512 units, ReLU activations
- Value network: Same architecture with single scalar output
- Character: Humanoid with 12 joints, 45 kg mass, 1.62 m height; spherical joints (3-DOF) except elbows/knees (1-DOF revolute); 197D state space, 36D action space
- Atlas robot: 169.5 kg, 1.82 m height, same joint structure
- Episode horizon: 20 seconds for cyclic skills
- Training: approximately 150 million samples, ~1 day on 16-core machine

**Adaptive State Initialization (ASI):**
- Maintains a distribution over reference trajectory states, sampling initial states from positions where the policy currently transitions from successful to unsuccessful tracking
- Focuses training effort on the most challenging portions of the reference motion
- Dynamically shifts as the policy improves, eventually covering the full trajectory

**Reward Function:**
Same [[DeepMimic]]-style multi-component imitation reward combining:
- Joint pose matching (quaternion differences)
- Joint velocity matching
- End-effector position matching
- Center-of-mass matching

## Results

### Table 1: Video-Based Motion Imitation Performance (Humanoid)
| Skill | Duration (s) | Samples (M) | Normalized Return |
|-------|:------------:|:------------:|:-----------------:|
| Walk | 0.87 | 122 | 0.932 |
| Run | 0.73 | 126 | 0.878 |
| Cartwheel A | 2.97 | 136 | 0.824 |
| Backflip A | 2.13 | 146 | 0.741 |
| Frontflip | 1.57 | 126 | 0.708 |
| Handspring A | 1.83 | 155 | 0.696 |
| Kick | 1.27 | 158 | 0.761 |
| Push | 1.10 | 225 | 0.487 |

Locomotion skills (Walk: 0.932, Run: 0.878) achieve the highest fidelity, while highly dynamic acrobatic skills are more challenging (Frontflip: 0.708, Push: 0.487). The Push task involves object interaction and is the most difficult. Sample requirements range from 122M (Walk) to 225M (Push), with complex skills generally needing more training.

### Table 2: Ablation — State Initialization Strategy (Humanoid)
| Skill | Fixed (FSI) | Reference (RSI) | Adaptive (ASI) |
|-------|:-----------:|:---------------:|:--------------:|
| Walk | 0.435 | 0.738 | 0.932 |
| Cartwheel A | 0.122 | 0.602 | 0.824 |
| Backflip A | 0.086 | 0.687 | 0.741 |
| Frontflip | 0.180 | 0.615 | 0.708 |

ASI substantially outperforms both fixed state initialization (FSI) and reference state initialization (RSI, from [[DeepMimic]]) across all skills. The improvement is most dramatic for Walk (0.435 -> 0.932) and Cartwheel (0.122 -> 0.824), where FSI fails almost completely. ASI's advantage comes from dynamically focusing training on the hardest portions of the trajectory.

### Table 3: Motion Reconstruction Ablation (Handspring, RSI)
| Condition | Normalized Return |
|-----------|:-----------------:|
| Without Motion Reconstruction | 0.391 |
| With Motion Reconstruction | 0.464 |

The motion reconstruction optimization stage provides a meaningful improvement (+0.073) by smoothing noisy pose estimates into physically consistent reference trajectories, though the full ASI initialization strategy provides a larger boost.

### Atlas Robot Transfer
| Skill | Normalized Return |
|-------|:-----------------:|
| Walk | 0.926 |
| Backflip A | 0.318 |

Skills transfer to the Atlas robot morphology (169.5 kg, much heavier than the 45 kg humanoid). Locomotion transfers well (Walk: 0.926) but highly dynamic skills degrade substantially (Backflip: 0.318) due to the significant mass and proportion differences.

## Metrics Used
- [[Episode Return]] — normalized cumulative imitation reward (0-1 scale) used as the primary performance metric across all skills and ablations
- [[Motion Naturalness]] — qualitative assessment via video demonstrations; the multi-component imitation reward serves as a quantitative proxy
- Normalized Return — same as [[Episode Return]], normalized to [0, 1] range for comparability across skills of different duration

## Datasets Used
- YouTube video clips — monocular videos of human performers executing acrobatics, martial arts, dance, and locomotion; the primary innovation is using web video rather than motion capture
- OpenPose training data — augmented with random rotations to handle inverted poses
- HMR pre-trained model — used for 3D pose/shape estimation with SMPL body model

## Related Papers
- [[DeepMimic]] — direct predecessor by the same lead author; SFV extends [[DeepMimic]]'s motion imitation framework from motion capture to video input, reusing the same reward function and PPO training but adding pose estimation and motion reconstruction stages
- [[DeepLoco]] — earlier hierarchical locomotion work by Peng and van de Panne; SFV focuses on single-skill imitation from video rather than hierarchical terrain-aware locomotion
- [[MCP]] — subsequent work by Peng that composes skills (potentially learned from video) into complex behaviors via multiplicative primitives
- [[ASE]] — scales motion imitation to large datasets with adversarial skill embeddings; SFV's video-based motion extraction could provide training data for [[ASE]]-style systems
- [[Vid2Player3D]] — applies video-based skill learning to sports (tennis from broadcast video), extending SFV's core insight that video can replace motion capture for physics-based animation
- [[MVAE]] — VAE-based motion modeling from motion capture; SFV bypasses the need for MoCap entirely by extracting motion from video
- [[Hierarchical Puppeteer]] — combines visual observations with motion tracking; SFV's pose estimation stage is conceptually related to the visual processing in [[Hierarchical Puppeteer|Puppeteer]]'s high-level controller
