---
tags: [metric]
aliases: [Mean Human-Normalized Score, HNS]
category: "reinforcement-learning"
higher_is_better: true
---

# Human Normalized Mean

## Definition
Human Normalized Mean is the arithmetic mean of per-game scores normalized by average (non-professional) human performance across the Atari 2600 benchmark suite. It uses typical human player baselines rather than professional gamer scores and reports the mean across all games.

## Formula
$$\text{Human Normalized Score}_i = \frac{\text{Agent Score}_i - \text{Random Score}_i}{\text{Human Score}_i - \text{Random Score}_i} \times 100\%$$

$$\text{Human Normalized Mean} = \frac{1}{N}\sum_{i=1}^{N} \text{Human Normalized Score}_i$$

where $i$ indexes individual games, $N$ is the total number of games, and Human Score refers to average (non-expert) human player performance.

## Interpretation
- A value of 100% means the agent matches average human performance on average across all games.
- Values well above 100% are common for strong RL agents, since some games yield extremely high normalized scores.
- The mean is sensitive to outlier games and can be inflated by a few games with extreme scores.
- Higher is better.

## Common Usage
Used alongside the median variant for comprehensive Atari evaluation. The mean captures aggregate performance but is less robust than the median. Reporting both mean and median is standard practice, as their divergence reveals how uniformly an agent performs across the game suite.

## Papers Using This Metric
- [[DreamerV2]] — reporting mean human-normalized Atari performance
- [[DreamerV3]] — evaluating general-purpose RL agents across the full Atari suite
