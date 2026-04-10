---
tags: [paper, domain/robotics, method/flow-matching, method/transformer, lineage/pi]
title: "pi0.5: a Vision-Language-Action Model with Open-World Generalization"
authors: [Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Manuel Y. Galliker, Dibya Ghosh, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Devin LeBlanc, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Allen Z. Ren, Lucy Xiaoyang Shi, Laura Smith, Jost Tobias Springenberg, Kyle Stachowicz, James Tanner, Quan Vuong, Homer Walke, Anna Walling, Haohuan Wang, Lili Yu, Ury Zhilinsky]
year: 2025
arxiv: "https://arxiv.org/abs/2504.16054"
repo: "https://github.com/Physical-Intelligence/openpi"
group: "VLA Models"
venue: "arXiv 2025"
domain: [robotics]
method: [flow-matching, transformer]
lineage: [pi]
predecessor: ["[[Pi0]]"]
importance: 4
aliases: [pi0.5, pi-zero-point-five, pi_0.5]
---

!PDFs/Pi0.5.pdf


# [[Pi0|pi0]].5: a Vision-Language-Action Model with Open-World Generalization

## Summary

[[Pi0|pi0]].5 is Physical Intelligence's second-generation VLA model that builds upon [[Pi0|pi0]] to achieve open-world generalization -- enabling robots to perform practically relevant tasks in real homes, outside of the lab. The key innovation is a co-training approach that leverages heterogeneous data sources including data from multiple robots, high-level semantic prediction, web data, and cross-embodiment demonstrations to enable broad manipulation generalization.

The model uses hybrid multi-modal examples that combine image observations, language commands, object detections, semantic subtask prediction, and low-level actions. During pre-training, [[Pi0|pi0]].5 uses discrete token prediction via the FAST tokenizer for action discretization, while post-training adds continuous flow matching with a dedicated action expert. A critical architectural contribution is the two-level inference hierarchy: high-level autoregressive subtask prediction followed by low-level flow-matching action generation conditioned on the predicted subtask.

[[Pi0|pi0]].5 demonstrates that an end-to-end learning-enabled robotic system can perform long-horizon and dexterous manipulation skills -- such as cleaning a kitchen or bedroom -- in entirely new homes that were never seen during training, with consistent performance across approximately 100 different training environments.

## Key Contributions

- Co-training recipe combining mobile manipulator data (MM), multi-environment data (ME), cross-embodiment lab data (CE), high-level subtask annotations (HL), web data (WD), and verbal instructions (VI)
- Hybrid discrete-continuous action representation: FAST tokenization for pre-training, flow matching for post-training
- Two-level inference: autoregressive high-level subtask prediction + low-level flow matching action generation
- Demonstration of generalization to entirely unseen homes for long-horizon kitchen and bedroom tasks
- Scaling analysis showing performance improves with number of training locations (3 to 104 homes)
- [[Pi0|pi0]].5 significantly outperforms both [[Pi0|pi0]] and [[Pi0|pi0]]-FAST+Flow on real-world tasks

## Architecture / Method

**Base Architecture:** Transformer-based VLA model extending [[Pi0|pi0]], with multimodal inputs (images, text, proprioceptive state).

**Action Expert:** Separate action expert weights for flow matching predictions, initialized randomly at the post-training stage, with 10 denoising steps for inference.

**Two-Level Inference:**
1. High-level: Autoregressive sampling of semantic subtask tokens (e.g., "pick up plate", "place in sink")
2. Low-level: 10 denoising flow matching steps, conditioned on the predicted subtask

**Input/Output:**
- Observations: Multiple camera images + joint angles, gripper pose, torso lift, base velocity
- Robot control: 18-19 DoF (dual 6-DOF arms, parallel grippers, mobile base, torso lift)
- Action chunks: Continuous target poses at 50 Hz

**Training:**
- Pre-training (280k steps): Discrete token prediction only (alpha=0), using MM, ME, CE, HL, WD data sources
- Post-training (80k steps): Joint next-token and flow matching (alpha=10.0), using MM, filtered ME, WD, HL, VI data sources

**Combined Loss Function:**
L = H(text/FAST tokens) + alpha * L2(flow matching vector field)

where alpha=0 during pre-training and alpha=10.0 during post-training.

## Results

### Table 1: Data Source Composition

| Data Source | Code | Description | Stage |
|-------------|:----:|-------------|-------|
| Mobile Manipulator | MM | ~400 hrs household tasks across ~100 homes | Pre-train + Post-train |
| Multi-Environment | ME | Non-mobile robots in diverse homes | Pre-train + Post-train (filtered) |
| Cross-Embodiment | CE | Lab tasks from multiple embodiments + [[Open X-Embodiment]] | Pre-train |
| High-Level Subtask | HL | Semantic subtask annotations | Pre-train + Post-train |
| Web Data | WD | Captions, VQA, localization (~97.6% of pre-train) | Pre-train + Post-train |
| Verbal Instructions | VI | Verbal instruction demonstrations (~11% of post-train HL) | Post-train |

