---
tags: [dataset]
aliases: [ADE20K, ADE-20K, MIT ADE20K]
category: "image"
year: 2017
---

# ADE20K

## Description
ADE20K is a comprehensive scene parsing dataset from MIT CSAIL, providing dense pixel-level annotations for over 27,000 images drawn from the SUN and Places databases. It covers 3,000+ object categories, with a benchmarking subset of 150 semantic classes. Many images include multi-level part annotations (objects, parts, and sub-parts), making it a key dataset for semantic segmentation research.

## Format
RGB images with pixel-wise segmentation masks encoding object class, instance ID, and part annotations. Faces and license plates are blurred.

## Size
25,210 images total: 20,210 training, 2,000 validation, and 3,000 test images. 150 classes used for benchmarking.

## License
Available under ADE20K Terms of Use (research use). See the official repository for details.

## How to Download
Official GitHub: https://github.com/CSAILVision/ADE20K. Also available via Hugging Face: https://huggingface.co/datasets/zhoubolei/scene_parse_150 and TensorFlow Datasets.

## Papers Using This Dataset
- [[V-JEPA 2.1]] — used for semantic segmentation evaluation
