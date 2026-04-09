---
tags: [metric]
aliases: [Language Following Accuracy]
category: "robotics"
higher_is_better: true
---

# Language Following Rate

## Definition
Language Following Rate measures the proportion of trials in which a robot correctly executes the behavior specified by a natural language instruction. It evaluates the agent's ability to ground language commands into appropriate physical actions, testing both language comprehension and action execution.

## Formula
$$\text{Language Following Rate} = \frac{\text{Number of Correctly Executed Instructions}}{\text{Total Number of Instructions}} \times 100\%$$

## Interpretation
- A high rate (close to 100%) indicates the agent reliably understands and executes diverse language instructions.
- A low rate may indicate failures in language grounding, action selection, or physical execution.
- This metric can be decomposed by instruction complexity (e.g., simple single-step vs. multi-step compositional instructions) to reveal specific weaknesses.
- Higher is better.

## Common Usage
Used in language-conditioned robotics and embodied AI to evaluate how well agents follow open-vocabulary or templated language commands. It is a key metric for evaluating vision-language-action models and instruction-following robot policies, particularly as generalist robot systems aim to handle diverse natural language specifications.

## Papers Using This Metric
- [[Gemini Robotics]] — evaluating language-grounded manipulation with diverse natural language instructions
- [[Pi0.5]] — measuring instruction-following capability of generalist robot policies
