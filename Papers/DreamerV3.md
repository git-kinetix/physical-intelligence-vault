---
tags: [paper, world-model]
title: "Mastering Diverse Domains through World Models"
authors: [Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, Timothy Lillicrap]
year: 2023
arxiv: "https://arxiv.org/abs/2301.04104"
repo: "https://github.com/danijar/dreamerv3"
group: "World Models"
importance: 
aliases: [DreamerV3, Dreamer V3]
---

!PDFs/DreamerV3.pdf


# Mastering Diverse Domains through World Models

## Summary
DreamerV3 is a general-purpose reinforcement learning algorithm that masters a wide range of domains with a single set of hyperparameters, eliminating the need for domain-specific tuning. The key insight is a collection of robustness techniques -- symlog predictions, percentile-based return normalization, free bits for KL regularization, and unimix categoricals -- that enable stable learning across domains with vastly different reward scales, observation types, and action spaces. DreamerV3 is the first algorithm to collect diamonds in [[Minecraft]] from scratch without human demonstrations or curricula.

Evaluated across 7 benchmarks encompassing over 150 diverse tasks -- including [[Atari 2600 Games|Atari 100K]], [[DeepMind Control Suite]] (vision and proprioceptive), [[BSuite]], [[Crafter]], DMLab, and [[Minecraft]] -- DreamerV3 outperforms specialized methods that were individually tuned for each domain. The algorithm also demonstrates strong scaling properties: larger models consistently improve both final performance and data efficiency. This work was published at ICLR 2024 and later extended as a Nature publication covering over 150 tasks.

## Key Contributions
- A single RL algorithm with fixed hyperparameters that outperforms domain-specific methods across 7 benchmarks and 150+ tasks
- First algorithm to collect diamonds in [[Minecraft]] end-to-end from pixel observations without human data, curricula, or reward shaping
- Introduction of symlog predictions (symlog encoding + two-hot loss) for handling diverse reward and value scales
- Percentile-based return normalization that adapts to any reward magnitude
- Demonstration of favorable scaling properties: larger models consistently improve performance and data efficiency
- Free bits and unimix categoricals for robust KL regularization

## Architecture / Method
DreamerV3 builds on the RSSM world model from [[DreamerV2]], adding several robustness techniques:

**World Model (RSSM with improvements):**
- **Sequence model:** h_t = f_phi(h_{t-1}, z_{t-1}, a_{t-1}) using GRU (or Block GRU for larger models)
- **Encoder:** z_t ~ q_phi(z_t | h_t, x_t) with 32 categorical variables of 32 classes each
- **Dynamics predictor:** z_hat_t ~ p_phi(z_hat_t | h_t)
- **Decoders:** reward, continuation (discount), and image decoders

**Key Robustness Innovations:**

1. **Symlog Predictions:** Observations, rewards, and values are predicted in symlog space: symlog(x) = sign(x) * ln(|x| + 1). The inverse symexp(x) = sign(x) * (exp(|x|) - 1) is used to recover original scale. This compresses large values while preserving sign and small-value sensitivity.

2. **Two-Hot Encoding:** Continuous targets (rewards, values) are discretized into bins and encoded as two-hot vectors, allowing the model to represent arbitrary distributions.

3. **Percentile Return Normalization:** Returns are normalized by the 5th and 95th percentiles of the return distribution computed from recent imagined trajectories, enabling adaptation to any reward scale.

4. **Free Bits (KL):** KL divergence is clipped to max(KL, free_nats) with free_nats = 1.0, preventing posterior collapse while allowing sufficient regularization.

5. **Unimix Categoricals:** Categorical distributions use a mixture with a uniform distribution (1% weight), preventing the model from becoming overconfident and losing gradient signal.

6. **Block GRU:** For larger model sizes, a more parameter-efficient Block GRU replaces the standard GRU.

**Actor-Critic:** Same imagination-based training as [[DreamerV2]], with Reinforce + straight-through gradients for the actor and lambda-returns for the critic.

## Results

### Table 1: [[Atari 2600 Games|Atari 100K]] Benchmark (Selected Tasks, 400K Environment Frames)

| Task | Random | Human | DreamerV3 |
|------|--------|-------|-----------|
| Alien | 228 | 7,128 | 959 |
| Asterix | 210 | 8,503 | 932 |
| Battle Zone | 2,360 | 37,188 | 12,250 |
| Crazy Climber | 10,780 | 35,829 | 97,190 |
| Kung Fu Master | 258 | 22,736 | 21,420 |
| **[[Human Normalized Median]]** | 0% | 100% | **49%** |
| **[[Human Normalized Mean]]** | 0% | 100% | **112%** |

On the extremely data-limited [[Atari 2600 Games|Atari 100K]] benchmark (only 2 hours of real-time play), DreamerV3 achieves 49% human-normalized median and 112% mean, outperforming prior methods including the transformer-based [[IRIS]], model-free SPR, and SimPLe. The mean exceeding 100% indicates superhuman performance on several games even with very limited data.

### Table 2: [[DeepMind Control Suite|DMC]] Proprioceptive Control (500K Environment Steps)

