---
tags: [paper, world-model, physics-simulation]
title: "DeepMimic: Example-Guided Deep Reinforcement Learning of Physics-Based Character Skills"
authors: [Xue Bin Peng, Pieter Abbeel, Sergey Levine, Michiel van de Panne]
year: 2018
arxiv: "https://arxiv.org/abs/1804.02717"
repo: "https://github.com/xbpeng/DeepMimic"
group: "World Models"
importance: 
aliases: [DeepMimic, Deep Mimic]
---

!PDFs/DeepMimic.pdf

# DeepMimic: Example-Guided Deep Reinforcement Learning of Physics-Based Character Skills

## Summary
DeepMimic presents a framework for learning physics-based character controllers that imitate a wide variety of reference motion clips using deep reinforcement learning. The core insight is that by directly rewarding a policy for producing motions that resemble reference animation data (from motion capture or keyframe animation), a simulated character can learn robust, physically grounded reproductions of highly dynamic skills including backflips, cartwheels, spinkicks, martial arts, and locomotion. Because the motions are executed in a physics simulation (Bullet), the learned controllers naturally handle perturbations, recover from disturbances, and adapt to changes in morphology without any explicit recovery programming.

The method combines an imitation objective with optional task objectives (e.g., walking toward a target location, striking an object, throwing a ball, navigating terrain), enabling characters to achieve goals while maintaining the style and quality of the reference motion. A key technical contribution is Reference State Initialization (RSI), which initializes training episodes from random states sampled along the reference motion rather than always from the start, dramatically improving exploration for highly dynamic skills with extended flight phases. The approach is demonstrated across 24 humanoid skills, 4 Atlas robot skills, and locomotion for a T-Rex and a dragon, making it one of the broadest demonstrations of physics-based motion imitation at its time of publication.

Published at SIGGRAPH 2018 (ACM Transactions on Graphics, Vol. 37, No. 4), DeepMimic has become a foundational reference in physics-based character animation and a key predecessor to subsequent work on motion imitation, skill learning, and sim-to-real transfer for humanoid robots. The code was open-sourced by the Berkeley Artificial Intelligence Research (BAIR) lab.

## Key Contributions
- Demonstrates that standard deep RL (PPO) can learn robust physics-based controllers that imitate a broad range of highly dynamic reference motions, including acrobatics, martial arts, and locomotion
- Introduces Reference State Initialization (RSI), which samples initial states from the reference motion trajectory to dramatically improve exploration for dynamic skills with flight phases
- Proposes a multi-component imitation reward combining joint pose, joint velocity, end-effector position, and center-of-mass matching, enabling high-fidelity motion reproduction
- Shows that combining imitation rewards with task-specific rewards enables goal-directed behavior (target heading, striking, throwing, terrain navigation) while preserving motion quality
- Demonstrates generalization across four different character morphologies: a humanoid (34 DOF), Atlas robot (31 DOF), T-Rex (55 DOF), and dragon (79 DOF)
- Provides an ablation study showing the complementary importance of RSI and early termination for learning dynamic skills

## Architecture / Method
DeepMimic uses Proximal Policy Optimization (PPO) to train control policies that imitate reference motions in a physics simulation.

**Simulation Environment:**
- Physics engine: Bullet Physics Library at 1.2 kHz simulation frequency
- Control frequency: 30 Hz (PD controllers at each joint with manually specified gains)
- Episode horizons: 20 seconds for cyclic skills, motion-specific duration for acyclic skills
- Early termination: episodes end when the torso or head contacts the ground

**Character Morphologies:**

| Character | Links | Mass (kg) | Height (m) | DOF | State Dim | Action Dim |
|-----------|:-----:|:---------:|:----------:|:---:|:---------:|:----------:|
| Humanoid | 13 | 45.0 | 1.62 | 34 | 197 | 36 |
| Atlas | 12 | 169.8 | 1.82 | 31 | 184 | 32 |
| T-Rex | 20 | 54.5 | 1.66 | 55 | 262 | 64 |
| Dragon | 32 | 72.5 | 1.83 | 79 | 418 | 94 |

**Policy and Value Networks:**
- Two fully-connected hidden layers with 1024 and 512 units respectively, ReLU activations
- Policy output: Gaussian action distribution with learned mean and fixed diagonal covariance
- Value network: identical architecture with a single linear output
- For vision-based terrain tasks: 3 convolutional layers (16 filters 8x8, 32 filters 4x4, 32 filters 4x4) followed by 64 FC units, concatenated with state/goal features before the FC layers

**Reward Function:**

The total reward combines an imitation objective and an optional task (goal) objective:

r_t = w^I * r_t^I + w^G * r_t^G

where w^I = 0.7 and w^G = 0.3 for combined tasks.

The imitation reward is a weighted sum of four components:

r_t^I = w^p * r_t^p + w^v * r_t^v + w^e * r_t^e + w^c * r_t^c

