---
tags: [paper, jepa]
title: "V-JEPA 2.1: Unlocking Dense Features in Video Self-Supervised Learning"
authors: [Lorenzo Mur-Labadia, Matthew Muckley, Amir Bar, Mido Assran, Koustuv Sinha, Mike Rabbat, Yann LeCun, Nicolas Ballas, Adrien Bardes]
year: 2026
arxiv: "https://arxiv.org/abs/2603.14482"
repo: "https://github.com/facebookresearch/vjepa2"
group: "JEPA Family"
importance: 
aliases: [V-JEPA 2.1, VJEPA2.1]
---

![[PDFs/V-JEPA 2.1.pdf]]


# [[V-JEPA 2]].1: Unlocking Dense Features in Video Self-Supervised Learning

## Summary

[[V-JEPA 2]].1 extends the [[V-JEPA]] family to produce high-quality dense visual representations for both images and videos while retaining strong global scene understanding. While [[V-JEPA 2]] excels at global video classification and action anticipation, its features underperform on dense prediction tasks (depth estimation, segmentation, video object segmentation). [[V-JEPA 2]].1 addresses this gap through four key innovations: (1) a dense context loss where both visible and masked tokens contribute to training, (2) deep self-supervision applied hierarchically across multiple encoder layers, (3) multi-modal tokenizers for unified image-video training, and (4) effective model and data scaling.

[[V-JEPA 2]].1 achieves state-of-the-art results across a remarkably broad set of tasks: 7.71 [[Mean Average Precision (mAP)|mAP]] on [[Ego4D]] short-term object-interaction anticipation, 40.8 [[Recall@5]] on [[EPIC-KITCHENS-100|EPIC-KITCHENS]] action anticipation, 77.7% top-1 on [[Something-Something v2|SSv2]] for global classification, 0.307 [[RMSE]] on [[NYUv2]] depth estimation, and a 20-point improvement in real-robot grasping over [[V-JEPA 2]]-AC. This makes it the first self-supervised video model to simultaneously excel at global understanding, dense prediction, and robotic control.

## Key Contributions

- Introduces a dense context loss that trains on both visible and masked tokens, dramatically improving dense feature quality
- Proposes multi-level prediction (deep self-supervision) across encoder layers for hierarchical feature learning
- Develops multi-modal tokenizers enabling unified image and video pretraining
- Scales to ViT-G (2B parameters) with effective data scaling strategies
- Achieves state-of-the-art across global classification, dense prediction, action anticipation, video QA, and robotics
- Demonstrates 20-point improvement in real-robot grasping over [[V-JEPA 2]]-AC
- First self-supervised video model competitive with DINOv2/DINOv3 on dense prediction tasks

## Architecture / Method

[[V-JEPA 2]].1 builds on [[V-JEPA 2]] with several architectural innovations:

**1. Dense Context Loss:**
In addition to the standard masked prediction loss (predicting masked tokens from visible context), [[V-JEPA 2]].1 adds a context loss where visible tokens also predict their own representations through the predictor. This forces all tokens (not just masked ones) to carry useful information, yielding dense per-token features. The context loss weight lambda is warmed up during training and uses distance-weighted attention.

**2. Multi-level Prediction (Deep Self-Supervision):**
The prediction loss is applied hierarchically across multiple encoder layers (not just the final layer), encouraging intermediate representations to also be predictive. This yields richer features at multiple abstraction levels.

**3. Multi-modal Tokenizers:**
Separate tokenizers for images and videos allow the model to handle both modalities during pretraining. The training mixture emphasizes YT-1B (72% weight) over Kinetics (1%) compared to [[V-JEPA 2]]'s more balanced mixture.

**4. Model and Data Scaling:**
Scaling from ViT-g (1B) to ViT-G (2B) and applying a cool-down phase with learning rate annealing yields consistent improvements across all tasks.

**Cumulative improvement (Table 1):** Starting from [[V-JEPA 2]] baseline, each component adds significant gains, particularly for dense tasks: [[ADE20K]] [[mIoU]] improves from 22.2 to 47.9 and [[NYUv2]] [[RMSE]] from 0.682 to 0.307.

## Results

### Table 1: Ablation - Cumulative Impact of Each Component (ViT-g scale unless noted)

