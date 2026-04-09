---
tags: [paper, jepa]
title: "LeWorldModel: Stable End-to-End Joint-Embedding Predictive Architecture from Pixels"
authors: [Lucas Maes, Quentin Le Lidec, Damien Scieur, Yann LeCun, Randall Balestriero]
year: 2026
arxiv: "https://arxiv.org/abs/2603.19312"
repo: "https://github.com/lucas-maes/le-wm"
group: "JEPA Family"
importance: 5
aliases: [LeWorldModel, LeWM, Le-World-Model]
---

![[PDFs/Le-World-Model.pdf]]


# LeWorldModel: Stable End-to-End Joint-Embedding Predictive Architecture from Pixels

## Summary

LeWorldModel (LeWM) is the first Joint-Embedding Predictive Architecture that trains stably end-to-end from raw pixels using only two loss terms: a next-embedding prediction loss and a regularizer enforcing Gaussian-distributed latent embeddings (SIGReg, inherited from [[Le-JEPA|LeJEPA]]). Previous JEPA-based world models suffered from representation collapse and required complex stabilization heuristics -- exponential moving averages, pretrained encoders, or up to six auxiliary loss terms. LeWM eliminates all of these dependencies, reducing tunable loss hyperparameters from six (in [[PLDM]], the only other end-to-end method) to just one.

With approximately 15 million trainable parameters, LeWM is trainable on a single GPU in a few hours and plans up to 48x faster than foundation-model-based world models (e.g., DINO-WM) while remaining competitive across diverse 2D and 3D control tasks. The latent space is shown to encode meaningful physical structure through probing of physical quantities (agent location, block location, block angle), and a violation-of-expectation evaluation confirms that the model reliably detects physically implausible events. LeWM outperforms [[PLDM]] on all tasks and surpasses DINO-WM on [[Push-T]] and Reacher even without pretrained visual features.

## Key Contributions

- First JEPA world model that trains stably end-to-end from pixels with only two loss terms
- Reduces tunable loss hyperparameters from six ([[PLDM]]) to one
- Uses SIGReg (from [[Le-JEPA|LeJEPA]]) to prevent representation collapse without EMA, pretrained encoders, or auxiliary losses
- Plans 48x faster than foundation-model-based approaches (DINO-WM) due to compact 192-dim per-frame latent tokens
- Demonstrates physical structure in learned latent space through probing and violation-of-expectation experiments
- Trainable on a single GPU in a few hours with ~15M parameters
- Outperforms [[PLDM]] on all tasks; competitive with DINO-WM despite not using pretrained features

## Architecture / Method

LeWM uses a simple encoder-predictor architecture trained with two losses:

**1. Encoder:** Maps raw pixel observations $o_t$ to compact latent embeddings $z_t = f_\theta(o_t)$. Each video frame is encoded as a single 192-dimensional token (roughly 200x fewer tokens than DINO-WM, which uses a pretrained DINO encoder).

**2. Action-Conditioned Predictor:** Given the current latent state $z_t$ and action $a_t$, predicts the next latent state:

$$\hat{z}_{t+1} = g_\phi(z_t, a_t)$$

**3. Next-Embedding [[Prediction Error|Prediction Loss]]:**

$$\mathcal{L}_{\text{pred}} = \| \hat{z}_{t+1} - z_{t+1} \|^2$$

Note: Unlike standard JEPA which uses stop-gradient on targets, LeWM trains end-to-end (both encoder branches share weights, gradients flow through the target).

**4. SIGReg Regularizer (from [[Le-JEPA|LeJEPA]]):**
Constrains the latent embedding distribution to be an isotropic Gaussian $\mathcal{N}(0, I)$ by matching its characteristic function:

$$\mathcal{L}_{\text{SIGReg}} = \sum_{k=1}^{K} \left| \hat{\varphi}(\omega_k) - \exp(-\|\omega_k\|^2/2) \right|^2$$

**Total Loss:**
$$\mathcal{L} = \mathcal{L}_{\text{pred}} + \lambda \cdot \mathcal{L}_{\text{SIGReg}}$$

where $\lambda$ is the single hyperparameter.

**Planning:** At inference, LeWM uses sampling-based planning (e.g., CEM or MPPI) to optimize action sequences in latent space. Planning completes in ~1 second per step vs. ~47 seconds for DINO-WM due to the compact 192-dim representation.

**Key design differences from prior work:**
- No EMA target encoder (unlike [[V-JEPA]], DINO-WM)
- No pretrained visual encoder (unlike DINO-WM)
- No auxiliary losses: variance, covariance, time-similarity, time-variance, time-covariance, inverse dynamics (unlike [[PLDM]] which uses all six)
- End-to-end gradient flow through both encoder branches

## Results

### Table 1: Physical Latent Probing on [[Push-T]]