- Pose reward (w^p = 0.65): exp[-2 * sum_j ||q_hat_j - q_j||^2] — matches joint orientations (quaternion differences)
- Velocity reward (w^v = 0.1): exp[-0.1 * sum_j ||dq_hat_j - dq_j||^2] — matches joint angular velocities
- End-effector reward (w^e = 0.15): exp[-40 * sum_e ||p_hat_e - p_e||^2] — matches hand and foot positions
- Center-of-mass reward (w^c = 0.1): exp[-10 * ||p_hat_c - p_c||^2] — matches whole-body center of mass

**Reference State Initialization (RSI):**
At the start of each training episode, a state is uniformly sampled from the reference motion and used to initialize the agent. This is critical for highly dynamic motions (backflips, sideflips) where the agent would otherwise rarely encounter promising states through random exploration. RSI effectively provides the agent with privileged access to the reference trajectory through the initial state distribution rather than only through the reward signal.

## Results

### Table 1: Character Morphology Summary
| Character | Links | Mass (kg) | Height (m) | DOF | State Dim | Action Dim |
|-----------|:-----:|:---------:|:----------:|:---:|:---------:|:----------:|
| Humanoid | 13 | 45.0 | 1.62 | 34 | 197 | 36 |
| Atlas | 12 | 169.8 | 1.82 | 31 | 184 | 32 |
| T-Rex | 20 | 54.5 | 1.66 | 55 | 262 | 64 |
| Dragon | 32 | 72.5 | 1.83 | 79 | 418 | 94 |

The four characters span a wide range of complexity from 31 to 79 degrees of freedom. The Atlas robot is substantially heavier (169.8 kg) and taller than the humanoid, requiring the policy to handle very different dynamics despite similar joint structures.

### Table 2: Motion Imitation Performance
| Skill | Cycle Time (s) | Samples (x10^6) | Normalized Return |
|-------|:--------------:|:----------------:|:-----------------:|
| Backflip | 1.75 | 72 | 0.729 |
| Balance Beam | 0.73 | 96 | 0.783 |
| Baseball Pitch | 2.47 | 57 | 0.785 |
| Cartwheel | 2.72 | 51 | 0.804 |
| Crawl | 2.93 | 68 | 0.932 |
| Dance A | 1.62 | 67 | 0.863 |
| Dance B | 2.53 | 79 | 0.822 |
| Frontflip | 1.65 | 81 | 0.485 |
| Getup Face-Down | 3.28 | 49 | 0.885 |
| Getup Face-Up | 4.02 | 66 | 0.838 |
| Headspin | 1.92 | 112 | 0.640 |
| Jog | 0.80 | 51 | 0.951 |
| Jump | 1.77 | 86 | 0.947 |
| Kick | 1.53 | 50 | 0.854 |
| Landing | 2.83 | 66 | 0.590 |
| Punch | 2.13 | 60 | 0.812 |
| Roll | 2.02 | 81 | 0.735 |
| Run | 0.80 | 53 | 0.951 |
| Sideflip | 2.44 | 64 | 0.805 |
| Spin | 4.42 | 191 | 0.664 |
| Spinkick | 1.28 | 67 | 0.748 |
| Vault 1-Handed | 1.53 | 41 | 0.695 |
| Vault 2-Handed | 1.90 | 87 | 0.757 |
| Walk | 1.26 | 61 | 0.985 |
| Atlas: Backflip | 1.75 | 63 | 0.630 |
| Atlas: Run | 0.80 | 48 | 0.846 |
| Atlas: Spinkick | 1.28 | 66 | 0.477 |
| Atlas: Walk | 1.26 | 44 | 0.988 |
| T-Rex: Walk | 2.00 | 140 | 0.979 |
| Dragon: Walk | 1.50 | 139 | 0.990 |

Locomotion skills (Walk, Jog, Run) achieve the highest normalized returns (0.951-0.990), indicating near-perfect imitation. Highly dynamic acrobatic skills like Frontflip (0.485) and Landing (0.590) are the most challenging. Cross-morphology transfer works well for locomotion (Atlas Walk: 0.988, Dragon Walk: 0.990) but degrades for dynamic skills (Atlas Spinkick: 0.477). Sample requirements range from 41M (Vault 1-Handed) to 191M (Spin), with more complex motions generally requiring more training.

### Table 3: Task Performance (Combined Imitation + Task Objectives)
| Environment | Samples (x10^6) | Normalized Return |
|-------------|:----------------:|:-----------------:|
| Walk - Target Heading | 85 | 0.911 |
| Jog - Target Heading | 108 | 0.876 |
| Run - Target Heading | 40 | 0.637 |
| Spinkick - Strike | 85 | 0.601 |
| Baseball Pitch - Throw | 221 | 0.675 |
| Run - Mixed Obstacles | 466 | 0.285 |
| Run - Dense Gaps | 265 | 0.650 |
| Winding Balance Beam | 124 | 0.439 |
| Atlas: Walk - Stairs | 174 | 0.808 |

