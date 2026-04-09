---
tags: [metric]
aliases: [Human Rating, Human Judgment Score, MOS]
category: "human-evaluation"
higher_is_better: true
---

# Human Evaluation Score

## Definition
Human Evaluation Score is a numerical rating assigned by human evaluators to assess the quality of generated outputs (e.g., videos, images, motions, or text) on a predefined scale. Evaluators rate individual samples on criteria such as visual quality, realism, coherence, or faithfulness to input conditions, and scores are averaged across raters and samples.

## Formula
$$\text{Human Evaluation Score} = \frac{1}{N \cdot R}\sum_{i=1}^{N}\sum_{j=1}^{R} s_{ij}$$

where $s_{ij}$ is the score assigned by rater $j$ to sample $i$, $N$ is the number of samples, and $R$ is the number of raters per sample. Scores are typically on a Likert scale (e.g., 1-5 or 1-7).

## Interpretation
- Higher scores indicate better perceived quality by human judges.
- The absolute scale depends on the rating protocol (e.g., 1-5 Likert scale, 0-100 continuous scale).
- Inter-rater agreement metrics (e.g., Cohen's kappa, Krippendorff's alpha) should accompany results to validate reliability.
- Scores are most meaningful when compared across methods within the same evaluation protocol.
- Higher is better.

## Common Usage
Used as a gold-standard evaluation in generative modeling when automated metrics are insufficient to capture perceptual quality. Common in video generation, world model evaluation, and content generation research where subjective human judgment is essential for assessing realism, coherence, and overall quality.

## Papers Using This Metric
- [[Hunyuan World 1.5]] — evaluating generated world simulation video quality through human ratings
