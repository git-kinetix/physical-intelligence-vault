---
tags: [paper, world-model, physics-simulation]
title: "MCP: Learning Composable Hierarchical Control with Multiplicative Compositional Policies"
authors: [Xue Bin Peng, Michael Chang, Grace Zhang, Pieter Abbeel, Sergey Levine]
year: 2019
arxiv: "https://arxiv.org/abs/1905.09808"
repo: "https://github.com/xbpeng/mcp"
group: "World Models"
importance: 
aliases: [MCP, Multiplicative Compositional Policies, Composable Hierarchical Control]
---

!PDFs/MCP.pdf

# MCP: Learning Composable Hierarchical Control with Multiplicative Compositional Policies

## Summary
MCP (Multiplicative Compositional Policies) introduces a method for learning reusable motor primitives that can be simultaneously activated and composed via multiplication to produce complex behaviors for physically simulated characters. The key insight is that multiplicative composition of Gaussian policy primitives -- computing the normalized product of their distributions -- allows multiple primitives to be active at the same time, each constraining the action distribution along different dimensions. This contrasts fundamentally with additive mixture models (Mixture-of-Experts) where only one primitive is active per timestep, limiting the character to behaviors prescribed by individual primitives and requiring temporal sequencing for complex tasks.

The framework operates in two phases: (1) pre-training, where a set of k=8 primitive policies are learned via motion imitation ([[DeepMimic]]-style) on a diverse corpus of reference motions, with a shared gating network that learns to activate different primitives based on the current state and goal; and (2) transfer, where the primitive policies are frozen and only the gating network is retrained to solve novel downstream tasks by recomposing the learned motor repertoire. The multiplicative composition formula combines k Gaussian primitives as a weighted product of experts: the composite mean at each action dimension is the precision-weighted average of primitive means, and the composite variance is the inverse of the sum of precision-weighted terms. Crucially, primitives observe only the state (not the goal), while the gating network observes both state and goal, enforcing a clean separation where primitives encode reusable motor skills and the gating network encodes task-specific composition strategies.

Published at NeurIPS 2019 by UC Berkeley researchers, MCP demonstrated substantial improvements over prior skill transfer methods on challenging continuous control tasks including soccer ball dribbling, object carrying, and heading control across three character morphologies (Biped, Humanoid, T-Rex). MCP was the only method that successfully learned the most difficult task (T-Rex dribbling), establishing multiplicative composition as a powerful paradigm for hierarchical skill reuse in physics-based character control.

## Key Contributions
- Introduces multiplicative composition of Gaussian policy primitives as an alternative to additive mixtures, enabling simultaneous activation of multiple primitives that each constrain the action distribution along different dimensions
- Demonstrates that multiplicative composition substantially outperforms additive Mixture-of-Experts, hierarchical switching, Option-Critic, finetuning, and latent space baselines on complex transfer tasks
- Shows that enforcing an architectural asymmetry -- primitives observe only state, gating network observes state and goal -- prevents degenerate solutions where a single primitive handles all goals and forces meaningful skill specialization
- Achieves successful transfer to the most challenging task (T-Rex soccer dribbling, 0.781) where all other methods fail (best alternative: 0.115), demonstrating the power of composable primitives for morphologies with limited training data
- Reveals that learned primitives develop interpretable phase-dependent activations (e.g., one primitive for left stance, another for right stance), recovering a decomposition analogous to manual gait-phase engineering

## Architecture / Method
MCP uses a two-phase approach: pre-training primitive policies via motion imitation, then transferring to downstream tasks by retraining only the gating network.

**Multiplicative Composition Formula:**

Given k primitive policies, each outputting a Gaussian distribution pi_i(a|s) = N(mu_i(s), Sigma_i(s)) with diagonal covariance, the composite policy is:

pi(a|s,g) = (1/Z) * product_{i=1}^{k} pi_i(a|s,g)^{w_i(s,g)}

