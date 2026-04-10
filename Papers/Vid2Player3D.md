---
tags: [paper, world-model]
title: "Learning Physically Simulated Tennis Skills from Broadcast Videos"
authors: [Haotian Zhang, Ye Yuan, Viktor Makoviychuk, Yunrong Guo, Sanja Fidler, Xue Bin Peng, Kayvon Fatahalian]
year: 2023
arxiv: ""
repo: "https://github.com/nv-tlabs/vid2player3d"
group: "World Models"
importance: 
aliases: [Vid2Player3D, vid2player3d, Learning Physically Simulated Tennis Skills from Broadcast Videos]
---

!PDFs/Vid2Player3D.pdf

# Learning Physically Simulated Tennis Skills from Broadcast Videos

## Summary
Vid2Player3D presents a system that learns diverse, physically simulated tennis skills from large-scale demonstrations of tennis play harvested from broadcast videos. The core challenge is that motions extracted from monocular broadcast footage are inherently noisy and incomplete compared to motion capture data, yet broadcast video provides access to a vast and diverse corpus of real-world tennis play that no motion capture setup could match. The system addresses this by combining a hierarchical controller architecture with physics-based motion correction: a low-level imitation policy learns to reproduce physically plausible motions from the noisy video estimates, while a high-level motion planning policy steers the character through a learned motion embedding space to achieve task goals like hitting incoming balls to target locations.

A key technical contribution is the hybrid control policy that overrides erroneous aspects of the learned motion embedding with corrections predicted by the high-level policy, enabling precise racket control despite the imperfect source data. The motion embedding is learned using a conditional variational autoencoder (CVAE) with a Mixture-of-Experts (MoE) decoder, building on the [[MVAE|Motion VAE]] architecture. The high-level policy is trained via reinforcement learning with a curriculum of three stages of increasing difficulty, using IsaacGym for massively parallel physics simulation. No explicit stroke-type annotations are required; the system discovers diverse stroke types (serves, forehands, backhands), spins (topspin, slice), and playing styles (one-handed/two-handed backhands, left/right-handed play) purely from the structure of the broadcast data.

Published at SIGGRAPH 2023 (ACM Transactions on Graphics, Vol. 42, No. 4) and awarded Best Paper Honorable Mention, this work from Stanford University, NVIDIA, University of Toronto, Vector Institute, and Simon Fraser University demonstrates that broadcast video can serve as a scalable source of demonstrations for learning complex, physically simulated character skills. The system can synthesize two physically simulated characters playing extended tennis rallies with simulated racket and ball dynamics.

## Key Contributions
- Demonstrates that complex physics-based tennis skills (serves, forehands, backhands with topspin/slice) can be learned from noisy broadcast video footage rather than clean motion capture, using a hierarchical imitation and planning framework
- Introduces a hybrid control policy where the high-level planner can override the motion embedding to achieve precise racket control, compensating for artifacts in video-extracted motions
- Proposes a four-stage pipeline: (1) kinematic motion estimation from video, (2) low-level imitation policy with physics-based correction, (3) motion embedding via conditional VAE with MoE decoder, (4) high-level motion planning policy trained via RL with curriculum learning
- Achieves diverse playing styles (one/two-handed backhands, left/right-handed play) from different players' video data without requiring explicit stroke-type labels or annotations
- Produces extended two-player rallies with simulated racket and ball dynamics, demonstrating coherent multi-shot sequences with realistic transitions between strokes

## Architecture / Method
The Vid2Player3D system consists of four main components trained in sequence:

**Stage 1: Kinematic Motion Estimation from Video**

A video annotation pipeline processes broadcast tennis footage to extract per-frame character poses. This includes player detection and tracking, camera estimation and court detection, 2D pose estimation, and 3D pose lifting. The pipeline is applied to 13 US Open matches (2017-2021) featuring players including Federer, Djokovic, Nadal, Zverev, and others. The extracted motions are noisy due to occlusion, low resolution, and the monocular estimation pipeline.

**Stage 2: Low-Level Imitation Policy**