Target heading tasks with locomotion skills achieve strong performance (Walk: 0.911, Jog: 0.876). The most challenging task is Run - Mixed Obstacles (0.285), which requires vision-based terrain navigation combining multiple obstacle types. Even the Atlas robot successfully learns to walk up stairs (0.808), demonstrating cross-morphology task transfer.

### Table 4: Reward Ablation — Imitation vs. Task Objectives ([[Success Rate]])
| Environment | r^I + r^G | r^I Only | r^G Only |
|-------------|:---------:|:--------:|:--------:|
| Spinkick - Strike | 99% | 19% | 55% |
| Baseball Pitch - Throw | 75% | 5% | 93% |

This ablation reveals that combining imitation and task rewards is critical for the Strike task (99% vs. 55% with task reward alone), where the specific motion style matters for successful execution. For Throwing, the task-only reward achieves higher success (93%) but produces unnatural motion; the combined reward maintains motion quality at the cost of some task success (75%). With imitation reward only, both tasks largely fail (19% and 5%), confirming that task-specific guidance is necessary for goal-directed behavior.

### Table 5: Ablation — Reference State Initialization (RSI) and Early Termination (ET)
| Skill | RSI + ET | ET Only | RSI Only |
|-------|:--------:|:-------:|:--------:|
| Backflip | 0.791 | 0.730 | 0.379 |
| Sideflip | 0.823 | 0.717 | 0.355 |
| Spinkick | 0.848 | 0.858 | 0.358 |
| Walk | 0.980 | 0.981 | 0.974 |

Early Termination (ET) is the more critical component: without it (RSI Only), dynamic skills catastrophically degrade (Backflip: 0.379, Sideflip: 0.355). RSI provides additional benefit for acrobatic skills (Backflip improves from 0.730 to 0.791 with RSI). For simple locomotion (Walk), both components are largely unnecessary (0.974-0.981 across all conditions), since the initial standing state naturally leads to walking exploration.

### Table 6: Robustness to External Perturbations (Maximum Tolerated Force, N, applied for 0.2s)
| Skill | Forward (N) | Sideways (N) |
|-------|:-----------:|:------------:|
| Backflip | 440 | 100 |
| Cartwheel | 200 | 470 |
| Run | 720 | 300 |
| Spinkick | 690 | 600 |
| Walk | 240 | 300 |

The learned policies exhibit substantial robustness to external perturbations despite never being explicitly trained on them. The Run policy tolerates up to 720N forward pushes (equivalent to a strong shove), while Spinkick tolerates 690N forward and 600N sideways. Asymmetry in tolerance (e.g., Cartwheel: 200N forward vs. 470N sideways) reflects the directional stability properties of each skill.

## Metrics Used
- [[Episode Return]] — normalized cumulative reward (0 to 1 scale) used as the primary performance metric, combining imitation and task reward components
- [[Success Rate]] — binary task completion percentage used for Strike (99%) and Throw (75%) tasks
- Perturbation Robustness — maximum external force (in Newtons, applied for 0.2s) that the policy can withstand without falling, measuring the physical robustness of learned controllers
- [[Motion Naturalness]] — qualitative assessment via video demonstrations; the imitation reward serves as a quantitative proxy for motion quality

## Datasets Used
- [[CMU Motion Capture Database]] — source of reference motion clips for the majority of demonstrated skills (locomotion, acrobatics, martial arts, dance); motions are retargeted to each character morphology
- Custom keyframed animations — used for certain skills where motion capture data was unavailable; demonstrates the method works with hand-authored reference motions as well

## Related Papers
- [[MVAE]] — also uses motion capture data to learn character controllers but through a VAE latent action space rather than direct imitation reward; shares co-author Michiel van de Panne; [[MVAE]] builds on DeepMimic's demonstration that RL can produce natural character motion
- [[Hierarchical Puppeteer]] — hierarchical world model with a low-level tracker pretrained on motion capture data; the tracker's motion imitation role is conceptually similar to DeepMimic's imitation objective, but [[Hierarchical Puppeteer|Puppeteer]] adds a high-level visual planner on top
- [[DreamerV3]] — general-purpose model-based RL; DeepMimic demonstrates that even model-free RL (PPO) suffices for physics-based character control when combined with well-designed imitation rewards
- [[Eureka]] — automated reward design for locomotion using LLMs; DeepMimic's manually designed multi-component imitation reward is exactly the kind of reward engineering that [[Eureka]] aims to automate
- [[TD-MPC2]] — scalable model-based RL for continuous control; used as a baseline in [[Hierarchical Puppeteer]], where it achieves comparable task performance but produces unnatural motions unlike DeepMimic-style imitation approaches
- [[GR00T]] — foundation model for humanoid robots that uses motion imitation for real-world deployment; conceptually extends DeepMimic's approach from simulation to physical hardware
