---
tags: [metric]
aliases: [Linear Probing Accuracy, Linear Evaluation, Linear Probe]
category: "representation"
higher_is_better: true
---

# Linear Probe Accuracy

## Definition
Linear Probe Accuracy measures the classification accuracy achieved by training a single linear layer (logistic regression) on top of frozen pretrained representations. The pretrained encoder's weights are kept fixed, and only the linear classifier is optimized. This evaluates how linearly separable the learned features are for a downstream task, serving as a standard benchmark for representation quality in self-supervised learning.

## Formula
$$\hat{y} = \arg\max_c \; (W \cdot f_\theta(x) + b)_c$$

$$\text{Linear Probe Accuracy} = \frac{1}{N} \sum_{i=1}^{N} \mathbb{1}[\hat{y}_i = y_i]$$

where $f_\theta(x)$ is the frozen pretrained feature extractor, $W$ and $b$ are the learned linear classifier parameters, and $c$ indexes classes.

## Interpretation
- A high linear probe accuracy indicates the pretrained representations encode class-relevant information in a linearly accessible form.
- A low linear probe accuracy may indicate that useful information is present but not linearly decodable, or that the representations are poor.
- The gap between linear probe accuracy and fine-tuned accuracy reveals how much non-linear structure remains to be exploited.
- Higher is better.

## Common Usage
Linear probing is the most widely used protocol for evaluating self-supervised visual representations. It is the standard evaluation on ImageNet-1K, Kinetics, and other benchmarks for models like DINO, MAE, V-JEPA, and their variants. It tests whether the learned features are "ready to use" for classification without additional complex decoders.

## Papers Using This Metric
- [[V-JEPA]] — used as a primary evaluation protocol for video representations on Kinetics-400 and Something-Something v2
- [[V-JEPA 2]] — used to evaluate frozen representations on Kinetics and ImageNet benchmarks
- [[Le-JEPA]] — used to evaluate quality of learned latent representations
