---
tags: [paper, world-model, physics-simulation]
title: "Learning Agile Robotic Locomotion Skills by Imitating Animals"
authors: [Xue Bin Peng, Erwin Coumans, Tingnan Zhang, Tsang-Wei Edward Lee, Jie Tan, Sergey Levine]
year: 2020
arxiv: "https://arxiv.org/abs/2004.00784"
repo: "https://github.com/erwincoumans/motion_imitation"
group: "World Models"
importance: 
aliases: [Learning Agile Robotic Locomotion, Robotic Imitation, Imitating Animals]
---

![[PDFs/Learning Agile Robotic Locomotion.pdf]]

# Learning Agile Robotic Locomotion Skills by Imitating Animals

## Summary
This paper presents an end-to-end framework for learning agile quadruped locomotion skills by imitating motion capture data recorded from real animals. The system transfers dynamic behaviors from a dog to a Unitree Laikago quadruped robot through a three-stage pipeline: motion retargeting (mapping animal mocap keypoints to robot morphology via inverse kinematics), motion imitation (training a control policy in simulation using PPO with a multi-component imitation reward), and domain adaptation (transferring the policy from simulation to the real robot using dynamics randomization and a latent space adaptation technique). The Laikago successfully reproduces a diverse repertoire of locomotion skills including pacing, trotting, backward trotting, spinning, side-stepping, hopping turns, and more, with the learned trot policy reaching 1.08 m/s compared to the manufacturer's fastest gait at 0.84 m/s.

A key technical contribution is the domain adaptation method, which combines dynamics randomization during simulation training with an information bottleneck that constrains the mutual information between dynamics parameters and a latent encoding. This produces policies that are robust to dynamics variation while remaining adaptable. For real-world deployment, the latent encoding is adapted online using advantage-weighted regression (AWR) with only approximately 50 trials per skill (5-10 seconds each), enabling rapid fine-tuning on the physical robot without retraining the full policy.

Published at RSS 2020 where it received the Best Paper Award, this work from Google Research and UC Berkeley demonstrated for the first time that a real quadruped robot could learn a diverse set of agile locomotion skills from animal motion capture data, bridging the gap between physics-based character animation (e.g., [[DeepMimic]]) and real-world robotic deployment.

## Key Contributions
- Presents a complete pipeline from animal motion capture to real robot deployment: motion retargeting via inverse kinematics, motion imitation via RL in simulation, and domain adaptation for sim-to-real transfer
- Demonstrates that a real Laikago quadruped robot can learn 10 diverse locomotion skills (pacing, trotting, backward trotting, spinning, side-stepping, turning, hop-turning, and more) from dog motion capture data
- Introduces a latent space domain adaptation method combining dynamics randomization with an information bottleneck (constraining mutual information between dynamics parameters and latent encoding via beta = 10^-4 KL penalty), enabling rapid real-world adaptation with only ~50 trials per skill
- Achieves 1.08 m/s with the learned trot policy, exceeding the manufacturer's fastest gait (0.84 m/s), while maintaining natural animal-like movement quality
- Provides systematic comparison of domain adaptation strategies: no randomization, robust (randomization only), and adaptive (randomization + latent adaptation), showing that the adaptive approach substantially outperforms alternatives on dynamic skills

## Architecture / Method
The framework consists of three stages that transform animal motion capture recordings into real robot locomotion skills.

**Stage 1: Motion Retargeting**

Animal motion capture data (from a real dog) is retargeted to the Laikago robot's morphology using inverse kinematics. Keypoints on the animal skeleton (feet, hips, shoulders) are mapped to corresponding points on the robot, accounting for differences in limb proportions, joint ranges, and body structure. The retargeted motions serve as reference trajectories for the imitation stage.

**Stage 2: Motion Imitation**

A control policy is trained in PyBullet simulation to imitate the retargeted reference motions using Proximal Policy Optimization (PPO).

- **Robot:** Unitree Laikago quadruped, 18 DOF (3 actuated DOF per leg, 6 under-actuated DOF for the root torso)
- **State:** Joint positions, joint velocities, root orientation, root angular velocity, and a phase variable indexing into the reference motion
- **Action:** Target joint angles for PD controllers at each actuated joint

**Reward Function** — five components with weights:

| Component | Weight | Description |
|-----------|:------:|-------------|
| Pose reward (r^p) | 0.5 | Matches joint rotations to reference |
| Velocity reward (r^v) | 0.05 | Matches joint angular velocities |
| End-effector reward (r^e) | 0.2 | Matches foot positions in 3D |
| Root pose reward (r^rp) | 0.15 | Matches torso position and orientation |
| Root velocity reward (r^rv) | 0.1 | Matches torso linear and angular velocity |

Each reward component uses an exponential kernel: r = exp(-k * ||reference - actual||^2), producing smooth gradients that guide the policy toward the reference motion.

**Policy Network:**

- Two fully-connected hidden layers with 512 and 256 units, ReLU activations
- Output layer produces Gaussian action distribution means; fixed diagonal standard deviation
- Value function: separate network with 512 and 256 hidden units

**Stage 3: Domain Adaptation**

**[[Sim-to-Real Transfer|Dynamics Randomization]]:** Simulation parameters (masses, friction, motor strength, latency) are randomized during training to produce policies that generalize across dynamics variations.

