---
tags: [metric]
aliases: [Linear Probing MSE, Linear Probe Mean Squared Error]
category: "representation"
higher_is_better: false
---

# Linear Probe MSE

## Definition
Linear Probe MSE measures the Mean Squared Error achieved by a linear regression layer trained on top of frozen pretrained representations for a regression task. Similar to linear probe accuracy for classification, this metric evaluates how well the learned features support linear prediction of continuous target variables. A low MSE indicates the representations encode information about the target quantity in a linearly accessible form.

## Formula
$$\hat{y} = W \cdot f_\theta(x) + b$$

$$\text{Linear Probe MSE} = \frac{1}{N} \sum_{i=1}^{N} (y_i - \hat{y}_i)^2$$

where $f_\theta(x)$ is the frozen pretrained feature extractor, $W$ and $b$ are the learned linear regression parameters, $y_i$ is the ground-truth continuous target, and $\hat{y}_i$ is the prediction.

## Interpretation
- A low MSE indicates the pretrained representations encode the target variable in a linearly decodable manner.
- A high MSE suggests the relationship between the representation and the target is either weak or highly non-linear.
- Comparison with MLP Probe MSE reveals whether non-linear decoding significantly improves prediction.
- Lower is better.

## Common Usage
Linear Probe MSE is used to evaluate self-supervised representations for regression tasks, particularly in robotics and physical prediction. It tests whether representations encode continuous physical quantities (e.g., positions, velocities, forces) that can be read out with a simple linear mapping, indicating strong representation quality for control and prediction.

## Papers Using This Metric
- [[Le-World-Model]] — used to evaluate how well learned representations predict continuous physical quantities via linear readout
