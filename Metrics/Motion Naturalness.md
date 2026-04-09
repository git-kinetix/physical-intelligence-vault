---
tags: [metric]
aliases: [Motion Quality Score, Naturalness Score]
category: "human-evaluation"
higher_is_better: true
---

# Motion Naturalness

## Definition
Motion Naturalness is a quality metric that evaluates how realistic and human-like generated motion sequences appear. It can be assessed through human evaluation (subjective ratings of naturalness) or computed automatically by comparing statistical properties of generated motions to those of real human motion capture data.

## Formula
When computed automatically, common formulations include comparison of motion feature distributions:

$$\text{Motion Naturalness} \propto -D_{\text{KL}}\left(p_{\text{generated}} \| p_{\text{real}}\right)$$

or assessed via human rating on a Likert scale. When using learned quality models, it may be a regression score predicting perceived naturalness. There is no single universal formula.

## Interpretation
- High naturalness indicates generated motions look smooth, physically plausible, and human-like.
- Low naturalness indicates artifacts such as foot sliding, jittering, unnatural joint angles, floating, or physically implausible movements.
- Human judges are the most reliable evaluators, as they are highly sensitive to subtle motion artifacts.
- Higher is better.

## Common Usage
Used in character animation, motion generation, humanoid robotics, and virtual avatar research. It is a central quality metric for any system that generates human-like motion, whether for games, film, VR/AR, or humanoid robot control. Often evaluated alongside metrics like motion diversity and text-motion alignment.

## Papers Using This Metric
- [[Hierarchical Puppeteer]] — evaluating the quality and realism of hierarchically generated character motions
