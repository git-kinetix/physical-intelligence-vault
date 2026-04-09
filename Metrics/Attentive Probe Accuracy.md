---
tags: [metric]
aliases: [Attentive Probing Accuracy, Attentive Probe, Attention Probe]
category: "representation"
higher_is_better: true
---

# Attentive Probe Accuracy

## Definition
Attentive Probe Accuracy measures the classification accuracy achieved by training a lightweight attentive pooling mechanism followed by a linear classifier on top of frozen pretrained representations. Unlike a simple linear probe that operates on a single pooled feature vector, the attentive probe uses cross-attention to dynamically aggregate information across spatial or spatiotemporal token representations before classification. This provides a slightly richer readout while still keeping the backbone frozen.

## Formula
$$z = \text{CrossAttention}(q, \; f_\theta(x))$$

$$\hat{y} = \arg\max_c \; (W \cdot z + b)_c$$

$$\text{Attentive Probe Accuracy} = \frac{1}{N} \sum_{i=1}^{N} \mathbb{1}[\hat{y}_i = y_i]$$

where $f_\theta(x)$ produces a sequence of frozen token representations, $q$ is a learnable query token, and $W, b$ are the linear classifier parameters. Only $q$, $W$, $b$, and the cross-attention parameters are trained.

## Interpretation
- Attentive probe accuracy is typically higher than linear probe accuracy because the cross-attention mechanism can selectively attend to the most task-relevant tokens.
- A large gap between attentive and linear probe accuracy suggests that discriminative information is distributed across tokens and requires non-trivial aggregation.
- Higher is better.

## Common Usage
Attentive probing was introduced as an evaluation protocol for Vision Transformer representations, particularly in the V-JEPA line of work. It provides a middle ground between the simplicity of linear probing and the full flexibility of fine-tuning, testing whether spatially distributed information in token representations can be effectively combined for classification.

## Papers Using This Metric
- [[V-JEPA]] — introduced as an evaluation protocol for frozen video representations alongside linear probing
- [[V-JEPA 2]] — used to evaluate video and image representations on classification benchmarks
