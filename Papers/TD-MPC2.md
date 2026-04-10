---
tags: [paper, world-model, physics-simulation]
title: "TD-MPC2: Scalable, Robust World Models for Continuous Control"
authors: [Nicklas Hansen, Hao Su, Xiaolong Wang]
year: 2024
arxiv: "https://arxiv.org/abs/2310.16828"
repo: "https://github.com/nicklashansen/tdmpc2"
group: "World Models"
importance: 
aliases: [TD-MPC2, TDMPC2]
---

!PDFs/TD-MPC2.pdf

# TD-MPC2: Scalable, Robust World Models for Continuous Control

## Summary
TD-MPC2 is a model-based reinforcement learning algorithm that performs local trajectory optimization (planning) in the latent space of a learned implicit (decoder-free) world model. It builds on the original TD-MPC algorithm (Hansen et al., 2022) with a series of improvements focused on algorithmic robustness and scalability. The key contributions are (1) improved algorithmic robustness by revisiting core design choices (SimNorm, discrete regression, ensemble Q-functions, maximum entropy policy prior), and (2) careful architectural design that can accommodate datasets with multiple embodiments and action spaces without relying on domain knowledge. TD-MPC2 uses a single set of hyperparameters across all 104 tasks.

Evaluated on 104 diverse continuous control tasks spanning 4 domains -- [[DeepMind Control Suite]] (39 tasks), Meta-World (50 tasks), ManiSkill2 (5 tasks), and MyoSuite (10 tasks) -- TD-MPC2 consistently outperforms existing model-based and model-free methods including SAC, [[DreamerV3]], TD-MPC, CURL, and DrQ-v2. The paper further demonstrates that TD-MPC2 scales to a single 317M parameter agent that performs 80 tasks across multiple domains, embodiments, and action spaces, with performance consistently increasing with model and data size. Published as a Spotlight at ICLR 2024.

## Key Contributions
- A model-based RL algorithm that achieves state-of-the-art performance across 104 continuous control tasks with a **single set of hyperparameters**, eliminating per-task tuning
- Introduction of **SimNorm** (Simplicial Normalization): projects latent representations onto fixed-dimensional simplices via softmax, biasing toward sparsity without enforcing hard constraints
- **Discrete regression** for reward and value prediction in log-transformed space, making the objective magnitude-independent across tasks
- Demonstration of **scaling laws** for world models: a single 317M parameter multitask agent trained on 80 tasks across 12 embodiments, with capabilities consistently increasing with model size
- **Learnable task embeddings** that condition all model components and enable multitask and few-shot learning
- **Action masking** via zero-padding to accommodate varying observation and action space dimensions without domain knowledge
- Release of 300+ model checkpoints, datasets (545M and 345M transitions), and code

## Architecture / Method
TD-MPC2 learns an implicit, control-centric world model that predicts outcomes (returns) conditioned on action sequences, without decoding observations. The architecture consists of five MLP components, all using LayerNorm + Mish activations:

1. **Encoder** h: Maps observations s to normalized latent representations z (via SimNorm)
2. **Latent dynamics** d: Models forward dynamics z' = d(z, a, e) in latent space
3. **Reward predictor** R: Predicts reward r of a transition
4. **Terminal value** Q: Predicts discounted sum of future rewards (ensemble of 5 Q-functions with 1% dropout)
5. **Policy prior** p: Predicts action a* that maximizes Q, trained as a stochastic maximum entropy RL policy

All components are conditioned on a learnable task embedding e (96-dimensional, L2-norm constrained to 1).

**Model objective:** Components are jointly optimized via:
- Joint-embedding prediction (latent dynamics matching via stop-gradient)
- Cross-entropy loss for reward and value prediction (discrete regression with 101 bins in log-transformed space)
- Temporal weighting with coefficient lambda = 0.5

**Planning:** TD-MPC2 uses Model Predictive Path Integral (MPPI) for local trajectory optimization at inference time. The planner samples 512 action sequences, evaluates them using the world model (rolling out H=3 steps and bootstrapping with the learned terminal value Q), and iteratively refines the sampling distribution. The policy prior guides initial sampling and reduces computational cost.