**Latent Dynamics Encoder:** An encoder network (two FC layers with 256 and 128 ReLU units) maps dynamics parameters to a Gaussian latent distribution. The policy is conditioned on samples from this latent space. An information bottleneck constrains the mutual information between dynamics parameters and the latent encoding:

Objective: maximize E[Return] - beta * E[D_KL(E(.|mu) || rho(.))]

where beta = 10^-4 controls the robustness-adaptability tradeoff. Lower beta produces more adaptive but less robust policies; higher beta produces more robust but less adaptive policies.

**Real-World Adaptation:** The latent encoding is adapted on the real robot using advantage-weighted regression (AWR). Approximately 50 trials per skill (5-10 seconds each) are collected on the physical robot, and the latent distribution is updated by weighting samples by their advantage values, iteratively searching for the encoding that best matches the real dynamics.

## Results

### Table 1: Real-World Performance (Normalized Return, 0-1)
| Skill | No Rand | Robust | Adaptive (Before) | Adaptive (After) |
|-------|:-------:|:------:|:-----------------:|:----------------:|
| Dog Pace | 0.128 +/- 0.033 | 0.350 +/- 0.172 | 0.395 +/- 0.277 | **0.827 +/- 0.020** |
| Dog Trot | 0.171 +/- 0.031 | 0.471 +/- 0.102 | 0.237 +/- 0.092 | **0.593 +/- 0.070** |
| Dog Backwards Trot | 0.072 +/- 0.004 | 0.120 +/- 0.126 | 0.167 +/- 0.048 | **0.656 +/- 0.071** |
| Dog Spin | 0.098 +/- 0.033 | 0.209 +/- 0.081 | 0.121 +/- 0.035 | **0.751 +/- 0.116** |
| In-Place Steps | 0.822 +/- 0.002 | **0.845 +/- 0.004** | 0.771 +/- 0.001 | 0.778 +/- 0.002 |
| Side-Steps | 0.541 +/- 0.070 | **0.782 +/- 0.009** | 0.310 +/- 0.114 | 0.710 +/- 0.057 |
| Turn | 0.108 +/- 0.008 | 0.410 +/- 0.227 | 0.594 +/- 0.018 | **0.606 +/- 0.014** |
| Hop-Turn | 0.174 +/- 0.050 | 0.478 +/- 0.054 | 0.493 +/- 0.012 | **0.518 +/- 0.005** |
| Running Man | 0.149 +/- 0.004 | 0.430 +/- 0.031 | 0.488 +/- 0.045 | **0.503 +/- 0.008** |

The adaptive method (with latent space adaptation on the real robot) substantially outperforms all alternatives on dynamic locomotion skills. Dog Pace improves from 0.395 (before adaptation) to 0.827 (after ~50 trials of real-world adaptation). For simpler quasi-static skills (In-Place Steps, Side-Steps), the robust baseline (dynamics randomization only) is competitive or slightly better, since these skills are less sensitive to dynamics mismatch. Without any randomization, most dynamic skills fail almost completely on the real robot (0.072-0.174 normalized return).

**Speed comparison:** The learned Dog Trot policy reaches 1.08 m/s, exceeding the Laikago's fastest manufacturer gait at 0.84 m/s.

## Metrics Used
- [[Episode Return]] — normalized cumulative imitation reward (0-1 scale), combining pose, velocity, end-effector, root pose, and root velocity components; primary metric for both simulation and real-world evaluation
- [[Motion Naturalness]] — qualitative assessment via video demonstrations; the imitation reward serves as a quantitative proxy, with policies trained to match animal motion capture data
- [[Success Rate]] — implicit in the deployment success of each skill on the physical Laikago robot

## Datasets Used
- Dog motion capture data — motion capture recordings from a real dog, retargeted to the Laikago morphology via inverse kinematics; covers pacing, trotting, backward trotting, spinning, and other locomotion gaits
- Custom motion clips — additional skills (in-place steps, side-steps, turning, hop-turn, running man) from hand-designed or retargeted reference motions

## Related Papers
- [[DeepMimic]] — direct predecessor by the same lead author; this work extends [[DeepMimic]]'s motion imitation framework from simulated characters to real robots via the addition of domain adaptation for sim-to-real transfer
- [[Sim-to-Real Transfer]] — same lead author's earlier work on dynamics randomization for sim-to-real transfer of manipulation policies; this paper extends the dynamics randomization concept with a latent space adaptation method for locomotion
- [[ASE]] — successor work that scales motion imitation to large unstructured motion datasets with adversarial skill embeddings; builds on the imitation reward and motion retargeting established here
- [[AMP]] — introduces adversarial motion priors that replace the hand-designed imitation reward used in this work with a learned discriminator, eliminating the need for explicit pose matching
- [[MVAE]] — VAE-based approach to character control from motion capture; operates in a learned latent action space rather than directly imitating reference motions
- [[Hierarchical Puppeteer]] — hierarchical humanoid control with motion capture-based tracking; conceptually extends the motion imitation paradigm to visual humanoid control with a two-level architecture
- [[Eureka]] — automated reward design for locomotion; could potentially automate the imitation reward engineering done manually in this work
- [[GR00T]] — humanoid foundation model that deploys learned locomotion policies on real hardware; traces lineage through this work's sim-to-real locomotion pipeline
