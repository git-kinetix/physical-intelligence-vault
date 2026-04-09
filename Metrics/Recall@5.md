---
tags: [metric]
aliases: [Recall at 5, R@5, Top-5 Recall]
category: "retrieval"
higher_is_better: true
---

# Recall@5

## Definition
Recall@5 measures the proportion of relevant items that appear within the top 5 predictions returned by the model. For action anticipation tasks, it checks whether the correct future action is among the model's top 5 predicted actions. It captures the model's ability to include the correct answer in a small shortlist of candidates.

## Formula
$$\text{Recall@5} = \frac{1}{N} \sum_{i=1}^{N} \mathbb{1}[y_i \in \text{Top-5}(\hat{y}_i)]$$

where $y_i$ is the ground-truth label for query $i$ and $\text{Top-5}(\hat{y}_i)$ is the set of the model's 5 highest-ranked predictions.

## Interpretation
- A high value (close to 1.0 or 100%) indicates the correct label almost always appears among the model's top 5 predictions.
- A low value indicates the model frequently fails to rank the correct answer in its top 5.
- Typical ranges depend on the number of classes and task difficulty; for EPIC-KITCHENS action anticipation, values typically range from 20--50%.
- Higher is better.

## Common Usage
Recall@K metrics are standard in information retrieval, recommendation systems, and action anticipation. In video understanding, Recall@5 is a primary metric for the EPIC-KITCHENS action anticipation benchmark, where models must predict the next action (verb, noun, or action pair) from egocentric video.

## Papers Using This Metric
- [[V-JEPA 2]] — used for EPIC-KITCHENS action anticipation evaluation
- [[V-JEPA 2.1]] — used for EPIC-KITCHENS action anticipation evaluation
