---
tags: [dataset]
aliases: [ERQA, Embodied Reasoning QA]
category: "evaluation-benchmark"
year: 2025
---

# ERQA Benchmark

## Description
ERQA (Embodied Reasoning Question Answering) is an open-source benchmark from Google DeepMind released alongside Gemini Robotics for evaluating embodied reasoning capabilities of multimodal models. It contains 400 multiple-choice questions covering spatial reasoning, world knowledge, trajectory reasoning, state estimation, and task reasoning in real-world robotic scenarios, using interleaved image-text inputs.

## Format
Multimodal multiple-choice QA in TFRecord format. Questions interleave images and text with single-letter answers (A, B, C, D).

## Size
400 examples across multiple embodied reasoning categories.

## License
Unknown (check GitHub repository)

## How to Download
- GitHub: https://github.com/embodiedreasoning/ERQA
- Data provided as `data/erqa.tfrecord`.
- Associated with Gemini Robotics: https://deepmind.google/models/gemini-robotics/gemini-robotics-er/

## Papers Using This Dataset
- [[Gemini Robotics]] — primary evaluation benchmark for Gemini Robotics-ER embodied reasoning
