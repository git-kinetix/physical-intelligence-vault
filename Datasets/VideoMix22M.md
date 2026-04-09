---
tags: [dataset]
aliases: [VM22M, VideoMix-22M]
category: "video"
year: 2025
---

# VideoMix22M

## Description
VideoMix22M (VM22M) is a large-scale video pre-training mixture assembled by Meta for V-JEPA 2.1, scaling up from the earlier VideoMix2M. It combines several publicly available video and image sources -- including Something-Something v2, Kinetics, HowTo100M, ImageNet, and a curated version of YT-Temporal-1B -- totaling over 1 million hours of video. The 10x increase in data over VM2M yields measurable improvements in downstream performance.

## Format
Video clips and images from multiple source datasets, used for self-supervised feature prediction pre-training.

## Size
22 million video and image samples, comprising over 1 million hours of video content.

## License
Composed of publicly available datasets, each with their own licenses. Not released as a standalone download.

## How to Download
Not available as a direct download. The dataset is a curated mixture of public datasets. See the V-JEPA 2 repository for details: https://github.com/facebookresearch/vjepa2

## Papers Using This Dataset
- [[V-JEPA 2.1]] — primary pre-training dataset, scaling from 2M to 22M samples
