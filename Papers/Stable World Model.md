---
tags: [paper, world-model]
title: "stable-worldmodel-v1: Reproducible World Modeling Research and Evaluation"
authors: [Lucas Maes, Quentin Le Lidec, Dan Haramati, Nassim Massaudi, Damien Scieur, Yann LeCun, Randall Balestriero]
year: 2026
arxiv: "https://arxiv.org/abs/2602.08968"
repo: "https://github.com/galilai-group/stable-worldmodel"
group: "World Models"
importance: 
aliases: [Stable World Model, SWM, stable-worldmodel, stable-worldmodel-v1]
---

![[PDFs/Stable World Model.pdf]]

# stable-worldmodel-v1: Reproducible World Modeling Research and Evaluation

## Summary

stable-worldmodel (SWM) is a modular, tested, and documented open-source research ecosystem for world model research. It addresses a critical fragmentation problem in the world models community: each new paper re-implements the same baselines, evaluation protocols, and data processing logic from scratch, leading to inconsistent comparisons and wasted effort. SWM provides a unified pipeline spanning efficient data collection, standardized environments, planning algorithms, and baseline implementations, all under a single PyTorch-based library installable via `pip install stable-worldmodel`.

A key contribution is the introduction of controllable Factors of Variation (FoV) across 16 standardized environments. Each environment exposes 6 to 17 controllable properties spanning visual (color, background), geometric (shape, size, angle, position), and physical (friction, density, velocity) dimensions. This enables systematic robustness and continual learning studies that were previously ad hoc. The paper demonstrates SWM's utility through a zero-shot robustness analysis of DINO-WM on the [[Push-T]] task, revealing that DINO-WM's 94% in-distribution success rate collapses to as low as 4% under distributional shifts -- a finding that underscores the need for standardized robustness evaluation.

The library ships with 4 baseline model implementations (DINO-WM, [[PLDM]], [[Le-World-Model|LeWM]], GCBC), multiple planning solvers (CEM, iCEM, MPPI, gradient-based), and 16 environments spanning manipulation ([[Push-T]]), navigation (Two-Room), [[DeepMind Control Suite]] (12 tasks), and [[OGBench]] (2 tasks). With 73% test coverage, comprehensive documentation, and active maintenance (99 PRs in 6 months), SWM sets a new standard for reproducibility in world model research.

## Key Contributions

- Introduces a modular, tested (73% coverage), and documented world-model research ecosystem that unifies data collection, training, and evaluation
- Provides 16 standardized environments with 6-17 controllable Factors of Variation each, enabling systematic robustness and continual learning studies
- Implements a unified "World" interface that decouples control logic from environment execution, with data stored in a single internal dictionary updated in place
- Ships with 4 baseline implementations (DINO-WM, [[PLDM]], [[Le-World-Model|LeWM]], GCBC) and multiple planning solvers (CEM, iCEM, MPPI, SGD/Adam, PGD, Augmented Lagrangian)
- Demonstrates through zero-shot robustness analysis that DINO-WM's performance collapses under distributional shifts (94% to as low as 4% success rate)
- Achieves significantly smaller codebase (3,562 LoC) than comparable libraries ([[PLDM]]: 6,796; DINO-WM: 4,349) while supporting more environments and baselines
- Supports dual dataset formats (HDF5 for performance, MP4 for visualization) and provides a CLI tool (`swm`) for dataset inspection and environment browsing

## Architecture / Method

**Core Abstraction -- World Interface:**
The central abstraction is the "World" class, which wraps Gymnasium environments and provides synchronous multi-environment management. Rather than returning observations and rewards directly, all data produced by the environments is stored in a single internal dictionary (`world.infos`) that is updated in place. Actions derive from attached policy objects implementing a `get_action(infos) -> actions` interface, cleanly decoupling control logic from environment execution. This design enables seamless switching between data collection, online evaluation, and model-based planning.

**Factors of Variation (FoV):**
Each environment exposes a set of controllable properties implemented as Gymnasium dictionary Spaces with hierarchical naming (e.g., `agent.color`, `block.size`, `floor.friction`). These FoVs span three categories:
- **Visual**: color, background color, light intensity
- **Geometric**: shape, size, angle, position
- **Physical**: friction, density, velocity, joint locks

