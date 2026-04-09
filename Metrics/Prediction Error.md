---
tags: [metric]
aliases: [Model Prediction Error, Prediction Loss, Forecast Error]
category: "representation"
higher_is_better: false
---

# Prediction Error

## Definition
Prediction Error measures the discrepancy between a model's predicted outputs and the actual ground-truth observations or states. In the context of world models and latent action models, it quantifies how accurately the model can forecast future observations, states, or latent representations given current context and actions.

## Formula
$$\text{Prediction Error} = \frac{1}{T}\sum_{t=1}^{T} \mathcal{L}(\hat{\mathbf{y}}_t, \mathbf{y}_t)$$

where $\hat{\mathbf{y}}_t$ is the model's prediction at time $t$, $\mathbf{y}_t$ is the ground-truth, and $\mathcal{L}$ is a loss function such as:

- Mean Squared Error: $\mathcal{L} = \|\hat{\mathbf{y}}_t - \mathbf{y}_t\|_2^2$
- Mean Absolute Error: $\mathcal{L} = \|\hat{\mathbf{y}}_t - \mathbf{y}_t\|_1$
- Cross-entropy or negative log-likelihood for discrete predictions

## Interpretation
- Low prediction error indicates the model accurately captures the dynamics of the environment and can reliably forecast future states.
- High prediction error indicates the model's internal dynamics are misaligned with reality, which will degrade planning and decision-making performance.
- Prediction error typically grows with the prediction horizon, as errors compound over multi-step rollouts.
- Lower is better.

## Common Usage
Fundamental evaluation metric for world models, dynamics models, and predictive models in RL and robotics. It directly measures the quality of the model's learned dynamics, which is critical for model-based planning and imagination-based policy learning. Often reported at multiple prediction horizons to assess error accumulation.

## Papers Using This Metric
- Learning Latent Action World Models — evaluating the accuracy of latent action world model predictions against ground-truth environment dynamics
