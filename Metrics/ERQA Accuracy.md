---
tags: [metric]
aliases: [Embodied Reasoning QA Accuracy, Embodied QA Accuracy]
category: "robotics"
higher_is_better: true
---

# ERQA Accuracy

## Definition
ERQA (Embodied Reasoning Question Answering) Accuracy measures a model's ability to correctly answer questions that require embodied spatial reasoning about physical scenes, objects, and their relationships. It specifically tests understanding of 3D spatial relationships, physical properties, affordances, and scene semantics from an embodied agent's perspective.

## Formula
$$\text{ERQA Accuracy} = \frac{\text{Number of Correctly Answered Embodied Reasoning Questions}}{\text{Total Number of Questions}} \times 100\%$$

## Interpretation
- A high accuracy indicates the model has strong embodied spatial reasoning and scene understanding capabilities.
- A low accuracy suggests the model struggles with physical reasoning, spatial relationships, or grounding abstract questions in visual/physical scene context.
- Performance is often analyzed by question category (e.g., spatial relations, object properties, physical reasoning) to identify specific weaknesses.
- Higher is better.

## Common Usage
Used in embodied AI and robotics to evaluate whether multimodal models truly understand the physical world beyond surface-level visual recognition. ERQA benchmarks test capabilities critical for robots that must reason about scenes to plan actions, such as understanding which objects are reachable, what fits where, or how objects physically interact.

## Papers Using This Metric
- [[Gemini Robotics]] — evaluating embodied reasoning capabilities for robotic scene understanding and manipulation planning