The low-level policy maps states to a Gaussian distribution over actions with an input-dependent mean and fixed diagonal covariance. The network uses a fully connected architecture with 3 hidden layers of [1024, 1024, 512] units with ReLU activations and a linear output. It is first pre-trained on the AMASS motion capture dataset (approximately 1 billion samples) and then fine-tuned on the tennis motion dataset extracted from broadcast videos. A key technique is the gradual reduction of residual forces: initially, external forces help correct motion artifacts, and these are progressively reduced by 1% every 10 million samples to encourage the policy to produce physically valid motions independently. The policy runs at 120 Hz simulation frequency with a physics simulation at 120 Hz.

**Stage 3: Motion Embedding**

The motion embedding is a conditional VAE adapted from the [[MVAE|Motion VAE]] (character-motion-vaes) architecture. The encoder is a three-layer feed-forward network with 256 hidden units per layer and ELU activations, producing a 32-dimensional latent space. The decoder uses a Mixture-of-Experts architecture with 6 identically structured expert networks and a gating network. Training uses scheduled sampling over three modes: supervised learning, scheduled sampling (decaying p), and autoregressive prediction, each for 50, 50, and 400 epochs respectively. Only 20% of the data includes motion phase labels; a curriculum with decaying sample probability q handles the limited supervision.

**Stage 4: High-Level Motion Planning Policy**

The high-level policy shares the same network architecture as the low-level policy. It outputs latent actions in the motion embedding space and optional joint correction overrides (the hybrid control mechanism). A ball trajectory prediction model precomputes plausible trajectories as a dense lookup table, parameterized by ball height, velocity, and spin velocity (sampled at 0.1m, 0.1m/s, and 0.5 RPS). Training uses PPO in IsaacGym with 30,720 parallel environments and a three-stage curriculum with increasing difficulty:
- Stage 1: 120 Hz simulation, large action variance (0.25), 600-step episodes
- Stage 2: 360 Hz simulation, medium action variance (0.04), 300-step episodes
- Stage 3: 360 Hz simulation, small action variance (0.0025), 300-step episodes

**Reward Design:**

The high-level policy uses simple rewards based on ball position at landing relative to target, weighted by coefficients alpha_r = 0.05 and alpha_g = 0.1. No complex reward shaping or explicit stroke-type rewards are needed.

## Results

The paper evaluates the system primarily through qualitative demonstrations and ablation studies. The system is demonstrated on diverse tennis scenarios:

### Stroke Diversity and Quality

The trained controllers execute a diverse repertoire of tennis strokes learned entirely from broadcast video:
- **Serve**: Overhead serving motions with ball toss
- **Forehand**: Both topspin and slice variations
- **Backhand**: One-handed and two-handed variants with topspin and slice
- **Playing styles**: Left-handed and right-handed play from different player data

### Ablation Studies

The paper includes ablation studies demonstrating the necessity of key components:

| Component Ablated | Effect |
|-------------------|--------|
| Physics-based correction (Stage 2) | Produces physically implausible motion with foot skating, jittering; decreases ball-hitting precision |
| Hybrid control override | Critical failure in precise racket control; ball placement accuracy degrades significantly |
| Residual force reduction | Without gradual reduction, character relies on non-physical forces; with full removal too early, training destabilizes |
| Curriculum (3-stage) | Without curriculum, high-level policy fails to learn; progressive difficulty is essential for convergence |

### Rally Performance

The system synthesizes extended rallies between two physically simulated characters. Both characters independently execute their learned policies, hitting balls back and forth with realistic stroke selection and court movement. The system handles the full serve-return-rally cycle with natural transitions between movement and stroke execution.

### Table 1: Low-Level Policy Hyperparameters
| Parameter | Value |
|-----------|-------|
| Simulation frequency (Hz) | 120 |
| Action distribution variance | 0.03 |
| Samples per update iteration | 262144 |
| Policy/value function minibatch size | 16384 |
| Discount (gamma) | 0.99 |
| Adam stepsize | 0.00002 |
| GAE(lambda) | 0.95 |
| TD(lambda) | 0.95 |
| PPO clip threshold | 0.2 |
| Episode length | 300 |