| Component | IN1K Acc. | [[Something-Something v2]] Acc. | NYU [[RMSE]] | [[ADE20K]] [[mIoU]] |
|-----------|-----------|-----------|----------|-------------|
| [[V-JEPA 2]] baseline | 82.2 | 72.8 | 0.682 | 22.2 |
| + Context Loss | 72.6 | 62.5 | 0.474 | 33.8 |
| + Multi-level Pred. | 80.8 | 72.1 | 0.463 | 38.6 |
| + Vision Mix | 81.6 | 72.6 | 0.415 | 41.4 |
| + Multi-modal Tok. | 81.6 | 72.6 | 0.415 | 41.4 |
| + Model Scaling | 84.8 | 76.1 | 0.365 | 47.1 |
| + Cool-down | 85.5 | 77.7 | 0.307 | 47.9 |

The context loss alone provides a massive dense prediction boost ([[ADE20K]]: 22.2 to 33.8; NYU [[RMSE]]: 0.682 to 0.474) but initially hurts global classification. Multi-level prediction recovers global performance while further improving dense tasks. The full pipeline achieves strong results on both fronts.

### Table 2: Context Loss Weighting Schemes (ViT-g)

| Scheme | lambda | Warmup | [[ADE20K]] [[mIoU]] | [[Something-Something v2]] Acc. |
|--------|--------|--------|-------------|-----------|
| [[V-JEPA 2]] baseline | 0 | -- | 22.2 | 72.8 |
| Fixed lambda=0.05 | 0.05 | No | 26.4 | 71.0 |
| Fixed lambda=0.2 | 0.2 | No | 29.6 | 62.5 |
| Fixed lambda=0.5 | 0.5 | No | 27.5 | 53.8 |
| Fixed lambda=1.0 | 1.0 | No | 24.6 | 51.1 |
| Warmup lambda=0.2 | 0.2 | Yes | 30.5 | 60.5 |
| Warmup lambda=0.5 | 0.5 | Yes | 32.2 | 61.5 |
| Distance-weighted | 0.5 | Yes | 33.8 | 62.5 |

The distance-weighted warmup scheme achieves the best dense task performance while mitigating the global classification degradation. Higher fixed lambda values hurt [[Something-Something v2|SSv2]] significantly.

### Table 3: Dataset Composition Comparison

| Source | Samples | Type | Hours | [[V-JEPA 2]] Weight | [[V-JEPA 2]].1 Weight |
|--------|---------|------|-------|-----------------|-------------------|
| [[Something-Something v2]] | 168K | EgoVideo | 168 | 0.056 | 0.170 |
| Kinetics | 733K | ExoVideo | 614 | 0.188 | 0.010 |
| [[HowTo100M]] | 1.1M | ExoVideo | 134K | 0.318 | 0.100 |
| ImageNet | 1M | Images | n/a | 0.250 | 0 |
| YT-1B | 19M | ExoVideo | 1.6M | 0.188 | 0.720 |

[[V-JEPA 2]].1 dramatically increases YT-1B weight (72% vs 18.8%) and removes ImageNet from the pretraining mixture, relying instead on the multi-modal tokenizer for image understanding.

### Table 4: Short-Term Object Interaction Anticipation ([[Ego4D]])

| Model | AP_b | AP_b+N | AP_b+V | AP_b+delta | AP_All | mAP_N | mAP_All |
|-------|------|--------|--------|------------|--------|-------|---------|
| STAformer | 38.3 | 28.3 | 16.6 | 12.27 | 4.06 | 29.4 | 5.67 |
| DINOv2 ViT-L | 45.1 | 37.8 | 21.9 | 14.4 | 5.25 | 28.3 | 5.25 |
| DINOv2 ViT-g | 47.8 | 38.1 | 23.6 | 14.1 | 5.73 | 30.6 | 5.44 |
| DINOv3 ViT-H+ | 48.9 | 40.2 | 23.4 | 13.6 | 5.45 | 32.4 | 5.20 |
| DINOv3 ViT-7B | 50.2 | 40.9 | 23.8 | 14.2 | 5.82 | 33.8 | 5.68 |
| [[V-JEPA 2]] ViT-g | 45.7 | 34.4 | 22.2 | 16.7 | 6.26 | 27.2 | 6.02 |
| [[V-JEPA 2]].1 ViT-g | 47.3 | 36.5 | 23.6 | 18.1 | 7.21 | 28.7 | 6.75 |
| [[V-JEPA 2]].1 ViT-G | 50.7 | 39.3 | 25.8 | 20.2 | **8.20** | 30.9 | **7.71** |

