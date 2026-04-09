---
tags: [metric]
aliases: [Mean Intersection over Union, Mean IoU]
category: "segmentation"
higher_is_better: true
---

# mIoU

## Definition
Mean Intersection over Union (mIoU) is the standard metric for semantic segmentation. It computes the Intersection over Union (IoU) for each class independently, then averages across all classes. This gives equal weight to each class regardless of its pixel frequency, making it robust to class imbalance.

## Formula
$$\text{IoU}_c = \frac{|P_c \cap G_c|}{|P_c \cup G_c|} = \frac{\text{TP}_c}{\text{TP}_c + \text{FP}_c + \text{FN}_c}$$

$$\text{mIoU} = \frac{1}{C} \sum_{c=1}^{C} \text{IoU}_c$$

where $P_c$ and $G_c$ are the predicted and ground-truth pixel sets for class $c$, and $C$ is the total number of classes.

## Interpretation
- A high mIoU (close to 1.0 or 100%) indicates the model accurately segments most classes with high overlap between predicted and ground-truth regions.
- A low mIoU indicates poor segmentation quality, with significant under- or over-segmentation.
- Typical ranges: state-of-the-art models on ADE20K achieve 50--65% mIoU; on Cityscapes, 80--85% mIoU.
- Higher is better.

## Common Usage
mIoU is the primary evaluation metric for semantic segmentation tasks on benchmarks such as ADE20K, Cityscapes, PASCAL VOC, and COCO-Stuff. It is widely used to evaluate both supervised and self-supervised visual representations for dense prediction.

## Papers Using This Metric
- [[V-JEPA 2.1]] — used for semantic segmentation evaluation (e.g., ADE20K)
