---
tags: [paper, domain/embodied-ai, method/rl, method/hierarchical]
title: "Habitat 3.0: A Co-Habitat for Humans, Avatars and Robots"
authors: [Xavier Puig, Eric Undersander, Andrew Szot, Mikael Dallaire Cote, Tsung-Yen Yang, Ruslan Partsey, Ruta Desai, Alexander William Clegg, Michal Hlavac, So Yeon Min, Vladimir Vondrus, Theophile Gervet, Vincent-Pierre Berges, John M. Turner, Oleksandr Maksymets, Zsolt Kira, Mrinal Kalakrishnan, Jitendra Malik, Devendra Singh Chaplot, Unnat Jain, Dhruv Batra, Akshara Rai, Roozbeh Mottaghi]
year: 2023
arxiv: "https://arxiv.org/abs/2310.13724"
repo: "https://github.com/facebookresearch/habitat-lab"
group: "Embodied AI"
venue: "ICLR 2024"
domain: [embodied-ai]
method: [rl, hierarchical]
lineage: [meta-fair]
predecessor: []
importance: 
aliases: [Habitat 3.0, Habitat3, Habitat 3]
---

![[PDFs/Habitat 3.0.pdf]]

# Habitat 3.0: A Co-Habitat for Humans, Avatars and Robots

## Summary
Habitat 3.0 is a simulation platform from Meta FAIR for studying collaborative human-robot tasks in home environments. It addresses a critical gap in embodied AI research: the lack of high-fidelity, high-speed simulators that support realistic humanoid avatars alongside robotic agents, enabling the study of social and cooperative interactions. The platform builds on the existing Habitat simulator infrastructure and introduces three major capabilities: accurate and efficient humanoid simulation, human-in-the-loop evaluation infrastructure, and collaborative task benchmarks.

The humanoid simulation uses SMPL-X parametric body models with 109-dimensional pose parameters and 10-dimensional shape parameters, achieving 1190 FPS with a humanoid and robot in the scene (compared to 1345 FPS with two robots), making it fast enough for large-scale reinforcement learning. Walking animations are driven by motion data from the AMASS dataset, and pick/place poses are pre-computed via VPoser. The human-in-the-loop infrastructure supports mouse/keyboard and VR interfaces, allowing real humans to interact with learned robot policies for more ecologically valid evaluation.

Two collaborative task benchmarks are introduced: Social Navigation (finding and following a humanoid avatar in unfamiliar environments) and Social Rearrangement (jointly reorganizing objects in a scene with a humanoid partner). Experiments demonstrate that learned policies generalize to novel partner behaviors and exhibit emergent social behaviors such as yielding space. Crucially, evaluations with simulated humanoid partners correlate with evaluations using real human participants, validating the platform's use as a proxy for human-robot interaction research.

## Key Contributions
- Introduces fast, realistic humanoid simulation using SMPL-X parametric models with articulated skeletons for collision detection and skinned meshes for rendering, achieving over 1100 FPS with humanoid-robot scenes
- Provides human-in-the-loop evaluation infrastructure supporting mouse/keyboard and VR interaction, enabling real human evaluation of robot policies
- Defines two collaborative benchmarks: Social Navigation (find-and-follow) and Social Rearrangement (cooperative object placement), with standardized metrics
- Demonstrates that evaluations using simulated humanoid partners correlate with real human partner evaluations, validating automated evaluation as a proxy
- Shows emergent cooperative robot behaviors (e.g., yielding space to humanoid partners) learned purely through RL without explicit social reward shaping
- Proposes a zero-shot coordination (ZSC) evaluation paradigm where trained robot policies must collaborate with unseen humanoid partner policies

## Architecture / Method
**Humanoid Representation:**
- Articulated skeleton with rotational joints for fast collision detection
- Skinned surface mesh rendered via linear blend skinning (LBS)
- SMPL-X parametric model: 109-dimensional pose parameters (J) and 10-dimensional shape parameters (beta)
- 12 base humanoid models with diverse genders, body shapes, and appearances (4 male, 4 female, 4 neutral)
- Walking animations sourced from the AMASS motion capture dataset
- Pick/place interaction poses pre-computed using VPoser

