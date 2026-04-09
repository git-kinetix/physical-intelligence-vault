---
tags: [metric]
aliases: [Crafter Achievement Score]
category: "reinforcement-learning"
higher_is_better: true
---

# Crafter Score

## Definition
Crafter Score is the geometric mean of success rates across 22 achievement milestones in the Crafter environment, an open-world survival game designed to test diverse RL capabilities including exploration, resource gathering, crafting, and combat. The geometric mean ensures that agents must make progress on all achievements rather than excelling at a few.

## Formula
$$\text{Crafter Score} = \left(\prod_{i=1}^{22} s_i\right)^{1/22} \times 100\%$$

where $s_i$ is the success rate (fraction of episodes achieving milestone $i$) for each of the 22 achievements.

## Interpretation
- A high score indicates the agent can reliably complete a broad range of achievements spanning exploration, survival, crafting, and combat.
- A low score indicates the agent fails to make progress on one or more achievement categories, since the geometric mean penalizes zero or near-zero success rates heavily.
- Typical scores range from near 0% (random agents) to ~20-30% for strong RL agents; expert human scores are around 50%.
- Higher is better.

## Common Usage
The Crafter benchmark was designed as a compact but comprehensive test of RL agent generality, requiring long-horizon planning, exploration, and diverse skill acquisition in a single environment. The Crafter Score serves as the primary aggregate metric for this benchmark.

## Papers Using This Metric
- [[DreamerV3]] — demonstrating broad capability of a general-purpose RL agent on the Crafter benchmark
