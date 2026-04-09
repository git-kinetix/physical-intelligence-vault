---
tags: [dataset]
aliases: [ImageNet-21K, ImageNet-22K, ImageNet Full, ImageNet-21K-P]
category: "image"
year: 2011
---

# ImageNet-22K

## Description
ImageNet-22K (also called ImageNet-21K) is the full ImageNet dataset containing approximately 21,841 classes and over 14 million images. It provides a much broader visual vocabulary than the 1K-class subset and is commonly used for large-scale pre-training before fine-tuning on downstream tasks.

## Format
JPEG images of variable resolution, organized by WordNet synset IDs into class directories.

## Size
14,197,122 images across 21,841 classes. Approximately 1.31 TB compressed. The cleaned version (ImageNet-21K-P) contains 12,358,688 images from 11,221 categories.

## License
Non-commercial research and educational use only. Same ImageNet Terms of Access as ImageNet-1K.

## How to Download
Registration required at https://www.image-net.org/download.php. The winter 2021 release (winter21_whole.tar.gz) removed problematic "person" subtree categories. Also available via Hugging Face: https://huggingface.co/datasets/timm/imagenet-22k-wds

## Papers Using This Dataset
- [[V-JEPA]] — used for large-scale pre-training evaluation
