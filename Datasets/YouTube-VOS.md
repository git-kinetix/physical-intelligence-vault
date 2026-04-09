---
tags: [dataset]
aliases: [YouTube-VOS, YTVOS, YouTube VOS 2019]
category: "video"
year: 2018
---

# YouTube-VOS

## Description
YouTube-VOS is the first large-scale benchmark for video object segmentation, featuring real-world YouTube videos with dense pixel-level object annotations. It supports semi-supervised, unsupervised, and referring video object segmentation tasks, and uniquely evaluates generalization to unseen object categories not present in training.

## Format
Video frames (JPEG) with per-frame instance segmentation masks in PNG format. Annotations include object instance IDs and category labels.

## Size
4,453 YouTube video clips across 94 object categories. The 2019 version: 3,471 training videos (65 categories, 6,459 instances), 507 validation videos (65 seen + 26 unseen categories), and 541 test videos. 197,272 total annotations.

## License
Unknown. Registration required on the competition platform.

## How to Download
Official website: https://youtube-vos.org/. Data download requires registration on the CodaLab competition platform. Dataset details: https://youtube-vos.org/dataset/vos/

## Papers Using This Dataset
- [[V-JEPA 2.1]] — used for video object segmentation evaluation
