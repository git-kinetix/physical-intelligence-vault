---
tags: [metric]
aliases: [Sample Efficiency, Data Efficiency Ratio]
category: "efficiency"
higher_is_better: true
---

# Data Efficiency

## Definition
Data Efficiency measures the performance an agent achieves relative to the amount of data (environment interactions, demonstrations, or training samples) it consumes. A more data-efficient method reaches a given performance level with fewer samples, or achieves higher performance with the same data budget.

## Formula
$$\text{Data Efficiency} = \frac{\text{Performance at } N \text{ samples}}{\text{Baseline Performance at } N \text{ samples}}$$

or reported as the number of environment steps required to reach a target performance threshold. There is no single universal formula; it is typically assessed by comparing learning curves or reporting performance at fixed data budgets (e.g., 100K, 1M steps).

## Interpretation
- Higher data efficiency means the agent learns faster from fewer interactions, which is critical for real-world robotics where data collection is expensive.
- A data-efficient agent's learning curve rises steeply early and plateaus sooner.
- Comparisons are typically made by fixing the data budget and comparing performance, or by measuring the data required to reach a target performance level.
- Higher is better (more performance per unit of data).

## Common Usage
Data efficiency is a central concern in model-based RL (where world models reduce the need for real environment interactions), offline RL, imitation learning, and robotic learning. It is especially important when transferring from simulation to real robots, where each real-world interaction is costly.

## Papers Using This Metric
- [[DreamerV1]] — demonstrating improved sample efficiency of world model-based RL over model-free methods
- [[DreamerV2]] — showing data-efficient learning from pixels on Atari and continuous control
- [[GR00T]] — evaluating how efficiently robot policies learn from limited demonstration data
