---
tags: [metric]
aliases: [Execution Time, Task Duration, Time to Completion]
category: "efficiency"
higher_is_better: false
---

# Task Completion Time

## Definition
Task Completion Time measures the elapsed wall-clock time (or number of environment steps) from the start of task execution to successful completion. It captures the speed and efficiency of an agent's behavior, penalizing unnecessary or redundant actions even when the task is eventually completed.

## Formula
$$\text{Task Completion Time} = t_{\text{end}} - t_{\text{start}}$$

where $t_{\text{start}}$ is the time at task initiation and $t_{\text{end}}$ is the time at which success criteria are met. Typically averaged across successful episodes only.

## Interpretation
- A low completion time indicates the agent executes the task efficiently with minimal wasted motion or hesitation.
- A high completion time may indicate suboptimal planning, excessive caution, or inefficient motion trajectories.
- This metric is only meaningful for successful episodes; failed episodes are typically excluded or reported separately.
- Lower is better.

## Common Usage
Used in robotics and embodied AI to evaluate operational efficiency alongside success rate. Two policies may have similar success rates but very different completion times, which matters for real-world throughput and deployment economics. It is particularly relevant for evaluating autonomous systems in production settings.

## Papers Using This Metric
- [[Pi0.6]] — measuring execution efficiency of autonomous robot policies in real-world task deployment