### Table 2: Motion Embedding Hyperparameters
| Parameter | Value |
|-----------|-------|
| Latent space dimension | 32 |
| Number of frames for condition | 1 |
| Number of frames for prediction | 1 |
| Sequence length | 10 |
| Number of seqs per epoch | 50000 |
| Batch size | 100 |
| Learning rate | 0.0001 |

### Table 3: High-Level Policy Hyperparameters (3-Stage Curriculum)
| Parameter | Stage 1 | Stage 2 | Stage 3 |
|-----------|---------|---------|---------|
| Simulation frequency (Hz) | 120 | 360 | 360 |
| Action distribution variance | 0.25 | 0.04 | 0.0025 |
| Samples per update iteration | 327680 | 983040 | 983040 |
| Policy/value function minibatch size | 16384 | 16384 | 16384 |
| Discount (gamma) | 0.99 | 0.99 | 0.99 |
| Adam stepsize | 0.0001 | 0.00002 | 0.00001 |
| GAE(lambda) | 0.95 | 0.95 | 0.95 |
| TD(lambda) | 0.95 | 0.95 | 0.95 |
| PPO clip threshold | 0.2 | 0.2 | 0.2 |
| Episode length | 600 | 300 | 300 |

The hyperparameter tables above are from the supplementary material and detail the training configuration for each stage of the system.

## Metrics Used
- [[Motion Naturalness]] — qualitative assessment of physical plausibility (absence of foot skating, jittering, ground penetration) used to evaluate the low-level imitation policy and the effect of physics-based correction
- [[Success Rate]] — whether the character successfully hits the incoming ball and lands it within the court boundaries, used to evaluate the high-level motion planning policy
- Ball Landing Accuracy — distance between the ball's actual landing position and the target position on the court, the primary quantitative metric for evaluating shot precision
- Stroke Diversity — qualitative metric assessing the variety of learned stroke types (forehand/backhand, topspin/slice, serve) without explicit annotations

## Datasets Used
- US Open Broadcast Videos — 13 matches from the US Open (2017-2021) featuring professional players including Federer, Djokovic, Nadal, Zverev, Medvedev, Goffin, Kyrgios, Berrettini, Nishikori, Schwartzman, Cilic, Anderson, and Del Potro; used as the primary source of tennis motion demonstrations
- AMASS Motion Capture Database — large-scale motion capture dataset used to pre-train the low-level imitation policy (approximately 1 billion training samples) before fine-tuning on tennis-specific video data
- [[CMU Motion Capture Database]] — subset included within AMASS; provides general human motion data for low-level policy pre-training

## Related Papers
- [[MVAE]] — Vid2Player3D directly builds on the [[MVAE|Motion VAE]] architecture for its motion embedding (Stage 3), using the same MoE decoder with 6 experts and scheduled sampling training procedure; the character-motion-vaes codebase is listed as a dependency
- [[DeepMimic]] — foundational work by Xue Bin Peng (co-author) on physics-based motion imitation via deep RL; Vid2Player3D extends this paradigm from clean motion capture clips to noisy broadcast video, and from single skills to multi-shot tennis play
- [[Hierarchical Puppeteer]] — shares the hierarchical controller philosophy (low-level tracker + high-level planner) but applied to humanoid locomotion in a world model context; Vid2Player3D uses a similar decomposition for tennis with a low-level imitator and high-level motion planner
- [[DreamerV3]] — general model-based RL; Vid2Player3D uses model-free RL (PPO) but operates in a learned latent action space similar in spirit to world model latent spaces
- [[TD-MPC2]] — scalable model-based continuous control; Vid2Player3D similarly tackles complex continuous control but through imitation learning from video rather than online learning
- [[Eureka]] — automated reward design; Vid2Player3D notably achieves complex skills with minimal reward engineering (just ball landing position), avoiding the need for elaborate reward functions