**Simplicial Normalization (SimNorm):** A key innovation for training stability. The latent representation z is partitioned into L groups, and each group is projected onto a simplex via softmax with temperature tau. This can be seen as a "soft" variant of VQ-VAE that biases toward sparsity without hard constraints.

**Multitask design:** Task embeddings, zero-padding for variable observation/action dimensions, and action masking during planning enable a single model to handle diverse tasks without domain knowledge.

## Results

### Table 1: Multi-task Scaling — Training Cost and [[Normalized Task Score|Normalized Score]] (80-Task Dataset)

| Params (M) | GPU Days (RTX 3090) | [[Normalized Task Score]] |
|------------|---------------------|------------------|
| 1 | 3.7 | 16.0 |
| 5 | 4.2 | 49.5 |
| 19 | 5.3 | 57.1 |
| 48 | 12 | 68.0 |
| **317** | **33** | **70.6** |

The normalized score is an average of individual task [[Success Rate|success rates]] (Meta-World) and [[Episode Return|episode returns]] normalized to [0, 100] (DMControl). Performance consistently increases with model size and does not appear to saturate at 317M parameters. Training cost scales sub-linearly: the 317M model requires only ~9x the GPU days of the 1M model while achieving 4.4x the normalized score.

### Table 2: Single-task Aggregate Performance (Figure 1 / Figure 4, approximate from bar charts)

| Domain | Tasks | SAC | [[DreamerV3]] | TD-MPC | **TD-MPC2** |
|--------|-------|-----|-----------|--------|-------------|
| DMControl | 39 | ~550 | ~540 | ~650 | **~700** |
| Meta-World | 50 | ~50 | ~30 | ~65 | **~75** |
| ManiSkill2 | 5 | ~40 | ~45 | ~55 | **~90** |
| Locomotion | 7 | ~50 | ~60 | ~70 | **~90** |
| MyoSuite | 10 | ~45 | ~55 | ~55 | **~60** |

*Note: Single-task results are presented as learning curves (Figures 4, 12-16) rather than tabular data. Values above are approximate aggregates read from bar charts in Figure 1. DMControl is measured in [[Episode Return]] (0-1000 scale); Meta-World, ManiSkill2, and MyoSuite are measured in [[Success Rate]] (0-100%). All methods use 3 seeds. TD-MPC2 uses the same hyperparameters across all tasks, while SAC and TD-MPC use per-task hyperparameters.*

TD-MPC2 outperforms all baselines across all four domains. The MyoSuite results are particularly noteworthy as the authors did not run any TD-MPC2 experiments on this benchmark prior to the reported results. [[DreamerV3]] experiences numerical instabilities on Dog tasks and generally struggles with fine-grained object manipulation. TD-MPC sometimes diverges due to exploding gradients (e.g., Walker Stand, Walker Walk), while TD-MPC2 remains stable.

### Table 3: Multi-task Scaling Across Dataset Sizes (Figure 22)

| Params (M) | DMControl 15 tasks | DMControl 30 tasks | [[DeepMind Control Suite]] + Meta-World 80 tasks |
|------------|-------------------|-------------------|--------------------------|
| 1 | — | 18.9 | 16.0 |
| 5 | 61.1 | 28.1 | 49.5 |
| 19 | 78.0 | 54.2 | 57.1 |
| 48 | 80.5 | 59.4 | 68.0 |
| 317 | — | 71.4 | 70.6 |

*Values read from Figure 22.* Performance scales with model size across all dataset sizes. Scores are higher on smaller task suites when comparing similar model capacities, since the model capacity is the same but there are fewer tasks to learn.

### Table 4: Test-Time Regularization (Table 10)

| No reg. | c = 0.001 | c = 0.01 | c = 0.1 |
|---------|-----------|----------|---------|
| 56.54 | 58.14 | **62.01** | 44.13 |

[[Normalized Task Score]] of a 19M parameter TD-MPC2 agent on the 80-task dataset with varying regularization strength c. The regularization penalizes trajectories with high Q-function ensemble disagreement during planning. Moderate regularization (c = 0.01) improves performance by ~10%, while too-strong regularization (c = 0.1) degrades it.

### Table 5: Ablation — Actor Choice (Figure 9, approximate bar chart values for 80-task multitask)

