---
tags: [dataset]
aliases: [LAION-5B, LAION-400M, LAION Dataset, Re-LAION-5B]
category: "multimodal"
year: 2022
---

# LAION

## Description
LAION (Large-scale Artificial Intelligence Open Network) is a collection of massive image-text pair datasets created by the open-source LAION organization. LAION-5B contains 5.85 billion CLIP-filtered image-text pairs (2.3B English, 2.2B multilingual, 1B unclassified language), making it one of the largest openly accessible multimodal datasets. Re-LAION-5B is a safety-revised version with additional filtering.

## Format
Image URLs paired with alt-text captions, CLIP embeddings, and metadata. Images must be downloaded from their original URLs. Distributed as Parquet files with metadata columns.

## Size
LAION-5B: 5.85 billion image-text pairs. LAION-400M: ~400 million pairs. Re-LAION-5B includes safety-filtered subsets.

## License
LAION-5B: Creative Commons Attribution 4.0 (CC BY 4.0). Re-LAION-5B: Apache License 2.0. Note: the dataset is uncurated and may contain disturbing content.

## How to Download
Official website: https://laion.ai/blog/laion-5b/. Available on Hugging Face: https://huggingface.co/datasets/laion/relaion400m. Download tools: https://github.com/rom1504/img2dataset

## Papers Using This Dataset
- [[Le-JEPA]] — used as a large-scale image-text pre-training source
