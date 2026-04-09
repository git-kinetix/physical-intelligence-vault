---
tags: [paper, vla]
title: "Gemini Robotics: Bringing AI into the Physical World"
authors: [Gemini Robotics Team, Google DeepMind]
year: 2025
arxiv: "https://arxiv.org/abs/2503.20020"
repo: "https://github.com/google-deepmind/gemini-robotics-sdk"
group: "VLA Models"
importance: 
aliases: [Gemini Robotics, Gemini Robotics-ER, Gemini VLA]
---

![[PDFs/Gemini Robotics.pdf]]


# Gemini Robotics: Bringing AI into the Physical World

## Summary

Gemini Robotics is Google DeepMind's family of Vision-Language-Action models built on Gemini 2.0, designed to bring advanced AI capabilities into physical robot control. The paper introduces two main models: Gemini Robotics, a generalist VLA model capable of directly controlling robots for complex manipulation tasks, and Gemini Robotics-ER (Embodied Reasoning), which extends Gemini's multimodal reasoning with enhanced spatial and temporal understanding for the physical world.

Gemini Robotics executes smooth and reactive movements across a wide range of complex manipulation tasks while being robust to variations in object types and positions, handling unseen environments, and following diverse open-vocabulary instructions. The model is trained on thousands of hours of real-world expert robot demonstrations collected on ALOHA 2 robots over 12 months, supplemented with web documents, code, multimodal content, and embodied reasoning data. Gemini Robotics-ER achieves state-of-the-art performance on embodied reasoning benchmarks ([[ERQA Benchmark|ERQA]]), 2D pointing, and 3D object detection, while Gemini Robotics demonstrates over 80% success rates on half of 20 diverse manipulation tasks and can learn new tasks from as few as 100 demonstrations.

The paper also introduces the [[ERQA Benchmark|ERQA]] benchmark (400 multiple-choice VQA questions) for evaluating embodied reasoning and presents a comprehensive framework for responsible development and safety of robotics foundation models.

## Key Contributions

- Gemini Robotics VLA: A generalist model for direct robot control built on Gemini 2.0, achieving strong performance across 20 diverse manipulation tasks
- Gemini Robotics-ER: An embodied reasoning model with state-of-the-art spatial-temporal understanding, including 2D/3D perception capabilities
- [[ERQA Benchmark]]: A new 400-question benchmark for evaluating embodied reasoning across spatial reasoning, trajectory reasoning, action reasoning, state estimation, pointing, multi-view reasoning, and task reasoning
- Few-shot learning: Over 70% success on 7 out of 8 new tasks with at most 100 demonstrations
- Long-horizon specialization: 100% success on lunch-box packing and 79% average across six specialized dexterous tasks
- Comprehensive safety and responsible development framework for robotics foundation models

## Architecture / Method

**Gemini Robotics (VLA):**
- Backbone: Distilled from Gemini Robotics-ER, running in the cloud
- Local action decoder: On-robot onboard computer
- Backbone query-to-response latency: <160 ms
- End-to-end latency (observations to action chunks): ~250 ms
- Effective control frequency: 50 Hz
- Training data: Thousands of hours of teleoperated demonstrations on ALOHA 2 robots + web data

**Gemini Robotics-ER (Embodied Reasoning):**
- Built on Gemini 2.0 with enhanced spatial-temporal understanding
- Capabilities: Object detection, trajectory prediction, grasp prediction, 3D bounding box estimation
- Supports in-context learning (ICL) from demonstration examples

**Training:**
- Large-scale teleoperated robot action dataset collected on a fleet of ALOHA 2 robots over 12 months
- Thousands of diverse tasks covering varied manipulation skills, objects, task difficulties, episode horizons, and dexterity requirements
- Supplemented with web documents, code, multimodal content, and embodied reasoning data

## Results

### Table 1: VLM Benchmark Comparison on Embodied Reasoning