[[V-JEPA 2]].1 ViT-G achieves the highest mAP_All (7.71), surpassing DINOv3 ViT-7B (5.68) despite being 3.5x smaller. The improvement is especially pronounced on temporal/spatial precision metrics (AP_b+delta: 20.2 vs. 14.2).

### Table 5: Action Anticipation on [[EPIC-KITCHENS-100]] ([[Recall@5]])

| Method | Parameters | Verb | Noun | Action |
|--------|-----------|------|------|--------|
| InAViT | 160M | 51.9 | 52.0 | 25.8 |
| Video-LLaMA | 7B | 52.9 | 52.0 | 26.0 |
| PlausiVL | 8B | 55.6 | 54.2 | 27.6 |
| [[V-JEPA 2]] ViT-g | 1B | 63.6 | 57.1 | 39.7 |
| [[V-JEPA 2]].1 ViT-g | 1B | 63.6 | 56.2 | 38.4 |
| [[V-JEPA 2]].1 ViT-G | 2B | 64.3 | 59.9 | **40.8** |

[[V-JEPA 2]].1 ViT-G sets a new state of the art at 40.8 action [[Recall@5|R@5]], improving over [[V-JEPA 2]] (39.7). The ViT-g variant of [[V-JEPA 2]].1 (38.4) slightly underperforms [[V-JEPA 2]] at the same scale, suggesting the dense features trade-off slightly on this task, but scaling to ViT-G recovers and exceeds performance.

### Table 6: Dense Vision Tasks ([[Linear Probe Accuracy|Linear Probe]])

| Method | Params | [[NYUv2]] [[RMSE]] | [[KITTI]] [[RMSE]] | [[ADE20K]] [[mIoU]] | [[Cityscapes]] [[mIoU]] | VOC12 [[mIoU]] | [[DAVIS-2017]]-S | YT-VOS-S |
|--------|--------|-----------|-----------|-------------|-----------------|------------|---------|----------|
| DINOv2 | 1B/14 | 0.372 | 2.624 | 49.5 | 75.6 | 83.1 | 63.9 | 65.6 |
| DINOv3 ViT-H+ | 0.8B/16 | 0.352 | 2.635 | 54.8 | 79.5 | 85.8 | 71.1 | 74.0 |
| DINOv3 ViT-7B | 7B/16 | 0.309 | 2.346 | 55.9 | 81.1 | 86.6 | 71.1 | 74.1 |
| InternVideo2-1B | 1B/14 | 0.471 | 4.739 | 28.4 | 35.6 | 65.2 | 50.6 | 51.2 |
| [[V-JEPA 2]] ViT-g | 1B/16 | 0.642 | 4.650 | 24.4 | 45.9 | 63.9 | 52.5 | 53.7 |
| [[V-JEPA 2]].1 ViT-g | 1B/16 | 0.350 | 2.601 | 47.8 | 71.8 | 84.7 | 68.1 | 72.3 |
| [[V-JEPA 2]].1 ViT-G | 2B/16 | **0.307** | **2.461** | 47.9 | 73.5 | **85.0** | 69.0 | **72.7** |

[[V-JEPA 2]].1 dramatically closes the gap with image-pretrained DINOv2/DINOv3 on dense tasks. [[NYUv2]] [[RMSE]] improves from 0.642 ([[V-JEPA 2]]) to 0.307 ([[V-JEPA 2]].1 ViT-G), competitive with DINOv3 7B (0.309). [[ADE20K]] [[mIoU]] jumps from 24.4 to 47.9, a 23.5-point improvement. Video object segmentation ([[DAVIS-2017|DAVIS]], YT-VOS) shows similar dramatic gains.

### Table 7: Video and Image Classification (Frozen Eval)

