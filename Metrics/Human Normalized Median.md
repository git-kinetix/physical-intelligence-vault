---
tags: [metric]
aliases: [Median Human-Normalized Score, HNM]
category: "reinforcement-learning"
higher_is_better: true
---

# Human Normalized Median

## Definition
Human Normalized Median is the median of per-game scores normalized by average (non-professional) human performance across the Atari 2600 benchmark suite. Unlike Gamer Normalized scores which use professional gamer baselines, this metric uses typical human player scores as the reference, and reports the median across games.

## Formula
$$\text{Human Normalized Score}_i = \frac{\text{Agent Score}_i - \text{Random Score}_i}{\text{Human Score}_i - \text{Random Score}_i} \times 100\%$$

$$\text{Human Normalized Median} = \text{median}_i\left(\text{Human Normalized Score}_i\right)$$

where $i$ indexes individual games and Human Score refers to average (non-expert) human player performance.

## Interpretation
- A value of 100% means the agent matches average human performance at the median game.
- Values above 100% indicate superhuman median performance relative to typical human players.
- The median is robust to outlier games and provides a conservative aggregate measure.
- Higher is better.

## Common Usage
This metric is used in Atari RL benchmarks when the reference baseline is average human performance rather than professional gamer scores. The distinction matters because professional gamer scores are substantially higher, making gamer-normalized scores appear lower. It is part of the standard reporting suite for large-scale Atari evaluations.

## Papers Using This Metric
- [[DreamerV2]] — reporting Atari performance normalized by average human baselines
- [[DreamerV3]] — comparing RL agents with human-level performance references
