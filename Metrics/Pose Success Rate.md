---
tags: [metric]
aliases: [Pose Estimation Success Rate, Viewpoint Accuracy]
category: "robotics"
higher_is_better: true
---

# Pose Success Rate

## Definition
Pose Success Rate measures the proportion of frames or instances in which the estimated camera pose or object pose falls within acceptable error thresholds relative to the ground-truth pose. It evaluates the reliability of pose estimation or view synthesis by checking whether both rotational and translational errors are below specified tolerances.

## Formula
$$\text{Pose Success Rate} = \frac{1}{N}\sum_{i=1}^{N} \mathbf{1}\left[\Delta R_i < \tau_R \;\wedge\; \Delta t_i < \tau_t\right] \times 100\%$$

where $\Delta R_i$ is the rotational error (e.g., geodesic distance on SO(3)), $\Delta t_i$ is the translational error, and $\tau_R$, $\tau_t$ are the respective thresholds.

## Interpretation
- A high success rate indicates the model reliably estimates poses within the specified tolerances.
- The choice of thresholds ($\tau_R$, $\tau_t$) determines the strictness of the evaluation; tighter thresholds require more precise estimation.
- Results are often reported at multiple threshold levels (e.g., 5/10/15 degrees, 5/10/15 cm) to characterize precision across difficulty levels.
- Higher is better.

## Common Usage
Used in 3D vision, visual odometry, SLAM, novel view synthesis, and robotic perception. It evaluates whether generated or estimated views correspond to correct camera poses, which is critical for robotics applications that rely on accurate spatial understanding and world models that generate view-consistent predictions.

## Papers Using This Metric
- [[NVIDIA Cosmos]] — evaluating camera pose accuracy in world model-generated video for robotic and autonomous driving applications
