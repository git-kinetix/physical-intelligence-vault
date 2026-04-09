---
tags: [dataset]
aliases: [TempCompass Benchmark]
category: "evaluation-benchmark"
year: 2024
---

# TempCompass

## Description
TempCompass is a benchmark for comprehensively evaluating the temporal perception ability of Video LLMs, published at ACL 2024 Findings. It covers ten temporal aspects (action, speed, direction, attribute change, event order, etc.) across four task types: multi-choice QA, yes/no QA, caption matching, and caption generation, using conflicting video pairs that share static content but differ in temporal dynamics.

## Format
Video-based QA benchmark with multiple task formats. Videos are paired to prevent single-frame bias exploitation.

## Size
Hundreds of test videos with multi-format question-answer pairs across 10 temporal aspects.

## License
CC-BY-SA 4.0 (website)

## How to Download
- GitHub: https://github.com/llyx97/TempCompass
- Project page: https://llyx97.github.io/tempcompass/
- Evaluation code released for benchmarking custom models.

## Papers Using This Dataset
- [[V-JEPA 2]] — evaluated on temporal comprehension (76.9 accuracy)
