---
tags: [paper, world-model, motion]
title: "DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos"
authors: [Shenyuan Gao, William Liang, Kaiyuan Zheng, Ayaan Malik, Seonghyeon Ye, Sihyun Yu, Wei-Cheng Tseng, Yuzhu Dong, Kaichun Mo, Chen-Hsuan Lin, Qianli Ma, Seungjun Nah, Loic Magne, Jiannan Xiang, Yuqi Xie, Ruijie Zheng, Dantong Niu, You Liang Tan, K.R. Zentner, George Kurian, Suneel Indupuru, Pooya Jannaty, Jinwei Gu, Jun Zhang, Jitendra Malik, Pieter Abbeel, Ming-Yu Liu, Yuke Zhu, Joel Jang, Linxi Fan]
year: 2026
arxiv: "https://arxiv.org/abs/2602.06949"
repo: "https://github.com/NVIDIA/DreamDojo"
group: "World Models"
importance: 
aliases: [DreamDojo, Dream Dojo]
---

!PDFs/Dream Dojo.pdf


# DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos

## Summary
DreamDojo is a foundation world model for robotics that learns diverse interactions and dexterous controls from 44,000 hours of egocentric human videos -- the largest video dataset used for world model pretraining to date. The key challenge it addresses is the scarcity of action-labeled robot data: while robot datasets are small and limited in skill diversity, vast amounts of unlabeled human video exist showing diverse manipulation and interaction skills. DreamDojo bridges this gap by introducing continuous latent actions as unified proxy actions, enabling transfer of interaction knowledge from unlabeled human videos to robot control.

Built on the [[NVIDIA Cosmos|Cosmos]]-Predict2.5 video diffusion model, DreamDojo is pretrained on the [[DreamDojo-HV]] dataset (43,827 hours, 1.1M trajectories, 6,015 skills, 1.1M scenes) and then post-trained on small-scale target robot data. The resulting model demonstrates strong understanding of physics and precise action controllability on out-of-distribution benchmarks. A distillation pipeline accelerates inference to 10.81 FPS for real-time applications. DreamDojo enables several downstream applications: live teleoperation of robots, policy evaluation (Pearson correlation r=0.995 with real-world outcomes), and model-based planning that doubles success rates. The work comes from NVIDIA, UC Berkeley, HKUST, and other leading institutions.

## Key Contributions
- Largest video dataset for world model pretraining: 44K hours of egocentric human video spanning 6,015 skills and 1.1M+ scenes (15x duration, 96x skills, 2000x scenes vs. prior robot datasets)
- Continuous latent action model that extracts semantically meaningful actions between frames in a self-supervised manner, enabling knowledge transfer from unlabeled videos
- Architecture innovations: relative action representation, chunked action injection, and temporal consistency loss
- Distillation pipeline achieving 4x speedup to 10.81 FPS real-time inference while maintaining quality
- Downstream applications: live teleoperation, policy evaluation (r=0.995), and model-based planning with 2x success rate improvement
- Two model scales: DreamDojo-2B and DreamDojo-14B

## Architecture / Method
DreamDojo is built on the [[NVIDIA Cosmos|Cosmos]]-Predict2.5 latent video diffusion model and extends it with action conditioning and latent action learning.

**Latent Action Model:**
- A self-supervised model that extracts continuous latent actions between consecutive frames
- Trained to reconstruct frame transitions, the latent actions capture semantically meaningful motion information
- These latent actions serve as unified proxy actions for both human videos (no action labels) and robot data (with action labels)
- Enables scaling to internet-level video data without requiring action annotations

**Architecture Design Choices:**
1. **Relative Action Representation:** Actions are represented relative to the current frame rather than in absolute coordinates, improving generalization across camera viewpoints and embodiments
2. **Chunked Action Injection:** Rather than injecting a single action per frame, actions are chunked and injected at multiple temporal scales into the diffusion model's conditioning pathway
3. **Temporal Consistency Loss:** An additional loss term that encourages consistency between predicted frames across time, reducing drift in long-horizon generation

**Model Scales:**
- DreamDojo-2B: 2 billion parameters, suitable for real-time applications
- DreamDojo-14B: 14 billion parameters, higher quality generation

