---
tags: [metric]
aliases: [Human Preference Win Rate]
category: "human-evaluation"
higher_is_better: true
---

# Human Preference Rate

## Definition
Human Preference Rate measures the percentage of human evaluators who prefer the output of one method over another in a pairwise comparison. Human raters are shown outputs from two or more methods (typically blinded) and asked to indicate which they prefer based on specified criteria such as quality, realism, or task relevance.

## Formula
$$\text{Human Preference Rate} = \frac{\text{Number of Raters Preferring Method A}}{\text{Total Number of Pairwise Comparisons}} \times 100\%$$

In multi-way comparisons, this extends to the fraction of times a method is ranked first or preferred over each alternative.

## Interpretation
- A rate above 50% in a two-way comparison indicates the method is preferred more often than not over the alternative.
- A rate significantly above 50% (with statistical significance) indicates a clear human preference.
- Rates near 50% indicate the methods are perceptually similar to human judges.
- This metric captures subjective quality aspects that automated metrics may miss.
- Higher is better.

## Common Usage
Used extensively in generative AI evaluation (text, image, video, motion generation) and in robotics when evaluating the naturalness or quality of generated behaviors. Human preference studies are the gold standard for evaluating subjective aspects of quality and are typically conducted with multiple raters and inter-rater agreement statistics.

## Papers Using This Metric
- [[Hierarchical Puppeteer]] — comparing motion generation quality via human preference studies
- [[Dream Dojo]] — evaluating generated training environments through human preference judgments
