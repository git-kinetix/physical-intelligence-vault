---
tags: [metric]
aliases: [Task Failure Rate, Error Rate]
category: "robotics"
higher_is_better: false
---

# Failure Rate

## Definition
Failure Rate measures the proportion of episodes or task attempts in which the agent fails to complete the task or triggers a failure condition (e.g., dropping an object, colliding, exceeding time limits, or entering an unrecoverable state). It is the complement of Success Rate and is often reported when characterizing system reliability.

## Formula
$$\text{Failure Rate} = \frac{\text{Number of Failed Episodes}}{\text{Total Number of Episodes}} \times 100\% = 1 - \text{Success Rate}$$

## Interpretation
- A low Failure Rate (close to 0%) indicates high reliability and consistent task completion.
- A high Failure Rate indicates the agent frequently fails, which is critical in real-world deployment where failures may have consequences (e.g., damaged objects, safety incidents).
- Failure Rate is sometimes broken down by failure mode (e.g., grasp failure, navigation failure, timeout) to provide diagnostic insight.
- Lower is better.

## Common Usage
Reported in robotics research to emphasize system reliability, particularly in contexts where the cost of failure is high (industrial deployment, human-robot interaction, autonomous operations). It is the natural complement to success rate and is preferred when the focus is on risk characterization.

## Papers Using This Metric
- [[Pi0.6]] — characterizing failure modes and reliability of autonomous robot task execution at scale
