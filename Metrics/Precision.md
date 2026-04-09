---
tags: [metric]
aliases: [Positive Predictive Value, PPV]
category: "classification"
higher_is_better: true
---

# Precision

## Definition
Precision measures the fraction of positive predictions that are actually correct. It answers the question: "Of all the instances the model predicted as positive, how many truly are positive?" Precision is critical when the cost of false positives is high.

## Formula
$$\text{Precision} = \frac{\text{TP}}{\text{TP} + \text{FP}}$$

where TP is the number of true positives and FP is the number of false positives.

## Interpretation
- A precision of 1.0 means every positive prediction is correct (no false positives).
- A low precision indicates many false positives among the model's positive predictions.
- Precision can be high even if recall is low (the model is conservative but correct when it does predict positive).
- Higher is better.

## Common Usage
Precision is a fundamental classification metric used in information retrieval, object detection, medical diagnosis, and any task where false positives are costly. It is typically reported alongside recall and F1 Score. In world model and video generation evaluation, precision can assess the correctness of predicted scene attributes or generated content.

## Papers Using This Metric
- [[NVIDIA Cosmos]] — used in world model evaluation for assessing prediction correctness
