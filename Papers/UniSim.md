---
tags: [paper, world-model, video-planning]
title: "Learning Interactive Real-World Simulators"
authors: [Sherry Yang, Yilun Du, Kamyar Ghasemipour, Jonathan Tompson, Leslie Kaelbling, Dale Schuurmans, Pieter Abbeel]
year: 2023
arxiv: "https://arxiv.org/abs/2310.06114"
repo: "https://github.com/universal-simulator/unisim"
group: "Video Generation / Planning"
importance: 
aliases: [UniSim, Universal Simulator]
---

![[PDFs/UniSim.pdf]]


# Learning Interactive Real-World Simulators

## Summary

UniSim is a universal simulator that learns to generate action-conditioned video of real-world interactions through generative modeling. Developed by researchers at Google, MIT, and UC Berkeley, UniSim addresses the fundamental challenge of training embodied AI agents: the need for interactive environments that capture the complexity of the real world. Rather than hand-crafting simulators, UniSim learns simulation directly from diverse video data.

The key innovation is the careful orchestration of heterogeneous datasets -- each providing a different aspect of real-world experience. Image datasets provide abundant object diversity, robotics datasets provide densely sampled action sequences, navigation datasets provide diverse movement patterns, and human activity datasets ([[Ego4D]], [[EPIC-KITCHENS-100|EPIC-KITCHENS]]) provide natural interaction dynamics. By combining these complementary sources, UniSim learns to simulate visual outcomes of both high-level language instructions ("open the drawer") and low-level continuous controls ("move by delta x, y").

UniSim demonstrates zero-shot transfer of policies trained entirely in the learned simulator to real-world environments. Vision-language policies and RL policies trained in UniSim successfully execute tasks on real robots without any real-world fine-tuning, validating the simulator's fidelity. The model was published at ICLR 2024.

## Key Contributions

- Proposes UniSim, a universal simulator that learns real-world interaction dynamics from diverse video data sources
- Demonstrates successful zero-shot sim-to-real transfer: policies trained entirely in UniSim deploy to real robots
- Shows that careful orchestration of heterogeneous datasets (images, robotics, navigation, human activity) enables comprehensive simulation
- Supports both high-level language instructions and low-level continuous actions as conditioning signals
- Achieves strong video generation quality ([[FVD]] 211.3 on [[Ego4D]]) with a 5.6B parameter Video U-Net
- Demonstrates applications in vision-language planning, reinforcement learning, and video captioning

## Architecture / Method

**Video U-Net Architecture:**
- A 5.6B parameter Video U-Net serves as the generative backbone
- The model generates future video frames conditioned on past observations and action inputs
- Trained on 512 TPU-v3 chips over 20 days

**Action Conditioning:**
- **High-level**: T5 language embeddings encode natural language instructions (e.g., "open the drawer")
- **Low-level**: Discretized continuous control values (e.g., delta x, y movements) are concatenated with language embeddings
- The same model handles both instruction types through a unified conditioning interface

**Multi-Dataset Training:**
UniSim is trained jointly on diverse data sources, each providing complementary aspects:
- **Image datasets**: Abundant object diversity and visual variety
- **Robotics datasets**: Dense action labels and manipulation dynamics
- **Navigation datasets ([[Ego4D]])**: Diverse camera movements and spatial understanding
- **Human activity datasets ([[EPIC-KITCHENS-100|EPIC-KITCHENS]])**: Natural interaction patterns
- **Panoramic scans**: Spatial scene understanding
- **Internet imagery**: Broad visual coverage

**Frame Conditioning:**
- Conditioning on 4 recent frames achieves [[FVD]] of 211.3 (vs. 315.7 for single-frame conditioning)
- The model uses a buffer of recent observations for temporal context

**Applications:**
1. **Vision-Language Planning**: High-level policies plan using generated video previews
2. **RL Training**: Low-level RL policies train entirely within UniSim-generated environments
3. **Video Captioning**: Synthetic data from UniSim improves captioning models

## Results

### Table 1: Video Generation Quality

| Configuration | [[FVD]] ([[Ego4D]]) | CLIP Score |
|--------------|-------------|------------|
| UniSim (4 frames, 5.6B) | 211.3 | 22.63 |
| UniSim (1 frame, 5.6B) | 315.7 | -- |
| UniSim (4 frames, 1.6B) | 224.6 | -- |

Conditioning on 4 recent frames and using the full 5.6B model provides the best generation quality.

### Table 2: Zero-Shot Sim-to-Real Transfer (RL Policy)

| Method | Overall Success |
|--------|----------------|
| UniSim + RL fine-tuning | 81% |
| Behavioral cloning baseline | 58% |
| Pointing-based (UniSim + RL) | 71% |
| Pointing-based (baseline) | 12% |

Policies trained in UniSim achieve 81% success when transferred zero-shot to real environments, compared to 58% for behavioral cloning.

### Table 3: Vision-Language Planning

| Method | Reduction in Distance to Goal (RDG) |
|--------|-------------------------------------|
| UniSim + hindsight data | 0.34 +/- 0.13 |
| Behavioral cloning | 0.11 +/- 0.13 |

UniSim-based planning achieves approximately 3x improvement in goal-reaching over behavioral cloning on block rearrangement tasks.

### Table 4: Video Captioning Transfer

| Training Data | CIDEr (ActivityNet) |
|--------------|---------------------|
| Real videos | 54.90 |
| UniSim synthetic | 46.23 |

Models fine-tuned exclusively on UniSim-generated synthetic data achieve 84% of the performance of models trained on real videos for video captioning.

### Table 5: Model Scale Ablation

| Model Size | [[FVD]] ([[Ego4D]]) |
|-----------|-------------|
| 5.6B | 211.3 |
| 1.6B | 224.6 |

Larger models produce higher-fidelity simulations, with improvements plateauing at larger scales.

## Metrics Used

- [[Frechet Video Distance (FVD)]] -- measures quality and diversity of generated video against real video distributions
- [[CLIP Score]] -- measures alignment between generated video frames and conditioning text
- [[CIDEr]] -- captioning quality metric for video captioning transfer evaluation
- [[Success Rate]] -- task completion rate for sim-to-real transfer evaluation
- [[Reduction in Distance to Goal (RDG)]] -- planning effectiveness metric

## Datasets Used

- [[Ego4D]] -- first-person human activity videos for navigation and interaction dynamics
- [[EPIC-KITCHENS]] -- kitchen activity videos for manipulation dynamics
- [[Open X-Embodiment]] -- robot manipulation trajectories for action-conditioned generation
- [[ActivityNet Captions]] -- video captioning benchmark for transfer evaluation
- [[Internet Imagery]] -- diverse images for visual coverage

## Related Papers

- [[UniPi]] -- closely related work by overlapping authors (Yilun Du), using video generation for universal policy learning
- [[Genie 2]] -- Google DeepMind's interactive environment generation, sharing the goal of learned interactive simulation
- [[NVIDIA Cosmos]] -- large-scale world model for physical AI, another approach to learned simulation
- [[DIAMOND]] -- diffusion-based world model for Atari, sharing the diffusion-based generation paradigm
- [[DreamerV3]] -- traditional learned world model for RL, representing the RSSM-based approach that UniSim aims to supersede with learned video simulation