| Task | D4PG | DreamerV3 |
|------|------|-----------|
| Acrobot Swingup | 125.5 | 154.5 |
| Finger Turn Hard | 379.2 | 841.0 |
| Hopper Hop | 67.5 | 111.0 |
| **Median** | 787.2 | **845.5** |
| **Mean** | 721.0 | **743.1** |

DreamerV3 outperforms D4PG on proprioceptive control tasks despite using a single configuration, while D4PG was tuned specifically for these tasks.

### Table 3: [[DeepMind Control Suite|DMC]] Visual Control (1M Environment Steps)

| Task | DrQ-v2 | DreamerV3 |
|------|--------|-----------|
| Acrobot Swingup | 128.4 | 210.0 |
| Cheetah Run | 691.0 | 728.7 |
| Finger Turn Hard | 220.0 | 810.8 |
| **Median** | 734.9 | **808.5** |
| **Mean** | 677.4 | **739.6** |

On visual control from pixels, DreamerV3 outperforms DrQ-v2 (a strong model-free baseline) by a significant margin, especially on harder tasks like Finger Turn Hard and Acrobot Swingup.

### Table 4: [[BSuite]] Results (Selected Categories)

| Category | Muesli | DreamerV3 |
|----------|--------|-----------|
| Catch | 0.955 | **0.970** |
| Mountain Car | 0.797 | **0.949** |
| Umbrella Distract | 0.217 | **0.957** |
| **Category Mean** | 0.537 | **0.627** |

DreamerV3 substantially outperforms Muesli on [[BSuite]], which tests fundamental RL capabilities like credit assignment, exploration, and memory. The large improvement on Umbrella Distract demonstrates superior handling of distractors.

### Table 5: [[Crafter|Crafter Benchmark]]

| Method | Score |
|--------|-------|
| **DreamerV3** | **14.5 +/- 1.6%** |
| LSTM-SPCNN | 12.1 +/- 0.8% |
| [[DreamerV2]] | 10.0 +/- 1.2% |
| PPO | 4.6 +/- 0.3% |
| Random | 1.6 +/- 0.0% |

On [[Crafter]] (a 2D survival game testing diverse skills), DreamerV3 achieves the highest score, outperforming both its predecessor [[DreamerV2]] and specialized methods.

### Table 6: [[Minecraft|Minecraft Diamond]] Collection

| Metric | Value |
|--------|-------|
| Seeds achieving diamonds | 24 of 40 |
| Average first diamond | 29.3M steps |
| Most diamonds in single seed | 6 |
| Total evaluation episodes | 50 across 40 seeds |

DreamerV3 is the first algorithm to collect diamonds in [[Minecraft]] end-to-end from scratch (without human data, curricula, or reward shaping). This requires a long sequence of 17+ subtasks including mining wood, crafting tools, finding caves, mining iron, smelting, and finally mining diamonds.

### Table 7: DMLab Results (50M Environment Steps)

| Method | Steps | Normalized Mean |
|--------|-------|-----------------|
| IMPALA | 10B | 51.3% |
| **DreamerV3** | **50M** | **54.2%** |

DreamerV3 matches or exceeds IMPALA's performance on DMLab using 200x fewer environment steps, demonstrating remarkable data efficiency on 3D navigation tasks.

## Metrics Used
- [[Human Normalized Median]] — median of per-game human-normalized scores; primary [[Atari 2600 Games|Atari 100K]] metric
- [[Human Normalized Mean]] — mean of per-game human-normalized scores
- [[Episode Return]] — cumulative reward per episode; primary metric for [[DeepMind Control Suite|DMC]], [[BSuite]], and [[Crafter]]
- [[Crafter Score]] — geometric mean of success rates across 22 achievements in [[Crafter]]
- [[BSuite Score]] — normalized score per category across 468 configurations
- [[Diamond Collection Rate]] — number of seeds successfully collecting diamonds in [[Minecraft]]
- [[Data Efficiency]] — performance as a function of environment steps

## Datasets Used
- [[Atari 100K]] — 26 Atari games with budget of 100K steps (400K frames with action repeat), testing extreme data efficiency
- DeepMind Control Suite (Vision) — continuous control tasks from pixels (64x64 RGB)
- DeepMind Control Suite (Proprioceptive) — continuous control tasks from state observations
- [[BSuite]] — 23 diagnostic environments with 468 configurations testing core RL capabilities
- [[Crafter]] — 2D open-world survival game with 22 achievements, testing diverse skill acquisition
- [[DMLab]] — 3D first-person navigation and exploration tasks
- [[Minecraft]] — open-ended 3D survival game; diamond collection as the primary evaluation task

## Related Papers
- [[DreamerV1]] — first [[DreamerV1|Dreamer]] agent with Gaussian latents and analytic value gradients
- [[DreamerV2]] — introduced discrete representations and KL balancing for Atari mastery
- DrQ-v2 — strong model-free baseline for visual continuous control
- PPO — widely applicable model-free policy gradient baseline
- IMPALA — scalable distributed actor-critic; baseline for DMLab
- [[IRIS]] — transformer-based world model baseline for [[Atari 2600 Games|Atari 100K]]
- SPR — self-predictive representations; model-free [[Atari 2600 Games|Atari 100K]] baseline
- Muesli — strong model-based baseline for [[BSuite]]
- TD-MPC2 — scalable world model for continuous control
