---
tags: [metric]
aliases: [P(X > Y), Probability of Superiority]
category: "reinforcement-learning"
higher_is_better: true
---

# Probability of Improvement

## Definition
Probability of Improvement is a statistical metric that estimates the probability that one algorithm outperforms another across a set of tasks or random seeds. It provides a robust, non-parametric way to compare RL algorithms that accounts for variability across tasks and runs, as recommended by the rliable statistical framework.

## Formula
$$P(X > Y) = \frac{1}{N \cdot M} \sum_{i=1}^{N} \sum_{j=1}^{M} \mathbf{1}\left[X_i > Y_j\right]$$

where $X_i$ and $Y_j$ are performance scores from algorithms $X$ and $Y$ respectively across $N$ and $M$ independent runs, and $\mathbf{1}[\cdot]$ is the indicator function. Confidence intervals are typically computed via bootstrapping.

## Interpretation
- A value of 0.5 indicates the two algorithms are equally likely to outperform each other (no difference).
- A value close to 1.0 means algorithm X almost always outperforms algorithm Y.
- A value close to 0.0 means algorithm Y almost always outperforms algorithm X.
- Unlike point estimates of mean performance, this metric captures the full distribution of outcomes.
- Higher is better (when evaluating whether algorithm X improves over Y).

## Common Usage
Recommended by the rliable framework for statistically rigorous comparison of RL algorithms. It is used instead of or alongside aggregate score comparisons to provide a more reliable assessment that accounts for the high variability inherent in RL experiments across seeds and environments.

## Papers Using This Metric
- [[TD-JEPA]] — comparing world model approaches using statistically rigorous evaluation methodology
