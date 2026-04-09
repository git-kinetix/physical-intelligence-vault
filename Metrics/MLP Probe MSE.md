---
tags: [metric]
aliases: [MLP Probing MSE, MLP Probe Mean Squared Error, Nonlinear Probe MSE]
category: "representation"
higher_is_better: false
---

# MLP Probe MSE

## Definition
MLP Probe MSE measures the Mean Squared Error achieved by a multi-layer perceptron (MLP) trained on top of frozen pretrained representations for a regression task. Compared to a linear probe, the MLP probe can exploit non-linear relationships between the representation and the target variable. The gap between MLP Probe MSE and Linear Probe MSE reveals how much useful information in the representation requires non-linear decoding to access.

## Formula
$$\hat{y} = \text{MLP}(f_\theta(x)) = W_L \cdot \sigma(\cdots \sigma(W_1 \cdot f_\theta(x) + b_1) \cdots) + b_L$$

$$\text{MLP Probe MSE} = \frac{1}{N} \sum_{i=1}^{N} (y_i - \hat{y}_i)^2$$

where $f_\theta(x)$ is the frozen pretrained feature extractor, $\text{MLP}$ is a multi-layer perceptron with learned weights $\{W_l, b_l\}$ and nonlinear activations $\sigma$, and $y_i$ is the ground-truth continuous target.

## Interpretation
- A low MLP Probe MSE indicates the pretrained representations contain information about the target variable, even if it is encoded non-linearly.
- If MLP Probe MSE is significantly lower than Linear Probe MSE, the representation encodes useful information in a non-linear subspace.
- If both are similar, the information is already linearly decodable and the MLP provides no additional benefit.
- Lower is better.

## Common Usage
MLP Probe MSE is used alongside Linear Probe MSE to provide a more comprehensive evaluation of representation quality for continuous prediction tasks. It is particularly relevant in robotics and physical scene understanding, where the relationship between visual features and physical quantities may be inherently non-linear.

## Papers Using This Metric
- [[Le-World-Model]] — used to evaluate how well learned representations predict continuous physical quantities via non-linear readout
