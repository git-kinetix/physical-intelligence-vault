---
tags: [paper, world-model, physics-simulation]
title: "Learning from Reward-Free Offline Data: A Case for Planning with Latent Dynamics Models"
authors: [Vlad Sobal, Wancong Zhang, Kyunghyun Cho, Randall Balestriero, Tim G. J. Rudner, Yann LeCun]
year: 2025
arxiv: "https://arxiv.org/abs/2502.14819"
repo: "https://github.com/vladisai/PLDM"
group: "World Models"
importance: 
aliases: [PLDM, Planning with Latent Dynamics Models]
---

!PDFs/PLDM.pdf

# Learning from Reward-Free Offline Data: A Case for Planning with Latent Dynamics Models

## Summary

PLDM (Planning with Latent Dynamics Models) addresses a core challenge in offline learning: how to train agents from trajectory data that lacks reward annotations and may be suboptimal. The paper systematically compares reinforcement learning and optimal control paradigms across six methods and 23 datasets on two navigation environments, evaluating six generalization properties required to scale to large offline datasets of suboptimal trajectories. The central finding is that model-based planning with a latent dynamics model trained via JEPA (Joint Embedding Predictive Architecture) emerges as the strongest approach for zero-shot generalization from imperfect offline data.

PLDM trains a latent dynamics model that predicts future latent states from current latent states and actions, using an L2 similarity loss with VICReg-inspired variance-covariance regularization to prevent representation collapse. At test time, PLDM performs planning via MPPI (Model Predictive Path Integral) to optimize action sequences that minimize the distance between predicted latent states and goal latent states, without requiring any reward function or policy learning. This enables flexible adaptation to new tasks (e.g., goal-avoidance) without retraining.

The paper demonstrates that while model-free goal-conditioned RL methods (GCIQL, HIQL) excel with abundant high-quality data, PLDM is the only method that achieves competitive performance across all settings, including low-data regimes, random-quality trajectories, unseen environment layouts, and novel tasks. PLDM is particularly strong in generalizing to out-of-distribution layouts and data-efficient learning, though it incurs higher inference cost due to online planning.

## Key Contributions

- Systematic comparison of six offline learning methods (HILP, HIQL, GCIQL, CRL, GCBC, PLDM) across 23 datasets and six generalization properties
- PLDM: a model-based planning approach using JEPA-trained latent dynamics with VICReg regularization and MPPI planning
- Demonstration that latent prediction (JEPA-style) outperforms pixel reconstruction (e.g., [[DreamerV3]]-style) for test-time planning representations
- PLDM achieves the best transfer to unseen environment layouts and novel tasks among all tested methods
- PLDM shows superior data efficiency, reaching ~80% [[Success Rate]] with only a few thousand transitions
- PLDM can adapt to entirely new task formulations (goal-avoidance) at test time without retraining, unlike policy-based methods

## Architecture / Method

PLDM consists of three main components:

**1. Encoder** $h_\theta$: Maps raw observations (64x64 pixel images) to latent state representations $z_0 = h_\theta(s_0)$.

**2. Ensemble of Predictors** $\{f_\theta^k\}_{k=1}^K$: Each predictor takes the previous latent state and action to predict the next latent state: $\hat{z}_t = f_\theta^k(\hat{z}_{t-1}, a_{t-1})$ for $k = 1, \ldots, K$. The ensemble provides uncertainty estimates used during planning.

**3. Training Objective**: The loss combines four components:
- **Similarity loss**: L2 distance between predicted and target latent states (target encoder is EMA-updated)
- **Variance regularization** ($\alpha$): Encourages each latent dimension to maintain variance, preventing collapse
- **Covariance regularization** ($\beta$): Decorrelates latent dimensions, encouraging diverse features
- **Time similarity** ($\delta$): Encourages features to capture time-varying information rather than static properties
- **Inverse Dynamics Model** ($\omega$): Predicts actions from consecutive latent states, improving action-relevant representations

**4. Planning via MPPI**: At test time, PLDM uses Model Predictive Path Integral control to optimize action sequences. The cost function minimizes L2 distance between the predicted latent state and the goal latent state, with an uncertainty regularization term from the predictor ensemble. PLDM replans at each step (or every $i$ steps for efficiency).

