---
tags: [metric]
aliases: [Normalized Score, Task-Normalized Score]
category: "robotics"
higher_is_better: true
---

# Normalized Task Score

## Definition
Normalized Task Score measures task performance scaled relative to baseline and expert reference levels, producing a standardized score that enables fair comparison across tasks with different raw score ranges. It maps performance onto a common scale where 0% represents the baseline and 100% represents expert-level performance.

## Formula
$$\text{Normalized Task Score} = \frac{S_{\text{agent}} - S_{\text{baseline}}}{S_{\text{expert}} - S_{\text{baseline}}} \times 100\%$$

where $S_{\text{agent}}$ is the agent's raw task score, $S_{\text{baseline}}$ is the score of a baseline method (e.g., random policy or simple heuristic), and $S_{\text{expert}}$ is the score of an expert (e.g., human teleoperator or best known method).

## Interpretation
- A value of 100% means the agent matches expert-level performance on the task.
- A value of 0% means the agent performs no better than the baseline.
- Values above 100% indicate the agent exceeds the expert reference.
- Normalization enables meaningful averaging across tasks with different score scales.
- Higher is better.

## Common Usage
Used in multi-task robotics and RL benchmarks to aggregate performance across tasks with heterogeneous reward structures or scoring systems. By normalizing to a common scale, it enables computing meaningful averages across diverse tasks and fair comparisons between methods.

## Papers Using This Metric
- [[GR00T]] — comparing robot policy performance across diverse manipulation tasks with varying difficulty and score ranges
