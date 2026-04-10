---
tags: [paper, jepa, motion]
title: "V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning"
authors: [Mido Assran, Adrien Bardes, David Fan, Quentin Garrido, Russell Howes, Mojtaba Komeili, Matthew Muckley, Ammar Rizvi, Claire Roberts, Koustuv Sinha, Artem Zholus, Sergio Arnaud, Abha Gejji, Ada Martin, Francois Robert Hogan, Daniel Dugas, Piotr Bojanowski, Vasil Khalidov, Patrick Labatut, Francisco Massa, Marc Szafraniec, Kapil Krishnakumar, Yong Li, Xiaodong Ma, Sarath Chandar, Franziska Meier, Yann LeCun, Michael Rabbat, Nicolas Ballas]
year: 2025
arxiv: "https://arxiv.org/abs/2506.09985"
repo: "https://github.com/facebookresearch/vjepa2"
group: "JEPA Family"
importance: 5
aliases: [V-JEPA 2, VJEPA2, V-JEPA2]
---

!PDFs/[[V-JEPA]] 2.pdf


# [[V-JEPA]] 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning

## Summary

[[V-JEPA]] 2 scales the original [[V-JEPA]] framework to significantly larger models and datasets, pretraining on [[VideoMix22M]] -- a dataset comprising over 1 million hours of internet video and images (22M samples across [[Something-Something v2|SSv2]], Kinetics, [[HowTo100M]], [[YouTube-Temporal-1B|YT-Temporal-1B]], and ImageNet). The paper demonstrates that self-supervised video models can serve as versatile visual encoders for understanding, prediction, and robotic planning. [[V-JEPA]] 2 achieves strong performance on motion understanding (77.3% top-1 on [[Something-Something v2|SSv2]]), state-of-the-art action anticipation (39.7 [[Recall@5]] on [[EPIC-KITCHENS-100|Epic-Kitchens]]-100), and competitive video question-answering when aligned with an LLM.

A major contribution is [[V-JEPA]] 2-AC (Action-Conditioned), a latent world model variant trained on less than 62 hours of unlabeled robot videos from the Droid dataset. [[V-JEPA]] 2-AC enables zero-shot robotic manipulation (reaching, grasping, pick-and-place) on Franka arms through planning with image goals -- without collecting any task-specific data, training, or reward signals. The system plans in latent space, achieving 80% success on pick-and-place tasks for cups and 65% for boxes, substantially outperforming baselines like [[Octo]] and [[NVIDIA Cosmos|Cosmos]].

## Key Contributions

- Scales [[V-JEPA]] to ViT-g with 1B+ parameters pretrained on 1M+ hours of video ([[VideoMix22M]])
- Achieves state-of-the-art on motion understanding ([[Something-Something v2|SSv2]]: 77.3%) and action anticipation (EK100: 39.7 [[Recall@5|R@5]])
- Introduces [[V-JEPA]] 2-AC, an action-conditioned world model for zero-shot robotic planning from latent features
- Demonstrates zero-shot robotic manipulation using only 62 hours of unlabeled robot video, no task-specific training
- Shows systematic scaling benefits: +4.0 points average from scaling data, model, training, and resolution
- Achieves state-of-the-art Video QA at 8B parameter scale when combined with Llama 3.1 8B

## Architecture / Method

[[V-JEPA]] 2 builds on the [[V-JEPA]] framework with several scaling improvements:

**Self-Supervised Pretraining:**
1. **Encoder**: ViT-g/16 (1B parameters) processes visible video patches
2. **Predictor**: A transformer predicts latent representations of masked spatiotemporal regions
3. **Target Encoder**: EMA of the encoder provides prediction targets
4. **Multi-block masking**: Samples target blocks at large spatiotemporal scales for semantic feature learning

**Scaling Recipe (cumulative improvements):**
- Data scaling: [[VideoMix2M]] to [[VideoMix22M]] (+1.0 pt avg)
- Model scaling: ViT-L to ViT-g (+1.5 pt avg)
- Training scaling: Extended schedule and optimization (+0.8 pt avg)
- Resolution scaling: 256px to 384px (+0.7 pt avg)

**Frozen Evaluation Protocol:**
- Encoder weights are frozen; a task-specific 4-layer attentive probe is trained on top of representations

**[[V-JEPA]] 2-AC (Action-Conditioned):**
- Trains an action-conditioned latent predictor on top of frozen [[V-JEPA]] 2 features
- Uses <62 hours of unlabeled robot videos from the Droid dataset
- Plans via sampling-based optimization (800 samples, 10 refinement steps) in latent space
- Achieves ~16 seconds planning time per action versus ~4 minutes for [[NVIDIA Cosmos|Cosmos]]

