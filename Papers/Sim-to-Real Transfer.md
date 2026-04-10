---
tags: [paper, domain/robotics, method/rl, lineage/peng]
title: "Sim-to-Real Transfer of Robotic Control with Dynamics Randomization"
authors: [Xue Bin Peng, Marcin Andrychowicz, Wojciech Zaremba, Pieter Abbeel]
year: 2018
arxiv: "https://arxiv.org/abs/1710.06537"
repo: ""
group: "World Models"
venue: "ICRA 2018"
domain: [robotics]
method: [rl]
lineage: [peng]
predecessor: ["[[DeepMimic]]"]
importance: 1
aliases: [Sim-to-Real Transfer, Dynamics Randomization, SimToReal]
---

!PDFs/Sim-to-Real Transfer.pdf

# Sim-to-Real Transfer of Robotic Control with Dynamics Randomization

## Summary
This paper presents a foundational approach for transferring robotic control policies trained in simulation to real-world hardware by randomizing the dynamics parameters of the simulator during training. The core insight is that a policy trained across a sufficiently diverse distribution of simulated dynamics will develop implicit system identification capabilities, enabling it to adapt to the unknown dynamics of the real world without any training on the physical system. The approach is demonstrated on a puck-pushing task using a 7-DOF Fetch Robotics arm, where an LSTM-based recurrent policy trained with dynamics randomization in MuJoCo achieves 0.89 success rate on the real robot, compared to 0.0 for a feedforward policy trained without randomization.

The method randomizes 95 dynamics parameters during training, including link masses, joint damping, puck mass/friction/damping, table height, controller gains, action timestep, and observation noise. The key architectural choice is the use of a recurrent (LSTM) policy that can implicitly infer the current dynamics from the history of observations and actions, rather than requiring explicit system identification. The policy is trained using Recurrent Deterministic Policy Gradient (RDPG) combined with Hindsight Experience Replay (HER), an off-policy algorithm that augments training data with replayed goals for sample-efficient learning of goal-conditioned policies.

Published at ICRA 2018 by researchers from OpenAI and UC Berkeley, this work established dynamics randomization as a standard technique for sim-to-real transfer, influencing a broad lineage of subsequent robotics research including domain randomization for locomotion, manipulation, and dexterous control. The paper demonstrates that the reality gap can be bridged not by making simulation more accurate, but by making the policy robust to a wide range of possible dynamics.

## Key Contributions
- Introduces dynamics randomization as a principled approach to sim-to-real transfer, randomizing 95 simulation parameters (link masses, joint damping, puck properties, controller gains, action timestep, observation noise) during training to produce policies that generalize to real-world dynamics
- Demonstrates that LSTM-based recurrent policies can implicitly perform online system identification from observation-action histories, achieving 0.89 real-world success rate versus 0.67 for feedforward policies with randomization and 0.0 for feedforward policies without randomization
- Combines Recurrent Deterministic Policy Gradient (RDPG) with Hindsight Experience Replay (HER) for sample-efficient off-policy training of goal-conditioned recurrent policies
- Provides systematic ablation showing that action timestep randomization and observation noise are the most critical randomization components for successful sim-to-real transfer
- Uses an omniscient critic that receives ground-truth dynamics parameters during training while the actor only observes states, enabling more stable value estimation without leaking privileged information to the deployed policy

## Architecture / Method
The system trains a goal-conditioned policy in MuJoCo simulation with randomized dynamics, then deploys it zero-shot on a real 7-DOF Fetch Robotics arm for a puck-pushing task.

**Task Setup:**

- **Robot:** 7-DOF Fetch Robotics arm with position controller
- **Task:** Push a puck to a random target location on a table
- **State space:** 52-dimensional (arm joint positions/velocities, gripper position, puck position/orientation/velocities)
- **Action space:** 7-dimensional (relative joint angle offsets)
- **Reward:** Binary sparse reward: r_t = 0 if puck is within threshold of target, r_t = -1 otherwise
- **Episode length:** 100 control timesteps (~4 seconds)

**Dynamics Randomization:**

95 parameters are randomized during training, sampled uniformly from specified ranges at the start of each episode:

| Parameter | Range |
|-----------|-------|
| Link Mass | [0.25, 4] x default |
| Joint Damping | [0.2, 20] x default |
| Puck Mass | [0.1, 0.4] kg |
| Puck Friction | [0.1, 5] |
| Puck Damping | [0.01, 0.2] Ns/m |
| Table Height | [0.73, 0.77] m |
| Controller Gains | [0.5, 2] x default |
| Action Timestep | [125, 1000] Hz |
| Observation Noise | Added to all observations |

