---
tags: [metric]
aliases: [Task Success Rate, Completion Rate]
category: "robotics"
higher_is_better: true
---

# Success Rate

## Definition
Success Rate measures the proportion of trials or episodes in which an agent successfully completes a specified task according to predefined success criteria. It is the most widely used binary outcome metric in robotic manipulation and embodied AI evaluation.

## Formula
$$\text{Success Rate} = \frac{\text{Number of Successful Episodes}}{\text{Total Number of Episodes}} \times 100\%$$

## Interpretation
- A high value (close to 100%) indicates the agent reliably completes the task under the tested conditions.
- A low value indicates frequent failures; the agent struggles with the task or generalizes poorly.
- Typical ranges vary by task difficulty: simple pick-and-place tasks may reach 90%+, while complex long-horizon manipulation tasks may report 30-60%.
- Higher is better.

## Common Usage
Success Rate is the primary evaluation metric in robotic manipulation, navigation, and embodied AI research. It is used to compare policy performance across tasks, environments, and generalization conditions (e.g., unseen objects, new scenes). Nearly every robotics benchmark reports this metric.

## Papers Using This Metric
- [[V-JEPA 2]] — evaluating embodied task completion in simulated and real-world robotics
- [[Le-World-Model]] — measuring task success in model-based planning for robotics
- [[GR00T]] — evaluating humanoid and manipulation policy performance across tasks
- [[Pi0]] — reporting manipulation task completion rates
- [[Pi0.5]] — measuring generalist robot policy success across diverse tasks
- [[Pi0.6]] — evaluating large-scale autonomous robot task execution
- [[Gemini Robotics]] — benchmarking multimodal robotic manipulation performance
