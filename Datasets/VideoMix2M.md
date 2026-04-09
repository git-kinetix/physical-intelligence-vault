---
tags: [dataset]
aliases: [VM2M, VideoMix-2M]
category: "video"
year: 2024
---

# VideoMix2M

## Description
VideoMix2M is a curated mixture of 2 million video clips assembled by Meta for self-supervised pre-training of the V-JEPA model. It combines clips from multiple publicly available video datasets into a single pre-training corpus. V-JEPA models learn visual representations by passively watching pixels from this dataset without any labels, text, or pretrained encoders.

## Format
Video clips from multiple source datasets, used for self-supervised feature prediction pre-training.

## Size
2 million video clips from public video datasets.

## License
Composed of publicly available datasets, each with their own licenses. Not released as a standalone download.

## How to Download
Not available as a direct download. The dataset is a curated mixture of public datasets. See the V-JEPA repository for details: https://github.com/facebookresearch/jepa

## Papers Using This Dataset
- [[V-JEPA]] — primary pre-training dataset
- [[V-JEPA 2]] — used as the initial pre-training data mixture before scaling to VM22M
