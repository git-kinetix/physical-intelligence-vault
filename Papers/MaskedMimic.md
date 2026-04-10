---
tags: [paper, domain/character-animation, method/masked-prediction, method/rl, lineage/peng]
title: "MaskedMimic: Unified Physics-Based Character Control Through Masked Motion Inpainting"
authors: [Chen Tessler, Yunrong Guo, Ofir Nabati, Gal Chechik, Xue Bin Peng]
year: 2024
arxiv: "https://arxiv.org/abs/2409.14393"
repo: "https://github.com/NVlabs/ProtoMotions"
group: "World Models"
venue: "SIGGRAPH Asia 2024"
domain: [character-animation]
method: [masked-prediction, rl]
lineage: [peng]
predecessor: ["[[CALM]]"]
importance: 4
aliases: [MaskedMimic, Masked Mimic]
---

!PDFs/MaskedMimic.pdf

# MaskedMimic: Unified Physics-Based Character Control Through Masked Motion Inpainting

## Summary
MaskedMimic introduces a single unified physics-based controller for simulated humanoids that reformulates character control as a general motion inpainting problem. Rather than training separate specialist policies for each control modality (motion tracking, VR tracking, text-conditioned generation, path following, object interaction), MaskedMimic trains one model to synthesize physically plausible motions from partial (masked) motion descriptions. By randomly masking subsets of joints, timesteps, and conditioning signals during training, the model learns to infer coherent full-body motion from any combination of sparse constraints.

The key insight is that diverse control tasks can all be expressed as partial motion specifications: VR tracking provides head and hand positions, path following constrains the pelvis trajectory, text commands describe high-level style, and keyframe animation specifies joint targets at particular times. MaskedMimic unifies all these modalities under a single masked conditioning framework, enabling seamless composition (e.g., text-stylized path following) and smooth transitions between tasks without task-specific reward engineering.

Published in ACM Transactions on Graphics (SIGGRAPH Asia 2024) by researchers at NVIDIA, Bar-Ilan University, and Simon Fraser University, MaskedMimic represents a significant advance in physics-based character animation. The fully-constrained controller reduces tracking failure rate by 62.5% compared to PHC+ on unseen motions, achieves 99.2% success rate on full-body tracking and 98.1% on VR tracking, and generalizes to irregular terrains and novel object interactions. The system is trained with approximately 30 billion environment steps over 2 weeks on 4 A100 GPUs using 16,384 parallel environments.

## Key Contributions
- Formulates physics-based character control as a unified motion inpainting problem, where a single model handles all control modalities (full-body tracking, sparse joint tracking, VR control, text commands, path following, object interaction) through masked conditioning
- Trains a single controller that subsumes and outperforms prior specialist methods: reduces PHC+ tracking failure rate by 62.5% on unseen motions while simultaneously supporting text, path, steering, reaching, and object interaction tasks
- Enables seamless composition of control modalities (e.g., text-conditioned path following, stylized steering) and smooth transitions between disparate tasks without explicit transition policies
- Demonstrates robust generalization to irregular terrains, unseen objects, and novel motion combinations not seen during training
- Introduces a scalable training methodology using prioritized motion sampling and progressive KL coefficient scheduling to handle the diversity of the AMASS motion capture dataset

## Architecture / Method
MaskedMimic builds on the motion tracking framework but fundamentally restructures how control signals are provided to the policy.

**Problem Formulation:**

Character control is cast as motion inpainting: given a partial motion description (some joints at some timesteps, possibly with text or scene context), the policy must synthesize a complete, physically valid motion that satisfies the given constraints. Training randomly masks different subsets of the available conditioning, forcing the model to learn robust inference from any partial specification.

**Two-Stage Training:**

1. **Fully-Constrained Controller (pi_FC):** First, a motion tracking policy is trained that receives full target keyframes for all joints. This stage uses approximately 30 billion steps (~2 weeks on 4 A100 GPUs) with 16,384 parallel environments. The policy learns to track diverse motions from the AMASS dataset across flat and irregular terrains.

2. **Partially-Constrained Controller (pi_PC):** The fully-constrained controller is then fine-tuned with random masking of joints and timesteps, plus additional conditioning modalities (text from HumanML3D, scene/object information from SAMP). This stage uses approximately 10 billion steps (~2 weeks). During training, random subsets of joints are masked, random future timesteps are dropped, and text/scene conditioning is randomly included or excluded.

**Conditioning Modalities:**

- **Keyframe conditioning:** Target joint positions/rotations at future timesteps, with random joint and temporal masking
- **Text conditioning:** Natural language motion descriptions from HumanML3D, encoded and provided as additional context
- **Scene conditioning:** Object geometry and interaction targets from the SAMP dataset
- **Combinations:** Any subset of the above can be composed at inference time

**Policy Architecture:**

The policy operates at 30 Hz control frequency with 120 Hz physics simulation. It outputs actions that drive the simulated character through PD control at each joint. The action covariance is fixed at sigma = exp(-2.9).

**Motion Tracking Reward:**

The reward function combines six weighted components:
- Global joint positions (gp)
- Global joint rotations (gr)
- Root height (rh)
- Joint velocities (jv)
- Joint angular velocities (jav)
- Energy penalty (eg)

**Early Termination:**

A trial is terminated if the average joint deviation exceeds 0.25 meters on flat terrain or 0.5 meters on irregular terrain.

**Training Details:**

- Prioritized motion sampling with minimum weight 3e-3 to ensure coverage of rare motions
- KL coefficient linearly increased from 0.0001 to 0.01 during training
- Data augmentation via motion mirroring (left-right flip)
- Conditioned joints: Left Ankle, Right Ankle, Pelvis, Head, Left Hand, Right Hand

