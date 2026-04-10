---
tags: [paper, video-planning, motion]
title: "Learning Universal Policies via Text-Guided Video Generation"
authors: [Yilun Du, Mengjiao Yang, Bo Dai, Hanjun Dai, Ofir Nachum, Joshua B. Tenenbaum, Dale Schuurmans, Pieter Abbeel]
year: 2023
arxiv: "https://arxiv.org/abs/2302.00111"
group: "Video Generation / Planning"
importance: 
aliases: [UniPi, Universal Policy]
---

!PDFs/UniPi.pdf


# Learning Universal Policies via Text-Guided Video Generation

## Summary

UniPi (Universal Policy) reframes sequential decision-making as a text-conditioned video generation problem. Developed by researchers at MIT, Google Brain, UC Berkeley, and University of Alberta, UniPi proposes that instead of directly predicting actions, a planner should synthesize a video depicting the desired future trajectory, and then a small inverse dynamics model extracts the low-level actions from the generated frames. This formulation enables combinatorial generalization to novel goals specified in natural language and transfer of visual knowledge from internet-scale video data.

The key insight is that by operating in a unified image-space representation, video generation can serve as a universal planning interface that generalizes across different environments and embodiments. A text-conditioned video diffusion model generates planned trajectories, while hierarchical planning via temporal super-resolution enables long-horizon tasks. The generated video plans are then translated into executable actions by a lightweight task-specific inverse dynamics model.

UniPi was presented at NeurIPS 2023 and demonstrated strong performance on combinatorial manipulation tasks, multi-task environments, and real robot experiments. The approach significantly outperforms prior planning methods like Diffuser and behavioral cloning, particularly on novel task combinations and unseen instructions. UniPi is closely related to [[UniSim]], with shared authors exploring complementary aspects of video generation for embodied AI.

## Key Contributions

- Proposes casting sequential decision-making as text-conditioned video generation, enabling language-guided planning
- Demonstrates combinatorial generalization: novel combinations of objects, locations, and relations not seen during training
- Introduces hierarchical video planning through temporal super-resolution for long-horizon tasks
- Shows that internet-scale visual knowledge transfers to robot planning via video generation
- Achieves significant improvements over Diffuser and behavioral cloning baselines (4-6x on combinatorial tasks)
- Demonstrates real robot video generation and planning from natural language instructions

## Architecture / Method

**UniPi consists of four major components:**

**1. Text-Conditioned Video Diffusion Model:**
- A video diffusion model trained to generate future frame sequences conditioned on the current observation and a text instruction
- Uses pretrained T5 language features for text conditioning
- First-frame tiling: the initial observation is tiled and concatenated with the noisy video during denoising, ensuring generated videos start from the correct state
- Trained with the video diffusion algorithm (Ho et al.)

**2. Hierarchical Planning (Temporal Super-Resolution):**
- For long-horizon tasks, planning is decomposed hierarchically
- First, a coarse video plan is generated with sparse temporal resolution (e.g., every Nth frame)
- Then, a temporal super-resolution model fills in the intermediate frames
- This enables planning over much longer horizons than single-shot video generation allows

**3. Flexible Behavior Synthesis:**
- Text conditioning enables specifying diverse goals in natural language
- The model can combinatorially compose instructions (e.g., "pick the red block" + "place on the blue plate") even for combinations not seen during training
- Plans can be re-generated at any point, allowing replanning on failure

**4. Task-Specific Inverse Dynamics Model:**
- A small neural network trained to predict low-level control actions given pairs of consecutive video frames
- Translates the visual plan into executable robot commands
- Task-specific and lightweight, requiring minimal training data
- Bridges the gap between video-space planning and action-space execution

## Results

### Table 1: Combinatorial Task Performance ([[Success Rate]] %)

| Model | Seen Place | Seen Relation | Novel Place | Novel Relation |
|-------|-----------|--------------|-------------|----------------|
| **UniPi** | 59.1 +/- 2.5 | 53.2 +/- 2.0 | 60.1 +/- 3.9 | 46.1 +/- 3.0 |
| Diffuser | 9.0 +/- 1.2 | 11.2 +/- 1.0 | 12.5 +/- 2.4 | 9.6 +/- 1.7 |
| Image + TT | 17.4 +/- 2.9 | 12.8 +/- 1.8 | 13.2 +/- 4.1 | 9.1 +/- 2.5 |

UniPi achieves 4-6x higher success rates than Diffuser and behavioral cloning baselines on both seen and novel task combinations, demonstrating strong combinatorial generalization.

### Table 2: Multi-Task Environment Results ([[Success Rate]] %)

| Model | Place Bowl | Pack Object | Pack Pair |
|-------|-----------|------------|-----------|
| **UniPi** | 51.6 +/- 3.6 | 75.5 +/- 3.1 | 45.7 +/- 3.7 |
| Diffuser | 14.8 +/- 2.9 | 15.9 +/- 2.7 | 10.5 +/- 2.4 |
| Image + Transformer BC | 5.3 +/- 1.9 | 5.7 +/- 2.1 | 7.8 +/- 2.6 |

UniPi significantly outperforms baselines across all multi-task manipulation scenarios.

### Table 3: Real Robot Video Generation Quality

| Configuration | CLIP Score | FID | [[FVD]] | Success |
|--------------|-----------|-----|-----|---------|
| Pretrained | 24.54 +/- 0.03 | 14.54 +/- 0.57 | 264.66 +/- 13.64 | 77.1% |
| No Pretrain | 24.43 +/- 0.04 | 17.75 +/- 0.56 | 288.02 +/- 10.45 | 72.6% |

Pretraining on internet video data improves both video generation quality and downstream planning success rate.

## Metrics Used

- [[Success Rate]] -- task completion rate for manipulation tasks across seen and novel combinations
- [[FVD|Frechet Video Distance]] ([[FVD]]) -- quality and diversity of generated video plans
- Frechet Inception Distance (FID) -- per-frame image quality of generated videos
- CLIP Score -- alignment between generated video frames and text instructions

## Datasets Used

- CLIPort Simulation -- simulated tabletop manipulation environments for combinatorial and multi-task evaluation
- Real Robot Demonstrations -- real-world robot manipulation data for video generation and planning
- Internet Video Data -- pretraining data for the video diffusion model

## Related Papers

- [[UniSim]] -- closely related work by overlapping authors (Yilun Du, Schuurmans, Abbeel), learning interactive simulators from video; UniPi focuses on planning while [[UniSim]] focuses on simulation
- [[Genie 2]] -- Google DeepMind's interactive environment generation, sharing the vision of video-based world models for agent training
- [[NVIDIA Cosmos]] -- large-scale world model for physical AI, operating at much larger scale
- [[Pi0]] -- Physical Intelligence's VLA model that takes a different approach (direct action prediction) to the same robot control problem
- [[DreamerV3]] -- learned world model for RL that imagines futures in latent space rather than pixel space
