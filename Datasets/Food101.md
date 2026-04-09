---
tags: [dataset]
aliases: [Food-101, Food101]
category: "image"
year: 2014
---

# Food101

## Description
Food-101 is an image classification dataset consisting of 101 food categories, created by the Computer Vision Lab at ETH Zurich. Each category contains 1,000 images (750 training, 250 test), sourced from Foodspotting. The training set intentionally includes noisy labels to test model robustness, while the test set is manually curated.

## Format
JPEG images rescaled to a maximum side length of 512 pixels, organized by food category.

## Size
101,000 images across 101 food categories. Approximately 4.65 GB download.

## License
Images are sourced from Foodspotting; use beyond scientific fair use must be negotiated with original image owners per Foodspotting terms of use.

## How to Download
Official source: https://data.vision.ee.ethz.ch/cvl/datasets_extra/food-101/. Also available via Hugging Face: https://huggingface.co/datasets/ethz/food101, torchvision, and TensorFlow Datasets.

## Papers Using This Dataset
- [[Le-JEPA]] — used for image classification benchmarking