**Distillation Pipeline:**
- Teacher model: 35 denoising steps, 2.72 FPS
- Student model: 4 denoising steps, 10.81 FPS (~4x speedup)
- Context window: 12 frames for student model
- Maximum generation horizon: 1 minute (600 frames)
- Resolution: 640x480 pixels

**Training Pipeline:**
1. Pretrain latent action model on large-scale video data
2. Pretrain video diffusion model on [[DreamDojo-HV]] dataset (44K hours)
3. Post-train on target robot data with real action labels
4. Distill teacher model to student for real-time inference

## Results

### Table 1: Dataset Scale Comparison

| Dataset | Type | Hours | Trajectories | Skills | Scenes |
|---------|------|-------|-------------|--------|--------|
| **[[DreamDojo-HV]]** | **Human** | **43,827** | **1,135K** | **6,015** | **1,135K** |
| **Our Full Mixture** | **Human** | **44,711** | **1,179K** | **>=6,015** | **>=1,135K** |
| [[AgiBot-World]] | Robot | 2,900 | 1,000K | 87 | 106 |
| [[DROID]] | Robot | 350 | 76K | 86 | 564 |

DreamDojo's training data exceeds prior robot datasets by enormous margins: 15x more hours than [[AgiBot-World]], 96x more skills than any robot dataset, and 2,000x more unique scenes. This scale advantage is the core enabler of DreamDojo's generalization capabilities.

### Table 2: Action Conditioning Ablation

| Pretraining | Action Type | In-lab [[PSNR]] | In-lab [[SSIM]] | In-lab [[LPIPS]] | [[EgoDex]] [[PSNR]] | [[EgoDex]] [[SSIM]] | [[EgoDex]] [[LPIPS]] |
|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|
| None | Robot action | 20.58 | 0.774 | 0.222 | 19.95 | 0.787 | 0.219 |
| Action-free | None | 20.80 | 0.773 | 0.222 | 19.92 | 0.783 | 0.222 |
| **Latent action** | **Latent** | **20.91** | **0.776** | **0.219** | **20.34** | **0.790** | **0.214** |

Pretraining with latent actions consistently outperforms both no pretraining and action-free pretraining, validating the latent action approach. The improvement is larger on the out-of-distribution [[EgoDex]] benchmark, demonstrating better generalization.

### Table 3: Data Mixture Effects (DreamDojo-14B)

| Evaluation Set | [[PSNR]] | [[SSIM]] | [[LPIPS]] |
|---------------|------|------|-------|
| In-lab Eval | 21.41 | 0.788 | 0.208 |
| [[EgoDex]] Eval | 20.53 | 0.787 | 0.213 |
| [[DreamDojo-HV]] Eval | 18.92 | 0.751 | 0.228 |
| Counterfactual Eval | 21.09 | 0.793 | 0.185 |

The 14B model achieves strong performance across all evaluation sets, including out-of-distribution benchmarks. The Counterfactual Eval (testing physics understanding through counterfactual scenarios) achieves particularly good [[LPIPS]] (0.185), suggesting strong physical reasoning.

### Table 4: Human Preference Evaluation (Out-of-Distribution Win Rates)

| Comparison | Physics Win Rate | Action Win Rate |
|------------|-----------------|-----------------|
| DreamDojo-2B vs. [[NVIDIA Cosmos]]-Predict2.5 | 62.5% | 63.45% |
| DreamDojo-14B vs. [[NVIDIA Cosmos]]-Predict2.5 | 73.5% | 72.55% |
| DreamDojo-14B vs. DreamDojo-2B | 72.5% | 65.53% |

Human evaluators consistently prefer DreamDojo over the base [[NVIDIA Cosmos|Cosmos]]-Predict2.5 model for both physics understanding and action controllability. The 14B model is substantially preferred over the 2B model, demonstrating clear scaling benefits. The win rates of 73.5% (physics) and 72.55% (action) for DreamDojo-14B vs. [[NVIDIA Cosmos|Cosmos]] show significant improvement from the pretraining and post-training pipeline.

### Table 5: Architecture Design Ablation (GR-1 Validation Set)

