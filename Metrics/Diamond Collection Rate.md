---
tags: [metric]
aliases: [Diamonds per Episode, Diamond Rate]
category: "reinforcement-learning"
higher_is_better: true
---

# Diamond Collection Rate

## Definition
Diamond Collection Rate measures the average number of diamonds collected per episode (or per unit time) by an RL agent in Minecraft. Obtaining diamonds requires a long sequence of prerequisite steps (gathering wood, crafting tools, mining stone, mining iron, smelting, crafting an iron pickaxe, finding and mining diamond ore), making it a demanding test of long-horizon planning and exploration.

## Formula
$$\text{Diamond Collection Rate} = \frac{\text{Total Diamonds Collected}}{\text{Number of Episodes}}$$

or equivalently measured as diamonds per minute of gameplay.

## Interpretation
- A high rate indicates the agent can reliably execute the long chain of prerequisite actions needed to reach and mine diamonds.
- A rate of 0 means the agent never successfully completes the full diamond collection sequence.
- Even small positive values (e.g., 0.1-1.0 diamonds per episode) represent significant capability, as the task requires coordinating dozens of sequential subtasks over thousands of steps.
- Higher is better.

## Common Usage
This metric is the flagship evaluation for RL agents in Minecraft-based benchmarks (e.g., MineRL, MineDojo). Collecting diamonds is considered one of the hardest standard challenges in open-world RL because it requires long-horizon planning, hierarchical reasoning, and robust execution across many subtasks.

## Papers Using This Metric
- [[DreamerV3]] — demonstrating the first general-purpose RL agent to collect diamonds in Minecraft from scratch