**LLM Alignment:**
- [[V-JEPA]] 2 encoder is aligned with Llama 3.1 8B for video question answering
- Uses a learned projection layer between the frozen video encoder and the LLM

## Results

### Table 1: [[VideoMix22M]] Pretraining Dataset Composition

| Source | Samples | Type | Total Hours | Curation | Weight |
|--------|---------|------|-------------|----------|--------|
| [[Something-Something v2]] | 168K | EgoVideo | 168 | No | 0.056 |
| Kinetics | 733K | ExoVideo | 614 | No | 0.188 |
| [[HowTo100M]] | 1.1M | ExoVideo | 134K | No | 0.318 |
| [[YouTube-Temporal-1B]] | 19M | ExoVideo | 1.6M | Yes | 0.188 |
| ImageNet | 1M | Images | n/a | No | 0.250 |

The dataset contains over 1 million hours of video, with [[YouTube-Temporal-1B]] providing the bulk of video hours. [[Something-Something v2|SSv2]] is upweighted relative to its size given its importance for motion understanding.

### Table 2: Frozen Video and Image Classification

| Method | Params | [[Something-Something v2]] | [[Diving-48]] | [[Jester]] | [[Kinetics-400]] | COIN | IN1K | Avg. |
|--------|--------|------|-----------|--------|------|------|------|------|
| DINOv2 (w/ reg) | 1.1B | 50.6 | 82.5 | — | 83.4 | — | 86.2 | — |
| InternVideo2-1B | 1B | 69.7 | 86.4 | — | 89.4 | — | 85.8 | — |
| SigLIP2 | — | — | — | — | — | — | — | — |
| [[V-JEPA]] | 630M | 72.2 | — | — | 81.9 | — | 77.4 | 84.2 |
| [[V-JEPA]] 2 ViT-L/16 | 300M | 73.7 | 89.0 | — | — | — | — | — |
| [[V-JEPA]] 2 ViT-g/16 | 1B | 75.3 | — | — | — | — | 84.6 | — |
| [[V-JEPA]] 2 ViT-g/16_384 | 1B | 77.3 | 90.2 | — | — | — | — | 88.2 |

[[V-JEPA]] 2 achieves the best average performance (88.2%) across all six classification tasks. [[Something-Something v2|SSv2]] accuracy of 77.3% represents a +7.6 point improvement over InternVideo2-1B, demonstrating exceptional motion understanding.

### Table 3: Action Anticipation on [[EPIC-KITCHENS-100]] ([[Recall@5]])

| Method | Params | Verb | Noun | Action |
|--------|--------|------|------|--------|
| InAViT | 160M | 51.9 | 52.0 | 25.8 |
| Video-LLaMA | 7B | 52.9 | 52.0 | 26.0 |
| PlausiVL | 8B | 55.6 | 54.2 | 27.6 |
| [[V-JEPA]] 2 ViT-L | 300M | — | — | 32.7 |
| [[V-JEPA]] 2 ViT-g_384 | 1B | 63.6 | 57.1 | **39.7** |

[[V-JEPA]] 2 achieves 39.7 action [[Recall@5]] on EK100, a 44% relative improvement over PlausiVL (27.6), the previous state of the art. The model shows strong scaling behavior from ViT-L (32.7) to ViT-g (39.7).

### Table 4: Video Question Answering ([[V-JEPA]] 2 + Llama 3.1 8B)

| Method | Encoder/LLM Params | [[PerceptionTest]] | MVP | [[TempCompass]] | [[TemporalBench]] | [[TOMATO]] | Avg. |
|--------|-------------------|----------------|-----|-------------|---------------|--------|------|
| InternVL-2.5 | —/7B | 68.9 | 39.9 | 68.3 | 24.3 | 29.4 | — |
| Qwen2VL | 675M/7B | 66.9 | 29.2 | 67.9 | 20.4 | 31.5 | — |
| Tarsier 2 | —/7B | — | — | 75.3 | — | — | — |
| [[V-JEPA]] 2 ViT-g_384 | 1B/8B | **84.0** | **44.5** | **76.9** | **36.7** | **40.3** | — |

[[V-JEPA]] 2 combined with Llama 3.1 8B achieves state-of-the-art on all five Video QA benchmarks at the 8B scale, with a +15.1 point lead on [[PerceptionTest]] and +12.4 points on [[TemporalBench]] vs. InternVL-2.5.

### Table 5: Zero-Shot Robot Manipulation Success Rates (%)

