---
tags: [paper, robotics]
title: "Eureka: Human-Level Reward Design via Coding Large Language Models"
authors: [Yecheng Jason Ma, William Liang, Guanzhi Wang, De-An Huang, Osbert Bastani, Dinesh Jayaraman, Yuke Zhu, Linxi Fan, Anima Anandkumar]
year: 2023
arxiv: "https://arxiv.org/abs/2310.12931"
repo: "https://github.com/eureka-research/Eureka"
group: "Robotics"
importance: 
aliases: [Eureka]
---

![[PDFs/Eureka.pdf]]


# Eureka: Human-Level Reward Design via Coding Large Language Models

## Summary

Eureka is a reward design algorithm that leverages large language models (specifically GPT-4) to automatically generate reward functions for reinforcement learning, achieving human-level or better performance across a diverse suite of manipulation and locomotion tasks. Developed by researchers at NVIDIA, University of Pennsylvania, and Caltech, Eureka addresses one of the most persistent bottlenecks in RL: designing effective reward functions that guide agents toward desired behaviors.

The core approach is elegantly simple: given the environment source code and a task description, GPT-4 generates candidate reward function implementations in Python. These are evaluated in parallel by training RL policies in NVIDIA Isaac Gym, and the results are fed back to GPT-4 for iterative refinement via an evolutionary optimization process. Eureka requires no task-specific prompting, reward templates, or pre-defined reward components -- it operates zero-shot from environment code alone.

Across 29 tasks spanning 10 distinct robot morphologies (including humanoids, quadrupeds, dexterous hands, and articulated objects), Eureka outperforms human-designed reward functions on 83% of tasks with an average normalized improvement of 52%. Most notably, Eureka enables a simulated Shadow Hand to perform pen spinning for the first time, a highly dexterous manipulation skill requiring rapid, coordinated finger movements. The paper was accepted at ICLR 2024.

## Key Contributions

- Introduces Eureka, a zero-shot LLM-powered reward design algorithm that outperforms human experts on 83% of tested tasks
- Achieves an average 52% normalized improvement over expert human-designed rewards across 29 tasks and 10 robot morphologies
- Demonstrates the first simulated Shadow Hand pen spinning through curriculum learning with Eureka-generated rewards
- Proposes evolutionary optimization over reward code: GPT-4 iteratively generates, evaluates, and refines reward functions
- Requires no task-specific prompting, reward templates, or manual reward engineering
- Enables gradient-free in-context RLHF: human feedback can be incorporated to improve reward quality without model updating
- Shows that LLM-generated rewards are often novel and uncorrelated with human designs, especially on harder tasks

## Architecture / Method

**Eureka operates through the following pipeline:**

**1. Environment as Context:**
- The full environment source code (from NVIDIA Isaac Gym) is provided to GPT-4
- The task description specifies the desired behavior in natural language
- No reward templates, few-shot examples, or pre-defined reward components are given

**2. Reward Code Generation:**
- GPT-4 generates complete Python reward function implementations
- Multiple candidate reward functions are generated in parallel (typically 16 candidates per iteration)
- Each reward function maps environment state variables to scalar reward signals

**3. Parallel Policy Training:**
- Each candidate reward function is used to train an RL policy in NVIDIA Isaac Gym
- Training runs in parallel across GPU-accelerated environments
- Performance metrics (task success, training curves) are collected for each candidate

**4. Evolutionary Optimization:**
- Training results are fed back to GPT-4 as context for the next iteration
- GPT-4 uses in-context learning to understand which reward designs worked and why
- New candidate rewards are generated, building on successful patterns from prior iterations
- This process repeats for multiple generations (typically 3-5 iterations)

**5. Optional Human Feedback (RLHF):**
- Human operators can provide natural language feedback on observed agent behaviors
- GPT-4 incorporates this feedback to adjust reward functions
- This enables a gradient-free form of RLHF without model fine-tuning
- When initialized with human rewards, "Eureka (Human Init.)" uniformly outperforms both pure Eureka and pure human rewards

**Curriculum Learning for Pen Spinning:**
- Pen spinning requires a multi-stage curriculum
- Eureka generates rewards for progressively more difficult sub-goals
- The curriculum enables the Shadow Hand to learn rapid pen rotation that was previously impossible

## Results

### Table 1: Overall Performance Summary

| Metric | Value |
|--------|-------|
| Tasks outperforming human experts | 83% (24/29) |
| Average normalized improvement over human | 52% |
| Robot morphologies tested | 10 |
| Total tasks evaluated | 29 |

### Table 2: Task Distribution

| Source | Tasks | Robot Types |
|--------|-------|-------------|
| Isaac Gym Environments | 9 | Humanoid, Quadruped, Dexterous Hand, etc. |
| Dexterous Manipulation Benchmark | 20 | Shadow Hand bimanual manipulation |
| **Total** | **29** | **10 morphologies** |

### Table 3: Comparison with Baselines

| Method | Avg. [[Normalized Task Score]] | Tasks > Human |
|--------|----------------------|---------------|
| **Eureka** | 1.52 (52% improvement) | 83% |
| **Eureka (Human Init.)** | Best across all tasks | 100% |
| Human Expert Rewards | 1.00 (baseline) | -- |
| L2R (Learning to Reward) | < Human on most tasks | < 50% |

Eureka (Human Init.) -- initialized with human-designed rewards and then refined by GPT-4 -- uniformly outperforms both pure Eureka and pure human rewards across all tasks.

### Table 4: Reward Correlation Analysis

| Task Difficulty | Correlation with Human Rewards |
|----------------|-------------------------------|
| Easy tasks | Moderate positive correlation |
| Hard tasks | Low or negative correlation |

On harder tasks, Eureka discovers novel reward structures that are less correlated (or even negatively correlated) with human-designed rewards, yet still outperform them -- suggesting that LLMs can find unintuitive but effective reward signals.

### Table 5: Pen Spinning Achievement

| Capability | Status |
|-----------|--------|
| Shadow Hand pen spinning (simulated) | First-ever demonstration |
| Rotation speed | Rapid, sustained circular motion |
| Training method | Eureka rewards + curriculum learning |

## Metrics Used

- [[Normalized Improvement]] -- performance relative to human expert reward baseline (1.0 = human-level)
- [[Task Success Rate]] -- percentage of tasks where Eureka exceeds human expert performance
- [[Reward Correlation]] -- correlation between Eureka-generated and human-designed reward functions
- [[Training Return]] -- cumulative RL training return achieved with each reward function

## Datasets Used

- [[NVIDIA Isaac Gym]] -- GPU-accelerated physics simulator providing 29 RL environments across 10 robot morphologies
- [[Dexterous Manipulation Benchmark]] -- 20 bimanual Shadow Hand manipulation tasks
- [[Isaac Gym Locomotion/Manipulation Tasks]] -- 9 diverse locomotion and manipulation environments

## Related Papers

- [[GR00T]] -- NVIDIA's foundation model for humanoid robots; Eureka's reward design could complement [[GR00T]]'s policy learning
- [[Pi0]] -- Physical Intelligence's VLA model; represents a complementary approach (imitation learning) to the RL-based approach that Eureka's rewards support
- [[DreamerV3]] -- world model-based RL agent; Eureka's reward functions could be used to train [[DreamerV3]] policies
- [[NVIDIA Cosmos]] -- NVIDIA's world foundation model; part of the same NVIDIA research ecosystem advancing physical AI
