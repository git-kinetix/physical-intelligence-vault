---
tags: [metric]
aliases: [J and F Mean, Jaccard and F-measure Mean, J&F, DAVIS Score]
category: "segmentation"
higher_is_better: true
---

# J&F Mean

## Definition
J&F Mean is the primary evaluation metric for video object segmentation (VOS), used on the DAVIS benchmark. It is the average of two complementary scores: the Jaccard index (J), which measures region-based overlap (IoU) between predicted and ground-truth masks, and the F-measure (F), which measures contour-based accuracy by comparing the boundary of predicted masks to ground-truth boundaries. Together, they capture both region accuracy and boundary precision.

## Formula
$$\mathcal{J} = \frac{|M_p \cap M_{gt}|}{|M_p \cup M_{gt}|}$$

$$\mathcal{F} = \frac{2 \cdot P_c \cdot R_c}{P_c + R_c}$$

$$\text{J\&F Mean} = \frac{\mathcal{J} + \mathcal{F}}{2}$$

where $M_p$ and $M_{gt}$ are the predicted and ground-truth masks, and $P_c$ and $R_c$ are precision and recall computed on the mask contours.

## Interpretation
- J&F Mean ranges from 0 to 1 (or 0% to 100%), with higher values indicating better segmentation.
- State-of-the-art methods on DAVIS 2017 achieve J&F Mean values of 85--90%.
- The J component captures overall mask overlap, while the F component rewards accurate boundary delineation.
- Higher is better.

## Common Usage
J&F Mean is the standard metric for semi-supervised and unsupervised video object segmentation on the DAVIS benchmark. It evaluates how well a model can track and segment objects across video frames, capturing both spatial accuracy and temporal consistency. It is widely used to evaluate video understanding models and self-supervised visual representations.

## Papers Using This Metric
- [[V-JEPA 2.1]] — used to evaluate video object segmentation performance on the DAVIS benchmark