For Gaussian primitives, this yields closed-form composite parameters at each action dimension j:
- Composite mean: mu^j = [1 / sum_l(w_l / sigma_l^j)] * sum_i(w_i / sigma_i^j * mu_i^j)
- Composite variance: sigma^j = (sum_i(w_i / sigma_i^j))^{-1}

This is a precision-weighted combination where primitives with lower variance (higher confidence) contribute more to the composite action.

**Primitive Policy Network:**
- k = 8 primitives across all experiments
- Shared encoder: 512 -> 256 hidden units from state input
- Per-primitive branches: 256 hidden units each
- Output: mean mu_i(s) and diagonal covariance Sigma_i(s) per primitive
- ReLU activations throughout
- Primitives observe only state s, NOT the goal g

**Gating Network:**
- Separate state encoder: 512 -> 256 hidden units
- Separate goal encoder: 256 hidden units
- Concatenated features processed via 256-unit hidden layer
- Sigmoid output layer producing weights w(s,g) in [0, 1]^k
- Only the gating network observes the goal g, enforcing task-agnostic primitives

**Pre-Training Phase:**
- [[DeepMimic]]-style motion imitation with PPO
- Goal g_t = (s_hat_{t+1}, s_hat_{t+2}): target states for next 2 timesteps from reference motion
- Reference motions randomly switched within episodes to encourage skill transitions
- Biped/Humanoid: 230 seconds of motion capture data (walks, turns)
- T-Rex: 11 seconds of artist-generated keyframes (1 forward walk, 2 left turns, 2 right turns)

**Transfer Phase:**
- Primitive policies frozen; only gating network retrained
- Task-specific reward functions (heading, carry, dribble)
- PPO with gamma=0.99 (vs. 0.95 during pre-training)

**Character Specifications:**

| Character | Links | Mass (kg) | Height (m) | DOF | State Dim | Action Dim |
|-----------|:-----:|:---------:|:----------:|:---:|:---------:|:----------:|
| Biped | 12 | 42 | 1.34 | 23 | 105 | 17 |
| Humanoid | 13 | 45 | 1.62 | 34 | 196 | 28 |
| T-Rex | 20 | 54.5 | 1.66 | 55 | 261 | 49 |
| Ant | - | - | - | 14 | - | 8 |

States include relative link positions, rotations (quaternions), and linear/angular velocities. Actions specify target rotations for PD controllers at each joint. Control frequency: 30 Hz.

**Training Hyperparameters:**
- PPO clip threshold: 0.02
- Batch size: 4096, minibatch: 256
- SGD momentum: 0.9
- Pre-train policy learning rate: 1-2e-5
- Transfer policy learning rate: 5e-5
- Value function learning rate: 1e-2
- GAE lambda: 0.95, TD(lambda) with lambda=0.95

## Results

### Table 1: Transfer Task Performance (Normalized Return, 0-1)
| Task | Scratch | Finetune | Hierarchical | Option-Critic | MOE | Latent Space | MCP |
|------|:-------:|:--------:|:------------:|:-------------:|:---:|:------------:|:---:|
| Heading: Biped | 0.927+/-0.032 | 0.970+/-0.002 | 0.834+/-0.001 | 0.952+/-0.012 | 0.918+/-0.002 | 0.970+/-0.001 | **0.976+/-0.002** |
| Carry: Biped | 0.027+/-0.035 | 0.324+/-0.014 | 0.001+/-0.002 | 0.346+/-0.011 | 0.013+/-0.013 | 0.456+/-0.031 | **0.575+/-0.032** |
| Dribble: Biped | 0.072+/-0.012 | 0.651+/-0.025 | 0.546+/-0.024 | 0.046+/-0.008 | 0.073+/-0.021 | 0.768+/-0.012 | **0.782+/-0.008** |
| Dribble: Humanoid | 0.076+/-0.024 | 0.598+/-0.030 | 0.198+/-0.002 | 0.058+/-0.007 | 0.043+/-0.021 | 0.751+/-0.006 | **0.805+/-0.006** |
| Dribble: T-Rex | 0.065+/-0.032 | 0.074+/-0.011 | - | 0.098+/-0.013 | 0.070+/-0.017 | 0.115+/-0.013 | **0.781+/-0.021** |
| Holdout: Ant | **0.951+/-0.093** | 0.885+/-0.062 | - | - | - | 0.745+/-0.060 | 0.812+/-0.030 |

