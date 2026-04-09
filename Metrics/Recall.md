---
tags: [metric]
aliases: [Sensitivity, True Positive Rate, TPR, Hit Rate]
category: "classification"
higher_is_better: true
---

# Recall

## Definition
Recall measures the fraction of actual positive instances that the model correctly identifies. It answers the question: "Of all the truly positive instances, how many did the model find?" Recall is critical when the cost of false negatives is high, i.e., when missing a positive instance is costly.

## Formula
$$\text{Recall} = \frac{\text{TP}}{\text{TP} + \text{FN}}$$

where TP is the number of true positives and FN is the number of false negatives.

## Interpretation
- A recall of 1.0 means the model finds every positive instance (no false negatives).
- A low recall indicates the model misses many positive instances.
- Recall can be high even if precision is low (the model predicts positive liberally, catching everything but also producing many false positives).
- Higher is better.

## Common Usage
Recall is a fundamental classification metric used in information retrieval, medical screening, object detection, and any task where missing positive instances is costly. It is typically reported alongside precision and F1 Score. In video generation and world model evaluation, recall can assess coverage of ground-truth scene elements or events.

## Papers Using This Metric
- [[NVIDIA Cosmos]] — used in world model evaluation for assessing detection coverage