| Method | Params | [[Something-Something v2]] | [[Diving-48]] | [[Kinetics-400]] | IN1K |
|--------|--------|------|-----------|------|------|
| VideoMAEv2 | 1B | 56.1 | — | 82.8 | 71.4 |
| InternVideo2-1B | 1B | 67.3 | — | 87.9 | — |
| VideoPrism | 1B | 68.5 | 71.3 | 87.6 | — |
| DINOv3 ViT-H+ | 0.8B | 69.8 | — | 86.7 | 87.9 |
| DINOv3 ViT-7B | 7B | 70.1 | — | 87.8 | 88.4 |
| DINOv2 | 1.1B | 50.7 | 82.5 | 83.6 | 86.1 |
| InternVideo2s-1B | 1B | 69.7 | 86.4 | 89.4 | 85.8 |
| [[V-JEPA 2]] ViT-g | 1B | 77.3 | 90.2 | 87.3 | 85.1 |
| [[V-JEPA 2]].1 ViT-g | 1B | 76.9 | 89.0 | 87.0 | 84.8 |
| [[V-JEPA 2]].1 ViT-G | 2B | **77.7** | 89.2 | 87.7 | 85.5 |

[[V-JEPA 2]].1 ViT-G achieves the highest [[Something-Something v2|SSv2]] accuracy (77.7%), slightly improving over [[V-JEPA 2]] (77.3%). The model remains highly competitive on appearance tasks ([[Kinetics-400|K400]]: 87.7, IN1K: 85.5) while unlocking dense features.

### Table 8: Robot Manipulation Planning

| Method | Samples | Iterations | Horizon | Time | Reach | Grasp | Pick-&-Place |
|--------|---------|-----------|---------|------|-------|-------|--------------|
| [[V-JEPA 2]] | 800 | 10 | 1 | 3s | 100% | 60% | 80% |
| [[V-JEPA 2]].1 ViT-g | 800 | 10 | 1 | 3s | 100% | 70% | 80% |
| [[V-JEPA 2]].1 ViT-G | 300 | 15 | 8 | 14s | 100% | **80%** | 80% |

[[V-JEPA 2]].1 ViT-G achieves 80% grasping success (vs. 60% for [[V-JEPA 2]]), a 20-point improvement. The longer planning horizon (8 steps) and higher iteration count enable more precise manipulation, though at increased planning time.

### Table 9: Navigation Planning Performance

| Model | Time | [[TartanDrive]] [[Absolute Trajectory Error (ATE)]]/[[Relative Trajectory Error (RTE)]] | [[Scand]] [[Absolute Trajectory Error (ATE)]]/[[Relative Trajectory Error (RTE)]] | [[Sacson]] [[Absolute Trajectory Error (ATE)]]/[[Relative Trajectory Error (RTE)]] | Avg [[Absolute Trajectory Error (ATE)]] | Avg [[Relative Trajectory Error (RTE)]] |
|-------|------|---------------------|---------------|----------------|---------|---------|
| NWM | 103.2s | 5.831/1.219 | 1.113/0.297 | 4.037/0.928 | 3.032 | 0.696 |
| [[V-JEPA 2]].1 ViT-g | 10.6s | 5.758/1.200 | 1.094/0.299 | 3.904/0.921 | 2.975 | 0.690 |
| [[V-JEPA 2]].1 ViT-G | 10.6s | 5.687/1.187 | 1.038/0.285 | 4.054/0.938 | 2.990 | 0.688 |

[[V-JEPA 2]].1 matches NWM on navigation accuracy while being ~10x faster (10.6s vs. 103.2s). [[TartanDrive]] [[Absolute Trajectory Error (ATE)|ATE]] of 5.687 is the best achieved.

### Table 10: Video Question Answering

| Method | Enc/LLM Params | [[PerceptionTest]] | MVP | [[TempCompass]] | [[TemporalBench]] | [[TOMATO]] | [[TVBench]] | [[MVBench]] | Avg. |
|--------|---------------|----------------|-----|-------------|---------------|--------|---------|---------|------|
| InternVL-2.5 | —/7B | 68.9 | 39.9 | 68.3 | 24.3 | 29.4 | 61.6 | 72.6 | 52.1 |
| Qwen2VL | 675M/7B | 66.9 | 29.2 | 67.9 | 20.4 | 31.5 | 46.0 | 67.0 | 47.0 |
| PLM 8B | 1B/8B | 82.7 | 39.7 | 72.7 | 28.3 | 33.2 | 63.5 | 77.1 | 56.7 |
| [[V-JEPA 2]] ViT-g_384 | 1B/8B | 84.0 | 44.5 | 76.9 | 36.7 | 40.3 | 60.6 | 73.5 | 59.5 |
| [[V-JEPA 2]].1 ViT-G | 2B/8B | **85.1** | **47.9** | **77.8** | **39.2** | **41.7** | **65.1** | **78.3** | **60.2** |

