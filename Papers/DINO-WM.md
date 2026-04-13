---
tags: [paper, domain/robotics, domain/ssl, method/rl, method/masked-prediction, lineage/jepa]
title: "DINO-WM: World Models on Pre-trained Visual Features enable Zero-shot Planning"
authors: [Gaoyue Zhou, Hengkai Pan, Yann LeCun, Lerrel Pinto]
year: 2024
arxiv: "https://arxiv.org/abs/2411.04983"
repo: "https://github.com/gaoyuezhou/dino_wm"
group: "World Models"
venue: "ICML 2025"
domain: [robotics, ssl]
method: [rl, masked-prediction]
lineage: [jepa]
predecessor: ["[[I-JEPA]]"]
importance: 
aliases: [DINO-WM, DINO World Model]
---

![[PDFs/DINO-WM.pdf]]

# DINO-WM: [[World Models]] on Pre-trained Visual Features enable Zero-shot Planning

## Summary

DINO-WM introduces a world modeling approach that learns visual dynamics on compact patch-level embeddings from a frozen DINOv2 encoder rather than reconstructing raw pixel observations. Given offline, task-agnostic behavioral trajectories, DINO-WM trains a Vision Transformer-based transition model to predict future DINOv2 patch features conditioned on actions. At test time, the model performs zero-shot goal-conditioned planning via Model Predictive Control (MPC) using the Cross-Entropy Method (CEM), optimizing action sequences to minimize the latent-space distance between predicted future states and a visually specified goal -- without requiring expert demonstrations, reward functions, or pre-learned inverse models.

The key insight is that DINOv2's spatial patch features provide a rich, object-centric representation prior that captures fine-grained spatial structure far better than global CLS tokens or pixel-space reconstructions. By decoupling dynamics learning from visual representation learning and from pixel reconstruction, DINO-WM avoids the compounding errors and mode collapse issues that plague generative world models. The transition model operates on the frozen patch embedding space with a causal attention mask, enabling multi-step rollouts that remain faithful over extended planning horizons.

Evaluated across six diverse environments spanning 2D navigation (Maze, Wall), robotic manipulation (Reacher, [[Push-T]]), and deformable object manipulation (Rope, Granular), DINO-WM substantially outperforms model-based RL baselines ([[DreamerV3]], [[TD-MPC2]], [[IRIS]]) on zero-shot goal reaching. It also generalizes to novel object shapes and environment configurations not seen during training. The work originates from NYU and Meta FAIR (Yann LeCun, Lerrel Pinto) and was accepted to ICML 2025.

## Key Contributions

- Introduces a task-agnostic world model that operates on frozen DINOv2 patch embeddings rather than reconstructing pixels, enabling dynamics learning to be decoupled from visual representation learning
- Demonstrates that DINOv2 spatial patch features capture fine-grained object structure far better than CLS tokens (R3M, ResNet, DINO CLS), yielding ~45% improvement on complex manipulation tasks
- Achieves zero-shot goal-conditioned planning at test time via CEM-based MPC in the latent patch feature space, without expert demonstrations, reward modeling, or inverse models
- Shows that an optional pixel decoder can be trained independently of the transition model without harming planning performance (and in fact adding decoder loss during transition training hurts performance)
- Demonstrates strong generalization to novel object shapes (Tetris-like objects in [[Push-T]]) and environment configurations (randomized walls, varied particle counts) not seen during training
- Establishes scaling behavior: more offline data monotonically improves both planning success rate and visual prediction quality ([[LPIPS]], [[SSIM]])

## Architecture / Method

DINO-WM consists of three components operating on a pre-trained visual feature space:

**1. Observation Model (Frozen DINOv2 Encoder):** A pre-trained DINOv2 vision transformer maps each image observation $o_t$ to a grid of spatial patch embeddings $z_t \in \mathbb{R}^{N \times E}$, where $N$ is the number of patches and $E$ is the embedding dimension. The encoder is completely frozen -- no fine-tuning is performed. The patch-level representation preserves spatial structure and object boundaries, which is critical for manipulation tasks.

**2. Transition Model (Decoder-Only ViT):** A Vision Transformer with decoder-only architecture predicts future patch embeddings conditioned on current state and action:

$$\mathcal{L}_{\text{pred}} = \| P_\theta(\text{enc}_\theta(o_{t-H:t}), \phi(a_{t-H:t})) - \text{enc}_\theta(o_{t+1}) \|^2$$

