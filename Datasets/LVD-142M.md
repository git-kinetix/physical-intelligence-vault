---
tags: [dataset]
aliases: [LVD-142M, LVD142M]
category: "image"
year: 2023
---

# LVD-142M

## Description
LVD-142M is a curated dataset of 142 million images assembled by Meta AI for self-supervised pre-training of the DINOv2 vision foundation model. It was created through an automated retrieval pipeline that selects images from a pool of 1.2 billion uncurated web-crawled images that are visually similar to those in curated datasets (ImageNet-22K, ImageNet-1K, Google Landmarks, and fine-grained datasets). The curation includes PCA hash deduplication, NSFW filtering, and face blurring.

## Format
Images (various formats) sourced from publicly available web crawl repositories, filtered and deduplicated.

## Size
142 million images, curated from a pool of 1.2 billion uncurated images.

## License
Unknown. The dataset itself has not been publicly released. Only the models trained on it are available.

## How to Download
Not publicly available for download. Meta has not released the raw dataset. The DINOv2 models trained on LVD-142M are available at https://github.com/facebookresearch/dinov2 and on Hugging Face.

## Papers Using This Dataset
- [[Le-JEPA]] — used for self-supervised visual representation pre-training
