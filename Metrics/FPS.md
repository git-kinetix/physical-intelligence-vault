---
tags: [metric]
aliases: [Frames Per Second, Inference Speed, Throughput]
category: "robotics"
higher_is_better: true
---

# FPS

## Definition
Frames Per Second (FPS) measures the throughput or inference speed of a model, quantifying how many frames (or samples) the model can process per second. In robotics and real-time systems, FPS is a critical deployment metric that determines whether a model can operate within the latency requirements of the application. It encompasses the full inference pipeline including preprocessing, forward pass, and postprocessing.

## Formula
$$\text{FPS} = \frac{N_{\text{frames}}}{T_{\text{total}}}$$

where $N_{\text{frames}}$ is the number of frames processed and $T_{\text{total}}$ is the total wall-clock time in seconds. Equivalently, FPS is the reciprocal of per-frame latency:

$$\text{FPS} = \frac{1}{\text{latency per frame (seconds)}}$$

## Interpretation
- Higher FPS indicates faster inference, enabling real-time or near-real-time operation.
- For robotics control, 10--30 FPS is often required for responsive manipulation; 30+ FPS for real-time visual tasks.
- FPS depends heavily on hardware (GPU model, batch size, precision) and should always be reported with hardware context.
- Higher is better for deployment, but FPS must be weighed against model accuracy.

## Common Usage
FPS is a standard deployment metric in robotics, autonomous driving, video processing, and any real-time inference application. It is used to compare model efficiency and determine deployment feasibility. In world model and policy learning research, FPS indicates whether the model can run faster than real-time (enabling planning) or at real-time (enabling direct deployment).

## Papers Using This Metric
- [[Hierarchical Puppeteer]] — used to measure inference speed of the hierarchical control policy
- [[NVIDIA Cosmos]] — used to report tokenizer and world model inference throughput
