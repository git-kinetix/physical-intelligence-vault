---
tags: [paper, vla, motion]
title: "GR00T N1: An Open Foundation Model for Generalist Humanoid Robots"
authors: [Johan Bjorck, Fernando Castaneda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, Joel Jang, Zhenyu Jiang, Jan Kautz, Kaushil Kundalia, Lawrence Lao, Zhiqi Li, Zongyu Lin, Kevin Lin, Guilin Liu, Edith Llontop, Loic Magne, Ajay Mandlekar, Avnish Narayan, Soroush Nasiriany, Scott Reed, You Liang Tan, Guanzhi Wang, Zu Wang, Jing Wang, Qi Wang, Jiannan Xiang, Yuqi Xie, Yinzhen Xu, Zhenjia Xu, Seonghyeon Ye, Zhiding Yu, Ao Zhang, Hao Zhang, Yizhou Zhao, Ruijie Zheng, Yuke Zhu]
year: 2025
arxiv: "https://arxiv.org/abs/2503.14734"
repo: "https://github.com/NVIDIA/Isaac-GR00T"
group: "VLA Models"
importance: 5
aliases: [GR00T, GR00T-N1, GR00T N1, GR00T-N1-2B, NVIDIA GR00T]
---

!PDFs/GR00T.pdf


# GR00T N1: An Open Foundation Model for Generalist Humanoid Robots

## Summary

GR00T N1 is NVIDIA's open foundation model for generalist humanoid robots, introducing a dual-system Vision-Language-Action (VLA) architecture. The model combines a vision-language module (System 2) that interprets the environment through vision and language instructions with a diffusion transformer module (System 1) that generates fluid motor actions in real time. Both modules are tightly coupled and jointly trained end-to-end.

The model is trained on a heterogeneous "data pyramid" consisting of real-robot trajectories (from the Fourier GR-1 humanoid, [[Open X-Embodiment]], and AgiBot-Alpha), human egocentric videos, and synthetically generated datasets including neural trajectories and simulation trajectories via [[DexMimicGen]]. GR00T-N1-2B, the publicly released variant, contains 2.2 billion total parameters and was pre-trained using approximately 50,000 H100 GPU hours.

GR00T N1 outperforms state-of-the-art imitation learning baselines on standard simulation benchmarks ([[RoboCasa]], [[DexMimicGen]], GR-1 tasks) and demonstrates strong performance with high data efficiency on the Fourier GR-1 humanoid robot for language-conditioned bimanual manipulation tasks.

## Key Contributions

- Dual-system VLA architecture combining a vision-language module (System 2) with a diffusion transformer action module (System 1)
- A "data pyramid" training strategy that leverages real robot data, simulation data, and human video data through latent actions and neural trajectories
- Neural trajectory generation technique that augments real robot data by 10x using video generation models
- [[DexMimicGen]] pipeline producing 540,000 simulation demonstrations (6,500 hours equivalent)
- Open-source release of the GR00T-N1-2B model with 2.2B parameters
- Demonstration of strong data efficiency, achieving 42.6% average success with only 10% of available training data

## Architecture / Method

GR00T N1 uses a dual-system architecture:

**System 2 (Vision-Language Module):** Built on Eagle-2 VLM with a SigLIP-2 image encoder at 224x224 resolution producing 64 image tokens per frame, and a SmolLM2 LLM backbone. The VLM component contains 1.34B parameters. Representations are extracted from the 12th (middle) layer of the LLM rather than the final layer, which was found to yield both faster inference and higher policy success rates.

**System 1 (Diffusion Transformer):** A flow-matching diffusion transformer that takes the VLM embeddings as conditioning and generates action chunks of size H=16. At inference time, K=4 denoising steps are used. The flow-matching loss is:

L_fm(theta) = E[||V_theta(phi_t, A_t^tau, q_t) - (epsilon - A_t)||^2]

**Data Pyramid:**
- Base layer: Web-scale human egocentric videos ([[Ego4D]], [[Ego-Exo4D]], [[Assembly-101]], [[EPIC-KITCHENS-100|EPIC-KITCHENS]], [[HOI4D]], [[HoloAssist]], [[RH20T-Human]]) trained with latent action labels
- Middle layer: Synthetic data including ~827 hours of neural trajectories (10x augmented from 88 hours real data) and 540,000 [[DexMimicGen]] simulation demonstrations
- Peak layer: Real robot demonstrations from GR-1 humanoid, [[Open X-Embodiment]], and AgiBot-Alpha

**Training:** Pre-trained on up to 1024 H100 GPUs connected via NVIDIA Quantum-2 InfiniBand. Neural trajectory generation required 105,000 L40 GPU hours. Fine-tuning can be performed on a single A6000 GPU.

## Results

### Table 1: Training Data Generation Strategies

| Strategy | Real-Robot Data | Simulated Robot Data | Human Video |
|----------|:-:|:-:|:-:|
| Latent Actions | Yes | Yes | Yes |
| Neural Trajectories | Yes | Yes | -- |
| Simulation Trajectories | Yes | Yes | -- |

