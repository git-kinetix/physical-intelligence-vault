---
tags: [paper, world-model, physics-simulation]
title: "Character Controllers Using Motion VAEs"
authors: [Hung Yu Ling, Fabio Zinno, George Cheng, Michiel van de Panne]
year: 2020
arxiv: "https://arxiv.org/abs/2103.14274"
repo: "https://github.com/electronicarts/character-motion-vaes"
group: "World Models"
importance: 
aliases: [MVAE, Motion VAE, Character Controllers Using Motion VAEs]
---

!PDFs/MVAE.pdf

# Character Controllers Using Motion VAEs

## Summary
Motion VAE (MVAE) introduces a framework for synthesizing realistic, goal-directed human movement by learning data-driven generative models from motion capture data using autoregressive conditional variational autoencoders. The core idea is that the latent variables of a learned VAE define a compact, structured action space that governs how a character's motion evolves over time. By sampling different latent codes, the model produces diverse yet plausible next-pose predictions, enabling stochastic motion generation that captures the natural variability of human movement.

The framework operates in two stages: first, a kinematic generative model (the MVAE) is trained on motion capture clips to learn the manifold of natural human motion; second, deep reinforcement learning (PPO) is used to train controllers that select latent actions to achieve specific goals such as target reaching, joystick-style directional control, path following, and maze navigation. A key architectural choice is the use of a Mixture-of-Experts (MoE) decoder with 6 expert networks, combined with scheduled sampling during training to ensure stable autoregressive rollouts. The approach requires no motion classification labels, foot contact annotations, or gait-phase information.

Published at SIGGRAPH 2020 (ACM Transactions on Graphics), this work from the University of British Columbia and Electronic Arts Vancouver demonstrates that VAE-learned latent spaces can serve as effective and compact action representations for character control, bridging generative modeling and reinforcement learning for physically plausible animation.

## Key Contributions
- Introduces an autoregressive conditional VAE (Motion VAE) that learns a generative model of human motion, where latent variables define a structured action space for character controllers
- Demonstrates that deep reinforcement learning (PPO) can effectively operate in the learned latent action space to produce goal-directed, natural-looking character movements
- Proposes a Mixture-of-Experts (MoE) decoder architecture with latent variable injection at every layer to prevent posterior collapse and improve motion quality
- Employs scheduled sampling during MVAE training, progressively transitioning from teacher-forced to fully autoregressive prediction for stable long-horizon rollouts
- Evaluates on four diverse control tasks (target reaching, joystick control, path following, maze navigation) using a single motion capture dataset without requiring motion labels or annotations

## Architecture / Method
The MVAE framework consists of two main components: the Motion VAE generative model and RL-based controllers that operate in its latent space.

**Motion VAE (Generative Model):**

The MVAE is an autoregressive conditional VAE that predicts the next pose one frame at a time. Given the current pose, it produces a distribution over next-state predictions conditioned on stochastic latent variables.

- **Pose Representation:** Includes root position, root facing direction, linear velocities, joint positions (3D), joint velocities (3D), and joint orientations (6D forward/upward vectors). No motion labels or foot contact annotations are used.
- **Encoder:** Three-layer feed-forward network with 256 hidden units per layer and ELU activations. Takes the previous pose p_{t-1} and current pose p_t as input, outputs mean and variance for the latent distribution via the reparameterization trick. Latent dimension: 32.
- **Decoder:** Mixture-of-Experts (MoE) architecture with 6 expert networks. A gating network (three-layer feedforward, 256 hidden units, ELU) selects expert blending weights. Each expert has a structure similar to the encoder. Crucially, the latent variable z is passed to every layer of the expert networks to prevent posterior collapse.
- **Loss Function:** Beta-VAE objective combining MSE reconstruction loss and KL divergence, with beta = 0.2 to minimize posterior collapse.

**Training Procedure:**

- Scheduled sampling over 180 epochs: supervised learning for 20 epochs (always use ground truth), scheduled sampling for 20 epochs (progressively increase autoregressive proportion), and fully autoregressive prediction for 140 epochs
- Rollout length L = 8 frames (1/4 second) during training
- Adam optimizer with learning rate linearly decayed from 1e-4 to zero
- Mini-batch size: 64
- Training time: approximately 2 hours on an NVIDIA GeForce GTX 1060

**RL-Based Controllers:**

