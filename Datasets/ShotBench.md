---
tags: [dataset]
aliases: [ShotBench, Shot Bench]
category: "evaluation-benchmark"
year: 2024
---

# ShotBench

## Description
ShotBench is a shot boundary detection benchmark created by NVIDIA as part of the Cosmos video curation pipeline. It evaluates whether algorithms can reliably detect shot transitions (cuts, fades, dissolves) in heavily edited videos with complex visual effects. The benchmark aggregates existing shot detection datasets and compares methods like TransNetV2, AutoShot, and PySceneDetect.

## Format
Video clips with annotated shot boundaries from existing datasets including RAI, BBC Planet Earth, ClipShots, and SHOT.

## Size
Composed of multiple existing shot boundary datasets. Exact total size not publicly documented.

## License
Unknown. Composed of existing datasets with their own licenses.

## How to Download
Official GitHub: https://github.com/NVlabs/ShotBench. Described in the NVIDIA Cosmos paper (arXiv:2501.03575).

## Papers Using This Dataset
- [[NVIDIA Cosmos]] — used to evaluate shot boundary detection for the video curation pipeline