Latent action learning applies broadly to diverse video datasets. Neural trajectories require datasets with robot actions, while simulation trajectories require a physics simulator.

### Table 2: Simulation Results (100 demonstrations per task)

| Model | [[RoboCasa]] | DexMG | GR-1 | Average |
|-------|----------|-------|------|---------|
| BC Transformer | 26.3% | 53.9% | 16.1% | 26.4% |
| Diffusion Policy | 25.6% | 56.1% | 32.7% | 33.4% |
| GR00T-N1-2B | 32.1% | 66.5% | 50.0% | 45.0% |

GR00T-N1-2B outperforms both baselines across all three simulation benchmark suites, with particularly large gains on the GR-1 humanoid tasks (+17.3% over Diffusion Policy) and an overall average improvement of +11.6% over Diffusion Policy.

### Table 3: Real-World Results on GR-1 Humanoid

| Model | Pick-and-Place | Articulated | Industrial | Coordination | Average |
|-------|:-:|:-:|:-:|:-:|:-:|
| Diffusion Policy (10% Data) | 3.0% | 14.3% | 6.7% | 27.5% | 10.2% |
| Diffusion Policy (Full Data) | 36.0% | 38.6% | 61.0% | 62.5% | 46.4% |
| GR00T-N1-2B (10% Data) | 35.0% | 62.0% | 31.0% | 50.0% | 42.6% |
| GR00T-N1-2B (Full Data) | 82.0% | 70.9% | 70.0% | 82.5% | 76.8% |

GR00T-N1-2B achieves 76.8% average success rate with full data, a +30.4% improvement over Diffusion Policy. With only 10% of available data, GR00T-N1-2B (42.6%) nearly matches the full-data Diffusion Policy (46.4%), demonstrating strong data efficiency.

### Table 4: Simulation Performance Across Dataset Sizes ([[RoboCasa]] Kitchen, selected tasks)

| Task | Demos | Diffusion Policy | GR00T-N1-2B |
|------|:-----:|:-:|:-:|
| Close Drawer | 30 | 57.5% | 76.9% |
| Close Drawer | 100 | 88.2% | 96.1% |
| Turn Off Sink Faucet | 100 | 63.7% | 67.7% |

GR00T-N1-2B consistently outperforms Diffusion Policy across varying dataset sizes, with larger relative gains in the low-data regime.

### Neural Trajectories Ablation (Figure 9)

| Setting | 30 Demos | 100 Demos | 300 Demos |
|---------|:--------:|:---------:|:---------:|
| [[RoboCasa]] improvement with neural trajectories | +4.2% | +8.8% | +6.8% |
| Real-world GR-1 improvement | -- | +5.8% avg | -- |

Co-training with neural trajectories provides consistent improvements across all data regimes, with the largest benefit at 100 demonstrations.

### Pre-training Zero-Shot Evaluation (Real Robot)

| Task | Trials | [[Success Rate]] |
|------|:------:|:------------:|
| Coordinated bimanual task | 15 | 76.6% |
| Novel object placement | 15 | 73.3% |

The pre-trained model demonstrates strong zero-shot transfer capabilities on real-robot bimanual tasks.

## Metrics Used

- [[Success Rate]] -- primary evaluation metric across all simulation and real-world experiments, measured as percentage of successful task completions
- [[Data Efficiency]] -- evaluated by comparing performance at 10% vs 100% of available training data
- [[Inference Time]] -- measured for real-time action generation on the humanoid robot
- [[Task Progress Score]] -- partial scoring system for multi-phase execution in real-world evaluation

## Datasets Used

- [[Open X-Embodiment]] -- cross-embodiment robot demonstration dataset used in the data pyramid's peak layer
- [[Ego4D]] -- large-scale egocentric video dataset used in the base layer for latent action pre-training
- [[Ego-Exo4D]] -- egocentric and exocentric video dataset used for human video pre-training
- [[Assembly-101]] -- procedural activity dataset of assembly tasks used in the video pre-training layer
- [[EPIC-KITCHENS]] -- egocentric kitchen activity dataset used for latent action learning
- [[HOI4D]] -- hand-object interaction dataset used in the base layer of the data pyramid
- [[HoloAssist]] -- mixed-reality instructional dataset used for human video pre-training
- [[RH20T-Human]] -- human demonstration dataset used for latent action pre-training
- [[RoboCasa]] -- simulation benchmark used for evaluation with kitchen manipulation tasks
- [[DexMimicGen]] -- synthetic simulation demonstration pipeline generating 540,000 trajectories for training and evaluation

## Related Papers

- [[Pi0]] -- Physical Intelligence's VLA flow model, a contemporary approach to generalist robot control
- [[Gemini Robotics]] -- Google DeepMind's VLA model built on Gemini 2.0 for robot manipulation
- [[Pi0.5]] -- Physical Intelligence's model with open-world generalization via co-training
- [[Pi0.6]] -- Physical Intelligence's VLA with reinforcement learning from experience
