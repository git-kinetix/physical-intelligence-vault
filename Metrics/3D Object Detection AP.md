---
tags: [metric]
aliases: [3D Detection Average Precision, 3D AP, 3D mAP]
category: "robotics"
higher_is_better: true
---

# 3D Object Detection AP

## Definition
3D Object Detection Average Precision (AP) measures the accuracy of a model's 3D object detection by computing the area under the precision-recall curve for 3D bounding box predictions. A predicted 3D bounding box is considered correct if its 3D Intersection over Union (IoU) with a ground-truth box exceeds a specified threshold.

## Formula
$$\text{AP} = \int_0^1 p(r) \, dr$$

where $p(r)$ is the precision at recall level $r$, computed over the precision-recall curve. A detection is a true positive if:

$$\text{IoU}_{3D}(\hat{B}, B) = \frac{|\hat{B} \cap B|}{|\hat{B} \cup B|} \geq \tau$$

where $\hat{B}$ and $B$ are the predicted and ground-truth 3D bounding boxes, and $\tau$ is the IoU threshold (commonly 0.25, 0.5, or 0.7).

## Interpretation
- An AP of 100% indicates perfect detection with no false positives or missed objects at all recall levels.
- Higher IoU thresholds demand more precise 3D localization and sizing.
- Mean AP (mAP) averages across object categories to give an aggregate score.
- Typical values range from 20-80% depending on scene complexity, object category, and IoU threshold.
- Higher is better.

## Common Usage
Standard metric for 3D object detection in autonomous driving (KITTI, nuScenes, Waymo), indoor scene understanding (ScanNet, SUN RGB-D), and robotic perception. It is essential for evaluating a robot's ability to perceive and localize objects in 3D space for downstream manipulation or navigation.

## Papers Using This Metric
- [[Gemini Robotics]] — evaluating 3D scene understanding and object detection for robotic manipulation
