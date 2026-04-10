---
tags: [paper, world-model, motion]
title: "PEVA: Whole-Body Conditioned Egocentric Video Prediction"
authors: [Yutong Bai, Danny Tran, Amir Bar, Yann LeCun, Trevor Darrell, Jitendra Malik]
year: 2025
arxiv: "https://arxiv.org/abs/2506.21552"
repo: ""
group: "Video Prediction"
importance: 
aliases: [PEVA, Predict Egocentric Video from Human Actions]
---

!PDFs/PEVA.pdf

# PEVA: Whole-Body Conditioned Egocentric Video Prediction

## Summary

PEVA (Predict Egocentric Video from human Actions) addresses the challenge of predicting first-person video conditioned on human body movements. The system generates realistic egocentric video sequences given past video context and a future action represented as a relative 3D body pose trajectory. The core architecture is an autoregressive conditional diffusion transformer (CDiT) trained on Nymeria, a large-scale dataset of real-world egocentric video paired with synchronized full-body motion capture. PEVA uses a 48-dimensional action space encoding root translation (3 DOF) and 15 upper-body joint relative rotations (15 x 3 Euler angles) to condition generation through action concatenation with latent tokens.

The paper introduces a hierarchical evaluation protocol that decomposes complex human movements into atomic actions (hand movements in four directions, forward locomotion, left/right rotation) to systematically assess the model's understanding of how specific joint-level movements affect the egocentric visual field. PEVA consistently outperforms baselines including Diffusion Forcing and standard CDiT across perceptual metrics ([[LPIPS]], [[DreamSim]], FID), with performance scaling favorably with model size from S to XXL variants. The model can produce coherent 16-second rollouts conditioned on full-body motion trajectories.

## Key Contributions

- Introduces whole-body 3D pose conditioning for egocentric video prediction via relative joint rotations
- Proposes an autoregressive conditional diffusion transformer architecture with action concatenation
- Designs a hierarchical evaluation protocol decomposing movements into atomic actions for systematic assessment
- Demonstrates scaling behavior from PEVA-S to PEVA-XXL with consistent quality improvements
- Achieves state-of-the-art egocentric video prediction on the Nymeria dataset
- Enables coherent long-horizon (16-second) autoregressive video rollouts

## Architecture / Method

PEVA builds on a Conditional Diffusion Transformer (CDiT) with the following key design choices:

**Tokenization:** Video frames are encoded using a Stable Diffusion VAE with 2x2 spatial patches, converting 224x224 RGB frames into latent tokens.

**Action Representation:** Actions are encoded as a 48-dimensional vector: $d_{act} = 48 = 3 + 15 \times 3$, comprising 3 root translation components and 15 upper-body joint relative rotations as Euler angles ($\phi, \theta, \psi$). The action is represented as relative 3D body pose change between timesteps.

**Conditioning Mechanism:** Actions are concatenated directly with latent tokens (found superior to AdaLN-based action embedding with $d=512$). A context window of 3-15 frames is used to predict 64-frame trajectories.

**Training:** Autoregressive sequence-level training with random timeskips -- 16 frames are sampled from 32-second windows at 4 FPS. The model is trained at 224x224 resolution with an 80/20 train/validation split on Nymeria.

**Inference / Rollout:** Starting with context frames encoded via VAE, the current action is appended, the model predicts the next frame, which is then added to the context window (dropping the oldest frame), and this process repeats for each action in the sequence.

**Model Variants:** PEVA-S, PEVA-B, PEVA-L, PEVA-XL, and PEVA-XXL, following the DiT scaling convention.

## Results

### Table 1: Baseline Perceptual Metrics (Single-Step Prediction, 2s Ahead)

| Model | [[LPIPS]] ↓ | [[DreamSim]] ↓ | FID ↓ |
|-------|---------|------------|-------|
| DF* (Diffusion Forcing) | 0.352 ± 0.003 | 0.244 ± 0.003 | 73.052 ± 1.101 |
| CDiT | 0.313 ± 0.001 | 0.202 ± 0.002 | 63.714 ± 0.491 |
| PEVA (XL) | 0.303 ± 0.001 | 0.193 ± 0.002 | 62.293 ± 0.671 |

PEVA outperforms both baselines across all perceptual metrics. Compared to Diffusion Forcing, PEVA achieves a 13.9% improvement in [[LPIPS]], 20.9% in [[DreamSim]], and 14.7% in FID, demonstrating superior perceptual similarity, semantic consistency, and generative quality.

### Table 2: Atomic Action Performance ([[LPIPS]] ↓)

| Model | Navigation | LH-Left | LH-Right | LH-Up | LH-Down | RH-Left | RH-Right | RH-Up | RH-Down | Forward | Rot.L |
|-------|------------|---------|----------|-------|---------|---------|----------|-------|---------|---------|-------|
| DF* | 0.393 ± 0.011 | 0.314 | 0.279 | 0.292 | 0.306 | 0.332 | 0.323 | 0.304 | 0.315 | 0.305 | 0.296 |
| CDiT | 0.348 ± 0.004 | 0.284 | 0.249 | 0.258 | 0.265 | 0.279 | 0.267 | 0.286 | 0.273 | 0.277 | 0.268 |
| PEVA (XL) | 0.337 ± 0.006 | 0.277 | 0.242 | 0.244 | 0.257 | 0.272 | 0.263 | 0.271 | 0.267 | 0.268 | 0.256 |
| PEVA (XXL) | 0.325 ± 0.006 | 0.269 | 0.234 | 0.236 | 0.241 | 0.251 | 0.247 | 0.256 | 0.254 | 0.252 | 0.245 |