## Results

### Table 1: Full-Body Motion Tracking on Flat Terrain

| Method | Train [[Success Rate]] (%) | Test [[Success Rate]] (%) |
|--------|:----------------------:|:---------------------:|
| PHC+ | — | — |
| MaskedMimic FC (ours) | ~99+ | 99.2 |

MaskedMimic's fully-constrained tracker (FC) achieves a 99.2% success rate on test motions from the AMASS dataset, reducing the tracking failure rate on unseen motions by 62.5% compared to PHC+. A trial is considered failed if at any frame the average joint deviation exceeds the threshold.

### Table 2: VR Tracking on Flat Terrain (Head + Hands)

| Method | Train MPOJPE (mm) | Test MPOJPE (mm) | [[Success Rate]] (%) |
|--------|:------------------:|:-----------------:|:----------------:|
| PULSE | Higher | Higher (overfits) | Lower |
| [[ASE]] | — | — | Lower |
| [[CALM]] | — | — | Lower |
| MaskedMimic (ours) | 39.5 | 45.8 | 98.1 |

Despite not being explicitly trained on VR tracking as a distinct task, MaskedMimic outperforms dedicated VR tracking methods (PULSE, [[ASE]], [[CALM]]) by a significant margin. PULSE exhibits more pronounced overfitting to training data, while MaskedMimic demonstrates superior generalization. MPOJPE measures tracking error on the observed joints (head, left hand, right hand), while full-body MPJPE measures reconstruction quality on all joints.

### Table 3: Joint Sparsity Analysis

| Conditioned Joints | Relative Difficulty |
|---|---|
| Feet only | Most challenging |
| Hands only | Less challenging than feet |
| Pelvis only | Less demanding than head/hands |
| Head only | Significant impact on full-body reconstruction |
| Head + Hands (VR setup) | Strong full-body inference |

The joint sparsity analysis reveals that conditioning on different joint subsets yields varying difficulty levels, with foot tracking being most challenging and head position having outsized influence on full-body motion inference.

### Table 4: Motion Tracking on Irregular Terrain

| Condition | Train [[Success Rate]] | Test [[Success Rate]] |
|---|:---:|:---:|
| Full-body tracking | >95% | >95% |
| VR tracking | >95% | >95% |

MaskedMimic exhibits similar success rates and tracking errors across both train and test sets on randomly generated irregular terrain, demonstrating robust generalization without terrain-specific training.

### Table 5: Goal-Conditioned Task Performance (5000 random episodes per task)

| Task | Modality | Description |
|---|---|---|
| Path Following | Pelvis constraints | Character follows waypoint trajectories; success if within 2m of goal |
| Steering | Pelvis constraints | Game-controller-like directional control across rough terrain and stairs |
| Reaching | Hand constraints | Hand target reaching with temporal specifications |
| Path + Text | Combined | Text-stylized path following (e.g., "walk while waving") |
| Object Interaction | Scene conditioning | Sitting, interacting with held-out objects 2-10m away |

### Table 6: Training Compute

| Component | Steps | Duration | Hardware |
|---|:---:|:---:|:---:|
| Fully-Constrained (pi_FC) | ~30B | ~2 weeks | 4x A100, 16384 envs |
| Partially-Constrained (pi_PC) | ~10B | ~2 weeks | 4x A100, 16384 envs |

## Metrics Used
- [[Success Rate]] — primary metric; a trial fails if average joint deviation exceeds 0.25m (flat) or 0.5m (irregular terrain) at any frame
- MPJPE (Mean Per-Joint [[Tdist|Position Error]]) — measures full-body reconstruction quality in millimeters on all joints, including unobserved ones
- MPOJPE (Mean Per-Observed-Joint [[Tdist|Position Error]]) — measures tracking accuracy on the subset of conditioned/observed joints only
- Displacement Error — path-following deviation from target trajectory, reported in centimeters
- [[Episode Return]] — cumulative reward combining joint position, rotation, velocity, and energy components

## Datasets Used
- AMASS (Archive of Motion Capture as Surface Shapes) — core motion capture dataset providing diverse full-body kinematic recordings for training the fully-constrained controller; filtered to remove artifacts; augmented via left-right mirroring
- HumanML3D — text-labeled motion sequences derived from AMASS, providing natural language descriptions paired with motions for training text-conditioned control
- SAMP (Stochastic Approach to Motion Prediction) — object interaction motion clips providing scene-conditioned training data for sitting and object manipulation tasks

## Related Papers
- [[DeepMimic]] — foundational motion imitation framework that MaskedMimic subsumes and substantially outperforms; MaskedMimic generalizes the single-clip tracking paradigm to unified multi-modal control
- [[MVAE]] — VAE-based motion generation predecessor; MaskedMimic extends the VAE lineage by conditioning on masked partial motion descriptions rather than complete latent codes
- [[Hierarchical Puppeteer]] — hierarchical world model for humanoid control; both target versatile humanoid behavior but MaskedMimic unifies control modalities via inpainting rather than hierarchical decomposition
- [[LeVERB]] — language-conditioned humanoid whole-body control; MaskedMimic also supports text conditioning but within a broader unified framework that simultaneously handles keyframes, paths, and objects
- [[GR00T]] — NVIDIA's foundation model for humanoid robot control; MaskedMimic addresses the simulated character animation counterpart, sharing the goal of versatile humanoid control through unified architectures
- [[UniPi]] — uses video generation for planning; MaskedMimic similarly generates motion from partial specifications but operates in physics simulation rather than pixel space
- [[Eureka]] — automated reward design for locomotion; MaskedMimic avoids extensive reward engineering by unifying tasks under the motion inpainting formulation