Sampling can be constrained to specific ranges or fully randomized at reset, evaluation, or dataset-recording time, enabling fine-grained control over distribution shifts.

**Evaluation Protocols:**
The library supports two evaluation modes:
- **Online evaluation**: samples initial states and goals per episode at runtime
- **Offline evaluation**: selects (initial state, goal) pairs from expert trajectories with step-count constraints to ensure task feasibility within a given budget

Goal-conditioned tasks can specify goals as target states, target images, or reward functions.

**Planning Solvers:**
SWM implements a suite of planning algorithms operating in learned latent spaces:
- **Sampling-based**: Cross-Entropy Method (CEM), improved CEM (iCEM), Model Predictive Path Integral (MPPI)
- **Gradient-based**: SGD, Adam, Projected Gradient Descent (PGD)
- **Constrained optimization**: Augmented Lagrangian method

**Supported Baselines:**
- **DINO-WM** (JEPA) -- world model built on pretrained DINOv2 visual features
- **[[PLDM]]** (JEPA) -- latent dynamics model for offline reward-free RL
- **[[Le-World-Model|LeWM]]** (JEPA) -- end-to-end JEPA from pixels with SIGReg regularization
- **GCBC** (Behaviour Cloning) -- goal-conditioned behavioral cloning baseline

## Results

### Table 1: Latent World-Model Codebases Comparison

| Metric | SWM (ours) | [[PLDM]] | DINO-WM |
|---|---|---|---|
| Backend | PyTorch | PyTorch | PyTorch |
| Documentation | Yes | No | No |
| # Baselines | 4 | 1 | 1 |
| # Environments | 16 | 2 | 4 |
| # FoV (per env) | 6-17 | 0 | 0 |
| Type Checking | Yes | Yes | No |
| Test Coverage | 73% | 0% | 0% |
| Last Commit | <<1 week | >>3 months | >>10 months |
| PRs (6 months) | 99 | 1 | 0 |
| # Lines of Code | 3,562 | 6,796 | 4,349 |

SWM achieves substantially more functionality (4x baselines, 8x environments vs [[PLDM]]) in roughly half the lines of code, with dramatically better engineering practices (73% test coverage vs 0%, active maintenance vs stale repos). The FoV system is entirely unique to SWM, with neither [[PLDM]] nor DINO-WM offering any controllable factors of variation.

### Table 2: DINO-WM Zero-Shot Robustness on [[Push-T]] ([[Success Rate]] %)

| Factor of Variation | Property | [[Success Rate]] (%) |
|---|---|---|
| Color | Anchor | 20.0 |
| Color | Agent | 18.0 |
| Color | Block | 18.0 |
| Color | Background | 10.0 |
| Size | Anchor | 14.0 |
| Size | Agent | 4.0 |
| Size | Block | 16.0 |
| Angle | Anchor | 12.0 |
| Angle | Agent | 12.0 |
| Position | Anchor | 4.0 |
| Shape | Agent | 18.0 |
| Shape | Block | 8.0 |
| Velocity | Agent | 14.0 |
| None (baseline) | -- | 94.0 |

This table reveals severe fragility in DINO-WM under distributional shift. The in-distribution baseline achieves 94% success rate, but every single factor of variation causes dramatic performance collapse. The worst cases are position changes to the anchor (4%) and size changes to the agent (4%), representing a ~90 percentage point drop. Even seemingly minor visual changes like color shifts cause 74-84 percentage point drops. This demonstrates that DINO-WM's strong in-distribution performance does not generalize, motivating the need for systematic robustness evaluation via SWM's FoV framework.

### Table 3: SWM Environments Summary (All 16 Environments)

