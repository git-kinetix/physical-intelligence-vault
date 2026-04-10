---
tags: [paper, world-model, physics-simulation]
title: "DeepLoco: Dynamic Locomotion Skills Using Hierarchical Deep Reinforcement Learning"
authors: [Xue Bin Peng, Glen Berseth, KangKang Yin, Michiel van de Panne]
year: 2017
arxiv: ""
repo: "https://github.com/xbpeng/DeepLoco"
group: "World Models"
importance: 
aliases: [DeepLoco, Deep Loco, Dynamic Locomotion Skills]
---

![[PDFs/DeepLoco.pdf]]

# DeepLoco: Dynamic Locomotion Skills Using Hierarchical Deep Reinforcement Learning

## Summary
DeepLoco introduces a two-level hierarchical deep reinforcement learning framework for learning physics-based locomotion skills for a simulated 3D biped character. The key insight is that locomotion control can be decomposed into a high-level controller (HLC) that plans footstep targets at a coarse timescale (2 Hz) and a low-level controller (LLC) that executes robust walking gaits at a fine timescale (30 Hz). This hierarchical decomposition allows the high-level controller to reason about terrain and task-level objectives while the low-level controller handles the complexities of balance and joint coordination, enabling the system to learn environment-aware locomotion with limited prior knowledge.

The low-level controller takes the current joint posture and HLC-specified stepping targets as input and outputs target joint angles for PD controllers, trained with a reward function that combines reference motion pose matching (~50%), root position tracking (~10%), center-of-mass matching (~10%), reference speed matching (~5%), and HLC footstep/heading goals (~30%). The high-level controller processes high-dimensional inputs including an 11x11 meter terrain heightmap (extending 10 meters ahead, with heights relative to the torso) and outputs the next two footstep targets and body heading direction. Both controllers are trained using the CACLA (Continuous Actor-Critic Learning Automaton) algorithm with neural networks consisting of dense layers (512 and 256 hidden units).

Published at SIGGRAPH 2017 (ACM Transactions on Graphics, Vol. 36, No. 4) by researchers at the University of British Columbia and the National University of Singapore, DeepLoco was among the first demonstrations that deep RL could learn terrain-aware, goal-directed locomotion for physics-based characters. The work established hierarchical control as a foundational paradigm for character animation, directly influencing the design of subsequent systems including [[DeepMimic]], [[MCP]], and [[ASE]].

## Key Contributions
- Introduces a two-level hierarchical DRL framework that decomposes locomotion into high-level footstep planning (2 Hz) and low-level gait execution (30 Hz), enabling environment-aware locomotion with minimal prior knowledge
- Demonstrates that a high-level controller can reason directly over terrain heightmaps (11x11 m) to plan footstep targets, enabling navigation over complex terrains including gaps, stepping stones, and obstacles
- Shows that low-level controllers can be trained for multiple locomotion styles (normal walk, gangsta lean, silly walk) with robustness to force-based disturbances and terrain variations
- Enables style interpolation between different learned gaits by blending low-level controller parameters
- Demonstrates high-level goal-directed tasks including trail following through varied terrain, soccer ball dribbling toward a target, and navigation through static and dynamic obstacles

## Architecture / Method
DeepLoco uses a hierarchical control architecture with two levels, both trained via deep reinforcement learning.

**Simulation Environment:**
- Physics engine: Bullet Physics at 3 kHz simulation frequency
- Low-level control frequency: 30 Hz (PD controllers at each joint with fixed proportional gains; derivative gains set to 10% of proportional gains)
- High-level control frequency: 2 Hz (planning at the timescale of individual steps)
- Character: 3D biped with articulated legs

**Low-Level Controller (LLC):**
- RL algorithm: CACLA (Continuous Actor-Critic Learning Automaton) with Actor and Critic networks
- Network architecture: Dense layers with 512 and 256 hidden units
- State input: Current joint postures plus stepping targets from HLC
- Action output: 8 target joint angles for PD controllers
- Phase input: Scalar sweeping 0 to 1, divided into four gait phases, with 4 neurons switched on/off cyclically over the input phase
- Reward function components:
  - Reference animation pose matching (~50%)
  - Reference root position tracking (~10%)
  - Center-of-mass matching (~10%)
  - Reference animation speed matching (~5%)
  - HLC footstep goal achievement (~20%)
  - HLC heading goal achievement (~10%)
