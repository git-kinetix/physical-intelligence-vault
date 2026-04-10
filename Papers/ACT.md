---
tags: [paper, vla, motion]
title: "Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware"
authors: [Tony Z. Zhao, Vikash Kumar, Sergey Levine, Chelsea Finn]
year: 2023
arxiv: "https://arxiv.org/abs/2304.13705"
repo: "https://github.com/tonyzhaozh/act"
group: "VLA Models"
importance: 
aliases: [ACT, Action Chunking with Transformers]
---

!PDFs/ACT.pdf

# Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware

## Summary

ACT (Action Chunking with Transformers) presents a low-cost bimanual teleoperation system called ALOHA together with a novel imitation learning algorithm for fine-grained robot manipulation. The ALOHA hardware system costs under $20K and consists of two pairs of ViperX 6-DoF robot arms (leader-follower) with custom 3D-printed fingertips, enabling precise bimanual teleoperation at 50Hz. The system is capable of contact-rich, precision tasks that typically require high-end robotics hardware.

The core algorithmic contribution is Action Chunking with Transformers, which addresses the compounding error problem in imitation learning by predicting sequences of future actions ("action chunks") rather than single-step actions. This reduces the effective decision horizon, mitigating the impact of temporally correlated errors and non-Markovian human behavior. The policy is trained as the decoder of a Conditional Variational Autoencoder (CVAE) with a transformer backbone, where the CVAE encoder captures the style variable z from demonstration action sequences at training time, and the decoder policy conditions on current observations and z to produce action chunks. At test time, the encoder is discarded and z is set to the mean of the prior distribution.

ACT achieves 80-96% success rates on 6 challenging real-world bimanual tasks (e.g., opening a translucent condiment cup, slotting a battery) using only 50 demonstrations per task (approximately 10 minutes of data). It significantly outperforms prior imitation learning methods including BC-ConvMLP, BeT, RT-1, and VINN across both simulated and real-world evaluations. The paper was published at RSS 2023.

## Key Contributions

- Introduces ALOHA, a low-cost (<$20K) open-source bimanual teleoperation system capable of high-precision manipulation
- Proposes Action Chunking: predicting action sequences of length k instead of single actions, reducing the effective horizon by k-fold (e.g., 4x reduction with k=100 at 50Hz)
- Trains the policy as a CVAE decoder to handle multi-modal human demonstration distributions and mitigate compounding errors
- Demonstrates 80-96% success on 6 real-world fine manipulation tasks with only 50 demonstrations each
- Achieves strong performance in simulation (Transfer Cube, Bimanual Insertion) and transfers to real-world bimanual tasks
- Provides open-source code and hardware designs for full reproducibility

## Architecture / Method

**CVAE Framework:** ACT is trained as a Conditional VAE with an encoder and decoder, both implemented as transformers. The CVAE encoder takes the current action sequence and joint positions as input, processes them through a BERT-like transformer encoder, and outputs the mean and variance of a style variable z's distribution (parameterized as a diagonal Gaussian). The CVAE decoder (the policy) conditions on observations and z to predict action chunks. At test time, the encoder is discarded and z is set to the prior mean (zero).

**Transformer Encoder (CVAE Encoder):** Inputs to the encoder are the current joint positions and the target action sequence of length k from the demonstration dataset, projected by a learned [CLS] token similar to BERT. After passing through the transformer, the feature corresponding to [CLS] is used to predict the mean and variance of z.

**Transformer Decoder (Policy):** Takes the current observations (images + joint positions) and the style variable z as input. The observation includes 4 RGB images (each 480x640) from front, top, and two wrist cameras, plus a 14-dimensional joint position vector (7 DoF per arm). Images are encoded using a ResNet18 backbone, which converts 480x640x3 RGB images into 15x20x512 feature maps, then flattened along spatial dimensions to 300x512. Joint positions are projected to the embedding dimension using a linear layer. A 3D sinusoidal positional embedding is added. The transformer decoder predicts action sequences using cross-attention, where keys and values come from the encoder output.

