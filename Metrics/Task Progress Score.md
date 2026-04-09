---
tags: [metric]
aliases: [Partial Task Score, Task Progress]
category: "robotics"
higher_is_better: true
---

# Task Progress Score

## Definition
Task Progress Score is a partial-credit metric that assigns a continuous score based on how much of a multi-step task an agent completes, rather than using a binary success/failure criterion. It rewards agents for making meaningful progress toward task completion even when the full task is not achieved.

## Formula
$$\text{Task Progress Score} = \frac{\text{Number of Completed Subtask Milestones}}{\text{Total Number of Subtask Milestones}}$$

or defined as a continuous function of distance to the goal state at each phase of the task. The specific formulation depends on the task decomposition.

## Interpretation
- A score of 1.0 indicates full task completion.
- A score between 0 and 1 indicates partial progress, with higher values meaning more subtask milestones were achieved.
- A score of 0 means no meaningful progress was made toward the goal.
- This metric is more informative than binary success rate for complex, long-horizon tasks where partial completion still reflects meaningful capability.
- Higher is better.

## Common Usage
Used in robotic manipulation and embodied AI research for evaluating performance on complex multi-step tasks where binary success rate is too coarse. It provides a richer signal for comparing methods that may all fail to fully complete a task but differ in how far they progress. Particularly valuable during early-stage development and for long-horizon tasks.

## Papers Using This Metric
- [[GR00T]] — evaluating partial task completion for humanoid robot policies on multi-step manipulation tasks