| Configuration | [[PSNR]] | [[SSIM]] | [[LPIPS]] |
|--------------|------|------|-------|
| Baseline | 16.20 | 0.557 | 0.315 |
| + Relative actions | 16.52 | 0.576 | 0.304 |
| + Chunked injection | 17.63 | 0.620 | 0.267 |
| + Temporal loss | 17.63 | 0.622 | 0.266 |
| Full model (Counterfactual) | 20.98 | 0.796 | 0.189 |

Each architecture component provides incremental improvement. Chunked action injection provides the largest single gain ([[PSNR]] 16.52 to 17.63), while relative actions and temporal loss provide meaningful but smaller contributions.

### Table 6: Distillation Results (GR-1 Long Evaluation, 600 frames)

| Model | [[PSNR]] | [[SSIM]] | [[LPIPS]] | FPS |
|-------|------|------|-------|-----|
| Teacher | 14.09 | 0.442 | 0.412 | 2.72 |
| **Student** | **13.15** | **0.379** | **0.485** | **10.81** |

The student model achieves approximately 4x speedup (10.81 vs. 2.72 FPS) with an acceptable quality trade-off. The quality decrease is modest given the dramatic speed improvement, enabling real-time applications.

### Table 7: Downstream Application — Policy Evaluation (AgiBot Fruit Packing)

| Metric | Value |
|--------|-------|
| Pearson correlation (r) | 0.995 |
| [[Mean Maximum Rank Violation]] | 0.003 |

DreamDojo achieves near-perfect correlation (r=0.995) between simulated and real-world policy evaluation, making it a reliable proxy for evaluating robot policies without physical execution.

### Table 8: Model-Based Planning Results

| Metric | Improvement |
|--------|-------------|
| Planning vs. uniform sampling | ~2x success rate |
| Converged checkpoints | ~2x improvement |
| High-variance policy group | 17% improvement |

Model-based planning using DreamDojo as a simulator roughly doubles success rates compared to uniform action sampling, demonstrating the model's value for decision-making.

## Metrics Used
- [[PSNR]] — [[PSNR|Peak Signal-to-Noise Ratio]]; measures pixel-level reconstruction quality of generated video frames (higher is better)
- [[SSIM]] — [[SSIM|Structural Similarity Index]]; measures perceptual structural similarity (higher is better)
- [[LPIPS]] — [[LPIPS|Learned Perceptual Image Patch Similarity]]; measures perceptual distance using learned features (lower is better)
- [[Human Preference Win Rate]] — percentage of human evaluators preferring one model's outputs for physics realism and action controllability
- [[Pearson Correlation]] — correlation between simulated and real-world policy evaluation outcomes
- [[Mean Maximum Rank Violation]] — measures ranking consistency between simulated and real evaluation
- [[FPS]] — frames per second; measures real-time generation speed
- [[Success Rate]] — task completion rate for downstream planning applications

## Datasets Used
- [[DreamDojo-HV]] — 43,827 hours of egocentric human video, 1.1M trajectories, 6,015 skills, 1.1M scenes; primary pretraining dataset
- [[AgiBot-World]] — 2,900 hours of robot manipulation data; used for comparison and downstream evaluation (fruit packing task)
- [[DROID]] — 350 hours, 76K trajectories of robot data; used for comparison
- [[EgoDex]] — egocentric dexterous manipulation benchmark; used for out-of-distribution evaluation
- [[GR-1 Dataset]] — robot data used for post-training and evaluation
- [[Ego4D]] — egocentric human video dataset (component of pretraining mixture)
- [[Epic-Kitchens]] — kitchen activity video dataset (component of pretraining mixture)

## Related Papers
- [[NVIDIA Cosmos|Cosmos]]-Predict2.5 — base video diffusion model that DreamDojo builds upon
- [[DreamerV3]] — model-based RL world model; different paradigm (latent state for RL vs. video generation for robotics)
- [[Genie 2]] — generative interactive environment model
- [[UniSim]] — universal simulator from real-world interaction data
- AVID — action-conditioned video prediction for robot learning
- SuSIE — subgoal synthesis for robot manipulation
- [[RT-2]] — robotic transformer for real-world control
