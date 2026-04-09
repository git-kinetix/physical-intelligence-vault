---
tags: [paper, jepa]
title: "ACT-JEPA: Novel Joint-Embedding Predictive Architecture for Efficient Policy Representation Learning"
authors: [Aleksandar Vujinovic, Aleksandar Kovacevic]
year: 2025
arxiv: "https://arxiv.org/abs/2501.14622"
repo: ""
group: "JEPA Family"
importance: 
aliases: [ACT-JEPA, Action JEPA]
---

![[PDFs/ACT-JEPA.pdf]]

# ACT-JEPA: Novel Joint-Embedding Predictive Architecture for Efficient Policy Representation Learning


## Summary

ACT-JEPA unifies imitation learning (IL) and self-supervised learning (SSL) to enhance policy representations for robot manipulation. The key insight is that jointly predicting action sequences and latent observation sequences provides a mutual regularization effect: the JEPA objective prevents overfitting to demonstration data by modeling environment dynamics, while the IL objective ensures the world model prioritizes control-relevant features. The architecture is trained end-to-end, learning shared representations that improve both policy performance and world model quality.

The method builds on the ACT (Action Chunking with Transformers) framework by adding a JEPA-based latent prediction branch. Four transformer-based components work together: a context encoder maps current observations to latent states, a target encoder (with EMA updates) encodes future observations into latent targets, a predictor forecasts future latent states via cross-attention, and an action decoder generates action sequences. Evaluated across [[Push-T]], ManiSkill, and Meta-World benchmarks, ACT-JEPA achieves up to 40% improvement in world model understanding (measured via probing) and up to 10% higher task success rates compared to the strongest ACT baseline. Critically, the joint end-to-end optimization is essential -- a two-stage approach (pre-train JEPA then fine-tune for actions) catastrophically fails.

## Key Contributions

- Unifies imitation learning and JEPA-based self-supervised learning in a single end-to-end architecture
- Demonstrates mutual regularization: JEPA prevents IL overfitting, IL ensures control-relevant world model features
- Achieves up to 40% reduction in world model prediction error ([[RMSE]]/[[Absolute Trajectory Error (ATE)|ATE]]) over ACT baselines
- Achieves up to 10% higher task success rate across manipulation benchmarks
- Shows that joint optimization is critical -- two-stage approaches catastrophically fail
- Validates across three diverse benchmarks: [[Push-T]] (2D), ManiSkill (3D sim), and Meta-World (multi-task)

## Architecture / Method

ACT-JEPA consists of four transformer-based components:

**1. Context Encoder $E_\theta$:** Encodes the current observation (RGB image) into a latent state representation $s_x = E_\theta(o_t)$. Uses a ResNet-18 backbone for image feature extraction followed by a transformer encoder.

**2. Target Encoder $E_{\bar{\theta}}$:** Encodes future observation sequences $o_{t+1:t+n}$ into latent target representations $s_{y_{t:t+n}}$. Updated via exponential moving average (EMA) of the context encoder weights (same architecture, no gradient).

**3. Predictor $P_\phi$:** Predicts future latent observation states using cross-attention on the context encoder representation. Takes the context latent $s_x$ and predicts $\hat{s}_{y_{t:t+n}}$ to match the target encoder outputs.

**4. Action Decoder $D_\tau$:** Generates action sequences using cross-attention on the context representation. Produces chunked action predictions $\hat{a}_{t:t+H}$ where $H$ is the action horizon.

**Training Objectives:**

The combined loss is:

$$\mathcal{L} = \mathcal{L}_{action} + \mathcal{L}_{obs}$$

- **Action Loss:** $\mathcal{L}_{action} = \|a_{t:t+H} - \hat{a}_{t:t+H}\|_1$ (L1 between predicted and target actions)
- **Observation Loss:** $\mathcal{L}_{obs} = \|s_{y_{t:t+n}} - \hat{s}_{y_{t:t+n}}\|_1$ (L1 in latent space between predicted and target latent states)

**Key Design Choices:**
- End-to-end joint optimization (not staged pre-training + fine-tuning)
- Cross-attention mechanism for both predictor and action decoder
- ResNet-18 backbone for image encoding at 96x96 or 128x128 resolution
- EMA target encoder following JEPA convention

## Results

### Table 1: World Model Evaluation (Probing — Frozen Encoder + Trained Decoder for Future Proprioceptive State Prediction)

