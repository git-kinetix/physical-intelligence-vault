---
tags: [paper, domain/ssl, method/masked-prediction, method/rl, lineage/jepa]
title: "TD-JEPA: Latent-predictive Representations for Zero-Shot Reinforcement Learning"
authors: [Marco Bagatella, Matteo Pirotta, Ahmed Touati, Alessandro Lazaric, Andrea Tirinzoni]
year: 2025
arxiv: "https://arxiv.org/abs/2510.00739"
group: "JEPA Family"
venue: "arXiv 2025"
domain: [ssl]
method: [masked-prediction, rl]
lineage: [jepa]
predecessor: ["[[I-JEPA]]"]
importance: 3
aliases: [TD-JEPA, Temporal Difference JEPA]
---

!PDFs/TD-JEPA.pdf


# TD-JEPA: Latent-predictive Representations for Zero-Shot Reinforcement Learning

## Summary

TD-JEPA introduces temporal difference (TD) learning into the Joint-Embedding Predictive Architecture framework for unsupervised reinforcement learning. The key insight is that standard JEPA-style one-step or few-step feature prediction captures only short-horizon dynamics, which is insufficient for downstream RL tasks that require reasoning about long-term consequences. By replacing the standard regression loss with a TD-based objective, TD-JEPA learns representations that are predictive of long-term latent dynamics across multiple policies from offline, reward-free transition data.

TD-JEPA trains explicit state and task encoders, a policy-conditioned multi-step predictor, and a set of parameterized policies directly in latent space, enabling zero-shot optimization of any reward function at test time. Theoretically, an idealized variant of TD-JEPA avoids representation collapse with proper initialization and learns encoders that capture a low-rank factorization of long-term policy dynamics, while the predictor recovers successor features in latent space. Empirically, TD-JEPA matches or outperforms state-of-the-art baselines across 13 datasets spanning locomotion, navigation, and manipulation tasks in [[ExoRL]] and [[OGBench]], with particularly strong performance in the challenging zero-shot RL from pixels setting.

## Key Contributions

- Combines temporal difference learning with JEPA for long-horizon latent prediction in unsupervised RL
- Trains state/task encoders, a policy-conditioned predictor, and parameterized policies entirely in latent space
- Provides theoretical guarantees: avoids collapse with proper initialization; learns low-rank factorization of long-term policy dynamics
- Predictor recovers successor features in latent space (theoretical result)
- Achieves state-of-the-art zero-shot RL performance from pixels across locomotion, navigation, and manipulation
- Evaluated on 65 tasks across 13 datasets in [[ExoRL]] and [[OGBench]] benchmarks

## Architecture / Method

TD-JEPA consists of the following components:

**1. State Encoder** $\phi$: Maps observations (pixels or proprioceptive states) to latent state representations $z = \phi(s)$.

**2. Task Encoder** $\psi$: Maps observations to task-relevant latent representations $w = \psi(s)$, used to define reward-like signals in latent space.

**3. Policy-Conditioned Predictor** $f_k$: Given the current latent state and a policy index $k$, predicts the future latent state representation. Unlike standard JEPA which uses a one-step or few-step prediction loss, TD-JEPA uses a temporal difference objective:

$$\mathcal{L}_{\text{TD}} = \mathbb{E}\left[\left\| f_k(\phi(s)) - \left(\psi(s') + \gamma \cdot \text{sg}(f_k(\phi(s')))\right) \right\|^2\right]$$

where $\gamma$ is a discount factor and sg denotes stop-gradient on the bootstrap target.

**4. Parameterized Policies** $\{\pi_k\}$: A set of policies operating in latent space, enabling zero-shot adaptation to new reward functions by selecting or combining policies that maximize the predicted latent reward.

**Key theoretical results:**
- With proper initialization, TD-JEPA avoids representation collapse (unlike naive JEPA which can collapse when predicting constant features)
- The learned encoders capture a low-rank factorization of the long-term policy-conditioned transition dynamics
- The predictor approximates successor features in the learned latent space

**Zero-shot evaluation protocol:** At test time, given a new reward function, TD-JEPA selects the policy whose latent-space successor features best align with the reward, without any additional training.

## Results

### Table 1: [[DeepMind Control Suite|DMC]] (DeepMind Control) RGB — Zero-Shot Normalized Returns (avg over 4 tasks)

| Method | Score | Std |
|--------|-------|-----|
| Laplacian | 293.1 | 15.1 |
| ICVF* | 438.7 | 14.9 |
| HILP | 391.2 | 23.8 |
| FB | 456.2 | 8.6 |
| RLDP | 525.7 | 13.3 |
| BYOL* | 513.8 | 11.6 |
| BYOL-gamma* | 582.4 | 9.8 |
| **TD-JEPA** | **628.8** | **5.5** |

