---
tags: [metric]
aliases: [Multi-choice Accuracy, TOMATO Accuracy]
category: "representation"
higher_is_better: true
---

# VQA Accuracy

## Definition
VQA (Visual Question Answering) Accuracy measures the proportion of visual questions that a model answers correctly, given an image or video as visual input and a natural language question. It evaluates a model's ability to jointly understand visual content and language to produce correct answers.

## Formula
$$\text{VQA Accuracy} = \frac{\text{Number of Correctly Answered Questions}}{\text{Total Number of Questions}} \times 100\%$$

For open-ended VQA with multiple human-annotated answers, the soft accuracy formula from the VQA benchmark is:

$$\text{Accuracy}_i = \min\left(\frac{\text{count of matching answers}}{3}, 1\right)$$

## Interpretation
- A high accuracy (close to 100%) indicates the model reliably understands both visual content and question semantics to produce correct answers.
- Random chance baseline depends on the answer space (e.g., 25% for 4-choice multiple-choice, much lower for open-ended).
- Multi-choice accuracy provides a controlled evaluation; open-ended accuracy tests generation capability.
- Higher is better.

## Common Usage
VQA Accuracy is the standard metric for visual question answering benchmarks. It is used to evaluate multimodal understanding in vision-language models, video understanding models, and embodied AI systems. Variants include video QA (where the input is a video clip) and embodied QA (where questions relate to physical scene understanding).

## Papers Using This Metric
- [[V-JEPA 2]] — evaluating video understanding and visual reasoning capabilities
- [[V-JEPA 2.1]] — measuring visual question answering accuracy on video understanding benchmarks
