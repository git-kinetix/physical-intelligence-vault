---
tags: [dataset]
aliases: [ILSVRC 2012, ImageNet-1K, ImageNet 1K]
category: "image"
year: 2012
---

# ImageNet-1K

## Description
ImageNet-1K (ILSVRC 2012) is the most widely used image classification benchmark, containing 1,000 object classes drawn from the larger ImageNet hierarchy. It has served as the de facto standard for evaluating visual representation learning since the original AlexNet result in 2012.

## Format
JPEG images of variable resolution, organized into class-specific directories. Typically resized to 224x224 or 256x256 for training.

## Size
1,281,167 training images, 50,000 validation images, and 100,000 test images across 1,000 classes. Approximately 150 GB total.

## License
Non-commercial research and educational use only. Researchers must agree to the ImageNet Terms of Access and accept full responsibility for their use.

## How to Download
Registration required at https://www.image-net.org/download.php. Also available via Hugging Face: https://huggingface.co/datasets/ILSVRC/imagenet-1k and through torchvision.

## Papers Using This Dataset
- [[V-JEPA]] — used for downstream image classification evaluation
- [[V-JEPA 2]] — used for downstream image classification evaluation
- [[V-JEPA 2.1]] — used for downstream image classification evaluation
- [[Le-JEPA]] — used for image classification benchmarking
- [[NVIDIA Cosmos]] — referenced as a standard vision benchmark