| Actor | 3 Tasks (Single) | Multitask (80) |
|-------|-------------------|----------------|
| Policy only | ~42.2 | ~48 |
| Planning only | ~51 | ~53.7 |
| **Planning + policy** | **~54** | **~54.2** |

### Table 6: Ablation — Normalization (Figure 9)

| Normalization | 3 Tasks (Single) | Multitask (80) |
|---------------|-------------------|----------------|
| No Norm | ~46.5 | ~35 |
| SimNorm | ~51 | ~51.0 |
| LN + SimNorm | ~54 | ~54.2 |

### Table 7: Ablation — Q-functions Ensemble Size (Figure 9)

| # Q-functions | 3 Tasks (Single) | Multitask (80) |
|---------------|-------------------|----------------|
| 2 | ~53.5 | ~54.2 |
| **5** | **~54** | **~54.2** |
| 10 | ~53 | ~57.8 |

### Table 8: Model Configurations (Table 9)

| | 1M | 5M* | 19M | 48M | 317M |
|--|-----|-----|-----|-----|------|
| Encoder dim | 256 | 256 | 1024 | 1792 | 4096 |
| MLP dim | 384 | 512 | 1024 | 1792 | 4096 |
| Latent state dim | 128 | 512 | 768 | 768 | 1376 |
| # encoder layers | 2 | 2 | 3 | 4 | 5 |
| # Q-functions | 2 | 2 | 5 | 5 | 8 |
| Task embedding dim | 96 | 96 | 96 | 96 | 96 |

*5M (base) is the default for single-task online RL experiments.

### Table 9: Environment Details (Table 6)

| | DMControl | Meta-World | ManiSkill2 | MyoSuite |
|--|-----------|------------|------------|----------|
| Episode length | 1,000 | 200 | 200 | 100 |
| Action repeat | 2 | 2 | 2 | 1 |
| Effective length | 500 | 100 | 100 | 100 |
| Total env. steps | 4M - 14M | 2M | 4M - 14M | 2M |
| Performance metric | Reward | Success | Success | Success |

DMControl tasks use [[Episode Return]] as the performance metric, while Meta-World, ManiSkill2, and MyoSuite use [[Success Rate]]. An episode is only considered successful if the final step meets the success criterion (a stricter definition than some prior work).

## Metrics Used
- [[Episode Return]] — primary performance metric for [[DeepMind Control Suite]] tasks (scale 0-1000)
- [[Success Rate]] — primary performance metric for Meta-World, ManiSkill2, and MyoSuite tasks
- [[Normalized Task Score]] — aggregate metric for multitask evaluation; averages individual task success rates and episode returns normalized to [0, 100]

## Datasets Used
- [[DeepMind Control Suite]] — 39 continuous control tasks (19 original + 11 new custom tasks including Locomotion subset with Humanoid and Dog embodiments); observation dims range from 3 to 223, action dims from 1 to 38
- Meta-World — 50 robotic manipulation tasks with shared embodiment (observation dim 39, action dim 4); used for single-task benchmarking and multi-task training
- ManiSkill2 — 5 object manipulation tasks including the challenging Pick YCB task with 74 objects; high degree of randomization and task variation
- MyoSuite — 10 musculoskeletal motor control tasks with physiologically accurate hand; high-dimensional action space (39 dims) including easy (fixed goal) and hard (random goal) variants

## Related Papers
- [[DreamerV3]] — primary model-based baseline; uses a generative (decoder-based) world model with RSSM, while TD-MPC2 uses an implicit (decoder-free) world model. [[DreamerV3]] experiences numerical instabilities on Dog tasks and struggles with fine-grained manipulation
- [[DreamerV2]] — predecessor to [[DreamerV3]]; categorical latent space design influenced TD-MPC2's discrete regression approach
- [[DreamerV1]] — foundational [[DreamerV1|Dreamer]] architecture using RSSM world models
- [[IRIS]] — transformer-based world model for Atari; mentioned in context of discrete action spaces which TD-MPC2 does not address
- [[DIAMOND]] — diffusion-based world model; related approach to learning environment dynamics
- [[TD-JEPA]] — combines temporal difference learning with joint-embedding predictive architectures, sharing the TD-learning and latent-space prediction paradigm with TD-MPC2
- [[Stable World Model]] — addresses training stability in world models, a concern also central to TD-MPC2's SimNorm and gradient stability improvements