| Method   | [[Push-T]] [[RMSE]] ↓ | [[Push-T]] [[Absolute Trajectory Error (ATE) ]] ↓ | ManiSkill [[RMSE]] ↓ | ManiSkill [[Absolute Trajectory Error (ATE) ]] ↓ | Meta-World [[RMSE]] ↓ | Meta-World [[Absolute Trajectory Error (ATE) ]] ↓ |
| ------ | --------------------- | ------------------------------------------------- | -------------------- | ------------------------------------------------ | --------------------- | ------------------------------------------------- |
| ACT      | 0.1424                | 0.1518                                            | 0.0531               | 0.2063                                           | 0.0295                | 0.0529                                            |
| ACT-JEPA | 0.0895                | 0.0915                                            | 0.0348               | 0.1354                                           | 0.0208                | 0.0375                                            |

ACT-JEPA achieves 29-40% reduction in world model prediction error across all benchmarks. The improvement is largest on [[Push-T]] (37% [[RMSE]] reduction, 40% [[Absolute Trajectory Error (ATE)|ATE]] reduction) and ManiSkill (34% [[RMSE]], 34% [[Absolute Trajectory Error (ATE)|ATE]]), demonstrating that the JEPA objective substantially enriches the learned representations with dynamics-relevant information.

### Table 2: Policy Performance (Average [[Success Rate|Task Success Rate]] %)

| Method | [[Push-T]] (1 task) ↑ | ManiSkill (5 tasks) ↑ | Meta-World (15 tasks) ↑ |
|--------|-------------------|----------------------|------------------------|
| AR Transformer | 0% | 8% | 38.3% |
| ACT | 34% | 26% | 90% |
| ACT-JEPA | 41% | 36% | 92% |

ACT-JEPA outperforms ACT across all benchmarks: +7% on [[Push-T]], +10% on ManiSkill (the largest gain, representing a 38.5% relative improvement), and +2% on Meta-World. The AR Transformer baseline without chunking fails on [[Push-T]] entirely and struggles on ManiSkill, highlighting the importance of action chunking. Meta-World shows the smallest gap because ACT already achieves 90%, leaving less room for improvement.

### Table 3: Joint Optimization vs. Two-Stage Approach (Average [[Success Rate|Task Success Rate]] %)

| Method | [[Push-T]] ↑ | ManiSkill ↑ | Meta-World ↑ |
|--------|----------|------------|--------------|
| ACT-JEPA (End-to-end) | 41% | 36% | 92% |
| Two-Stage (Pre-train JEPA → Fine-tune Actions) | 27% | 0% | 23.3% |

The two-stage approach catastrophically fails, particularly on ManiSkill (0% success) and Meta-World (23.3% vs 92%). This demonstrates that joint optimization is essential -- pre-training JEPA representations then fine-tuning for actions does not transfer the dynamics knowledge effectively. The mutual regularization from simultaneous optimization is the key mechanism.

## Metrics Used

- [[Success Rate]] — primary metric for policy evaluation; percentage of successfully completed tasks across evaluation episodes
- [[RMSE]] — [[RMSE|Root Mean Squared Error]]; used for world model probing evaluation measuring prediction accuracy of future proprioceptive states
- [[ATE]] — Absolute Trajectory Error; measures distance between predicted and ground-truth trajectories in world model probing
- [[Action Reconstruction Loss]] — L1 loss for action prediction quality during training

## Datasets Used

- [[Push-T]] — 2D manipulation task with 206 human demonstrations at 96x96 RGB resolution; push a T-shaped block to a target pose
- [[ManiSkill]] — 5 robotic manipulation tasks with 50 demonstrations per task at 128x128 RGB resolution; simulated 3D robot manipulation
- [[Meta-World]] — 15 diverse manipulation tasks with 40 demonstrations per task at 128x128 RGB resolution; multi-task robot learning benchmark

## Related Papers

- [[V-JEPA]] — foundational video JEPA; ACT-JEPA adapts the JEPA framework from video understanding to action-conditioned policy learning
- [[V-JEPA 2]] — extends [[V-JEPA]] with planning; shares the vision of using JEPA for embodied decision-making
- [[I-JEPA]] — image-based JEPA; ACT-JEPA builds on the same latent prediction paradigm but adds action decoding
- [[Le-JEPA]] — theoretical foundations for JEPA training; relevant to ACT-JEPA's design of the latent prediction loss
- [[TD-JEPA]] — applies temporal difference learning to JEPA for RL; complementary approach to using JEPA for control (unsupervised RL vs imitation learning)
- [[Le-World-Model]] — JEPA-based world model; ACT-JEPA can be seen as learning a world model jointly with a policy
- [[Pi0]] — VLA model for robot manipulation; ACT-JEPA addresses a similar problem domain (manipulation from demonstrations) with a fundamentally different architecture
- [[DreamerV3]] — world model for RL; ACT-JEPA shares the idea of jointly learning dynamics and policy but uses JEPA latent prediction instead of reconstruction
