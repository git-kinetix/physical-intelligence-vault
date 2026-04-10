---
tags: [paper, vla, motion]
title: "pi0: A Vision-Language-Action Flow Model for General Robot Control"
authors: [Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Lucy Xiaoyang Shi, James Tanner, Quan Vuong, Anna Walling, Haohuan Wang, Ury Zhilinsky]
year: 2024
arxiv: "https://arxiv.org/abs/2410.24164"
repo: "https://github.com/Physical-Intelligence/openpi"
group: "VLA Models"
importance: 5
aliases: [pi0, pi-zero, pi_0]
---

!PDFs/Pi0.pdf


# pi0: A Vision-Language-Action Flow Model for General Robot Control

## Summary

pi0 is Physical Intelligence's generalist robot foundation model, presenting a novel flow matching architecture built on top of a pre-trained vision-language model (PaliGemma 3B) to inherit internet-scale semantic knowledge. The model addresses the core challenges of data diversity, generalization, and robustness required for real-world robot deployment.

The approach consists of a 3B parameter VLM backbone coupled with a smaller 300M parameter action expert that uses flow matching to generate continuous robot actions. pi0 is pre-trained on over 10,000 hours of robot data spanning 7 robot platforms and 68 distinct tasks, including single-arm robots, dual-arm robots, and mobile manipulators. The model can perform tasks zero-shot after pre-training, follow language instructions, and acquire new skills via fine-tuning with as few as 1-20 hours of task-specific data.

pi0 significantly outperforms prior VLA models ([[OpenVLA]], [[Octo]]) and task-specific baselines ([[ACT]], Diffusion Policy) across zero-shot evaluation, language-conditioned control, and fine-tuning experiments on dexterous manipulation tasks including laundry folding, table bussing, grocery bagging, and box assembly.

## Key Contributions

- Novel flow matching VLA architecture combining a pre-trained VLM backbone with a dedicated action expert for robot control
- Demonstration of effective pre-training on a large heterogeneous dataset spanning 7 robot platforms and 68 tasks (10,000+ hours)
- Strong zero-shot generalization to unseen task configurations after pre-training alone
- Effective fine-tuning recipe where pre-trained pi0 outperforms both from-scratch baselines and other pre-trained models
- Language-conditioned control enabling both human instruction following and high-level VLM policy guidance
- Real-time inference at up to 50 Hz with 73ms on-board latency

## Architecture / Method

**Base Model:** PaliGemma 3B vision-language model providing the backbone with internet-scale pre-training.

**Action Expert:** A smaller transformer module (300M parameters, width 1024, MLP dim 4096) that processes robot proprioceptive states and generates actions. The action expert uses AdaLN-Zero layers (similar to DiT) and is interleaved with the VLM backbone through cross-attention.

**Flow Matching:** Actions are generated via a conditional flow matching process. The model learns a denoising vector field over a linear-Gaussian probability path with tau in [0, 1]. Timestep sampling uses a Beta distribution (s=0.999) emphasizing low/noisy timesteps. At inference, 10 forward Euler integration steps with delta=0.1 are used to generate action chunks of H=50 timesteps.

**Training Recipe:**
- Pre-training: 700k steps on the full heterogeneous mixture ([[Open X-Embodiment|OXE]] subset "Magic Soup" at 9.1%, Physical Intelligence proprietary data at 90.9%)
- Post-training (fine-tuning): Task-specific data, typically 5-100+ hours depending on task complexity
- Dataset weighting: Tasks weighted by n^0.43 where n = number of samples to down-weight overrepresented combinations

**Robot Platforms:** UR5e (7D), Bimanual UR5e (14D), Franka (8D), Bimanual Trossen (14D), Bimanual ARX & AgileX (14D), Mobile Trossen & ARX (16D), Mobile Fibocom holonomic base (17D).

**Total Parameters:** 3.3 billion (3B VLM + 300M action expert).

## Results

### Table 1: [[Inference Latency|Inference Time]] Breakdown

| Component | Time |
|-----------|------|
| Image encoders | 14 ms |
| Observation forward pass | 32 ms |
| 10x action forward pass (flow) | 27 ms |
| Network latency (if off-board) | 13 ms |
| **Total on-board inference** | **73 ms** |
| **Total off-board inference** | **86 ms** |

