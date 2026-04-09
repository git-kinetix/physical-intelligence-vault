---
tags: [metric]
aliases: [Surprise Metric, Representational Surprise]
category: "representation"
higher_is_better: false
---

# Surprise Score

## Definition
Surprise Score quantifies how unexpected or novel an observation is relative to a model's learned expectations. It measures the degree to which an input deviates from what the world model predicts, typically computed as the prediction error or negative log-likelihood of the observation under the model's predictive distribution.

## Formula
$$\text{Surprise} = -\log p_\theta(\mathbf{o}_t \mid \mathbf{o}_{<t}, \mathbf{a}_{<t})$$

or equivalently measured as:

$$\text{Surprise} = \|\mathbf{o}_t - \hat{\mathbf{o}}_t\|^2$$

where $\mathbf{o}_t$ is the actual observation, $\hat{\mathbf{o}}_t$ is the model's predicted observation, and $p_\theta$ is the model's predictive distribution.

## Interpretation
- A high Surprise Score indicates the observation was unexpected given the model's predictions, suggesting novel or out-of-distribution events.
- A low Surprise Score indicates the model's predictions closely match reality, suggesting the world is behaving as expected.
- In world model research, surprise can drive exploration (seeking surprising states) or be used to detect anomalies and distribution shifts.
- Lower is generally better (indicating accurate predictions), though higher surprise can be desirable for exploration.

## Common Usage
Used in world model evaluation, curiosity-driven exploration, and anomaly detection. In the context of world models, surprise measures how well the model captures the dynamics of the environment. It is also connected to the free energy principle and active inference frameworks.

## Papers Using This Metric
- [[Le-World-Model]] — measuring prediction surprise to evaluate world model quality and representation learning