| Environment ID | # FoV | Category |
|---|---|---|
| swm/PushT-v1 | 16 | Manipulation |
| swm/TwoRoom-v1 | 17 | Navigation |
| swm/OGBCube-v0 | 11 | [[OGBench]] |
| swm/OGBScene-v0 | 12 | [[OGBench]] |
| swm/HumanoidDMControl-v0 | 7 | DeepMind Control |
| swm/CheetahDMControl-v0 | 7 | DeepMind Control |
| swm/HopperDMControl-v0 | 7 | DeepMind Control |
| swm/ReacherDMControl-v0 | 8 | DeepMind Control |
| swm/WalkerDMControl-v0 | 8 | DeepMind Control |
| swm/AcrobotDMControl-v0 | 8 | DeepMind Control |
| swm/PendulumDMControl-v0 | 6 | DeepMind Control |
| swm/CartpoleDMControl-v0 | 6 | DeepMind Control |
| swm/BallInCupDMControl-v0 | 9 | DeepMind Control |
| swm/FingerDMControl-v0 | 10 | DeepMind Control |
| swm/ManipulatorDMControl-v0 | 8 | DeepMind Control |
| swm/QuadrupedDMControl-v0 | 7 | DeepMind Control |

The 16 environments span four categories: manipulation ([[Push-T]]), navigation (Two-Room), [[OGBench]] (Cube, Scene), and 12 [[DeepMind Control Suite]] tasks. FoV counts range from 6 (Pendulum, Cartpole) to 17 (Two-Room), with manipulation and navigation tasks generally having more variation dimensions than locomotion tasks. Each FoV can be independently controlled at reset time for fine-grained robustness evaluation.

## Metrics Used

- [[Success Rate]] -- primary evaluation metric, defined as the percentage of evaluation episodes that end satisfying the goal condition; used for all robustness experiments
- [[Zero-Shot Generalization]] -- models trained in-distribution are evaluated on shifted environments without retraining or fine-tuning
- [[Test Coverage]] -- software engineering metric (73%) used to quantify codebase reliability
- [[Lines of Code]] -- used as a proxy for codebase complexity and maintainability

## Datasets Used

- [[Push-T]] -- 2D manipulation task where agent pushes a T-shaped block to a target pose; primary environment for DINO-WM robustness analysis (16 FoVs)
- [[Two-Room]] -- 2D navigation task with door-based room transitions; highest FoV count at 17
- [[OGBench]] -- offline goal-conditioned RL benchmark; Cube and Scene variants (11 and 12 FoVs)
- [[DeepMind Control Suite]] -- 12 continuous control tasks (Humanoid, Cheetah, Hopper, Reacher, Walker, Acrobot, Pendulum, Cartpole, Ball-in-Cup, Finger, Manipulator, Quadruped); 6-10 FoVs each
- [[HDF5]] -- primary dataset storage format optimized for performance
- [[MP4]] -- alternative dataset format for visualization

## Related Papers

- [[Le-World-Model]] -- [[Le-World-Model|LeWM]] is one of the 4 baselines included in SWM; same lead author (Lucas Maes); [[Le-World-Model|LeWM]] was developed using the SWM ecosystem
- [[DIAMOND]] -- diffusion-based world model for Atari; represents the generative (pixel-space) approach to world modeling that contrasts with SWM's focus on latent JEPA-based methods
- [[IRIS]] -- autoregressive world model using discrete tokens; another generative approach that SWM's latent baselines (DINO-WM, [[PLDM]], [[Le-World-Model|LeWM]]) aim to surpass
- [[DreamerV1]] -- foundational learned world model for model-based RL; SWM builds on the lineage of world models for planning and control
- [[DreamerV2]] -- extends [[DreamerV1]] with discrete representations; part of the world model evolution that motivated standardized benchmarking
- [[DreamerV3]] -- general algorithm mastering diverse domains; represents the state-of-the-art in end-to-end world model RL that SWM environments can benchmark against
- [[I-JEPA]] -- image-based JEPA that inspired the visual encoder design used in DINO-WM and related baselines
- [[V-JEPA]] -- video JEPA extending self-supervised prediction to temporal sequences; foundational to the JEPA world model paradigm
- [[TD-JEPA]] -- temporal difference JEPA combining JEPA with TD learning; related latent world model approach
- [[Le-JEPA]] -- introduces SIGReg regularization used by [[Le-World-Model|LeWM]]; same research group (Mila/NYU/Brown)