PEVA-XXL achieves the best performance across all atomic actions, with particularly strong improvements on navigation (0.325 vs 0.393 for DF*) and hand movements. The consistent improvement from XL to XXL demonstrates favorable scaling behavior.

### Table 3: Model Ablations (Single-Step Prediction, 2s Ahead)

| Configuration | [[LPIPS]] ↓ | [[DreamSim]] ↓ | [[PSNR]] ↑ | FID ↓ |
|---------------|---------|------------|--------|-------|
| Context: 3 frames | 0.304 ± 0.002 | 0.199 ± 0.003 | 16.469 ± 0.044 | 63.966 ± 0.421 |
| Context: 7 frames | 0.304 ± 0.001 | 0.195 ± 0.002 | 16.443 ± 0.068 | 62.540 ± 0.314 |
| Context: 15 frames | 0.303 ± 0.001 | 0.193 ± 0.002 | 16.511 ± 0.061 | 62.293 ± 0.671 |
| Action Embedding (d=512) | 0.317 ± 0.003 | 0.202 ± 0.002 | 16.195 ± 0.081 | 63.101 ± 0.341 |
| Action Concatenation | 0.303 ± 0.001 | 0.193 ± 0.002 | 16.511 ± 0.061 | 62.293 ± 0.671 |

Ablations reveal that (1) longer context windows marginally improve [[DreamSim]] and FID, (2) action concatenation is superior to AdaLN-based action embedding, and (3) the default configuration (15 frames, concatenation) achieves the best overall performance.

### Table 4: Model Scaling

| Model Variant | [[LPIPS]] ↓ | [[DreamSim]] ↓ | [[PSNR]] ↑ | FID ↓ |
|---------------|---------|------------|--------|-------|
| PEVA-S | 0.370 ± 0.002 | 0.327 ± 0.002 | 15.743 ± 0.060 | 101.38 ± 0.450 |
| PEVA-B | 0.337 ± 0.001 | 0.246 ± 0.002 | 16.013 ± 0.091 | 74.338 ± 1.057 |
| PEVA-L | 0.308 ± 0.002 | 0.202 ± 0.001 | 16.417 ± 0.037 | 64.402 ± 0.496 |
| PEVA-XL | 0.303 ± 0.001 | 0.193 ± 0.002 | 16.511 ± 0.061 | 62.293 ± 0.671 |
| PEVA-XXL | 0.298 ± 0.002 | 0.186 ± 0.003 | 16.556 ± 0.060 | 61.100 ± 0.517 |

Larger models consistently improve across all metrics. From PEVA-S to PEVA-XXL, [[LPIPS]] improves by 19.5%, [[DreamSim]] by 43.1%, and FID by 39.7%, confirming strong scaling behavior for action-conditioned egocentric video generation.

### Table 5: Arm Motion Statistics (Mean Relative Rotations)

| Segment | Statistic | Right Arm (φ, θ, ψ) | Left Arm (φ, θ, ψ) |
|---------|-----------|----------------------|---------------------|
| Shoulder | Mean | (0.0027, -0.0012, -0.0015) | (0.0624, 0.0687, 0.1494) |
| Shoulder | Variance | (0.0010, -0.0006, 0.0003) | (0.0625, 0.0697, 0.1496) |
| Upper Arm | Mean | (0.0107, -0.0011, -0.0020) | (0.1119, 0.1647, 0.1791) |
| Upper Arm | Variance | (-0.0062, -0.0004, -0.0013) | (0.0991, 0.1593, 0.1611) |
| Forearm | Mean | (0.0068, -0.0035, 0.0077) | (0.1937, 0.2107, 0.2261) |
| Forearm | Variance | (-0.0036, -0.0063, 0.0002) | (0.1791, 0.2012, 0.2186) |
| Hand | Mean | (0.0065, 0.0001, 0.004) | (0.2417, 0.229, 0.2631) |
| Hand | Variance | (-0.0024, -0.0032, -0.0001) | (0.2126, 0.2237, 0.2475) |

This table characterizes the kinematic statistics of the Nymeria dataset for the atomic arm motion actions (relative Euler angle rotations per body segment). The left arm shows significantly larger motion ranges than the right arm across all segments, reflecting the dataset's motion distribution.

## Metrics Used

- [[LPIPS]] — [[LPIPS|Learned Perceptual Image Patch Similarity]]; primary metric for perceptual quality of predicted frames (lower is better)
- [[DreamSim]] — semantic similarity metric measuring high-level visual correspondence (lower is better)
- FID — Frechet Inception Distance; measures distributional quality of generated frames (lower is better)
- [[PSNR]] — [[PSNR|Peak Signal-to-Noise Ratio]]; pixel-level reconstruction quality (higher is better)

## Datasets Used

- Nymeria — large-scale dataset of real-world egocentric video paired with synchronized XSens motion capture body pose data; sampled at 4 FPS, 224x224 resolution, 80/20 train/val split; provides the paired egocentric video and 3D body pose trajectories for training and evaluation

## Related Papers

- [[V-JEPA 2]] — self-supervised video model; PEVA shares the goal of learning predictive video representations but uses action-conditioned diffusion rather than JEPA
- [[V-JEPA 2.1]] — extends [[V-JEPA 2]] with planning capabilities; related to PEVA's embodied prediction focus
- [[UniSim]] — universal simulator for interactive video generation; related action-conditioned video prediction approach
- [[UniPi]] — universal policy via text-conditioned video generation; shares the video-as-world-model paradigm
- [[Genie 2]] — generative interactive environment; related controllable video generation for embodied AI
- [[DreamerV3]] — world model for RL; PEVA can be viewed as a video-space world model conditioned on body kinematics
- [[GR00T]] — humanoid robot foundation model; PEVA's whole-body conditioning is relevant to humanoid embodied AI