MCP outperforms all baselines on every complex transfer task. The most striking result is T-Rex Dribble, where MCP achieves 0.781 while all alternatives score below 0.115 -- MCP is the only method that learns a successful policy. For the simple Heading task, all methods perform reasonably well, but MCP still leads (0.976). The Carry task requires mobile manipulation (pickup, transport, place) and shows a large gap between MCP (0.575) and the next-best method, Latent Space (0.456). The only task where Scratch outperforms is the Ant Holdout, which involves a simple morphology and out-of-distribution transfer directions.

### Ablation: Number of Primitives
| k (Primitives) | Performance Trend |
|:--------------:|-------------------|
| 4 | Similar to k=8 |
| 8 | Best overall (default) |
| 16 | Slight decrease |
| 32 | Substantial decrease |

Performance degrades at k=32 because the gating weight dimensionality exceeds the action space dimension (e.g., 32 > 28 for the Humanoid), diminishing the benefits of multiplicative composition.

### Primitive Activation Analysis
Learned primitives develop interpretable, phase-dependent activation patterns. During locomotion, specific primitives activate during left stance vs. right stance phases, recovering a decomposition analogous to hand-designed gait-phase controllers. Pre-trained models produce structured exploration in downstream tasks (maintaining balance while exploring), whereas training from scratch results in immediate falling.

## Metrics Used
- [[Episode Return]] — normalized cumulative return (0-1 scale) used as the primary performance metric across all tasks and baselines, averaged over 3 seeds
- [[Success Rate]] — implicit in the Carry task evaluation, where the character must successfully pick up, transport, and place an object
- Normalized Return — primary metric: task reward normalized to [0, 1], with standard deviation reported across seeds

## Datasets Used
- [[CMU Motion Capture Database]] — 230 seconds of walking and turning motions used for Biped and Humanoid pre-training; no segmentation or labeling required
- Artist-generated keyframes — 11 seconds of T-Rex locomotion (1 forward walk, 2 left turns, 2 right turns) used for T-Rex pre-training

## Related Papers
- [[DeepMimic]] — provides the motion imitation pre-training framework that MCP builds upon; MCP reuses [[DeepMimic]]'s reward function and PPO training for the pre-training phase, then adds multiplicative composition for transfer
- [[DeepLoco]] — earlier hierarchical locomotion work by Peng; [[DeepLoco]]'s soccer dribbling task reappears in MCP as a transfer benchmark, and [[DeepLoco]]'s HLC/LLC hierarchy inspired MCP's primitive/gating decomposition
- [[SFV]] — video-based skill learning by Peng; the skills extracted from video via [[SFV]] could serve as pre-training data for MCP's primitives
- [[ASE]] — subsequent adversarial skill embedding approach that also pre-trains a reusable low-level controller, but uses GAN-based latent spaces rather than multiplicative composition; [[ASE]] scales to larger motion datasets than MCP
- [[CALM]] — extends [[ASE]] with conditional control over which motion style to execute; MCP's gating mechanism is a more explicit form of the style-selection that [[CALM]] learns implicitly
- [[MVAE]] — VAE-based latent action space for character control; MCP's Latent Space baseline is conceptually similar to [[MVAE]]'s approach, and MCP outperforms it on all complex tasks
- [[Hierarchical Puppeteer]] — hierarchical world model for humanoid control; the tracker/puppeteer decomposition parallels MCP's primitive/gating separation, with the tracker encoding reusable motor skills and the puppeteer encoding task strategy