Web data dominates the pre-training mixture, providing broad visual and semantic grounding, while robot-specific data sources are critical for manipulation performance.

### Table 2: Environment Scaling Results

| Training Locations | Relative Performance |
|:------------------:|:--------------------:|
| 3 | Baseline (lowest) |
| 12 | Improved |
| 22 | Further improved |
| 53 | Near-oracle |
| 82 | Near-oracle |
| 104 | Near-oracle |
| Oracle (test homes in training) | Best (upper bound) |

Performance improves monotonically with the number of training locations. The 104-location model effectively matches the oracle setting where test homes are included in training, demonstrating that sufficient environmental diversity eliminates the generalization gap.

### Table 3: Data Source Ablation (Mock Home Tasks)

| Model Variant | Impact |
|---------------|--------|
| Full Pi0.5 | Best performance (baseline) |
| No WD (web data) | Minimal impact on in-distribution mock tasks |
| No ME (multi-environment) | Large degradation |
| No CE (cross-embodiment) | Large degradation |
| No ME or CE | Severe performance loss |

Multi-environment data (ME) and cross-embodiment data (CE) are both critical for strong manipulation performance, while web data primarily benefits out-of-distribution generalization.

### Table 4: Language Following Ablation

| Model | In-Distribution Objects | Out-of-Distribution Objects |
|-------|:-----------------------:|:---------------------------:|
| Full Pi0.5 | High | Moderate |
| No WD | Maintained | Significantly degraded |
| No ME | Degraded | Degraded |
| No CE | Degraded | Degraded |

Web data is particularly important for out-of-distribution object generalization. Without web data, the model maintains performance on familiar objects but struggles with novel ones.

### Table 5: Model Comparison

| Model | Relative Performance vs Pi0.5 |
|-------|:-----------------------------:|
| Pi0.5 (full) | Best |
| [[Pi0]]-FAST+Flow | Significantly worse |
| [[Pi0]] (original) | Significantly worse |

[[Pi0|pi0]].5 significantly outperforms both [[Pi0|pi0]] and [[Pi0|pi0]]-FAST+Flow, demonstrating the value of the co-training recipe and two-level inference hierarchy.

### Table 6: High-Level Inference Analysis

| Method | Relative Performance |
|--------|:--------------------:|
| Pi0.5 (explicit HL + LL) | Best (~100%) |
| Implicit HL (no runtime HL) | ~95% |
| No VI (verbal instructions) | Significantly degraded |
| No WD (web data) | Significantly degraded |
| No HL (no high-level data) | Much worse |
| GPT-4 zero-shot HL | Worst |
| Human oracle HL | ~equivalent to explicit HL |

The relatively small verbal instruction dataset is critical for strong high-level subtask prediction. GPT-4 zero-shot high-level planning performs worst, suggesting that learning task structure from embodied data is essential.

### Real Home Evaluation

| Setting | Details |
|---------|---------|
| Test environments | 3 new homes (never seen during training) |
| Task types | Kitchen cleaning, bedroom tidying |
| Rooms evaluated | 3 kitchens + 3 bedrooms |
| Trials per environment | 10 |
| Task duration | 2-5 minutes per multi-stage task |
| Key tasks | Items in drawer, Dishes in sink, Laundry basket |

The model demonstrates consistent success across entirely unseen environments, validating the open-world generalization claim.

## Metrics Used

- [[Task Progress Score]] -- primary metric measuring percentage of task completion based on rubric (e.g., 50% = half of dishes placed in sink)
- [[Success Rate]] -- percentage of successful task completions
- [[Language Following Rate]] -- percentage of correct object selection given language instructions
- In-Distribution vs OOD Performance -- separate evaluation on familiar and novel objects

## Datasets Used

- Physical Intelligence Mobile Manipulator Dataset -- ~400 hours of household tasks across ~100 homes
- Physical Intelligence Multi-Environment Dataset -- non-mobile robot demonstrations in diverse real homes
- [[Open X-Embodiment]] -- cross-embodiment robot data used as part of CE data source
- Web Data (Captions, VQA, Localization) -- internet-scale visual and language data for grounding

## Related Papers

- [[Pi0]] -- predecessor model providing the base VLA architecture and flow matching approach
- [[Pi0.6]] -- successor model adding reinforcement learning from experience via [[Pi0.6|RECAP]]
- [[GR00T]] -- NVIDIA's humanoid VLA model, alternative approach to generalist robot control
- [[Gemini Robotics]] -- Google DeepMind's Gemini-based VLA for robot manipulation
