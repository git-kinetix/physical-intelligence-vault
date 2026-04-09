---
tags: [metric]
aliases: [Behaviour Suite Score, bsuite Score]
category: "reinforcement-learning"
higher_is_better: true
---

# BSuite Score

## Definition
BSuite Score is the aggregate performance score on DeepMind's Behaviour Suite (bsuite), a collection of carefully designed diagnostic experiments that test specific RL agent capabilities including credit assignment, exploration, memory, generalization, and noise robustness. Each experiment yields a score between 0 and 1, and the aggregate combines these across all core capabilities.

## Formula
$$\text{BSuite Score} = \frac{1}{K}\sum_{k=1}^{K} \bar{s}_k$$

where $\bar{s}_k$ is the average score for capability category $k$ (e.g., credit assignment, exploration, memory) and $K$ is the number of capability categories. Individual experiment scores $s_k \in [0, 1]$.

## Interpretation
- A score of 1.0 indicates perfect performance across all diagnostic experiments.
- A score near 0.0 indicates failure on most diagnostic tasks.
- The breakdown by capability category is often more informative than the aggregate, revealing specific strengths and weaknesses of an agent.
- Higher is better.

## Common Usage
BSuite is used to diagnose and understand RL agent capabilities beyond raw task performance. It is particularly valuable for identifying failure modes and comparing agents on specific axes of competence (e.g., does the agent handle partial observability, long credit assignment chains, or stochastic rewards?).

## Papers Using This Metric
- [[DreamerV3]] — profiling the diagnostic capabilities of a general-purpose world model agent
