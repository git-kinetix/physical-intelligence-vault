---
tags: [metric]
aliases: [ATE, Absolute Pose Error, APE]
category: "geometric"
higher_is_better: false
---

# Absolute Trajectory Error (ATE)

## Definition
Absolute Trajectory Error (ATE) measures the global consistency of an estimated trajectory against a ground-truth trajectory, typically in SLAM or visual odometry systems. After aligning the estimated and ground-truth trajectories using a rigid-body transformation (Sim(3) or SE(3)), ATE computes the root mean square error of the translational differences between corresponding poses. It captures global drift and overall trajectory accuracy.

## Formula
$$\text{ATE} = \sqrt{\frac{1}{N} \sum_{i=1}^{N} \| \text{trans}(S \cdot P_i^{-1} \cdot Q_i) \|^2}$$

where $Q_i$ is the $i$-th ground-truth pose, $P_i$ is the $i$-th estimated pose, $S$ is the optimal alignment transformation (computed via least squares), and $\text{trans}(\cdot)$ extracts the translational component.

## Interpretation
- ATE is measured in meters (or the unit of the coordinate system). Lower values indicate better global trajectory accuracy.
- A value of 0 indicates the estimated trajectory perfectly matches the ground truth after alignment.
- ATE captures accumulated drift over the entire trajectory.
- Typical values depend on the trajectory length and environment; indoor SLAM systems often achieve ATE in the range of centimeters to tens of centimeters.
- Lower is better.

## Common Usage
ATE is the standard metric for evaluating visual odometry, visual SLAM, and structure-from-motion systems. It is used on benchmarks such as TUM RGB-D, EuRoC, KITTI, and ScanNet. In representation learning, ATE evaluates whether learned features support accurate geometric reasoning and camera pose estimation.

## Papers Using This Metric
- [[V-JEPA 2.1]] — used to evaluate visual odometry and geometric understanding capabilities of learned representations
