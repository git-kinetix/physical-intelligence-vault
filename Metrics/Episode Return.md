---
tags: [metric]
aliases: [Cumulative Reward, Episodic Return, Undiscounted Return]
category: "reinforcement-learning"
higher_is_better: true
---

# Episode Return

## Definition
Episode Return is the cumulative sum of rewards obtained by an agent over the course of a single episode in a reinforcement learning environment. It is the most fundamental performance metric in RL, directly reflecting how well the agent optimizes the reward signal.

## Formula
$$G = \sum_{t=0}^{T} r_t$$

where $r_t$ is the reward at time step $t$ and $T$ is the terminal time step of the episode. The discounted variant uses $G = \sum_{t=0}^{T} \gamma^t r_t$ where $\gamma$ is the discount factor.

## Interpretation
- A high Episode Return means the agent accumulates large rewards, indicating strong task performance or optimal behavior.
- A low or negative return indicates suboptimal or failing policies.
- Typical ranges depend entirely on the environment's reward structure (e.g., Atari scores range from 0 to millions; continuous control tasks may range from 0 to ~10,000).
- Higher is better.

## Common Usage
Episode Return is the standard evaluation metric across virtually all RL benchmarks, including Atari, MuJoCo continuous control, DM Control Suite, and robotic simulation. It is typically averaged over multiple evaluation episodes and reported with confidence intervals.

## Papers Using This Metric
- [[DreamerV1]] — evaluating world model-based policy learning on continuous control tasks
- [[DreamerV2]] — reporting performance on Atari and continuous control benchmarks
- [[DreamerV3]] — comparing returns across diverse RL domains with a single algorithm
- [[TD-JEPA]] — measuring RL performance with temporal difference-based world models