The approach is motivated by the insight that self-supervised latent prediction (JEPA-style) learns better representations for planning than pixel-level reconstruction, as confirmed by comparisons showing that reconstruction-based methods like [[DreamerV3]] underperform in test-time planning.

## Results

### Table 1: Generalization Stress-Testing Summary

Summary of method performance across six generalization properties (three stars = strong, two = moderate, one = weak):

| Property | HILP | HIQL | GCIQL | CRL | GCBC | PLDM |
|----------|------|------|-------|-----|------|------|
| Transfer to new environment layouts | 1/3 | 1/3 | 1/3 | 1/3 | 1/3 | 3/3 |
| Transfer to a new task | 2/3 | 1/3 | 1/3 | 1/3 | 1/3 | 3/3 |
| Data efficiency | 1/3 | 2/3 | 3/3 | 2/3 | 2/3 | 3/3 |
| Best-case performance | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 | 3/3 |
| Learn from random policy trajectories | 3/3 | 1/3 | 3/3 | 1/3 | 1/3 | 2/3 |
| Stitch suboptimal trajectories | 3/3 | 1/3 | 3/3 | 1/3 | 1/3 | 2/3 |

PLDM is the only method that achieves strong (3/3) performance on environment transfer, task transfer, data efficiency, and best-case performance simultaneously. HILP excels at learning from random data and trajectory stitching but fails to transfer to new layouts.

### Table 2: Two-Rooms Best-Case Performance (Good-Quality Data vs. No Door-Passing Trajectories)

| Method | Good-quality data | No door-passing trajectories |
|--------|-------------------|------------------------------|
| CRL | 189.3 +/- 10.7 | 114.7 +/- 14.1 |
| GCBC | 186.0 +/- 12.0 | 118.4 +/- 11.2 |
| GCIQL | 198.0 +/- 10.9 | 199.6 +/- 10.4 |
| HILP | 100.0 +/- 10.0 | 100.0 +/- 10.0 |
| HIQL | 196.4 +/- 11.3 | 126.3 +/- 15.6 |
| PLDM | 197.8 +/- 10.7 | 134.4 +/- 12.7 |

With good-quality data, GCIQL (198.0) and PLDM (197.8) lead. When door-passing trajectories are removed, GCIQL maintains strong performance (199.6) while most other methods degrade significantly. HILP's lower scores reflect a different measurement scale (it uses a distance-based representation that doesn't directly optimize the same reward). PLDM (134.4) degrades less than CRL, GCBC, and HIQL, demonstrating better trajectory stitching.

### Table 3: Diverse PointMaze Dataset Parameters

| # Transitions | # Layouts | # Episodes/Layout | Episode Length |
|---------------|-----------|-------------------|----------------|
| 1,000,000 | 5 | 2,000 | 100 |
| 1,000,000 | 10 | 1,000 | 100 |
| 1,000,000 | 20 | 500 | 100 |
| 1,000,000 | 40 | 250 | 100 |

The total number of transitions is held constant at 1M while varying layout diversity. As the number of layouts increases, episodes per layout decrease proportionally.

### Table 4: Single Maze Setting — [[Success Rate]]

| Method | [[Success Rate]] |
|--------|-------------|
| GCIQL | 1.000 +/- 0.000 |
| HIQL | 1.000 +/- 0.000 |
| HILP | 1.000 +/- 0.000 |
| PLDM | 0.990 +/- 0.001 |
| CRL | 0.980 +/- 0.001 |
| GCBC | 0.970 +/- 0.024 |

In the simplest single-maze setting with high-quality data, goal-conditioned RL methods (GCIQL, HIQL, HILP) achieve perfect [[Success Rate]]. PLDM reaches 0.990, slightly below perfect, since its training objective is dynamics prediction rather than direct policy optimization. This represents the "best-case" scenario where model-free methods have the advantage of abundant, high-quality, in-distribution data.

### Table 5: PLDM Loss Component Ablation Study

