---
tags: [metric]
aliases: [Perceptual Straightening, Trajectory Straightening Index]
category: "representation"
higher_is_better: true
---

# Temporal Straightening

## Definition
Temporal Straightening measures the degree to which temporal trajectories in a learned representation space form straight (linear) paths. Inspired by the perceptual straightening hypothesis from neuroscience, this metric evaluates whether a representation transforms complex, nonlinear dynamics in pixel space into simpler, more linear trajectories in latent space, which would facilitate prediction and planning.

## Formula
$$\text{Straightening Index} = 1 - \frac{\text{Var}(\theta_t)}{\text{expected variance under random walk}}$$

where $\theta_t$ is the angle between consecutive displacement vectors along the trajectory in representation space:

$$\theta_t = \arccos\left(\frac{(\mathbf{z}_{t+1} - \mathbf{z}_t) \cdot (\mathbf{z}_t - \mathbf{z}_{t-1})}{\|\mathbf{z}_{t+1} - \mathbf{z}_t\| \cdot \|\mathbf{z}_t - \mathbf{z}_{t-1}\|}\right)$$

A perfectly straight trajectory has $\theta_t = 0$ for all $t$.

## Interpretation
- A high Straightening Index (close to 1) indicates that temporal trajectories are nearly linear in the representation space, suggesting the representation has disentangled temporal dynamics into simple, predictable paths.
- A low index indicates curved, complex trajectories that are harder to predict linearly.
- This metric connects to the hypothesis that good representations simplify temporal prediction.
- Higher is better.

## Common Usage
Used in representation learning and world model research to evaluate whether learned latent spaces produce temporally coherent, predictable representations. It draws on the neuroscience hypothesis that biological visual systems straighten temporal trajectories to simplify prediction of future states.

## Papers Using This Metric
- [[Le-World-Model]] — evaluating whether learned world model representations produce temporally straight trajectories
