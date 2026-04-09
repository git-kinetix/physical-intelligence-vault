---
tags: [dataset]
aliases: [K710, Kinetics710]
category: "video"
year: 2022
---

# Kinetics-710

## Description
Kinetics-710 is a merged video action recognition dataset that combines the training sets of Kinetics-400, Kinetics-600, and Kinetics-700, removing duplicate videos by YouTube ID. The merging of action categories across the three source datasets yields 710 unique classes. It was introduced alongside the UniFormerV2 model to provide a larger, deduplicated training set for video understanding.

## Format
Video clips (MP4) approximately 10 seconds long, sourced from YouTube. Uses annotation files that reference the original Kinetics-400/600/700 video files.

## Size
Approximately 650,000 unique video clips across 710 action classes (reduced from 1.14M total across all three source datasets after deduplication).

## License
Creative Commons Attribution 4.0 International (CC BY 4.0), following the license of the underlying Kinetics datasets.

## How to Download
Requires downloading Kinetics-400/600/700 separately and applying the merged annotation files. MMAction2 provides annotation support: https://mmaction2.readthedocs.io/en/latest/dataset_zoo/kinetics710.html. UniFormerV2 repo: https://github.com/OpenGVLab/UniFormerV2/blob/main/DATASET.md

## Papers Using This Dataset
- [[V-JEPA 2.1]] — used for video action recognition evaluation
