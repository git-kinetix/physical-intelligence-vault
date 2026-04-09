---
tags: [metric]
aliases: [Zero-Shot Normalized Return, Normalized Zero-Shot Performance]
category: "reinforcement-learning"
higher_is_better: true
---

# Normalized Zero-Shot Returns

## Definition
Normalized Zero-Shot Returns measures an agent's performance on tasks it has not been explicitly trained on, with scores normalized relative to baseline and expert performance levels. It quantifies how well learned representations or policies transfer to new tasks without any task-specific fine-tuning.

## Formula
$$\text{Normalized Zero-Shot Return} = \frac{G_{\text{agent}} - G_{\text{random}}}{G_{\text{expert}} - G_{\text{random}}} \times 100\%$$

where $G_{\text{agent}}$ is the episode return of the zero-shot agent, $G_{\text{random}}$ is the return of a random policy, and $G_{\text{expert}}$ is the return of a trained expert.

## Interpretation
- A value of 100% means the agent matches expert-level performance on unseen tasks without any fine-tuning.
- A value of 0% means the agent performs no better than random on the transfer tasks.
- Values between 0-100% reflect partial transfer capability; values above 100% indicate the zero-shot agent exceeds the expert baseline.
- Higher is better.

## Common Usage
Used in transfer learning and representation learning for RL to evaluate how well pre-trained world models, representations, or policies generalize to unseen tasks. It is particularly relevant for evaluating self-supervised or unsupervised pre-training approaches in RL.

## Papers Using This Metric
- [[TD-JEPA]] — evaluating zero-shot transfer of temporal difference world model representations to downstream RL tasks
