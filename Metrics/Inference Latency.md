---
tags: [metric]
aliases: [Inference Time]
category: "efficiency"
higher_is_better: false
---

# Inference Latency

## Definition
Inference Latency measures the time elapsed from when an input is provided to a model until the model produces its output (e.g., action prediction, next token, or plan). In robotics, this directly determines the control loop frequency and real-time responsiveness of the system.

## Formula
$$\text{Inference Latency} = t_{\text{output}} - t_{\text{input}}$$

Typically reported as mean latency in milliseconds, often with percentile statistics (p50, p95, p99) to characterize tail latency. May also be reported as control frequency: $f = 1 / \text{latency}$ in Hz.

## Interpretation
- Low latency (e.g., <50ms) enables high-frequency control loops necessary for reactive robotic manipulation.
- High latency introduces delays that can cause instability, missed catches, or unsafe behavior in physical systems.
- There is often a tradeoff between model capacity/accuracy and inference latency.
- Typical targets: <10ms for real-time control, <100ms for near-real-time planning, <1s for high-level decision making.
- Lower is better.

## Common Usage
Critical metric in robotics, autonomous driving, and any real-time AI system. It determines whether a model can be deployed in a closed-loop control setting. Large foundation models for robotics must carefully optimize inference latency to maintain acceptable control frequencies (typically 5-50 Hz for manipulation).

## Papers Using This Metric
- [[Pi0]] — measuring real-time inference speed of the vision-language-action model
- [[GR00T]] — evaluating control frequency of humanoid robot foundation models
- [[Gemini Robotics]] — benchmarking inference speed of multimodal robotic models
