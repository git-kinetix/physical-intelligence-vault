---
tags: [metric]
aliases: [Root Mean Square Error, Root Mean Squared Error]
category: "depth"
higher_is_better: false
---

# RMSE

## Definition
Root Mean Square Error (RMSE) measures the square root of the average squared differences between predicted and ground-truth values. It penalizes large errors more heavily than mean absolute error due to the squaring operation, making it sensitive to outliers. In depth estimation, RMSE quantifies how closely predicted depth maps match ground-truth depth measurements.

## Formula
$$\text{RMSE} = \sqrt{\frac{1}{N} \sum_{i=1}^{N} (y_i - \hat{y}_i)^2}$$

where $y_i$ is the ground-truth value, $\hat{y}_i$ is the predicted value, and $N$ is the number of samples or pixels.

## Interpretation
- A low RMSE (close to 0) indicates predictions closely match the ground truth.
- A high RMSE indicates large prediction errors, especially the presence of significant outliers.
- Typical ranges depend on the task and scale: for monocular depth estimation on NYUv2, RMSE values typically range from 0.3--0.5 meters.
- Lower is better.

## Common Usage
RMSE is one of the most widely used regression metrics across all of machine learning. In computer vision, it is a standard metric for depth estimation (monocular and stereo), surface reconstruction, and pose estimation. It is also used in robotics for trajectory prediction and control error quantification.

## Papers Using This Metric
- [[V-JEPA 2.1]] — used for monocular depth estimation evaluation