- Exploration noise added during training but not at inference time

**High-Level Controller (HLC):**
- Network architecture: CNN-based network processing terrain heightmap input
- Terrain input: 11x11 meter heightmap centered on the character, extending 10 meters ahead, with ground heights expressed relative to the torso
- State input: Task-dependent features including character and ball/object coordinates plus terrain map
- Action output: Next two footstep target positions and body heading direction
- Reward: Task-specific formulations (e.g., path following uses exp(-(velocity - 1)^2) targeting 1 m/s movement speed)

**Training Pipeline:**
The LLC is trained first to produce robust walking gaits that satisfy stepping-target and style objectives. The HLC is then trained on top of the frozen (or co-trained) LLC, learning to plan footstep targets that achieve task-level goals. Both levels use CACLA with separate Actor and Critic networks.

## Results

DeepLoco demonstrates qualitative results across multiple locomotion tasks, evaluated on a simulated 3D biped character in Bullet physics.

### Low-Level Controller Capabilities
| Capability | Description |
|-----------|-------------|
| Normal Walking | Robust forward locomotion tracking reference animation |
| Style Variation | Multiple learned styles (normal, gangsta lean, silly walk) |
| Style Interpolation | Smooth blending between different gait styles |
| Disturbance Rejection | Robustness to external force-based perturbations |
| Terrain Adaptation | Adaptation to uneven ground and terrain variations |

The low-level controllers demonstrate robustness to force-based disturbances, terrain variations, and style interpolation. Multiple locomotion styles can be learned by training separate LLCs with different reference motions, and smooth style transitions are achieved by interpolating between controller parameters.

### High-Level Controller Tasks
| Task | Description |
|------|-------------|
| Trail Following | Following paths through varied terrain (gaps, stepping stones, slopes) |
| Soccer Dribbling | Dribbling a soccer ball toward a target location using indirect contact dynamics |
| Static Obstacle Navigation | Navigating around stationary obstacles in the environment |
| Dynamic Obstacle Navigation | Avoiding moving obstacles while maintaining forward progress |

The high-level controller successfully learns to interpret terrain heightmaps and plan appropriate footstep sequences for navigating challenging terrains. The soccer dribbling task demonstrates the ability to combine locomotion with object interaction through indirect control. The paper primarily reports qualitative demonstrations via video rather than tabulated quantitative metrics.

## Metrics Used
- [[Episode Return]] — cumulative reward used to evaluate both LLC and HLC training performance
- [[Motion Naturalness]] — qualitative assessment of gait quality via video demonstrations; the reference motion matching reward serves as a quantitative proxy
- Task Completion — qualitative evaluation of whether the character successfully follows trails, dribbles the ball to the target, or navigates obstacles

## Datasets Used
- Reference motion animations — walking gaits and style variations used as imitation targets for the low-level controller training; includes normal walking plus stylized variants

## Related Papers
- [[DeepMimic]] — direct successor by the same lead author that extends single-reference motion imitation to 24+ diverse skills (backflips, martial arts, acrobatics) on a more complex humanoid character; DeepLoco's hierarchical stepping-target framework influenced [[DeepMimic]]'s approach to combining imitation and task objectives
- [[MCP]] — uses motion imitation pre-training (building on DeepLoco/[[DeepMimic]]) followed by multiplicative composition of primitives for downstream tasks including soccer dribbling, which DeepLoco first demonstrated
- [[ASE]] — scales the hierarchical pre-training paradigm pioneered by DeepLoco to large motion capture datasets with adversarial skill embeddings, similarly using a low-level controller / high-level controller architecture
- [[MVAE]] — alternative approach to locomotion control using VAE-learned latent action spaces; shares co-author Michiel van de Panne with DeepLoco
- [[Hierarchical Puppeteer]] — extends the two-level hierarchical control paradigm to visual observations with a world model, conceptually building on DeepLoco's HLC/LLC decomposition
- [[Eureka]] — automated reward design for locomotion; DeepLoco's hand-crafted multi-component reward function is the type of engineering that [[Eureka]] aims to automate
