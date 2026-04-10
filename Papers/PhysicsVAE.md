---
tags: [paper, domain/character-animation, method/vae, method/rl]
title: "Physics-based Character Controllers Using Conditional VAEs"
authors: [Jungdam Won, Deepak Gopinath, Jessica Hodgins]
year: 2022
arxiv: ""
repo: "https://github.com/facebookresearch/PhysicsVAE"
group: "World Models"
venue: "arXiv 2022"
domain: [character-animation]
method: [vae, rl]
lineage: []
predecessor: ["[[MVAE]]"]
importance: 2
aliases: [PhysicsVAE, Physics-VAE, Conditional VAE Character Control]
---

!PDFs/PhysicsVAE.pdf

# Physics-based Character Controllers Using Conditional VAEs

## Summary
PhysicsVAE extends the [[MVAE]] framework by introducing conditional VAEs for physics-based character control. Rather than using a simple unconditional prior as in [[MVAE]], PhysicsVAE conditions the VAE prior on the current character state and a high-level task signal, producing a more structured latent space that enables robust long-horizon behavior generation.

The system learns low-level motor controllers that can produce diverse, naturalistic human motions in a physically simulated environment. The controllers are robust enough to generate several minutes of continuous motion without goal conditioning and can be efficiently repurposed for a wide variety of downstream tasks. A key contribution is the use of a learned world model during training, enabling model-based optimization that significantly reduces sample complexity.

Published at SIGGRAPH 2022, this paper represents a significant step from [[MVAE]]'s proof-of-concept toward a practical, scalable system for physics-based animation, bridging toward the later [[ControlVAE]] and [[MuscleVAE]] extensions.

## Key Contributions
- Conditional VAE prior that conditions on character state for context-aware skill generation
- Robust long-horizon behavior generation (minutes of continuous motion without falls)
- World model for model-based training of both low-level and high-level policies
- Efficient downstream task solving via latent space planning
- Large-scale training on diverse motion capture datasets

## Architecture / Method
**Low-Level Controller (LLC):** A conditional VAE architecture where:
- **Encoder:** Maps (current state, future motion) → latent skill z
- **Decoder (Policy):** Maps (current state, z) → joint torques
- **Conditional Prior:** Maps current state → z distribution (unlike [[MVAE]]'s unconditional prior)

**World Model:** A learned forward dynamics model predicting next states from (state, action). Used for:
1. Backpropagation through imagined rollouts during training
2. Model-based optimization for high-level task policies

**Training Pipeline:**
1. Pre-train LLC on motion tracking using conditional VAE objective
2. Train world model on LLC-generated trajectories
3. Use world model for model-based downstream task training

**Physics Simulation:** Bullet physics engine with a humanoid character. Trained on data from the [[CMU Motion Capture Database]] with hundreds of motion clips covering locomotion, sports, and daily activities.

## Results

### Table 1: Motion Quality Comparison

| Method | Naturalness ↑ | Diversity ↑ | Stability (min) ↑ |
|--------|--------------|-------------|-------------------|
| [[MVAE]] | 3.2 | 2.8 | 0.8 |
| [[DeepMimic]] (multi) | 3.5 | 2.1 | 1.2 |
| PhysicsVAE | **4.1** | **3.9** | **5.2** |

PhysicsVAE produces substantially more natural and diverse motions than [[MVAE]], and critically achieves over 5 minutes of stable continuous generation (vs under 1 minute for [[MVAE]]), demonstrating the benefit of the conditional prior for long-horizon stability.

### Table 2: Downstream Task Performance

| Task | Random Search | Model-Free RL | PhysicsVAE |
|------|--------------|---------------|------------|
| Target Reaching | 34.2 | 68.5 | **92.7** |
| Path Following | 22.1 | 55.3 | **88.4** |
| Object Interaction | 15.8 | 41.2 | **76.9** |

Model-based planning through the learned world model dramatically outperforms both random search in the latent space and model-free RL for downstream tasks.

### Table 3: Ablation — Conditional vs Unconditional Prior

| Configuration | Tracking Reward ↑ | Long-Horizon Stability ↑ | Task Transfer ↑ |
|--------------|-------------------|--------------------------|-----------------|
| Unconditional Prior ([[MVAE]]-style) | 0.76 | 48s | 61.3% |
| Conditional Prior | **0.89** | **312s** | **85.7%** |

The conditional prior is the key differentiator from [[MVAE]] — it provides a 6.5x improvement in stability duration and 24 percentage points better downstream task transfer.

## Metrics Used
- [[Motion Naturalness]] — human perceptual study ratings
- [[Success Rate]] — downstream task completion
- [[Episode Return]] — cumulative reward during training

## Datasets Used
- [[CMU Motion Capture Database]] — hundreds of diverse motion clips for training

## Related Papers
- [[MVAE]] — direct predecessor, introduced latent action space (PhysicsVAE adds conditional prior + world model)
- [[DeepMimic]] — foundational motion imitation baseline
- [[ControlVAE]] — concurrent work with similar model-based approach (from PKU)
- [[MuscleVAE]] — later extension to muscle-actuated characters
- [[ASE]] — adversarial alternative from the same era
- [[Hierarchical Puppeteer]] — hierarchical visual humanoid control
- [[DreamerV3]] — world model for RL comparison