| Benchmark | Gemini 1.5 Flash | Gemini 1.5 Pro | Gemini 2.0 Flash | Gemini 2.0 Pro Exp | GPT-4o mini | GPT-4o | Claude 3.5 Sonnet |
|-----------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| [[ERQA Benchmark]] | 42.3 | 41.8 | 46.3 | 48.3 | 37.3 | 47.0 | 35.5 |
| RealworldQA (test) | 69.0 | 64.5 | 71.6 | 74.5 | 65.0 | 71.9 | 61.4 |
| BLINK (val) | 59.2 | 64.4 | 65.0 | 65.2 | 56.9 | 62.3 | 60.2 |

Gemini 2.0 Pro Exp achieves the highest scores on [[ERQA Benchmark|ERQA]] (48.3) and RealworldQA (74.5), while remaining competitive on BLINK. GPT-4o is a strong competitor on [[ERQA Benchmark|ERQA]] (47.0) and RealworldQA (71.9).

### Table 2: Chain-of-Thought Impact on [[ERQA Benchmark|ERQA]]

| Prompt Variant | Gemini 2.0 Flash | Gemini 2.0 Pro Exp | GPT-4o mini | GPT-4o | Claude 3.5 Sonnet |
|----------------|:---:|:---:|:---:|:---:|:---:|
| Without CoT | 46.3 | 48.3 | 37.3 | 47.0 | 35.5 |
| With CoT | 50.3 | 54.8 | 40.5 | 50.5 | 45.8 |

Chain-of-thought prompting consistently improves all models on [[ERQA Benchmark|ERQA]]. Claude 3.5 Sonnet shows the largest relative improvement (+10.3 points), while Gemini 2.0 Pro Exp achieves the highest absolute score (54.8).

### Table 3: 2D Pointing Benchmarks (Open-Vocabulary)

| Benchmark | Gemini Robotics-ER | Gemini 2.0 Flash | Gemini 2.0 Pro | GPT-4o mini | GPT-4o | Claude 3.5 Sonnet | Molmo 7B-D | Molmo 72B |
|-----------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Paco-LVIS | 71.3 | 46.1 | 45.5 | 11.8 | 16.2 | 12.4 | 45.4 | 47.1 |
| Pixmo-Point | 49.5 | 25.8 | 20.9 | 5.9 | 5.0 | 7.2 | 14.7 | 12.5 |
| Where2Place | 45.0 | 33.8 | 38.8 | 13.8 | 20.6 | 16.2 | 45.0 | 63.8 |

Gemini Robotics-ER dominates on Paco-LVIS (71.3) and Pixmo-Point (49.5), dramatically outperforming all other models. On Where2Place, Molmo 72B leads (63.8) while Gemini Robotics-ER achieves 45.0.

### Table 4: 3D Object Detection on [[SUN-RGBD]]

| Model | AP@15 |
|-------|:-----:|
| Gemini Robotics-ER | 48.3 |
| ImVoxelNet* | 43.7 |
| Gemini 2.0 Pro Exp | 32.5 |
| Gemini 2.0 Flash | 30.7 |
| Implicit3D | 24.1 |
| Total3DU | 14.3 |

*ImVoxelNet evaluated on an easier set of 10 categories. Gemini Robotics-ER achieves state-of-the-art 3D object detection performance (48.3 AP@15) on the full [[SUN-RGBD]] benchmark.

### Table 5: ALOHA 2 Simulation Task Success Rates (50 trials)

| Model | Context | Avg | Banana Lift | Banana in Bowl | Mug on Plate | Bowl on Rack | Banana Handover | Fruit Bowl | Pack Toy |
|-------|:-------:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Gemini 2.0 Flash | Zero-shot | 27 | 34 | 54 | 46 | 24 | 26 | 4 | 0 |
| Gemini Robotics-ER | Zero-shot | 53 | 86 | 84 | 72 | 60 | 54 | 16 | 0 |
| Gemini 2.0 Flash | ICL | 51 | 94 | 90 | 36 | 16 | 94 | 0 | 26 |
| Gemini Robotics-ER | ICL | 65 | 96 | 96 | 74 | 36 | 96 | 4 | 54 |

