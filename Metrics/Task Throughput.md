---
tags: [metric]
aliases: [Tasks Per Hour, Throughput Rate]
category: "efficiency"
higher_is_better: true
---

# Task Throughput

## Definition
Task Throughput measures the number of tasks successfully completed per unit of time (e.g., tasks per hour or tasks per shift). It combines both success rate and execution speed into a single operational metric that reflects the productive capacity of a robotic system.

## Formula
$$\text{Task Throughput} = \frac{\text{Number of Successfully Completed Tasks}}{\text{Total Elapsed Time}}$$

Equivalently, it can be expressed as:

$$\text{Task Throughput} = \frac{\text{Success Rate}}{\text{Mean Task Completion Time}}$$

## Interpretation
- A high throughput indicates the robot completes many tasks quickly and reliably, reflecting both speed and reliability.
- A low throughput may result from either frequent failures (low success rate), slow execution (high completion time), or both.
- This metric is directly relevant to real-world deployment economics and production planning.
- Higher is better.

## Common Usage
Used in robotics research and deployment to evaluate end-to-end operational efficiency. It is particularly important for industrial and logistics applications where the economic value of a robot is directly tied to how many tasks it can complete in a given time window. It naturally integrates success rate and speed into a single productivity measure.

## Papers Using This Metric
- [[Pi0.6]] — evaluating productive capacity of autonomous robot systems operating at scale
