---
tags: [metric]
aliases: [F1, F-measure, F-score, Dice Coefficient]
category: "classification"
higher_is_better: true
---

# F1 Score

## Definition
The F1 Score is the harmonic mean of precision and recall, providing a single metric that balances both concerns. It is especially useful when class distributions are imbalanced, as it penalizes models that achieve high precision at the expense of recall (or vice versa). The harmonic mean ensures that both precision and recall must be reasonably high for the F1 Score to be high.

## Formula
$$\text{F1} = 2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}} = \frac{2\text{TP}}{2\text{TP} + \text{FP} + \text{FN}}$$

where TP is true positives, FP is false positives, and FN is false negatives.

## Interpretation
- An F1 of 1.0 indicates perfect precision and recall.
- An F1 of 0.0 indicates the model has zero precision or zero recall.
- Typical ranges depend on the task; values above 0.8 are generally considered strong for most classification tasks.
- Higher is better.

## Common Usage
The F1 Score is used in binary and multi-class classification, information extraction, named entity recognition, and object detection. It is particularly valued when false positives and false negatives carry similar costs. In video generation and world model evaluation, F1 can measure the quality of discrete predictions such as scene categorization or object presence detection.

## Papers Using This Metric
- [[NVIDIA Cosmos]] — used to evaluate discrete prediction tasks in world model evaluation
