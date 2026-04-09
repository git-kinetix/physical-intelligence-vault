---
tags: [metric]
aliases: [Pointing Accuracy, 2D Localization Accuracy]
category: "robotics"
higher_is_better: true
---

# 2D Pointing Accuracy

## Definition
2D Pointing Accuracy measures the precision of a model's ability to identify and localize specific points in a 2D image, typically by predicting pixel coordinates corresponding to queried objects, parts, or locations. It evaluates spatial grounding — the model's ability to map semantic queries to precise image locations.

## Formula
$$\text{2D Pointing Accuracy} = \frac{\text{Number of Points Within Threshold}}{\text{Total Number of Queries}} \times 100\%$$

where a prediction is considered correct if the Euclidean distance between predicted and ground-truth pixel coordinates is below a threshold $\tau$:

$$\|\mathbf{p}_{\text{pred}} - \mathbf{p}_{\text{gt}}\|_2 < \tau$$

## Interpretation
- A high accuracy indicates the model can precisely localize queried objects or locations in images.
- The threshold $\tau$ determines how strict the evaluation is; tighter thresholds require more precise localization.
- This metric directly tests spatial grounding, which is prerequisite for robotic manipulation (e.g., knowing where to grasp).
- Higher is better.

## Common Usage
Used in robotic perception and vision-language models to evaluate spatial grounding capabilities. For robotics, accurate 2D pointing is essential for tasks like specifying grasp points, identifying target locations, and translating visual understanding into actionable spatial coordinates for manipulation.

## Papers Using This Metric
- [[Gemini Robotics]] — evaluating spatial grounding accuracy for robotic manipulation planning
