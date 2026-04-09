---
tags: [metric]
aliases: [L2 Distance to Goal, Goal Distance, End-Effector Distance]
category: "robotics"
higher_is_better: false
---

# Euclidean Distance to Goal

## Definition
Euclidean Distance to Goal measures the L2 (straight-line) distance between the agent's current state (e.g., end-effector position, object position, or robot configuration) and a specified target state in Euclidean space. It provides a continuous measure of how close the agent is to achieving the desired goal configuration.

## Formula
$$d = \|\mathbf{x}_{\text{current}} - \mathbf{x}_{\text{goal}}\|_2 = \sqrt{\sum_{i=1}^{n}(x_i^{\text{current}} - x_i^{\text{goal}})^2}$$

where $\mathbf{x}_{\text{current}}$ and $\mathbf{x}_{\text{goal}}$ are position vectors in $n$-dimensional space (typically $n=2$ or $n=3$).

## Interpretation
- A distance of 0 indicates the agent has exactly reached the goal position.
- Larger distances indicate the agent is farther from the goal, either due to incomplete execution or trajectory errors.
- Typical ranges depend on the workspace scale (e.g., millimeters for precision manipulation, meters for navigation).
- This metric provides a continuous performance signal even when binary success thresholds are not met.
- Lower is better.

## Common Usage
Widely used in robotic reaching, navigation, and goal-conditioned RL tasks. It serves as both an evaluation metric and a reward signal for goal-conditioned policies. It is particularly useful for evaluating precision of manipulation, path following, and visual servoing systems.

## Papers Using This Metric
- [[V-JEPA 2]] — evaluating world model-based planning accuracy for reaching target configurations in robotic tasks