Key architectural choices:
- **Causal attention mask:** Frame-level causal masking ensures each predicted frame only attends to current and past frames. This is essential for multi-step rollouts -- without it, performance degrades catastrophically at horizon $h \geq 2$ (from 0.88 to 0.36 success rate)
- **Action conditioning:** Actions are mapped through an MLP and concatenated to patch embedding vectors (not appended as separate tokens)
- **Context window:** The model conditions on $H$ previous frames (default $H=3$) to infer velocity and dynamics from consecutive observations
- **Teacher forcing:** During training, ground-truth observations are used as inputs at each step; at inference, predictions are fed back autoregressively

**3. Pixel Decoder (Optional):** Transposed convolution layers that reconstruct pixel images from predicted patch features. Trained independently with a separate reconstruction loss after the transition model is fixed. Used only for visualization -- the decoder is not needed for planning. Importantly, jointly training the decoder loss with the transition model actually hurts planning performance (0.80 vs 0.92 success rate on [[Push-T]]).

**Planning (MPC with CEM):** At test time, given a single goal image $o_g$ encoded to goal features $z_g$, DINO-WM optimizes an action sequence $\{a_t, \ldots, a_{t+H-1}\}$ using the Cross-Entropy Method to minimize:

$$\mathcal{L}_{\text{plan}} = \| \hat{z}_{t+H} - z_g \|^2$$

where $\hat{z}_{t+H}$ is the predicted future embedding after executing the action sequence through the transition model. CEM iteratively samples and refines action distributions over multiple rounds, selecting the first action from the best sequence for execution in a receding-horizon fashion.

## Results

### Table 1: Zero-Shot Planning Performance (Main Results)

Comparison against model-based RL baselines across six environments. SR = [[Success Rate]] (higher is better), CD = Chamfer Distance (lower is better). All baselines are given equivalent offline training data.

| Model | Maze (SR) | Wall (SR) | Reach (SR) | PushT (SR) | Rope (CD) | Granular (CD) |
|-------|-----------|-----------|------------|------------|-----------|---------------|
| [[IRIS]] | 0.74 | 0.04 | 0.18 | 0.32 | 1.11 | 0.37 |
| [[DreamerV3]] | 1.00 | 1.00 | 0.64 | 0.30 | 2.49 | 1.05 |
| [[TD-MPC2]] | 0.00 | 0.00 | 0.00 | 0.00 | 2.52 | 1.21 |
| **DINO-WM (Ours)** | **0.98** | **0.96** | **0.92** | **0.90** | **0.41** | **0.26** |

DINO-WM achieves the best performance on 4 of 6 environments (Reach, PushT, Rope, Granular). [[DreamerV3]] excels on simple navigation (Maze, Wall) where reward shaping helps, but fails on complex manipulation. [[TD-MPC2]] fails entirely in the zero-shot setting as it requires online reward signals.

### Table 2: Pre-trained Encoder Comparison

Ablation comparing different frozen visual encoders for the transition model.

| Encoder | Maze (SR) | Wall (SR) | Reach (SR) | PushT (SR) | Rope (CD) | Granular (CD) |
|---------|-----------|-----------|------------|------------|-----------|---------------|
| R3M | 0.94 | 0.34 | 0.40 | 0.42 | 1.13 | 0.95 |
| ResNet | 0.98 | 0.12 | 0.06 | 0.20 | 1.08 | 0.90 |
| DINO CLS | 0.96 | 0.58 | 0.60 | 0.44 | 0.84 | 0.79 |
| **DINOv2 Patch (Ours)** | **0.98** | **0.96** | **0.92** | **0.90** | **0.41** | **0.26** |

DINOv2 patch features dramatically outperform alternatives. The gap is largest on manipulation tasks requiring fine spatial reasoning (Reach: 0.92 vs 0.60 for DINO CLS; PushT: 0.90 vs 0.44).

### Table 3: Generalization to Novel Configurations

Evaluation on unseen environment configurations (randomized walls, novel object shapes, varied particle counts).

| Model | WallRandom (SR) | PushObj (SR) | GranularRandom (CD) |
|-------|-----------------|--------------|---------------------|
| [[IRIS]] | 0.06 | 0.14 | 0.86 |
| [[DreamerV3]] | 0.76 | 0.18 | 1.53 |
| R3M | 0.40 | 0.16 | 1.12 |
| ResNet | 0.40 | 0.14 | 0.98 |
| DINO CLS | 0.64 | 0.18 | 1.36 |
| **DINO-WM (Ours)** | **0.82** | **0.34** | **0.63** |

### Table 4: Visual Prediction Quality ([[LPIPS]] and [[SSIM]])

Lower [[LPIPS]] and higher [[SSIM]] indicate better visual fidelity of predicted future frames via the optional decoder.

