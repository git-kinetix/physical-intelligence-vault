---
tags: [metric]
aliases: [Median Gamer-Normalized Score]
category: "reinforcement-learning"
higher_is_better: true
---

# Gamer Normalized Median

## Definition
Gamer Normalized Median is the median of per-game scores normalized by professional human gamer performance across the Atari 2600 benchmark suite. Each game's score is scaled so that 0% corresponds to a random agent and 100% corresponds to the professional human gamer baseline, and the median is taken across all games.

## Formula
$$\text{Gamer Normalized Score}_i = \frac{\text{Agent Score}_i - \text{Random Score}_i}{\text{Gamer Score}_i - \text{Random Score}_i} \times 100\%$$

$$\text{Gamer Normalized Median} = \text{median}_i\left(\text{Gamer Normalized Score}_i\right)$$

where $i$ indexes individual Atari games.

## Interpretation
- A value of 100% means the agent matches professional human gamer performance at the median game.
- Values above 100% indicate superhuman median performance.
- The median is more robust than the mean to outlier games where agents achieve extremely high or low scores.
- Higher is better.

## Common Usage
This metric is standard for evaluating RL agents on the Atari 2600 benchmark (typically the ALE 26 or 57 game suites). It provides a single aggregate number summarizing performance relative to skilled human players, using the median to resist inflation from a few dominating games.

## Papers Using This Metric
- [[DreamerV2]] — comparing model-based RL performance across the Atari 57 game suite
- [[DreamerV3]] — demonstrating general-purpose RL agent performance on Atari benchmarks
