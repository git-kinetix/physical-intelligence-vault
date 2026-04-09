---
tags: [dataset]
aliases: [CIFAR100]
category: "image"
year: 2009
---

# CIFAR-100

## Description
CIFAR-100 is a fine-grained variant of CIFAR-10, containing the same number of images but spread across 100 classes grouped into 20 superclasses. Each class has only 600 images (500 training, 100 test), making it a more challenging classification benchmark that tests a model's ability to discriminate among visually similar categories.

## Format
32x32 pixel RGB images stored in binary batches (Python pickle format).

## Size
60,000 images total: 50,000 training and 10,000 test images across 100 classes. Approximately 163 MB download size.

## License
Apache License 2.0.

## How to Download
Available directly from https://www.cs.toronto.edu/~kriz/cifar.html. Also accessible via torchvision, TensorFlow Datasets, and Hugging Face: https://huggingface.co/datasets/uoft-cs/cifar100

## Papers Using This Dataset
- [[Le-JEPA]] — used for image classification benchmarking