| Property       | Model   | Linear MSE (down)   | Linear r (up) | MLP MSE (down)      | MLP r (up) |
| -------------- | ------- | ------------------- | ------------- | ------------------- | ---------- |
| Agent Location | DINO-WM | 1.888 +/- 0.500     | **0.977**     | **0.003 +/- 0.022** | **0.999**  |
| Agent Location | [[PLDM]]    | 0.090 +/- 0.311     | 0.955         | 0.014 +/- 0.119     | 0.993      |
| Agent Location | LeWM    | **0.052 +/- 0.149** | 0.974         | 0.004 +/- 0.056     | 0.998      |
| Block Location | DINO-WM | **0.006 +/- 0.007** | **0.997**     | 0.002 +/- 0.003     | **0.999**  |
| Block Location | [[PLDM]]    | 0.122 +/- 0.341     | 0.938         | 0.011 +/- 0.066     | 0.994      |
| Block Location | LeWM    | 0.029 +/- 0.073     | 0.986         | **0.001 +/- 0.006** | **0.999**  |
| Block Angle    | DINO-WM | **0.050 +/- 0.101** | **0.979**     | **0.009 +/- 0.052** | **0.995**  |
| Block Angle    | [[PLDM]]    | 0.446 +/- 0.625     | 0.745         | 0.056 +/- 0.184     | 0.972      |
| Block Angle    | LeWM    | 0.187 +/- 0.359     | 0.902         | 0.021 +/- 0.139     | 0.990      |

LeWM consistently outperforms [[PLDM]] on all physical probing tasks, often by large margins (e.g., Block Angle linear r: 0.902 vs. 0.745). While DINO-WM achieves the best linear probing results due to its pretrained features, LeWM matches or surpasses it on MLP probing for Agent and Block Location, indicating that LeWM's learned features encode physical structure that is accessible with slightly nonlinear probes.

### Table 2: [[PLDM]] Hyperparameter Grid — Loss Coefficients Requiring Tuning

| Loss Coefficient | Tuned Value | Description |
|------------------|-------------|-------------|
| alpha (variance) | 18.0 | Embedding variance |
| beta (covariance) | 12 | Embedding covariance |
| gamma (time-sim) | 0.2 | Temporal similarity |
| zeta (time-var) | 0.7 | Temporal variance |
| nu (time-cov) | 0.0 | Temporal covariance |
| mu (IDM) | 0.0 | Inverse dynamics model |

This table illustrates the complexity of [[PLDM]]'s hyperparameter space (6 loss coefficients requiring careful grid search), compared to LeWM's single lambda parameter. Even with exhaustive tuning, [[PLDM]] underperforms LeWM on most tasks.

### Key Control Performance Summary

| Task | DINO-WM | [[PLDM]] | LeWM | Notes |
|------|---------|------|------|-------|
| [[Push-T]] | Competitive | Baseline | **+18% over [[PLDM]]** | LeWM surpasses DINO-WM |
| Reacher | Competitive | Baseline | **Best** | LeWM surpasses DINO-WM |
| [[OGBench]]-Cube | **Best** | Lower | Lower than DINO-WM | DINO-WM benefits from pretrained 3D priors |
| Two-Room | **Best** | Lower | Lower | Low intrinsic dimensionality challenge |

LeWM achieves a ~96% success rate on [[Push-T]] and outperforms [[PLDM]] on all tasks. DINO-WM retains an edge on visually complex 3D tasks ([[OGBench]]-Cube) due to richer visual priors from large-scale pretraining, but LeWM outperforms it on [[Push-T]] and Reacher despite learning from scratch.

### Planning Speed Comparison

| Model | Tokens per Frame | [[Planning Time]] per Step | Relative Speed |
|-------|-----------------|----------------------|----------------|
| DINO-WM | ~38,400 (pretrained) | ~47 seconds | 1x |
| LeWM | 192 (learned) | ~1 second | **48x faster** |

The compact 192-dimensional per-frame latent representation (vs. ~38,400 tokens for DINO-WM) enables 48x faster planning, making LeWM practical for real-time robotic control.

### Violation-of-Expectation (Surprise Detection)

LeWM reliably detects physically implausible events through surprise measurements in latent space. The model produces higher surprise scores for physical perturbations (e.g., objects passing through walls) compared to merely visual perturbations (e.g., color changes), confirming that the latent space encodes genuine physical structure rather than surface-level visual statistics.

## Metrics Used

- [[Success Rate]] — primary control task metric (percentage of successful task completions)
- [[Linear Probe MSE]] — mean squared error of linear regression from latent embeddings to physical quantities
- [[Pearson Correlation (r)]] — correlation between predicted and true physical quantities from latent probing
- [[MLP Probe MSE]] — nonlinear (MLP) probing of physical quantities from latent space
- [[Planning Time]] — wall-clock time per planning step (seconds)
- [[Surprise Score]] — violation-of-expectation metric measuring prediction error for implausible vs. plausible events
- [[Temporal Straightening]] — cosine similarity of velocity vectors in latent space (trajectory smoothness)
- [[t-SNE Visualization]] — qualitative latent space structure visualization

## Datasets Used

- [[Push-T]] — 2D block pushing manipulation task (primary benchmark)
- [[OGBench-Cube]] — 3D robotic manipulation with a robotic arm
- [[Two-Room]] — 2D navigation environment with room transitions
- [[Reacher]] — 2-joint robotic arm reaching task

## Related Papers

- [[LeJEPA]] — sister paper providing the SIGReg regularizer and theoretical foundations used in LeWM
- [[DINO-WM]] — foundation-model-based world model baseline; uses pretrained DINO features; LeWM is 48x faster
- [[PLDM]] — only other end-to-end JEPA world model; requires 6 loss coefficients vs. LeWM's 1
- [[V-JEPA]] — video JEPA for representation learning; LeWM applies similar principles to world modeling
- [[V-JEPA 2]] — action-conditioned variant ([[V-JEPA 2]]-AC) shares the goal of latent-space robotic planning
- [[TD-JEPA]] — TD-learning-based JEPA for RL; complementary approach to long-horizon planning
- [[I-JEPA]] — foundational image JEPA; LeWM extends JEPA principles from representation learning to world modeling
