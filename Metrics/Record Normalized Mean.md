---
tags: [metric]
aliases: [Clipped Record Normalized Mean]
category: "reinforcement-learning"
higher_is_better: true
---

# Record Normalized Mean

## Definition
Record Normalized Mean is the arithmetic mean of per-game scores normalized by the record (state-of-the-art) performance on each game, typically clipped at 100% to prevent any single game from dominating the aggregate. This normalizes agent performance against the best known result for each game rather than against human baselines.

## Formula
$$\text{Record Normalized Score}_i = \frac{\text{Agent Score}_i - \text{Random Score}_i}{\text{Record Score}_i - \text{Random Score}_i} \times 100\%$$

$$\text{Clipped Record Normalized Mean} = \frac{1}{N}\sum_{i=1}^{N} \min\left(\text{Record Normalized Score}_i,\; 100\%\right)$$

where $i$ indexes individual games, $N$ is the total number of games, and Record Score is the best known score for that game.

## Interpretation
- A value of 100% means the agent matches or exceeds the state-of-the-art on every game.
- Clipping at 100% prevents a single game with an anomalously high score from inflating the aggregate.
- This metric is particularly useful for comparing generalist agents, as it measures how close an agent gets to the best specialized performance across all games.
- Higher is better.

## Common Usage
Used in Atari RL benchmarks to evaluate how close a single general-purpose agent comes to matching the best known (often specialized) results on each game. The clipping variant is standard because it yields a fairer aggregate that reflects breadth of competence rather than dominance on a few games.

## Papers Using This Metric
- [[DreamerV2]] — comparing model-based RL against record Atari scores
- [[DreamerV3]] — evaluating a single general-purpose agent against per-game SOTA