- **Algorithm:** Proximal Policy Optimization (PPO)
- **Controller network:** Two hidden layers with 256 units and ReLU activations; output normalized with Tanh and scaled to [-4, +4] to produce latent actions
- **Tasks:** Target reaching (navigate to random targets in a 120x80 ft arena), Joystick control (follow directional commands at varying speeds), Path following (track a figure-8 parametric path with 4 lookahead targets), and Maze navigation (explore a procedural maze using 16-ray vision sensing)
- **Energy penalty** applied across all tasks to discourage excessive motion: E = (root velocities)^2 + (1/J) * sum of joint velocity magnitudes
- 100 parallel simulations; training time: 1-6 hours per task on a desktop GPU

**Sampling-Based Control Baseline:**

A Monte Carlo planning baseline is also tested, using N=200 rollouts with horizon H=4. This performs modestly on target reaching but struggles with joystick and path following tasks, motivating the RL approach.

## Results

### Table 1: Foot Skating Artifacts (cm/frame)
| Condition | Ground Truth | Beta=0.2, N=6 | Beta=0.4, N=6 | Beta=0.2, N=4 |
|-----------|:------------:|:--------------:|:--------------:|:--------------:|
| Motion Capture | 0.10 | - | - | - |
| Random Walk | - | 0.067 | 0.082 | 0.085 |
| Target | - | 0.27 | 0.15 | 0.24 |
| Joystick | - | 0.28 | 0.33 | 0.39 |
| Path | - | 0.30 | 0.28 | 0.44 |
| Maze | - | 0.24 | 0.21 | 0.38 |

Foot skating is measured as s = d(2 - 2^{h/H}), where d is foot displacement, h is foot height, and H = 3.3 cm. The default configuration (beta=0.2, N=6 experts) achieves the lowest foot skating on random walks (0.067 cm/frame, below the 0.10 ground truth reference). During goal-directed tasks, foot skating increases modestly to 0.24-0.30 cm/frame as the controller must make sharper directional changes. Increasing beta to 0.4 reduces foot skating on some tasks (Target: 0.15 vs 0.27) but increases it on others (Joystick: 0.33 vs 0.28), while reducing from 6 to 4 experts consistently increases skating artifacts.

### Table 2: Joystick Responsiveness (seconds to reach within 5 degrees of target direction)
| Configuration | Overall | Left Half-plane (0, pi] | Right Half-plane (pi, 2pi] |
|---------------|:-------:|:----------------------:|:--------------------------:|
| Beta=0.2, N=6 | 1.62 | 1.70 | 1.56 |
| Beta=0.4, N=6 | 1.71 | 1.66 | 1.77 |
| Beta=0.2, N=4 | 1.38 | 1.63 | 1.11 |

Response time measures how quickly the character reorients when the target direction changes every 5 seconds. The default model (beta=0.2, N=6) achieves 1.62 seconds overall. The configuration with 4 experts is faster overall (1.38 s) but shows a strong handedness bias (1.63 s left vs 1.11 s right), attributed to exploration-exploitation dynamics in RL where early random discovery of effective right turns biases subsequent learning. The 6-expert model exhibits more symmetric turning behavior.

## Metrics Used
- [[Motion Naturalness]] — foot skating measurement used as a proxy for motion quality, computed as s = d(2 - 2^{h/H}) in cm/frame
- [[Episode Return]] — cumulative discounted reward used to evaluate RL controller performance across all four tasks
- Joystick Responsiveness — frames (converted to seconds) required to reach within 5 degrees of a target facing direction
- Energy Penalty — regularization metric penalizing excessive root and joint velocities to encourage natural motion

## Datasets Used
- [[CMU Motion Capture Database]] — 17 minutes of walking, running, turning, dynamic stopping, and resting motions at 30 Hz (approximately 30,000 frames including mirrored augmentation), used to train the MVAE generative model; no motion labels, foot contact annotations, or gait-phase information required

## Related Papers
- [[Hierarchical Puppeteer]] — also uses motion capture data to bootstrap natural humanoid motion but via a hierarchical world model with a low-level tracker and high-level puppeteer; MVAE's latent action space concept is conceptually related to the tracker's command space
- [[DreamerV3]] — general-purpose model-based RL agent; MVAE similarly uses a learned latent space but specifically for character animation rather than general domains
- [[TD-MPC2]] — scalable model-based RL for continuous control; MVAE's RL controllers (PPO) operate in a VAE-learned action space rather than directly in joint/torque space
- [[UniPi]] — uses generative models (diffusion) for planning in video space; MVAE instead uses a VAE for planning in motion space
- [[Eureka]] — automated reward design for locomotion; MVAE hand-crafts task-specific rewards but uses a learned motion prior to ensure naturalness
