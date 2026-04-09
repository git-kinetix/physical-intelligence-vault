---
tags: [metric]
aliases: [MMRV, Max Rank Violation]
category: "representation"
higher_is_better: false
---

# Mean Maximum Rank Violation

## Definition
Mean Maximum Rank Violation measures the consistency of learned rankings or orderings by computing the average of the worst-case rank violations across a set of items. A rank violation occurs when the predicted ordering of two items disagrees with the ground-truth ordering, and the maximum violation captures the largest such disagreement for each query.

## Formula
$$\text{MMRV} = \frac{1}{N}\sum_{i=1}^{N} \max_{j: r_i < r_j} \left(\hat{r}_j - \hat{r}_i\right)^{+}$$

where $r_i$ is the ground-truth rank of item $i$, $\hat{r}_i$ is the predicted rank, and $(x)^{+} = \max(0, x)$. The inner max finds the worst violation for each item, and the outer average computes the mean across all items.

## Interpretation
- A value of 0 indicates perfect ranking consistency with no violations.
- Higher values indicate larger disagreements between predicted and true orderings, with the worst-case violations being the primary concern.
- This metric is more sensitive to catastrophic ranking errors than mean rank violation, as it focuses on the worst case per query.
- Lower is better.

## Common Usage
Used in ranking evaluation, preference learning, and reward modeling. It is particularly relevant for evaluating learned reward functions or preference models that must maintain consistent orderings, such as in RLHF or hierarchical motion generation where the quality ranking of generated outputs must be preserved.

## Papers Using This Metric
- [[Hierarchical Puppeteer]] — evaluating ranking consistency of hierarchical motion generation quality
