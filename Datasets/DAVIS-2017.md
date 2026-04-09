---
tags: [dataset]
aliases: [DAVIS, DAVIS 2017, DAVIS2017]
category: "video"
year: 2017
---

# DAVIS-2017

## Description
DAVIS (Densely Annotated VIdeo Segmentation) 2017 is a benchmark for semi-supervised video object segmentation, extending the original DAVIS 2016 dataset with multi-object annotations. It provides per-frame pixel-level segmentation masks for multiple objects in each video, making it a standard evaluation target for video object segmentation methods that must track and segment objects across frames.

## Format
Video frames (JPEG/PNG) with per-frame binary segmentation masks for each object instance. Available at 480p and full resolution.

## Size
90 sequences (50 re-annotated from DAVIS 2016 plus 40 new) for train+val, and 30 additional test-challenge sequences. 480p version is ~794 MB; full resolution is ~2.75 GB.

## License
BSD License.

## How to Download
Official website: https://davischallenge.org/. Download script provided in the official repository: https://github.com/fperazzi/davis-2017. Also available via TensorFlow Datasets.

## Papers Using This Dataset
- [[V-JEPA 2.1]] — used for video object segmentation evaluation
- [[NVIDIA Cosmos]] — referenced as a video segmentation benchmark