**Social Navigation Task:**
- Robot (Boston Dynamics Spot) must find and follow a humanoid avatar in an unseen environment
- Observations: egocentric depth camera, humanoid GPS sensor, humanoid detector
- Policy: LSTM with ResNet-18 backbone, two recurrent layers
- Output: linear and angular velocity commands
- The humanoid follows a shortest-path policy to random waypoints

**Social Rearrangement Task:**
- Robot and humanoid must cooperatively place two objects at target locations in a home scene
- Two-layer hierarchical policy: high-level policy selects among low-level skills (navigate, pick, place)
- Visual encoder: ResNet-18 processing 256x256 depth images
- Recurrent backbone: 2-layer LSTM with 512 hidden dimensions
- Action/value prediction networks on top of LSTM output
- Robot is trained with DD-PPO (decentralized distributed PPO)

**Zero-Shot Coordination (ZSC):**
- Population-based training: train a population of diverse humanoid partner policies
- At evaluation, the robot must coordinate with a held-out partner policy never seen during training
- This tests the robot's ability to adapt to novel human-like behaviors

**Simulation Performance:**
- 1190 FPS with one humanoid and one robot (vs. 1345 FPS with two robots)
- Caching strategy for humanoid motion data to optimize throughput
- Scenes from the Habitat Synthetic Scenes Dataset (HSSD)

## Results

### Table 1: Social Navigation Baseline Results
| Method | S (Find Success) | SPS (Success weighted by Path Steps) | F (Following Rate) | CR (Collision Rate) |
|--------|:-:|:-:|:-:|:-:|
| Heuristic Expert | 1.00 | 0.97 | 0.51 | 0.52 |
| End-to-end RL | 0.97 +/- 0.00 | 0.65 +/- 0.00 | 0.44 +/- 0.01 | 0.51 +/- 0.03 |
| - humanoid GPS | 0.76 +/- 0.02 | 0.34 +/- 0.01 | 0.29 +/- 0.01 | 0.48 +/- 0.03 |
| - humanoid detector | 0.98 +/- 0.00 | 0.68 +/- 0.00 | 0.37 +/- 0.01 | 0.64 +/- 0.05 |
| - arm depth | 0.94 +/- 0.01 | 0.54 +/- 0.01 | 0.19 +/- 0.01 | 0.71 +/- 0.08 |
| - arm depth + arm RGB | 0.96 +/- 0.00 | 0.61 +/- 0.01 | 0.38 +/- 0.02 | 0.55 +/- 0.04 |

The end-to-end RL policy achieves 97% finding success but with lower path efficiency (SPS 0.65) than the heuristic expert (0.97). Removing humanoid GPS has the largest impact, dropping finding success to 76%. Removing the arm depth camera severely degrades following rate (0.19), suggesting the arm camera is critical for close-range tracking.

### Table 2: Social Rearrangement Baseline Results
| Method | Train SR | Train RE | ZSC SR | ZSC RE |
|--------|:-:|:-:|:-:|:-:|
| Learn-Single | 98.50 +/- 0.48 | 159.2 +/- 1.0 | 50.94 +/- 39.55 | 106.02 +/- 34.32 |
| Plan-Pop1 | 91.2 +/- 2.63 | 152.4 +/- 5.4 | 50.44 +/- 39.02 | 109.75 +/- 34.63 |
| Plan-Pop2 | 66.89 +/- 1.47 | 110.06 +/- 6.83 | 70.23 +/- 7.02 | 102.13 +/- 11.10 |
| Plan-Pop3 | 77.79 +/- 2.86 | 118.95 +/- 6.04 | 71.79 +/- 7.38 | 101.99 +/- 15.18 |
| Plan-Pop4 | 72.42 +/- 1.32 | 105.49 +/- 1.7 | 71.32 +/- 6.47 | 103.53 +/- 9.8 |
| Learn-Pop | 92.20 +/- 2.21 | 135.32 +/- 3.43 | 48.52 +/- 35.51 | 99.80 +/- 31.02 |
| - oracle + learned skills | 41.09 +/- 21.5 | 79.62 +/- 1.76 | 21.44 +/- 18.16 | 76.45 +/- 9.23 |
| - depth + RGB | 76.70 +/- 3.15 | 110.04 +/- 3.05 | 70.89 +/- 8.18 | 100.16 +/- 14.79 |
| - Humanoid-GPS | 76.45 +/- 1.85 | 108.96 +/- 2.66 | 68.70 +/- 6.75 | 98.58 +/- 10.32 |