| Ablation | [[Success Rate]] (Two-Rooms) | [[Success Rate]] (Diverse Maze) |
|----------|-------------------------------|----------------------------------|
| Full model | 98.0 +/- 1.5 | 98.7 +/- 2.8 |
| w/o variance coeff ($\alpha$) | 13.4 +/- 9.2 | 11.4 +/- 6.5 |
| w/o covariance coeff ($\beta$) | 29.2 +/- 4.4 | 7.8 +/- 4.1 |
| w/o time similarity ($\delta$) | 71.0 +/- 3.0 | 95.6 +/- 3.2 |
| w/o IDM coeff ($\omega$) | 98.0 +/- 1.5 | 75.5 +/- 8.2 |

Variance and covariance regularization are critical — removing either causes catastrophic failure (13.4% and 29.2% respectively on Two-Rooms), confirming that VICReg-style collapse prevention is essential. Time similarity has a moderate impact on Two-Rooms (71.0%) but minimal impact on Diverse Maze (95.6%). The Inverse Dynamics Model is critical for Diverse Maze generalization (75.5% without it) but not for Two-Rooms, suggesting it helps learn action-relevant features needed for cross-layout transfer.

### Computational Cost (Two-Rooms)

| Method | Replan Interval | Time/Episode (sec) |
|--------|-----------------|-------------------|
| PLDM | Every 1 step | 13.44 +/- 0.11 |
| GCIQL | N/A (policy) | 0.12 +/- 0.03 |
| HIQL | N/A (policy) | 0.16 +/- 0.03 |

PLDM is approximately 100x slower than model-free methods at inference due to online MPPI planning at every step. This is a key limitation — while PLDM excels in generalization, the computational overhead makes it significantly more expensive at deployment.

## Metrics Used

- [[Success Rate]] — primary evaluation metric; percentage of episodes where the agent reaches the goal state within the time limit across all environments (Two-Rooms, Diverse PointMaze, Ant-U-Maze)
- Reward/return — used in Two-Rooms environment to measure cumulative task performance (Table 2)

## Datasets Used

- Two-Rooms Environment — custom 2D point-mass navigation with 64x64 pixel observations, 2D displacement actions, two rooms connected by a door; used for best-case performance, data quality, data efficiency, trajectory stitching, and task transfer experiments
- Diverse PointMaze — configurable maze layouts with RGB image observations and 2D acceleration actions; used for cross-layout generalization experiments with 5/10/20/40 training layouts
- Ant-U-Maze — U-shaped maze with quadruped locomotion (29D state, 8D actions); used for trajectory stitching experiments with varying episode lengths

## Related Papers

- [[V-JEPA]] — PLDM's latent dynamics model is inspired by JEPA's self-supervised latent prediction philosophy; [[V-JEPA]] applies this to video representation learning
- [[V-JEPA 2]] — extension of [[V-JEPA]] for video understanding; shares the JEPA latent prediction framework that PLDM adapts for dynamics modeling
- [[I-JEPA]] — image-based JEPA; foundational architecture that PLDM's encoder builds upon
- [[TD-JEPA]] — combines temporal difference learning with JEPA for zero-shot RL; complementary approach to PLDM's planning-based method, both leveraging JEPA for control
- [[DreamerV3]] — reconstruction-based world model baseline; paper explicitly compares against [[DreamerV3]]-style pixel reconstruction and finds JEPA-style latent prediction superior for planning
- [[DreamerV2]] — predecessor world model using reconstruction; PLDM's latent prediction approach is motivated as an alternative to reconstruction-based dynamics
- [[DreamerV1]] — original [[DreamerV1|Dreamer]] world model; part of the reconstruction-based lineage that PLDM departs from
- [[DIAMOND]] — diffusion-based world model; another approach to learned dynamics that differs from PLDM's JEPA-based latent prediction
- [[IRIS]] — transformer-based world model with discrete tokens; alternative world model architecture
- [[UniPi]] — uses diffusion models for planning with video prediction; shares PLDM's planning-at-test-time philosophy but operates in pixel space
- [[Le-World-Model]] — JEPA-based world model; closely related to PLDM's approach of using JEPA for dynamics prediction
- [[ACT-JEPA]] — action-conditioned JEPA for world modeling; directly related architecture using JEPA with action conditioning similar to PLDM
- [[Stable World Model]] — another learned world model approach; part of the broader landscape of world models that PLDM contributes to
- [[PEVA]] — video prediction conditioned on actions; related work on action-conditioned prediction, though focused on egocentric video
