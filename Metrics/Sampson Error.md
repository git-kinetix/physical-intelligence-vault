---
tags: [metric]
aliases: [Sampson Distance, Sampson Epipolar Error]
category: "geometric"
higher_is_better: false
---

# Sampson Error

## Definition
Sampson Error (also called Sampson Distance) is a first-order approximation of the geometric reprojection error for point correspondences under epipolar geometry. Given a fundamental matrix $F$ and a pair of corresponding points, the Sampson error measures the algebraic distance of the correspondence from satisfying the epipolar constraint, normalized by the gradient of the constraint. It provides a computationally efficient proxy for the more expensive optimal geometric (reprojection) error.

## Formula
$$\text{Sampson Error} = \frac{(x'^{\top} F x)^2}{(Fx)_1^2 + (Fx)_2^2 + (F^{\top}x')_1^2 + (F^{\top}x')_2^2}$$

where $x$ and $x'$ are corresponding points in homogeneous coordinates, $F$ is the fundamental matrix, and $(Fx)_k$ denotes the $k$-th component of the vector $Fx$.

## Interpretation
- Sampson Error is measured in squared pixels. Lower values indicate more accurate epipolar geometry estimation.
- A value of 0 means the correspondence perfectly satisfies the epipolar constraint.
- It serves as a good approximation to the reprojection error and is used as a quality criterion in RANSAC-based fundamental matrix estimation.
- Typical threshold values for inlier classification range from 0.5 to 3.0 pixels (squared).
- Lower is better.

## Common Usage
Sampson Error is widely used in multi-view geometry, structure from motion, and visual SLAM for evaluating fundamental matrix and essential matrix estimation quality. It is also used within RANSAC as an inlier/outlier criterion. In representation learning and foundation model evaluation, it tests whether learned features support accurate geometric reasoning for two-view correspondence problems.

## Papers Using This Metric
- [[NVIDIA Cosmos]] — used to evaluate geometric reasoning quality of tokenizer representations
