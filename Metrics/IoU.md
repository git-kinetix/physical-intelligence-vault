---
tags: [metric]
aliases: [Intersection over Union, Jaccard Index]
category: "segmentation"
higher_is_better: true
---

# IoU

## Definition
Intersection over Union (IoU), also known as the Jaccard Index, measures the overlap between a predicted region and a ground-truth region. It is computed as the area of intersection divided by the area of union of the two regions. IoU is a fundamental building block for many detection and segmentation metrics.

## Formula
$$\text{IoU} = \frac{|A \cap B|}{|A \cup B|} = \frac{|A \cap B|}{|A| + |B| - |A \cap B|}$$

where $A$ is the predicted region (bounding box or mask) and $B$ is the ground-truth region.

## Interpretation
- An IoU of 1.0 indicates perfect overlap between prediction and ground truth.
- An IoU of 0.0 indicates no overlap at all.
- In object detection, an IoU threshold of 0.5 is commonly used to determine a "correct" detection (AP@50), while stricter thresholds like 0.75 (AP@75) or averaged thresholds 0.5:0.95 are also used.
- Higher is better.

## Common Usage
IoU is used across object detection, instance segmentation, semantic segmentation, and video object segmentation. It serves as the threshold criterion for determining true positives in detection metrics (mAP) and as a direct evaluation metric for segmentation quality. In world model evaluation, IoU can measure the fidelity of predicted scene layouts or object placements.

## Papers Using This Metric
- [[NVIDIA Cosmos]] — used to evaluate tokenizer reconstruction quality and scene understanding
