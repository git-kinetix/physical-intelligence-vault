---
tags: [metric]
aliases: [RTE, Relative Pose Error, RPE]
category: "geometric"
higher_is_better: false
---

# Relative Trajectory Error (RTE)

## Definition
Relative Trajectory Error (RTE) measures the local accuracy of an estimated trajectory by comparing the relative motion between consecutive pose pairs against the ground truth. Unlike ATE which captures global drift, RTE evaluates the accuracy of individual motion increments (frame-to-frame or over fixed time intervals). This makes it sensitive to local tracking quality and less affected by accumulated drift.

## Formula
$$\text{RTE} = \sqrt{\frac{1}{N-\delta} \sum_{i=1}^{N-\delta} \| \text{trans}\left((Q_i^{-1} Q_{i+\delta})^{-1} (P_i^{-1} P_{i+\delta})\right) \|^2}$$

where $Q_i, Q_{i+\delta}$ are ground-truth poses at times $i$ and $i+\delta$, $P_i, P_{i+\delta}$ are the corresponding estimated poses, and $\delta$ is the fixed time interval (often 1 frame).

## Interpretation
- RTE is measured in meters (translational) or degrees (rotational) per time step. Lower values indicate better local motion estimation.
- RTE captures instantaneous tracking quality rather than accumulated drift.
- It is more informative than ATE for evaluating short-term motion estimation accuracy.
- Typical values are smaller than ATE since they measure per-step error rather than cumulative error.
- Lower is better.

## Common Usage
RTE is a standard metric for evaluating visual odometry, SLAM, and ego-motion estimation systems alongside ATE. It is particularly useful for evaluating local tracking accuracy on benchmarks like TUM RGB-D, EuRoC, and KITTI. In representation learning, RTE tests whether features support accurate frame-to-frame geometric estimation.

## Papers Using This Metric
- [[V-JEPA 2.1]] — used to evaluate local tracking accuracy of visual odometry with learned representations
