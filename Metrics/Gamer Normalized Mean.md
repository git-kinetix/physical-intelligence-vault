---
tags: [metric]
aliases: [Mean Gamer-Normalized Score]
category: "reinforcement-learning"
higher_is_better: true
---

# Gamer Normalized Mean

## Definition
Gamer Normalized Mean is the arithmetic mean of per-game scores normalized by professional human gamer performance across the Atari 2600 benchmark suite. Each game's score is scaled so that 0% corresponds to a random agent and 100% corresponds to the professional human gamer baseline, and the mean is taken across all games.

## Formula
$$\text{Gamer Normalized Score}_i = \frac{\text{Agent Score}_i - \text{Random Score}_i}{\text{Gamer Score}_i - \text{Random Score}_i} \times 100\%$$

$$\text{Gamer Normalized Mean} = \frac{1}{N}\sum_{i=1}^{N} \text{Gamer Normalized Score}_i$$

where $i$ indexes individual Atari games and $N$ is the total number of games.

## Interpretation
- A value of 100% means the agent matches professional human gamer performance on average across games.
- Values above 100% indicate superhuman mean performance.
- The mean is sensitive to outlier games where agents score extremely well or poorly, which can inflate or deflate the aggregate.
- Higher is better.

## Common Usage
Used alongside the median variant for Atari 2600 benchmarks. The mean captures total performance across all games but can be dominated by a few games with very high or low normalized scores. It is commonly reported together with the median to give a complete picture.

## Papers Using This Metric
- [[DreamerV2]] — reporting aggregate Atari performance with both mean and median normalization
- [[DreamerV3]] — comparing general-purpose RL performance on Atari benchmarks
