---
tags: [paper, world-model]
title: "Mastering Atari with Discrete World Models"
authors: [Danijar Hafner, Timothy Lillicrap, Mohammad Norouzi, Jimmy Ba]
year: 2021
arxiv: "https://arxiv.org/abs/2010.02193"
repo: "https://github.com/danijar/dreamerv2"
group: "World Models"
importance: 
aliases: [DreamerV2, Dreamer V2]
---

![[PDFs/DreamerV2.pdf]]


# Mastering Atari with Discrete World Models

## Summary
DreamerV2 is the first world-model-based reinforcement learning agent to achieve human-level performance on the Atari benchmark of 55 games. Building on [[DreamerV1]], it introduces two critical innovations: (1) replacing Gaussian latent variables with categorical (discrete) latent representations in the world model, and (2) KL balancing to improve the training dynamics of the RSSM. These changes enable the world model to more accurately capture the discrete, multi-modal nature of Atari environments.

The agent learns behaviors purely from predictions in the compact latent space of the world model. At 200M environment frames, DreamerV2 achieves a gamer-normalized median score of 2.15 and a gamer-normalized mean of 11.33, surpassing both IQN (1.29 median, 8.85 mean) and Rainbow (1.47 median, 9.12 mean), which are the top single-GPU model-free agents. Critically, DreamerV2 matches the computational budget and wall-clock time of these baselines while achieving strictly superior performance across all four aggregation metrics. The paper also demonstrates that DreamerV2 generalizes to continuous control, solving humanoid stand-up and walking tasks from pixels.

## Key Contributions
- First world-model-based agent to achieve human-level performance on the Atari benchmark (55 games)
- Introduction of categorical (discrete) latent representations for world models, outperforming Gaussian latents on 42 of 55 games
- KL balancing technique that separately scales gradients for the prior and posterior, improving world model training stability
- Demonstration that stopping reward gradients can improve representation learning by encouraging more general latent representations
- Ablation study quantifying the contribution of each design choice

## Architecture / Method
DreamerV2 extends the RSSM world model from [[DreamerV1]] with key architectural changes:

**Discrete RSSM World Model:**
- **Recurrent model:** h_t = f_phi(h_{t-1}, z_{t-1}, a_{t-1})
- **Representation model:** z_t ~ q_phi(z_t | h_t, x_t) — outputs a vector of 32 categorical distributions, each over 32 classes
- **Transition predictor:** z_hat_t ~ p_phi(z_hat_t | h_t) — predicts next latent from deterministic state alone
- **Decoders:** image decoder, reward predictor, discount predictor

The categorical latent state is represented as a vector of 32 independent categorical variables, each with 32 classes, giving a total of 32 x 32 = 1024 possible combinations per variable, enabling highly expressive discrete representations.

**KL Balancing:**
The KL loss is split into two parts with mixing coefficient alpha = 0.8:
- KL_loss = alpha * KL(sg(posterior) || prior) + (1 - alpha) * KL(posterior || sg(prior))
where sg() denotes stop-gradient. This encourages the prior (transition model) to become more accurate while allowing the posterior (representation model) to maintain rich representations.

**Actor-Critic in Imagination:**
- Actor trained with a combination of Reinforce and straight-through gradients
- Critic uses lambda-returns estimated from imagined trajectories
- Discount predictor replaces fixed discount, enabling the model to learn about episode boundaries

## Results

### Table 1: Atari Performance at 200M Environment Steps (55 Games, Sticky Actions)

| Agent | Gamer Median | Gamer Mean | Record Mean | Clipped Record Mean |
|-------|-------------|------------|-------------|-------------------|
| **DreamerV2** | **2.15** | **11.33** | **0.44** | **0.28** |
| IQN | 1.29 | 8.85 | 0.21 | 0.21 |
| Rainbow | 1.47 | 9.12 | 0.17 | 0.17 |
| C51 | 1.09 | 7.70 | 0.15 | 0.15 |
| DQN | 0.65 | 2.84 | 0.12 | 0.12 |

DreamerV2 outperforms all baselines across every aggregation metric. The gamer median of 2.15 means the agent exceeds human-level performance on over half of the 55 games. The particularly large gap in Record Mean (0.44 vs 0.21 for IQN) shows DreamerV2 achieves strong absolute scores, not just human-relative ones. Notably, Rainbow outperforms IQN on gamer median but underperforms on the other three metrics, showing the importance of evaluating with multiple aggregation methods.

### Table 2: Ablation Study at 200M Environment Steps

| Variant | Gamer Median | Gamer Mean | Record Mean | Clipped Record Mean |
|---------|-------------|------------|-------------|-------------------|
| **DreamerV2 (full)** | **1.64** | **11.33** | **0.36** | **0.25** |
| No Layer Norm | 1.66 | 5.95 | 0.38 | 0.25 |
| No Reward Gradients | 1.68 | 6.18 | 0.37 | 0.24 |
| No Discrete Latents | 1.08 | 3.71 | 0.24 | 0.19 |
| No KL Balancing | 0.84 | 3.49 | 0.19 | 0.16 |
| No Policy Reinforce | 0.69 | 2.74 | 0.16 | 0.15 |
| No Image Gradients | 0.04 | 0.31 | 0.01 | 0.01 |

The ablation reveals the relative importance of each component. Image gradients are the most critical (removing them destroys performance entirely). The Policy Reinforce loss and KL Balancing are the next most important. Interestingly, removing reward gradients slightly improves the median, suggesting that representations not specifically trained to predict past rewards may generalize better. Discrete latents provide a substantial boost over Gaussian alternatives, particularly on the mean metrics.

## Metrics Used
- [[Gamer Normalized Median]] — median of per-game human-normalized scores across 55 Atari games; primary aggregate metric
- [[Gamer Normalized Mean]] — mean of per-game human-normalized scores; sensitive to outlier performance
- [[Record Normalized Mean]] — scores normalized by world record rather than human performance
- [[Clipped Record Normalized Mean]] — record-normalized scores clipped to [0, 1] to reduce outlier influence
- [[Episode Return]] — raw cumulative reward per episode

## Datasets Used
- [[Atari 2600 Games]] — 55 Atari games from the Arcade Learning Environment ([[Atari 2600 Games|ALE]]) with sticky actions (repeat probability 0.25), evaluated at 200M environment frames
- [[DeepMind Control Suite]] — continuous control tasks used to demonstrate generalization beyond discrete action spaces (humanoid stand-up and walking from pixels)

## Related Papers
- [[DreamerV1]] — predecessor using Gaussian latent variables and analytic value gradients
- [[DreamerV3]] — successor achieving general cross-domain performance with a single configuration
- [[Rainbow]] — model-free DQN variant combining multiple improvements; key baseline
- [[IQN]] — Implicit Quantile Networks; top single-GPU model-free agent before DreamerV2
- [[C51]] — categorical distributional RL baseline
- [[PlaNet]] — earlier model-based agent using same RSSM but online planning