In-context learning (ICL) dramatically improves performance for both models. Gemini Robotics-ER with ICL achieves the highest average (65%), with near-perfect scores on Banana Lift (96%), Banana in Bowl (96%), and Banana Handover (96%).

### Table 6: Real-World ALOHA 2 Task Success Rates

| Context | Avg | Banana Handover | Fold Dress | Wiping |
|---------|:---:|:---:|:---:|:---:|
| Zero-shot | 25 | 30 | 0 | 44 |
| ICL | 65 | 70 | 56 | 67 |

In-context learning provides a massive improvement in real-world tasks, taking average success from 25% to 65%. The Fold Dress task goes from 0% zero-shot to 56% with ICL demonstrations.

### Table 7: Few-Shot Learning Results (at most 100 demonstrations)

| Metric | Value |
|--------|:-----:|
| Tasks with >70% success | 7 out of 8 |
| Tasks with 100% success | 2 |
| Demonstration budget | <=100 per task |

The model achieves strong performance on novel tasks with minimal training data, including origami and lunch-box manipulation.

### Table 8: Long-Horizon Specialization Results

| Metric | Value |
|--------|:-----:|
| Lunch-box packing | 100% success |
| Average across 6 specialized tasks | 79% success |
| Spelling game accuracy | ~60% |

Gemini Robotics achieves perfect performance on the full long-horizon lunch-box packing task and 79% average across specialized dexterous tasks that baselines cannot consistently complete.

### Table 9: Multi-Task Evaluation Highlights (20 diverse tasks)

| Metric | Value |
|--------|:-----:|
| Tasks with >80% success rate | 10 out of 20 |
| Gemini Robotics vs [[Pi0]] (reimplemented) | Significantly better on most tasks |
| Gemini Robotics vs multi-task diffusion policy | Significantly better |
| Only method with non-zero success on hardest tasks | Gemini Robotics |

Gemini Robotics is the only method achieving non-zero success on the most challenging deformable object manipulation tasks.

## Metrics Used

- [[Success Rate]] -- primary metric for manipulation tasks, measured as percentage of successful episodes
- [[Task Progress Score]] -- continuous progress measure for partial task completion
- [[ERQA Accuracy]] -- multiple-choice accuracy on the 400-question [[ERQA Benchmark|Embodied Reasoning QA]] benchmark
- [[2D Pointing Accuracy]] -- accuracy where predicted point falls within ground truth region mask (Paco-LVIS, Pixmo-Point, Where2Place)
- [[3D Object Detection AP]] -- [[Mean Average Precision (mAP)|Average Precision]] at [[IoU]]@15 on [[SUN-RGBD]] benchmark
- [[RealworldQA Accuracy]] -- multiple-choice accuracy on real-world visual QA
- [[BLINK Accuracy]] -- multiple-choice accuracy on the BLINK visual benchmark

## Datasets Used

- [[ALOHA 2 Teleoperation Dataset]] -- thousands of hours of expert demonstrations collected on ALOHA 2 fleet over 12 months, covering thousands of diverse tasks
- [[ERQA Benchmark]] -- 400 multiple-choice VQA questions across 7 embodied reasoning categories, introduced in this paper
- [[SUN-RGBD]] -- RGB-D dataset used for 3D object detection evaluation
- [[Paco-LVIS]] -- dataset used for 2D open-vocabulary pointing evaluation
- [[Pixmo-Point]] -- dataset used for 2D pointing evaluation
- [[Where2Place]] -- dataset used for placement-focused 2D pointing evaluation
- [[RealworldQA]] -- real-world visual question answering benchmark
- [[BLINK]] -- visual benchmark for embodied reasoning evaluation

## Related Papers

- [[Pi0]] -- Physical Intelligence's VLA flow model, reimplemented as a baseline in this paper
- [[Pi0.5]] -- Physical Intelligence's model with open-world generalization
- [[Pi0.6]] -- Physical Intelligence's VLA with RL from experience
- [[GR00T]] -- NVIDIA's VLA for humanoid robots