Timing measured on NVIDIA GeForce RTX 4090 GPU with 3 camera images. The model achieves real-time control at up to 50 Hz for dexterous tasks.

### Table 2: Zero-Shot Evaluation (Normalized Scores, 0-1 scale)

| Model | Shirt Folding | Bussing Easy | Bussing Hard | Grocery Bagging | Toast Extraction | Average |
|-------|:---:|:---:|:---:|:---:|:---:|:---:|
| [[Octo]] (93M) | 0.000 | 0.043 | 0.000 | 0.000 | 0.000 | 0.009 |
| [[OpenVLA]] (7B) | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| [[OpenVLA]] UR5e-only | 0.000 | 0.343 | 0.000 | 0.000 | 0.000 | 0.069 |
| pi0-small (470M) | 0.500 | 0.443 | 0.333 | 0.271 | 0.000 | 0.309 |
| **pi0 (3.3B)** | **1.000** | **0.971** | **0.875** | **0.786** | **0.750** | **0.876** |

pi0 achieves a perfect score on shirt folding and dramatically outperforms all baselines across every task. [[OpenVLA]] and [[Octo]] fail almost entirely on zero-shot evaluation, while pi0-small (without VLM pre-training) achieves moderate performance, demonstrating the importance of the VLM backbone.

### Table 3: Fine-Tuning Task Scoring Rubrics

| Task | Max Score | Scoring Description |
|------|:---------:|---------------------|
| Stack Bowls | 3 | Stacking quality + neatness |
| Towel Folding | 3 | Half-folds + neatness |
| Tupperware in Microwave | 4 | Open/grasp/place/close |
| Paper Towel Replacement | 4 | Removal + installation |
| Items in Drawer | 5 | Open/place items/close |

### Table 4: Complex Multi-Stage Task Evaluation

| Task | Description |
|------|-------------|
| Laundry Folding | Full shirt folding sequence |
| Mobile Laundry | Navigate + fold laundry |
| Mobile Dryer | Navigate + unload dryer |
| Table Bussing | Clear table of dishes and items |
| Box Assembly | Fold and assemble cardboard box |
| To-Go Box Packing | Pack items into takeout container |
| Egg Packing | Stack eggs into carton |

Scores are fractional (1.0 = perfect execution, 0.5 = halfway completion) averaged over 10 trials. pi0 achieves approximately 80% average across all tasks, while Diffusion Policy achieves approximately 35%.

### Key Performance Highlights

| Comparison | Result |
|------------|--------|
| pi0 vs all baselines (zero-shot) | pi0 avg 0.876 vs next best 0.309 (pi0-small) |
| pi0 vs Diffusion Policy (fine-tuning) | ~2x improvement on complex tasks |
| Pre-trained vs from-scratch | >2x improvement on similar tasks |
| pi0 stack bowls fine-tuning | ~100% success vs ~55% Diffusion Policy |

## Metrics Used

- [[Normalized Task Score]] -- primary metric, scored on a 0-1 scale representing fractional task completion based on task-specific rubrics
- [[Success Rate]] -- binary success/failure used for simpler tasks like shirt folding
- [[Task Progress Score]] -- fractional scores for partial completion of multi-stage tasks (e.g., 0.5 = halfway)
- [[Inference Latency]] -- measured in milliseconds for on-board and off-board deployment
- [[Language Following Accuracy]] -- measured for language-conditioned control with flat, human, and high-level VLM commands

## Datasets Used

- [[Open X-Embodiment]] -- cross-embodiment dataset comprising 9.1% of the pre-training mixture ("Magic Soup" subset)
- Physical Intelligence Proprietary Dataset -- 90.9% of pre-training mixture with 106M single-arm timesteps and 797M dual-arm timesteps across 68 tasks

## Related Papers

- [[Pi0.5]] -- successor model extending pi0 with open-world generalization via co-training on heterogeneous data
- [[Pi0.6]] -- successor model adding reinforcement learning from real-world experience via [[Pi0.6|RECAP]]
- [[GR00T]] -- NVIDIA's dual-system VLA for humanoid robots, a contemporaneous approach
- [[Gemini Robotics]] -- Google DeepMind's VLA built on Gemini 2.0, evaluated on similar manipulation tasks
- [[OpenVLA]] -- 7B parameter VLA baseline evaluated against pi0
- [[Octo]] -- 93M parameter diffusion-based baseline evaluated against pi0