TD-JEPA achieves the highest normalized returns on [[DeepMind Control Suite|DMC]] RGB tasks (628.8), outperforming the next best method BYOL-gamma (582.4) by 46.4 points with the lowest variance (5.5). This demonstrates superior long-horizon reasoning from pixel observations.

### Table 2: [[DeepMind Control Suite|DMC]] Proprioception — Zero-Shot Normalized Returns (avg over 4 tasks)

| Method | Score | Std |
|--------|-------|-----|
| Laplacian | 591.1 | 10.7 |
| ICVF* | 619.3 | 10.3 |
| HILP | 620.1 | 8.4 |
| FB | 648.2 | 4.1 |
| RLDP | 610.2 | 13.5 |
| BYOL* | 618.6 | 10.5 |
| BYOL-gamma* | 645.4 | 10.5 |
| **TD-JEPA** | **661.2** | **6.3** |

TD-JEPA also leads on proprioceptive [[DeepMind Control Suite|DMC]] tasks (661.2), though the gap is smaller than on RGB, suggesting the TD-based latent prediction is especially beneficial when learning from high-dimensional pixel inputs.

### Table 3: [[OGBench]] RGB — Zero-Shot [[Success Rate]] (avg over 9 tasks)

| Method | Score | Std |
|--------|-------|-----|
| Laplacian | 30.58 | 0.81 |
| ICVF* | 25.22 | 0.55 |
| HILP | 32.56 | 0.92 |
| FB | 39.89 | 0.47 |
| RLDP | 39.09 | 0.59 |
| BYOL* | 40.33 | 0.52 |
| BYOL-gamma* | 41.58 | 0.64 |
| **TD-JEPA** | **41.34** | **0.45** |

On [[OGBench]] RGB, TD-JEPA (41.34%) is competitive with BYOL-gamma (41.58%), both significantly outperforming other baselines. TD-JEPA has the lowest variance (0.45).

### Table 4: [[OGBench]] Proprioception — Zero-Shot [[Success Rate]] (avg over 9 tasks)

| Method | Score | Std |
|--------|-------|-----|
| Laplacian | 14.81 | 1.32 |
| ICVF* | 30.87 | 0.58 |
| HILP | 37.98 | 1.11 |
| FB | 39.04 | 0.66 |
| RLDP | 27.07 | 0.83 |
| BYOL* | 26.42 | 0.83 |
| BYOL-gamma* | 30.42 | 0.94 |
| TD-JEPA | 37.98 | 0.77 |

On [[OGBench]] proprioception, TD-JEPA (37.98%) ties with HILP and is competitive with FB (39.04%). The BYOL variants underperform here, suggesting their pixel-centric design does not translate as well to proprioceptive inputs.

## Metrics Used

- [[Normalized Zero-Shot Returns]] — primary metric for [[DeepMind Control Suite|DMC]] tasks; returns normalized by maximum achievable score of 1000
- [[Success Rate]] — primary metric for [[OGBench]] goal-reaching tasks (percentage of successful episodes)
- [[Probability of Improvement]] — statistical confidence metric measuring how often one method outperforms another across domains

## Datasets Used

- [[ExoRL / DMC]] — 4 locomotion/navigation domains from [[DeepMind Control Suite]] (walker, cheetah, quadruped, pointmass) with both proprioceptive and RGB variants
- [[OGBench]] — 9 navigation/manipulation domains (antmaze-mn, antmaze-ln, antmaze-ms, antmaze-ls, antmaze-me, cube-single, cube-double, scene, puzzle-3x3) with proprioceptive and RGB variants

Total: 65 tasks across 13 datasets (each domain has multiple reward functions).

## Related Papers

- [[V-JEPA]] — video JEPA that TD-JEPA extends with temporal difference learning for RL
- [[I-JEPA]] — image-based JEPA foundation
- FB (Forward-Backward) — strong unsupervised RL baseline using forward-backward representations
- HILP — hierarchical implicit latent planning baseline
- ICVF — implicit contrastive value function baseline
- BYOL-Explore — self-supervised RL baseline adapted with discount factor (BYOL-gamma)
- [[LeJEPA]] — provides theoretical grounding for JEPA training, related to TD-JEPA's collapse avoidance theory
- [[LeWorldModel]] — another JEPA-based approach to world modeling, complementary to TD-JEPA's RL focus
