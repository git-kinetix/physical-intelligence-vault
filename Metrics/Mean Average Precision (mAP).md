---
tags: [metric]
aliases: [mAP, Mean AP, Average Precision]
category: "retrieval"
higher_is_better: true
---

# Mean Average Precision (mAP)

## Definition
Mean Average Precision (mAP) computes the mean of the Average Precision (AP) scores across all classes or queries. AP summarizes the precision-recall curve for a single class by computing the area under it. mAP provides a single scalar that captures both the precision and recall trade-off across the entire dataset.

## Formula
$$\text{AP}_c = \int_0^1 p_c(r) \, dr \approx \sum_{k=1}^{n} (r_k - r_{k-1}) \, p(r_k)$$

$$\text{mAP} = \frac{1}{C} \sum_{c=1}^{C} \text{AP}_c$$

where $p_c(r)$ is the precision at recall level $r$ for class $c$, and $C$ is the number of classes or queries.

## Interpretation
- A high mAP (close to 1.0 or 100%) indicates the model ranks relevant items highly with few false positives across all classes.
- A low mAP indicates the model struggles to correctly retrieve or detect relevant items.
- Typical ranges vary: object detection on COCO achieves 40--65% mAP, while action detection or anticipation tasks may range from 20--50%.
- Higher is better.

## Common Usage
mAP is the standard metric for object detection (e.g., COCO, PASCAL VOC), action detection, information retrieval, and activity anticipation tasks. In video understanding, it is commonly used for temporal action detection and egocentric activity benchmarks like Ego4D.

## Papers Using This Metric
- [[V-JEPA 2.1]] — used for Ego4D tasks including action anticipation and activity recognition