Learn-Single achieves near-perfect training success (98.5%) but collapses under zero-shot coordination (ZSC SR 50.94% with high variance), revealing severe overfitting to a single partner. Population-based planning methods (Plan-Pop3, Plan-Pop4) achieve the best ZSC generalization (71.79% and 71.32%) with much lower variance, demonstrating that training against diverse partners is essential for robust coordination.

### Table 3: Human-in-the-Loop Coordination Results
| Method | CR (Collision Rate) | TS (Task Steps) | RC (Robot Contribution) | RE (Relative Efficiency) |
|--------|:-:|:-:|:-:|:-:|
| Solo (human only) | 0.0 | 1253.17 [1020.90-1533.26] | -- | 100.0 |
| Learn-Single | 0.12 [0.19-0.08] | 936.60 [762.50-1146.62] | 0.36 [0.33-0.39] | 133.80 |
| Plan-Pop3 | 0.13 [0.20-0.08] | 1015.05 [826.42-1242.60] | 0.44 [0.41-0.46] | 123.46 |

With real human participants (n=30), both robot policies reduce task completion time compared to solo human performance. Learn-Single achieves the highest relative efficiency (133.80%) meaning the human-robot team finishes 33.8% faster than the human alone. Plan-Pop3 achieves higher robot contribution (0.44 vs 0.36), indicating it takes on a larger share of the work. Both methods have similar collision rates (~0.12-0.13).

## Metrics Used
- [[Finding Success (S)]] -- binary success of the robot locating the humanoid within 1-2m distance
- [[Success weighted by Path Steps (SPS)]] -- efficiency of finding the humanoid relative to an oracle with ground-truth knowledge
- [[Following Rate (F)]] -- ratio of timesteps where the robot maintains 1-2m distance while facing the humanoid
- [[Collision Rate (CR)]] -- proportion of episodes with robot-humanoid collisions
- [[Success Rate (SR)]] -- both objects placed at target locations in Social Rearrangement
- [[Relative Efficiency (RE)]] -- speed-up of the human-robot team relative to the humanoid completing the task alone (200% means half the steps)
- [[Robot Contribution (RC)]] -- proportion of objects rearranged by the robot per episode
- [[Task Steps (TS)]] -- total number of simulation steps required for task completion

## Datasets Used
- [[Habitat Synthetic Scenes Dataset (HSSD)]] -- 59 photorealistic home scenes (37 train, 12 validation, 10 test) used as the 3D environment for all experiments
- [[AMASS]] -- large-scale motion capture dataset providing walking animations for the humanoid avatars
- [[SMPL-X]] -- parametric human body model used for humanoid representation with 109 pose and 10 shape parameters

## Related Papers
- [[GR00T]] -- NVIDIA's humanoid robot foundation model; Habitat 3.0's humanoid simulation and human-robot collaboration benchmarks are directly relevant to training and evaluating humanoid policies
- [[LeVERB]] -- humanoid language-conditioned VLA; addresses human-like motion generation which complements Habitat 3.0's focus on human-robot interaction environments
- [[Eureka]] -- automated reward design for robot locomotion; could be applied to design reward functions for Habitat 3.0's collaborative tasks
- [[UniSim]] -- learns simulation from video data as an alternative to hand-crafted simulators like Habitat; complementary approaches to generating training environments for embodied AI
- [[Genie 2]] -- generative interactive environment model; represents the neural alternative to Habitat 3.0's explicit simulation approach for embodied AI training
- [[Gemini Robotics]] -- Google's embodied reasoning VLA; Habitat 3.0 could serve as an evaluation platform for testing such models in social settings