**Policy Architecture (LSTM):**

- **Recurrent branch:** 128 fully-connected units followed by 128 LSTM units, processing current state, previous action, and goal
- **Feedforward branch:** Processes goal and current state features
- **Output layers:** Two additional 128-unit fully-connected layers with ReLU activations, followed by tanh output
- **Value network:** Similar architecture but additionally receives action and ground-truth dynamics parameters (omniscient critic)

**Training Algorithm:**

- **Algorithm:** Recurrent Deterministic Policy Gradient (RDPG) — the recurrent extension of DDPG
- **Experience replay:** Hindsight Experience Replay (HER) with replay probability k = 0.8
- **Optimizer:** Adam with step size 5 x 10^-4
- **Batch size:** 128 episodes x 100 steps
- **Training scale:** ~100 million samples over ~8000 iterations (~8 hours on 100-core cluster)

## Results

### Table 1: Dynamics Parameters Randomization Ranges
| Parameter | Range |
|-----------|-------|
| Link Mass | [0.25, 4] x default |
| Joint Damping | [0.2, 20] x default |
| Puck Mass | [0.1, 0.4] kg |
| Puck Friction | [0.1, 5] |
| Puck Damping | [0.01, 0.2] Ns/m |
| Table Height | [0.73, 0.77] m |
| Controller Gains | [0.5, 2] x default |
| Action Timestep | [125, 1000] Hz |

### Table 2: Real Robot Performance
| Model | Success (Sim) | Success (Real) | Trials |
|-------|:-------------:|:--------------:|:------:|
| LSTM + Dynamics Rand | 0.91 +/- 0.03 | **0.89 +/- 0.06** | 28 |
| FF + Dynamics Rand + History | 0.87 +/- 0.03 | 0.70 +/- 0.10 | 20 |
| FF + Dynamics Rand | 0.83 +/- 0.04 | 0.67 +/- 0.14 | 12 |
| FF (No Randomization) | 0.51 +/- 0.05 | 0.0 +/- 0.0 | 10 |

The LSTM policy with dynamics randomization achieves 0.89 real-world success rate with minimal sim-to-real degradation (0.91 in sim). Without dynamics randomization, the feedforward policy completely fails in the real world (0.0). Adding observation history to the feedforward policy (FF + Hist) partially bridges the gap (0.70) but the recurrent architecture remains substantially superior.

### Table 3: Randomization Ablation (LSTM on Real Robot)
| Configuration | Success (Real) | Trials |
|---------------|:--------------:|:------:|
| All Randomization | **0.89 +/- 0.06** | 28 |
| Fixed Link Mass | 0.64 +/- 0.10 | 22 |
| Fixed Puck Friction | 0.48 +/- 0.10 | 27 |
| Fixed Action Timestep | 0.29 +/- 0.11 | 17 |
| No Observation Noise | 0.25 +/- 0.12 | 12 |

Action timestep randomization and observation noise are the most critical components. Without observation noise, real-world success drops from 0.89 to 0.25, suggesting that noise injection during training is essential for handling the noisy observations on real hardware. Fixed action timestep similarly causes severe degradation (0.29), indicating that timing variability is a key aspect of the reality gap.

## Metrics Used
- [[Success Rate]] — binary task completion measured as whether the puck reaches within a threshold distance of the target position; primary evaluation metric for both simulation and real-world experiments
- [[Episode Return]] — cumulative sparse reward used during training (r_t = 0 for success, r_t = -1 otherwise)

## Datasets Used
- No external dataset; policies are trained entirely in MuJoCo simulation with randomized dynamics and evaluated zero-shot on the real Fetch robot

## Related Papers
- [[DeepMimic]] — same lead author (Xue Bin Peng), published same year (2018); [[DeepMimic]] focuses on motion imitation in simulation while this paper addresses the orthogonal problem of sim-to-real transfer via dynamics randomization
- [[Hierarchical Puppeteer]] — uses sim-to-real techniques for humanoid control; dynamics randomization from this work is a foundational technique for all subsequent sim-to-real locomotion research
- [[Eureka]] — automated reward design for sim-to-real locomotion; builds on the dynamics randomization paradigm established here
- [[GR00T]] — humanoid foundation model deploying learned policies on real hardware; the sim-to-real transfer approach traces lineage to this work
- [[DreamerV3]] — model-based RL that learns world models; this paper instead makes model-free policies robust to model uncertainty through randomization
- [[TD-MPC2]] — scalable model-based continuous control; this paper's dynamics randomization provides an alternative to model-based approaches for handling dynamics mismatch
