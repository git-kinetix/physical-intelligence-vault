---
tags: [metric]
aliases: [Translational Distance, Translation Error, Position Error]
category: "robotics"
higher_is_better: false
---

# Tdist

## Definition
Tdist (Translational Distance) measures the Euclidean distance between a predicted 3D position and the ground-truth position. It quantifies the accuracy of spatial localization in tasks involving camera pose estimation, object pose estimation, or 3D scene generation.

## Formula
$$T_{\text{dist}} = \|\mathbf{t}_{\text{pred}} - \mathbf{t}_{\text{gt}}\|_2 = \sqrt{\sum_{i=1}^{3}(t_{\text{pred},i} - t_{\text{gt},i})^2}$$

where $\mathbf{t}_{\text{pred}}$ and $\mathbf{t}_{\text{gt}}$ are the predicted and ground-truth 3D translation vectors.

## Interpretation
- A value of 0 indicates perfect positional accuracy.
- Larger values indicate greater spatial displacement error.
- Units match the coordinate system of the scene (typically meters or centimeters).
- Typical acceptable thresholds depend on the application: <1cm for precision manipulation, <10cm for navigation, <1m for large-scale scenes.
- Often reported alongside Rdist (rotational distance) to provide a complete 6-DOF pose error characterization.
- Lower is better.

## Common Usage
Used in 3D vision, visual odometry, SLAM, pose estimation, and world model evaluation to measure positional accuracy. It is the translational counterpart to Rdist and together they fully characterize the accuracy of 6-DOF pose predictions. Standard in benchmarks for autonomous driving, robotics, and 3D scene understanding.

## Papers Using This Metric
- [[Hunyuan World 1.5]] — evaluating translational accuracy of generated 3D-consistent video for world simulation
