---
tags: [paper, world-model, physics-simulation]
title: "SuperPADL: Scaling Language-Directed Physics-Based Control with Progressive Supervised Distillation"
authors: [Jordan Juravsky, Yunrong Guo, Sanja Fidler, Xue Bin Peng]
year: 2024
arxiv: "https://arxiv.org/abs/2407.10481"
repo: ""
group: "World Models"
importance: 
aliases: [SuperPADL, Super PADL]
---

![[PDFs/SuperPADL.pdf]]

# SuperPADL: Scaling Language-Directed Physics-Based Control with Progressive Supervised Distillation

## Summary

SuperPADL presents a scalable framework for physics-based text-to-motion control, published at SIGGRAPH 2024. While prior methods like [[PADL]] and [[ASE]] use reinforcement learning to train language-directed physics-based controllers, they struggle to scale beyond a few hundred motion clips due to RL instabilities at large data scales. SuperPADL overcomes this bottleneck by combining RL with supervised learning through a progressive distillation pipeline, training a single controller on over 5,000 diverse motion skills sourced from the AMASS dataset.

The core idea is a staged training approach. First, a large number of per-clip expert tracking policies are trained via RL (median training time under 1 hour each). These experts are then grouped and distilled into intermediate group controllers using a hybrid of behavior cloning (BC) warmup followed by RL fine-tuning ([[PADL]]+BC). Finally, the group controllers are distilled into a single global controller using the same BC-then-RL recipe but at larger scale. This progressive distillation avoids the instabilities of training a monolithic RL policy on thousands of motions, while preserving the motion quality and physical plausibility that RL provides.

The resulting global SuperPADL controller runs in real time on a consumer GPU, supports smooth transitions between skills, and significantly outperforms RL-only baselines at the 5,000+ motion scale. Users can interactively craft multi-stage animations by issuing text commands that dynamically switch between skills, representing a substantial leap in the scalability of language-directed physics-based animation.

## Key Contributions

- Scales language-directed physics-based control from ~130 motions ([[PADL]]) to 5,587 motion clips (~8.5 hours of motion capture data from AMASS)
- Introduces progressive supervised distillation: experts -> group controllers -> global controller, combining BC warmup with RL fine-tuning at each stage
- Demonstrates that pure RL baselines collapse at large data scales (producing controllers that can barely stay upright), while SuperPADL maintains high motion quality
- Achieves real-time inference on a consumer GPU with a single global policy
- Supports natural inter-skill transitions with 92.70% same-group and 90.92% cross-group transition success rates
- Augments motion captions to 48,207 total using ChatGPT paraphrasing for richer language conditioning

## Architecture / Method

**Stage 1: Expert Tracking Policies**
- One per-clip RL expert trained for each of 5,587 motion clips (5,866 initial, 5% rejected as physically implausible)
- Architecture: MLP with hidden layers [1024, 512], ELU activation
- Median training time: under 1 hour per policy on a single A40 GPU (30% complete in <30 minutes)
- Training uses standard motion imitation reward

**Stage 2: Group Controllers ([[PADL]]+BC)**
- Motions clustered into groups; one group controller per cluster
- Architecture: MLP with three hidden layers [1024, 1024, 512], ReLU activation, 128D motion index embedding
- Training: 2,000-epoch BC-only warmup (supervised distillation from expert policies), then PPO with 1 billion samples of online experience
- Training time: ~12 hours on a single A40 GPU per group
- BC loss supervises the student to match expert action distributions

**Stage 3: Global Controller**
- Single policy distilled from all group controllers
- Architecture: MLP with four hidden layers [3072, 3072, 3072, 2048], ELU activation with LayerNorm
- Training: 2,000-epoch BC warmup from group controllers, then PPO with 6 billion frames of online experience (7,900 total epochs)
- Training time: 12 hours on eight A40 GPUs
- Conditioned on text via the same CLIP-based motion-language embedding space as [[PADL]]

**Input Representation:**
- All policies use 5-frame history input (40-frame buffer sampled every 8 frames)
- Language conditioning via 128D latent from CLIP text encoder + learned projection

**Dataset:**
- 5,587 motion clips from AMASS (~8.5 hours total)
- 48,207 text captions (augmented via ChatGPT paraphrasing)
- 95% retention rate after physical plausibility filtering

## Results

### Table 1: Motion Quality ([[Precision]]/[[Recall]] AUC)

| Method | [[Precision]] AUC | [[Recall]] AUC |
|--------|--------------|------------|
| **SuperPADL (global)** | **1.18** | **1.11** |
| [[PADL]]+BC (group) | 1.12 | 0.73 |
| [[PADL]] (pure RL) | 0.99 | 0.70 |

SuperPADL's global controller achieves the highest precision and recall AUC, indicating superior motion quality and diversity. The pure RL baseline ([[PADL]]-style) degrades substantially at this scale.

### Table 2: Skill Transition Success Rates

| Transition Type | [[Success Rate]] | Falls Before Transition | Falls After Transition |
|----------------|-------------|------------------------|----------------------|
| Same-group | 92.70% | ~3% | ~4% |
| Cross-group | 90.92% | ~3% | ~6% |

The global controller achieves high transition success rates even between skills from different motion groups, enabling seamless multi-skill animations.

### Table 3: Language Command Comprehension (Human Evaluation)

| Response Category | Percentage |
|------------------|-----------|
| Correct caption identified | 57.33% |
| Incorrect caption selected | 19.33% |
| Multiple captions applicable | 5.00% |
| No caption applicable | 18.33% |

Human evaluators assessed whether the character's motion matched the issued text command. In 57.33% of cases evaluators correctly identified the command, and in an additional 5% multiple captions were deemed applicable.

### Training Costs

| Stage | Hardware | Wall-Clock Time |
|-------|----------|----------------|
| Per-clip experts (5,587) | 1x A40 each | Median <1 hour each |
| Group controllers | 1x A40 each | ~12 hours each |
| Global controller | 8x A40 | 12 hours |

## Metrics Used

- [[Precision]] AUC / [[Recall]] AUC — motion quality and diversity measured against reference motion distribution
- [[Success Rate]] — percentage of successful skill transitions without character falling
- Human evaluation accuracy — percentage of human evaluators correctly identifying the issued text command from character motion
- [[Motion Naturalness]] — qualitative assessment of generated motion quality

## Datasets Used

- AMASS — large-scale motion capture dataset; 5,587 clips (~8.5 hours) used after filtering
- [[CMU Motion Capture Database]] — subset of AMASS used for motion data

## Related Papers

- [[PADL]] — direct predecessor; SuperPADL scales [[PADL]]'s approach from 131 to 5,587 motions via progressive distillation
- [[DeepMimic]] — foundational physics-based motion imitation; SuperPADL's per-clip experts follow this paradigm
- [[ASE]] — adversarial skill embeddings; SuperPADL's group controllers build on the [[ASE]]/[[PADL]] skill reward formulation
- [[CALM]] — conditional adversarial latent models; related approach to controllable physics-based animation
- [[MaskedMimic]] — unified physics-based control through masked inpainting; concurrent work on scaling character control
- [[LeVERB]] — language-conditioned humanoid control on real robots; shares the language-to-motion interface goal
- [[CLoSD]] — closes the loop between diffusion planning and physics simulation; complementary approach to scalable character control
