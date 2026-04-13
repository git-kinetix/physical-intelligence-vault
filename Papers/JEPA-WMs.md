---
tags: [paper, domain/robotics, domain/ssl, method/rl, method/masked-prediction, lineage/jepa]
title: "What Drives Success in Physical Planning with Joint-Embedding Predictive World Models?"
authors: [Basile Terver, Tsung-Yen Yang, Jean Ponce, Adrien Bardes, Yann LeCun]
year: 2025
arxiv: "https://arxiv.org/abs/2512.24497"
repo: "https://github.com/facebookresearch/jepa-wms"
group: "JEPA Family"
venue: "arXiv 2025"
domain: [robotics, ssl]
method: [rl, masked-prediction]
lineage: [jepa]
predecessor: ["[[V-JEPA 2]]", "[[I-JEPA]]"]
importance: 
aliases: [JEPA-WMs, JEPA World Models, JEPA-WM]
---

!PDFs/JEPA-WMs.pdf

# What Drives Success in Physical Planning with Joint-Embedding Predictive World Models?

## Summary

JEPA-WMs presents a comprehensive empirical study of Joint-Embedding Predictive World Models for goal-conditioned physical planning. The authors characterize a family of planning approaches that operate in learned representation spaces by combining a frozen pretrained visual encoder with a learnable action-conditioned predictor and sampling-based planning in latent space. Rather than proposing an entirely new architecture, the paper systematically ablates seven critical design dimensions -- planning optimizer, multistep rollout training, proprioceptive input, training context window, visual encoder choice, predictor architecture, and model scaling -- to identify which technical choices truly drive planning success.

By combining the best findings from each ablation axis, the authors propose an improved JEPA-WM configuration that outperforms two established baselines, DINO-WM and [[V-JEPA 2|V-JEPA-2-AC]], across both navigation and manipulation tasks in simulation and on real-world robotic data from [[DROID]]. Key insights include: CEM with L2 distance is the most robust planner; two-step rollout training is optimal for simulated tasks while six-step is best for real-world data; DINOv2/DINOv3 encoders outperform video-based encoders ([[V-JEPA]]) due to superior fine-grained spatial features; AdaLN conditioning with RoPE positional embeddings yields the strongest predictor on average; and model scaling helps on complex real-world data but not on simple simulated tasks.