[[V-JEPA 2]].1 ViT-G achieves the highest average VQA score (60.2), improving over [[V-JEPA 2]] (59.5) with gains across all seven benchmarks. The largest improvements are on MVP (+3.4) and [[TVBench]] (+4.5).

## Metrics Used

- [[Top-1 Accuracy]] — classification on [[Something-Something v2|SSv2]], [[Diving-48]], [[Kinetics-400|K400]], IN1K
- [[Mean Average Precision (mAP)]] — [[Ego4D]] short-term object-interaction anticipation (multiple AP variants)
- [[Recall@5]] — action anticipation on [[EPIC-KITCHENS-100]]
- [[RMSE]] — depth estimation on [[NYUv2]] and [[KITTI]]
- [[mIoU]] — semantic segmentation on [[ADE20K]], [[Cityscapes]], [[PASCAL VOC12]]
- [[J&F Mean]] — video object segmentation on [[DAVIS-2017]] and [[YouTube-VOS]]
- [[Success Rate]] — robot manipulation tasks (reach, grasp, pick-and-place)
- [[Absolute Trajectory Error (ATE)]] — navigation planning accuracy
- [[Relative Trajectory Error (RTE)]] — navigation planning accuracy
- [[VQA Accuracy]] — video question answering on [[PerceptionTest]], MVP, [[TempCompass]], [[TemporalBench]], [[TOMATO]], [[TVBench]], [[MVBench]]

## Datasets Used

- [[Something-Something v2]] — motion understanding classification (168K videos)
- [[Kinetics-400]] — action recognition benchmark
- [[HowTo100M]] — instructional video pretraining data
- [[YT-Temporal-1B]] — large-scale YouTube video data (dominant pretraining source at 72%)
- [[ImageNet-1K]] — image classification benchmark
- [[Diving-48]] — fine-grained diving motion classification
- [[Ego4D]] — egocentric video anticipation benchmark
- [[EPIC-KITCHENS-100]] — egocentric kitchen action anticipation
- [[NYUv2]] — indoor depth estimation benchmark
- [[KITTI]] — outdoor depth estimation benchmark
- [[ADE20K]] — semantic segmentation benchmark
- [[Cityscapes]] — urban scene segmentation benchmark
- [[PASCAL VOC12]] — object segmentation benchmark
- [[DAVIS-2017]] — video object segmentation benchmark
- [[YouTube-VOS]] — video object segmentation benchmark
- [[TartanDrive]] — off-road robotic navigation dataset
- [[Scand]] — navigation dataset
- [[Sacson]] — navigation dataset
- [[PerceptionTest]] — video QA benchmark
- [[MVP]] — video QA benchmark
- [[TempCompass]] — temporal reasoning video QA benchmark
- [[TemporalBench]] — temporal understanding benchmark
- [[TOMATO]] — video QA benchmark
- [[TVBench]] — video QA benchmark
- [[MVBench]] — video QA benchmark
- [[Droid Dataset]] — robot manipulation data (inherited from [[V-JEPA 2]]-AC)

## Related Papers

- [[V-JEPA 2]] — direct predecessor; [[V-JEPA 2]].1 adds dense features while maintaining global performance
- [[V-JEPA]] — original paper establishing the [[V-JEPA]] framework
- [[DINOv2]] — image self-supervised baseline; [[V-JEPA 2]].1 closes the dense prediction gap
- [[DINOv3]] — state-of-the-art image SSL; [[V-JEPA 2]].1 is competitive on dense tasks at much smaller scale
- [[InternVideo2]] — video understanding baseline
- [[LeJEPA]] — provides theoretical grounding for JEPA training objectives
- [[LeWorldModel]] — applies JEPA principles to world modeling from pixels
