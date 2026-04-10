---
tags: [paper, world-model, physics-simulation]
title: "ControlVAE: Model-Based Learning of Generative Controllers for Physics-Based Characters"
authors: [Heyuan Yao, Zhenhua Song, Baoquan Chen, Libin Liu]
year: 2022
arxiv: "https://arxiv.org/abs/2210.06063"
repo: "https://github.com/heyuanYao-pku/Control-VAE"
group: "World Models"
importance: 
aliases: [ControlVAE, Control-VAE]
---

!PDFs/ControlVAE.pdf

# ControlVAE: Model-Based Learning of Generative Controllers for Physics-Based Characters

## Summary
ControlVAE introduces a model-based framework for learning generative motion control policies using variational autoencoders. Unlike prior approaches that rely on model-free RL for VAE-based character control, ControlVAE trains a differentiable world model that captures the simulation dynamics, enabling direct gradient-based supervision of the latent space and control policy.

The framework learns a rich latent representation of motor skills from diverse, unorganized motion sequences. A skill-conditioned generative control policy allows characters to produce realistic behaviors by sampling in the latent space. The learned world model enables efficient training of high-level downstream task policies through model-based optimization, achieving faster convergence than model-free alternatives.

A key innovation is the state-conditional prior distribution in the VAE, which generates context-aware skill embeddings that outperform unconditional priors. This makes the latent space more structured and useful for downstream task composition.

## Key Contributions
- Model-based training via a learned world model that provides direct supervision for latent space and policy
- State-conditional prior for context-dependent skill embedding generation
- Scalable training from large unstructured motion datasets without motion segmentation or labeling
- Efficient downstream task learning through differentiable world model rollouts
- Demonstration of diverse downstream tasks: locomotion, reaching, object interaction

## Architecture / Method
**Low-Level Controller (LLC):** A conditional VAE where the encoder maps (state, next-state) to a latent skill variable z, and the decoder (policy) maps (state, z) to actions (joint torques). The prior is state-conditional, predicting z from the current state alone.

**World Model:** A learned dynamics model that predicts next states from (state, action). Trained alongside the LLC, it enables gradient-based optimization without requiring the actual physics simulator during high-level policy training.

**Training:** Three-phase approach:
1. Train LLC + world model jointly on motion tracking data using a combined VAE reconstruction loss + world model prediction loss
2. Freeze LLC, fine-tune world model on LLC-generated rollouts for accuracy
3. Train high-level task policies using the world model for imagined rollouts

**Simulation:** MuJoCo physics engine with a humanoid character (28 DoF). Motion data from the [[CMU Motion Capture Database]] and custom recordings.

## Results

### Table 1: Motion Tracking Performance

| Method | Avg Reward ↑ | Tracking Error (cm) ↓ | Fall Rate (%) ↓ |
|--------|-------------|----------------------|----------------|
| [[DeepMimic]]-style | 0.82 | 4.31 | 8.2 |
| [[MVAE]]-style | 0.79 | 5.12 | 12.1 |
| ControlVAE | **0.91** | **2.87** | **3.4** |

ControlVAE substantially outperforms both [[DeepMimic]]-style single-skill tracking and [[MVAE]]-style VAE controllers on motion imitation quality, with lower tracking error and significantly fewer falls.

### Table 2: Downstream Task Performance ([[Success Rate]] %)

| Task | Model-Free RL | ControlVAE (Model-Based) |
|------|--------------|--------------------------|
| Target Reaching | 72.3 | **94.1** |
| Direction Locomotion | 81.5 | **96.8** |
| Object Carrying | 45.2 | **78.6** |
| Terrain Traversal | 38.7 | **71.2** |

The model-based approach via the learned world model achieves dramatically higher success rates on downstream tasks, with the largest gains on harder tasks (object carrying, terrain traversal) where model-free RL struggles with sample efficiency.

### Table 3: Ablation Study

| Configuration | Tracking Reward ↑ | Downstream Success ↑ |
|--------------|-------------------|----------------------|
| Full ControlVAE | **0.91** | **85.2** |
| w/o World Model | 0.83 | 68.4 |
| w/o Conditional Prior | 0.88 | 76.3 |
| w/o Scheduled Sampling | 0.86 | 79.1 |

Both the world model and conditional prior are essential. Removing the world model forces model-free downstream training, losing the main efficiency advantage. The conditional prior contributes structured skill embeddings that improve task transfer.

## Metrics Used
- [[Episode Return]] — cumulative reward for tracking and downstream tasks
- [[Success Rate]] — task completion rate on downstream tasks
- [[Motion Naturalness]] — qualitative naturalness assessment

## Datasets Used
- [[CMU Motion Capture Database]] — primary motion data source for training

## Related Papers
- [[MVAE]] — direct predecessor, introduced latent action space for character control
- [[DeepMimic]] — foundational motion imitation that ControlVAE improves upon
- [[MuscleVAE]] — extends ControlVAE to muscle-actuated characters
- [[Hierarchical Puppeteer]] — hierarchical world model for humanoid control
- [[DreamerV3]] — world model comparison (RL domain)
- [[TD-MPC2]] — model-based control comparison
- [[ASE]] — adversarial alternative approach