The work originates from Meta FAIR (Yann LeCun's group) and INRIA Paris, with code, data, and checkpoints publicly released. It serves as a practical recipe for building JEPA-based world models for robotic planning, complementing the theoretical grounding provided by [[Le-JEPA]] and the end-to-end training approach of [[Le-World-Model]].

## Key Contributions

- Systematic characterization of the JEPA-WM family: frozen encoder + learnable predictor + sampling-based planning in latent space
- Comprehensive ablation across seven design axes (planning optimizer, multistep rollout, proprioception, context window, encoder, predictor architecture, scaling) with controlled experiments
- Demonstrates CEM with L2 cost is the most robust planner overall; gradient-based methods only work on smooth cost landscapes (Metaworld)
- Shows DINOv2/DINOv3 encoders outperform video encoders ([[V-JEPA]]/[[V-JEPA]]-2) for manipulation and navigation due to superior fine-grained spatial features
- Identifies a scaling paradox: larger models hurt on simple simulated tasks but consistently help on real-world data ([[DROID]]), suggesting data complexity drives scaling requirements
- Proposes AdaLN-zero conditioning with RoPE as the best predictor architecture on average
- Produces a combined best model that outperforms both DINO-WM and [[V-JEPA]]-2-AC across 8 evaluation settings

## Architecture / Method

JEPA-WMs consist of four components operating in a learned embedding space:

**1. Frozen Visual Encoder** $E_\phi^{vis}$: A pretrained vision transformer (DINOv2, DINOv3, [[V-JEPA]], or [[V-JEPA]]-2) that maps image observations to patch-level embeddings. The encoder is frozen during world model training -- the paper focuses on learning dynamics (the predictor) rather than representations (the encoder).

**2. Proprioceptive Encoder** $E_\theta^{prop}$ (optional): A shallow MLP that encodes robot proprioceptive state (joint positions, velocities) into the same embedding space. Jointly trained with the predictor.

**3. Action Encoder** $A_\theta$: Encodes discrete or continuous actions into embeddings compatible with the predictor input.

**4. Learnable Predictor** $P_\theta$: A transformer that takes the current state embedding and action embedding and predicts the next-step state embedding. Three predictor conditioning variants are studied:
- **Feature conditioning** (DINO-WM style): Actions injected via sinusoidal positional embeddings added to visual tokens
- **Sequence conditioning** ([[V-JEPA]]-2-AC style): Actions appended as additional tokens in the sequence with RoPE positional embeddings
- **AdaLN conditioning** (proposed): Actions modulate layer normalization parameters (AdaLN-zero) with RoPE positional embeddings

**Training Objective:** MSE loss between predicted and actual next-state embeddings:

$$\mathcal{L} = \| P_\theta(E_\phi^{vis}(o_t), A_\theta(a_t)) - E_\phi^{vis}(o_{t+1}) \|^2$$

**Multistep Rollout Training:** The predictor is trained with cumulative losses over $k$-step unrolled trajectories using truncated backpropagation through time:

$$\mathcal{L}_{total} = \sum_{i=1}^{k} \mathcal{L}_i$$

Optimal $k=2$ for simulated tasks, $k=6$ for real-world [[DROID]] data.

**Planning:** At inference, goal-conditioned planning optimizes action sequences in embedding space using sampling-based methods. The cost function measures L2 distance between predicted future embeddings and the goal embedding. Four planners are compared:
- **CEM (Cross-Entropy Method):** Iteratively samples and refines action distributions; most robust overall
- **Nevergrad:** Meta-optimizer requiring minimal tuning; practical for real-world settings
- **Adam / Gradient Descent:** Gradient-based optimization; works well on smooth cost landscapes but fails on multi-modal ones

**Context Window:** The predictor conditions on $W$ previous frames (default $W=3$). At least $W=2$ is needed for the model to infer velocity from consecutive frames.

## Results

### Table 1: Best Model Comparison ([[Success Rate]] %)

Comparison of the proposed best JEPA-WM configuration against DINO-WM and [[V-JEPA]]-2-AC baselines across 8 evaluation settings. Numbers show success rate with standard deviation across 3 seeds in parentheses.

| Model | Maze | Wall | [[Push-T]] | MW-R | MW-RW | Rc-R | Rc-Pl | [[DROID]] |
|-------|------|------|--------|------|-------|------|-------|-------|
| DINO-WM | 81.6 (3.4) | 64.1 (4.6) | 66.0 (4.7) | 44.8 (8.9) | 35.1 (9.4) | 19.1 (13.4) | 21.7 (7.2) | 39.4 (2.1) |
| [[V-JEPA]]-2-AC | -- | -- | -- | -- | -- | 16.2 (8.3) | 33.1 (7.2) | 42.9 (2.5) |
| **Ours** | **83.9 (2.3)** | **78.8 (3.9)** | **70.2 (2.8)** | **58.2 (9.3)** | **41.6 (10.0)** | **25.4 (16.6)** | **30.7 (8.0)** | **48.2 (1.8)** |

MW-R = Metaworld Reach; MW-RW = Metaworld Reach-Wall; Rc-R = Robocasa Reach; Rc-Pl = Robocasa Place. [[V-JEPA]]-2-AC is only evaluated on environments with camera views compatible with its video encoder (Robocasa and [[DROID]]). The proposed model outperforms DINO-WM on all 8 tasks and [[V-JEPA]]-2-AC on 2 of 3 shared tasks (Robocasa Reach and [[DROID]]).

### Key Ablation Findings

**Planning Optimizer:** CEM with L2 distance cost is the most robust planner across all environments. Gradient-based optimizers (Adam, GD) excel on smooth Metaworld tasks but fail on multi-modal cost landscapes (navigation tasks with walls/doors). Nevergrad requires minimal hyperparameter tuning and is practical for real-world deployment.

**Multistep Rollout Training:** Optimal rollout length is $k=2$ for simulated environments (Maze, Wall, [[Push-T]], Metaworld) and $k=6$ for real-world [[DROID]] data. Longer rollouts beyond the optimum degrade performance due to compounding prediction errors.

**Proprioception:** Including proprioceptive input consistently improves performance across all environments, with particular benefit for precision manipulation tasks.

**Context Window:** $W=2$ is the minimum for velocity inference; $W=3$ is optimal for simulated tasks and $W=5$ for [[DROID]]. Longer contexts increase computational cost with diminishing returns.

**Visual Encoder:** DINOv2 and DINOv3 consistently outperform [[V-JEPA]] and [[V-JEPA]]-2 video encoders. The advantage comes from superior fine-grained object segmentation in DINO's spatial features. DINOv3 is preferred for photorealistic imagery ([[DROID]]).

**Predictor Architecture:** AdaLN-zero conditioning with RoPE positional embeddings performs slightly best on average, though results are task-dependent. Feature conditioning (DINO-WM style) is optimal for Metaworld specifically.

**Model Scaling:** Increasing encoder size (ViT-S to ViT-L) and predictor depth (3 to 12 layers) provides no benefit on simple simulated tasks but consistently improves performance on real-world data ([[DROID]], Robocasa). This suggests data complexity, not task complexity, drives scaling requirements.

## Metrics Used

- [[Success Rate]] -- primary metric across all environments; percentage of episodes where the agent reaches the goal
- [[LPIPS]] -- used to evaluate visual decoder quality by comparing predicted future frames against ground-truth
- L1 Action Error -- used for [[DROID]] evaluation; L1 distance between planner-proposed actions and ground-truth dataset actions

## Datasets Used

- [[Push-T]] -- 2D block pushing task; off-policy trajectory dataset with 90% train split
- PointMaze -- 2D point navigation through walls with doors; random goal sampling
- Wall -- 2D navigation with walls; custom environment
- Metaworld -- robotic manipulation benchmark; Reach and Reach-Wall tasks from the 42-task suite; data collected via [[TD-MPC2]] online agent
- [[RoboCasa]] -- simulated kitchen manipulation with multiple camera views; Reach and Place tasks from teleoperated trajectories
- [[DROID]] -- real-world Franka robot manipulation dataset with 3 camera views; 16 evaluation videos

## Related Papers

- [[V-JEPA 2]] -- video encoder used as one of the frozen encoders; [[V-JEPA]]-2-AC is a direct baseline
- [[V-JEPA]] -- original video JEPA; encoder variant tested in ablations
- [[I-JEPA]] -- image-based JEPA foundation for the architecture family
- [[Le-World-Model]] -- concurrent JEPA world model that trains end-to-end from pixels; complementary approach ([[Le-World-Model|LeWM]] avoids frozen encoders entirely)
- [[Le-JEPA]] -- provides theoretical grounding for JEPA training and collapse avoidance
- [[TD-JEPA]] -- extends JEPA with temporal difference learning for zero-shot RL; related latent-space planning approach
- [[PLDM]] -- [[PLDM|Planning with Latent Dynamics Models]]; another end-to-end JEPA world model baseline
- [[DreamerV3]] -- model-based RL baseline referenced for comparison in goal-conditioned settings
- [[TD-MPC2]] -- used to generate Metaworld training data via online agent; model-based RL baseline
- [[Octo]] -- Vision-Language-Action model baseline referenced for robotic manipulation
- [[DROID]] -- real-world robot dataset used for evaluation (also exists as a dataset node)
- [[ACT-JEPA]] -- related JEPA architecture for action-conditioned prediction