**Action Space:** 14-dimensional (7 DoF per arm) absolute joint positions. With action chunking, the policy outputs a k-length (k=100) action sequence at each step, but only the first few actions are executed before re-querying.

**Temporal Ensembling:** At inference, overlapping action chunks are aggregated with exponential weighting w_i = exp(-m * i), where m is a hyperparameter controlling the weight for older actions. This smooths execution and reduces jitter.

**Training Details:** ~80M parameters total. Trained for 8000 epochs on a single RTX 2080 Ti GPU, taking about 5 hours per task. 50 demonstrations per task (except Thread Velcro with 100). The CVAE objective has two terms: a reconstruction loss and a KL divergence term weighted by a hyperparameter beta. Lower beta yields less information transmitted through z.

**Hardware (ALOHA):** 4 ViperX 6-DoF robot arms (2 leader, 2 follower) with 6+1 gripper DoF each. Total system cost <$20K. Joint-space mapping between leader and follower robots. 4 Logitech C922x cameras streaming 480x640 RGB at 50Hz.

## Results

### Table 1: [[Success Rate]] (%) on Simulated and Real-World Tasks

| Method | Cube Transfer (sim) ||| Bimanual Insertion (sim) |||| Slide Ziploc (real) ||| Slot Battery (real) |||
| ------ | ------------------- | --- | --- | ------------------------ | --- | --- | --- | ------------------- | --- | --- | ------------------- | --- | --- |
|--------|---------|--------|----------|-------|---------|--------|-------|-------|------|-------|-------|--------|
| BC-ConvMLP | 34 ± 3 | 17 ± 1 | 1 ± 0 | 5 ± 0 | 1 ± 0 | 1 ± 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| BeT | 60 ± 16 | 51 ± 13 | 27 ± 1 | 21 ± 0 | 4 ± 0 | 3 ± 0 | 8 | 0 | 0 | 4 | 0 | 0 |
| RT-1 | 44 ± 4 | 33 ± 2 | 2 ± 0 | 2 ± 0 | 0 ± 0 | 1 ± 0 | 4 | 0 | 0 | 4 | 0 | 0 |
| VINN | 13 ± 17 | 9 ± 11 | 3 ± 0 | 6 ± 0 | 1 ± 0 | 1 ± 0 | 28 | 0 | 0 | 20 | 0 | 0 |
| **ACT (Ours)** | **97 ± 82** | **90 ± 60** | **86 ± 50** | **93 ± 76** | **90 ± 66** | **32 ± 20** | **92** | **96** | **88** | **100** | **100** | **96** |

For the 2 simulated tasks, results are reported with 3 seeds and 50 policy evaluations each (training with scripted data / human data). For the 2 real-world tasks, results are from 1 seed and 25 evaluations. ACT dramatically outperforms all baselines on every task and subtask. The baselines universally fail on real-world tasks (0% on most subtasks), while ACT achieves 88-100% on individual subtasks. In simulation, ACT achieves 86% on Transfer Cube and 32% on the harder Bimanual Insertion with scripted data, both far exceeding all baselines.

### Table 2: [[Success Rate]] (%) on Remaining 3 Real-World Tasks (vs. Best Baseline BeT)

| Method | Open Cup (real) || Thread Velcro (real) ||| Prep Tape (real) |||| Put On Shoe (real) ||||
| ------ | --------------- | --- | -------------------- | --- | --- | ---------------- | --- | --- | --- | ------------------ | --- | --- | --- |
|--------|---------|-------|----------|------|-------|--------|-------|-----|----------|------|------|--------|---------|--------|
| BeT | 12 | 0 | 0 | 24 | 0 | 0 | 8 | 0 | 0 | 0 | 12 | 0 | 0 | 0 |
| **ACT (Ours)** | **100** | **96** | **84** | **92** | **40** | **20** | **96** | **92** | **72** | **64** | **100** | **92** | **92** | **92** |