| Method | PushT [[LPIPS]] | Wall [[LPIPS]] | Rope [[LPIPS]] | Granular [[LPIPS]] | PushT [[SSIM]] | Wall [[SSIM]] | Rope [[SSIM]] | Granular [[SSIM]] |
|--------|-------------|------------|------------|----------------|------------|-----------|-----------|---------------|
| R3M | 0.045 | 0.008 | 0.023 | 0.080 | 0.956 | 0.994 | 0.982 | 0.917 |
| ResNet | 0.063 | 0.002 | 0.025 | 0.080 | 0.950 | 0.996 | 0.980 | 0.915 |
| DINO CLS | 0.039 | 0.004 | 0.029 | 0.086 | 0.973 | 0.996 | 0.980 | 0.912 |
| AVDC | 0.046 | 0.030 | 0.060 | 0.106 | 0.959 | 0.983 | 0.979 | 0.909 |
| **DINO-WM (Ours)** | **0.007** | **0.0016** | **0.009** | **0.035** | **0.985** | **0.997** | **0.985** | **0.940** |

DINO-WM achieves ~56% improvement in [[LPIPS]] over the best alternative, demonstrating that patch-level feature prediction preserves fine-grained visual detail.

### Table 5: Data Scaling ([[Push-T]])

Effect of training dataset size on planning success rate and visual prediction quality.

| Dataset Size | SR | [[SSIM]] | [[LPIPS]] |
|--------------|------|-------|-------|
| n=200 | 0.08 | 0.949 | 0.056 |
| n=1000 | 0.48 | 0.973 | 0.013 |
| n=5000 | 0.72 | 0.981 | 0.007 |
| n=10000 | 0.88 | 0.984 | 0.006 |
| n=18500 | 0.92 | 0.987 | 0.005 |

### Table 6: Causal Attention Mask Ablation ([[Push-T]] SR)

| Setting | h=1 | h=2 | h=3 |
|---------|-----|-----|-----|
| Without mask | 0.76 | 0.36 | 0.08 |
| With mask | 0.76 | 0.88 | 0.92 |

The causal attention mask is critical for multi-step rollouts. Without it, performance collapses from 0.92 to 0.08 at horizon h=3.

### Table 7: Decoder Loss Ablation ([[Push-T]])

| Configuration | [[Success Rate]] |
|---------------|-------------|
| Without decoder loss | 0.92 |
| With decoder loss | 0.80 |

Adding pixel reconstruction loss during transition model training hurts planning performance, confirming that decoupling dynamics from reconstruction is beneficial.

## Metrics Used

- [[Success Rate]] -- primary metric for navigation and rigid-body manipulation tasks (Maze, Wall, Reach, [[Push-T]]); binary task completion
- Chamfer Distance -- primary metric for deformable object tasks (Rope, Granular); measures geometric similarity between predicted and target configurations (lower is better)
- [[LPIPS]] -- evaluates perceptual quality of predicted future frames from the optional pixel decoder (lower is better)
- [[SSIM]] -- evaluates structural similarity of predicted future frames (higher is better)

## Datasets Used

- PointMaze (Maze) -- 2D force-actuated ball navigation to goal positions; 2000 random trajectories
- Wall -- 2D navigation with randomized wall/door positions; 1920-10240 trajectories
- Reacher (Reach) -- 2-joint robotic arm reaching task; 3000 trajectories of 100 steps
- [[Push-T]] -- pusher manipulating a T-shaped block to a target pose; 18500 demonstrations + 20000 random trajectories
- Rope -- XArm robot manipulating a soft rope; 1000 trajectories of 20 steps
- Granular -- XArm robot gathering granular particles; 1000 trajectories of 20 steps

## Related Papers

- [[I-JEPA]] -- DINOv2 shares the JEPA philosophy of learning in embedding space; DINO-WM builds on this by using frozen DINOv2 features as the world model's observation space
- [[V-JEPA]] -- video JEPA that predicts future video features; DINO-WM uses image-level DINOv2 features rather than video features
- [[DreamerV3]] -- model-based RL baseline; excels on navigation with reward shaping but fails on zero-shot manipulation
- [[TD-MPC2]] -- model-based RL baseline; requires online reward signals and fails entirely in the zero-shot offline setting
- [[IRIS]] -- transformer-based world model baseline; struggles on tasks requiring fine spatial reasoning
- [[PLDM]] -- concurrent JEPA-based world model for planning from offline data; complementary approach from the same research community
- [[Le-World-Model]] -- end-to-end JEPA world model that trains from pixels without frozen encoders; achieves 48x faster planning but DINO-WM retains edge on visually complex 3D tasks
- [[JEPA-WMs]] -- systematic ablation study that uses DINO-WM as a key baseline and improves upon it across 8 environments
- [[Stable World Model]] -- reproducibility library that includes DINO-WM as one of 4 baseline implementations and analyzes its zero-shot robustness
