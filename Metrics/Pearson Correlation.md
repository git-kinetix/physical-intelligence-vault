---
tags: [metric]
aliases: [Pearson Correlation Coefficient, Pearson's r, PCC, Linear Correlation]
category: "representation"
higher_is_better: true
---

# Pearson Correlation

## Definition
The Pearson Correlation Coefficient measures the linear relationship between two variables, yielding a value between -1 and +1. In the context of representation learning, it quantifies how well a model's predictions (or learned features) linearly correlate with ground-truth continuous values. It is scale-invariant and captures the strength and direction of the linear association.

## Formula
$$r = \frac{\sum_{i=1}^{N}(x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum_{i=1}^{N}(x_i - \bar{x})^2} \cdot \sqrt{\sum_{i=1}^{N}(y_i - \bar{y})^2}}$$

where $x_i$ and $y_i$ are paired observations, and $\bar{x}$ and $\bar{y}$ are their respective means.

## Interpretation
- $r = 1$ indicates a perfect positive linear relationship; $r = -1$ indicates a perfect negative linear relationship; $r = 0$ indicates no linear correlation.
- In regression evaluation, values above 0.8 typically indicate strong correlation; 0.5--0.8 moderate; below 0.5 weak.
- Pearson correlation is insensitive to scale and offset, making it useful when absolute prediction values matter less than relative ordering and trend.
- Higher (closer to 1) is typically better for positive correlation tasks.

## Common Usage
Pearson Correlation is used to evaluate regression predictions, assess representation quality for continuous targets, and measure agreement between predicted and ground-truth signals. In robotics and world model research, it is used to evaluate how well learned representations predict continuous physical quantities (e.g., forces, positions, joint angles).

## Papers Using This Metric
- [[Le-World-Model]] — used to evaluate how well learned representations predict continuous physical quantities
- [[Hierarchical Puppeteer]] — used to evaluate correlation between predicted and ground-truth control signals
