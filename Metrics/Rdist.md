---
tags: [metric]
aliases: [Rotational Distance, Rotation Error, Angular Distance]
category: "robotics"
higher_is_better: false
---

# Rdist

## Definition
Rdist (Rotational Distance) measures the angular difference between a predicted 3D rotation and the ground-truth rotation. It quantifies the accuracy of orientation estimation or generation in tasks involving 3D objects, cameras, or robot end-effectors, using geodesic distance on the rotation manifold SO(3).

## Formula
$$R_{\text{dist}} = \arccos\left(\frac{\text{tr}(\mathbf{R}_{\text{pred}}^T \mathbf{R}_{\text{gt}}) - 1}{2}\right)$$

where $\mathbf{R}_{\text{pred}}$ and $\mathbf{R}_{\text{gt}}$ are the predicted and ground-truth 3x3 rotation matrices, and $\text{tr}(\cdot)$ denotes the matrix trace. The result is in radians (or converted to degrees).

## Interpretation
- A value of 0 indicates perfect rotational alignment between prediction and ground truth.
- Larger values indicate greater angular discrepancy.
- Typical acceptable thresholds depend on the application: <5 degrees for precision manipulation, <15 degrees for coarse alignment.
- Often reported alongside Tdist (translational distance) to provide a complete 6-DOF pose error characterization.
- Lower is better.

## Common Usage
Used in 3D vision, pose estimation, novel view synthesis, and robotic manipulation to evaluate orientation accuracy. It is a standard component of 6-DOF pose evaluation and is commonly paired with translational distance to fully characterize spatial accuracy of predicted poses or generated views.

## Papers Using This Metric
- [[Hunyuan World 1.5]] — evaluating rotational accuracy of generated 3D-consistent video for world simulation
