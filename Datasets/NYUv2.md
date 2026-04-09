---
tags: [dataset]
aliases: [NYU Depth V2, NYU Depth Dataset V2, NYUD, NYUDv2]
category: "multimodal"
year: 2012
---

# NYUv2

## Description
NYU Depth V2 is an RGB-D dataset for indoor scene understanding, captured using a Microsoft Kinect sensor across 464 different indoor scenes spanning 26 scene types. It provides aligned RGB and depth image pairs with dense semantic labels, making it a standard benchmark for depth estimation, semantic segmentation, and surface normal prediction in indoor environments.

## Format
Aligned RGB and depth image pairs stored in MATLAB .mat format. Dense pixel-level semantic annotations for 1,449 labeled frames. Raw data includes unlabeled RGB-D video sequences.

## Size
1,449 densely labeled image pairs and 407,024 unlabeled frames across 464 scenes. Labeled dataset is ~2.8 GB; raw data exceeds 400 GB.

## License
MIT License.

## How to Download
Official source: https://cs.nyu.edu/~fergus/datasets/nyu_depth_v2.html. Also available via Hugging Face: https://huggingface.co/datasets/sayakpaul/nyu_depth_v2, Kaggle, and TensorFlow Datasets.

## Papers Using This Dataset
- [[V-JEPA 2.1]] — used for depth estimation and indoor scene understanding evaluation