ACT achieves 84% on Open Cup (full task completion through lid opening), 20% on the very difficult Thread Velcro insertion task, 64% on Prep Tape (through the final hang subtask), and 92% on Put On Shoe (full secure). BeT, the strongest baseline, achieves at most 24% on any single subtask and 0% on all final-stage subtasks, demonstrating that prior methods cannot complete any of these fine manipulation tasks end-to-end.

### Table 3: Ablation Results -- Action Chunking and Temporal Ensembling

| Chunk Size (k) | Scripted Data | Human Data |
|:--------------:|:------------:|:----------:|
| 1 | 44% | 1% |
| 10 | 86% | 16% |
| 50 | 90% | 37% |
| **100** | **90%** | **50%** |

Averaged across 2 simulated tasks and separately for scripted vs. human data. Action chunking is critical: without it (k=1), performance is only 44% with scripted data and catastrophically drops to 1% with human data. More chunking consistently improves performance with human data, illustrating that longer action sequences better handle the multi-modality and temporal correlations in human demonstrations.

### Table 4: Ablation Results -- CVAE Training

| Setting | Scripted Data | Human Data |
|---------|:------------:|:----------:|
| ACT (with CVAE) | 35.9% | 50% |
| ACT without CVAE | 35.9% | 25% |

Removing the CVAE objective makes almost no difference when training on scripted data (since scripted data is unimodal), but causes a significant drop from 50% to 25% on human data. This demonstrates that the CVAE objective is critical when learning from noisy, multi-modal human demonstrations.

### Summary of Real-World Task Success Rates

| Task | [[Success Rate]] | # Demos |
|------|:-----------:|:-------:|
| Slide Ziploc | 88% (Open) | 50 |
| Slot Battery | 96% (Insert) | 50 |
| Open Cup | 84% (Open Lid) | 50 |
| Thread Velcro | 20% (Insert) | 100 |
| Prep Tape | 64% (Hang) | 50 |
| Put On Shoe | 92% (Secure) | 50 |

ACT achieves remarkably high success rates on 4 of 6 real-world tasks (84-96%) using only 50 demonstrations (~10 minutes of data). Thread Velcro and Prep Tape are more challenging due to deformable objects and multi-stage coordination requirements, but ACT still significantly outperforms all baselines on these tasks.

## Metrics Used

- [[Success Rate]] -- primary metric, measured as binary task completion percentage over 25 real-world trials or 50 simulated episodes per seed
- [[Task Completion Time]] -- measured in a user study comparing 50Hz vs 5Hz teleoperation frequency; reducing from 50Hz to 5Hz causes a 62% increase in completion time
- Subtask [[Success Rate]] -- fine-grained metric tracking completion of individual subtasks within multi-stage tasks (e.g., Grasp, Place, Insert for Slot Battery)

## Datasets Used

- ALOHA Bimanual Demonstrations -- 50 human teleoperation demonstrations per task (100 for Thread Velcro), each 8-14 seconds at 50Hz (400-700 timesteps), collected via the ALOHA system
- Simulated Transfer Cube and Bimanual Insertion -- 50 scripted demonstrations and 50 human demonstrations per task in MuJoCo simulation using ALOHA leader robots

## Related Papers

- [[ACT-JEPA]] -- extends ACT with a JEPA-based self-supervised learning branch for joint representation learning, achieving up to 10% higher success rates
- [[Pi0]] -- Physical Intelligence's VLA model that uses ACT and Diffusion Policy as fine-tuning baselines and significantly outperforms both
- [[Pi0.5]] -- successor to [[Pi0]] with improved generalization, also benchmarked against ACT-style approaches
- [[OpenVLA]] -- open-source VLA that compares against Diffusion Policy (a contemporary of ACT) on fine-tuning tasks
- [[Octo]] -- open-source generalist policy that, like ACT, targets manipulation but uses diffusion-based action generation
- [[RT-2]] -- Google's VLA model; RT-1 (its predecessor) is used as a baseline in the ACT paper
- [[Gemini Robotics]] -- Google DeepMind's VLA that builds on the line of work ACT helped establish in imitation learning for manipulation