| Method | Location | Reach | Grasp Cup | Grasp Box | Reach w/ Obj Cup | Reach w/ Obj Box | Pick-Place Cup | Pick-Place Box |
|--------|----------|-------|-----------|-----------|------------------|------------------|----------------|----------------|
| [[Octo]] | Lab 1 | 100 | 20 | 0 | 20 | 70 | 20 | 10 |
| [[Octo]] | Lab 2 | 100 | 10 | 0 | 10 | 70 | 10 | 10 |
| [[Octo]] | Average | 100 | 15 | 0 | 15 | 70 | 15 | 10 |
| [[V-JEPA]] 2-AC | Lab 1 | 100 | 70 | 30 | 90 | 80 | 80 | 80 |
| [[V-JEPA]] 2-AC | Lab 2 | 100 | 60 | 20 | 60 | 70 | 80 | 50 |
| [[V-JEPA]] 2-AC | Average | 100 | 65 | 25 | 75 | 75 | 80 | 65 |

[[V-JEPA]] 2-AC dramatically outperforms [[Octo]] across all manipulation tasks. Pick-and-place success is 80% (cup) and 65% (box) vs. 15% and 10% for [[Octo]]. These results are achieved zero-shot -- without any task-specific data or training from the deployment environments.

### Table 6: Planning Comparison ([[V-JEPA]] 2-AC vs. [[NVIDIA Cosmos|Cosmos]])

| Model | [[Planning Time]] per Action | Samples | Refinement Steps | Grasp | Pick-Place |
|-------|-------------------------|---------|------------------|-------|------------|
| [[NVIDIA Cosmos]] | ~4 minutes | 80 | 10 | Lower | Lower |
| [[V-JEPA]] 2-AC | ~16 seconds | 800 | 10 | 65% | 80%/65% |

[[V-JEPA]] 2-AC plans 15x faster than [[NVIDIA Cosmos|Cosmos]] while achieving substantially higher manipulation success rates, demonstrating the efficiency of latent-space planning.

## Metrics Used

- [[Top-1 Accuracy]] — frozen probe-based classification on [[Something-Something v2|SSv2]], [[Kinetics-400|K400]], [[Diving-48]], [[Jester]], COIN, IN1K
- [[Recall@5]] — action anticipation metric on [[EPIC-KITCHENS-100]] (verb, noun, action)
- [[Success Rate]] — robot manipulation task completion (reach, grasp, pick-and-place)
- Paired Accuracy — video QA metric on MVP
- Test Accuracy — video QA metric on [[PerceptionTest]]
- [[Multi-choice Accuracy]] — video QA metric on [[TempCompass]]
- Multi-binary Short QA Accuracy — video QA metric on [[TemporalBench]]
- [[TOMATO Accuracy]] — video QA metric on [[TOMATO]] benchmark
- [[Planning Time]] — wall-clock time per planning action for robot control
- [[Euclidean Distance to Goal]] — distance metric for robot manipulation evaluation

## Datasets Used

- [[VideoMix22M]] — pretraining dataset (22M samples: [[Something-Something v2|SSv2]], Kinetics, [[HowTo100M]], [[YouTube-Temporal-1B|YT-Temporal-1B]], ImageNet)
- [[Something-Something v2]] — fine-grained motion understanding (168K videos)
- [[Kinetics-400]] — action recognition benchmark
- [[Kinetics-700]] — extended action recognition dataset
- [[HowTo100M]] — instructional video dataset
- [[YT-Temporal-1B]] — large-scale curated YouTube video dataset
- [[ImageNet-1K]] — image classification benchmark
- [[Diving-48]] — fine-grained diving motion classification
- [[Jester]] — hand gesture recognition dataset
- [[COIN]] — instructional video classification
- [[EPIC-KITCHENS-100]] — egocentric kitchen action anticipation benchmark
- [[PerceptionTest]] — video QA benchmark
- [[MVP]] — video QA benchmark
- [[TempCompass]] — temporal reasoning video QA benchmark
- [[TemporalBench]] — temporal understanding benchmark
- [[TOMATO]] — video QA benchmark
- [[Droid Dataset]] — robot manipulation trajectories (~62 hours of unlabeled video)
- [[Open-X Embodiment]] — multi-robot dataset (used by [[Octo]] baseline)

## Related Papers

- [[V-JEPA]] — predecessor; [[V-JEPA]] 2 scales the architecture and data by an order of magnitude
- [[V-JEPA 2.1]] — successor focusing on dense features and multi-level prediction
- [[I-JEPA]] — image-based JEPA that inspired the video extension
- DINOv2 — strong image self-supervised baseline; [[V-JEPA]] 2 surpasses it on motion tasks
- InternVideo2 — video understanding baseline that [[V-JEPA]] 2 outperforms on [[Something-Something v2|SSv2]]
- [[Octo]] — generalist robot policy baseline significantly outperformed by [[V-JEPA]] 2-AC
- [[Cosmos]] — foundation world model baseline; [[V-JEPA]] 2-AC plans 15x faster with higher success
