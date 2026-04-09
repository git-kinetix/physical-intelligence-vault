---
tags: [dataset]
aliases: [BDD100K, Berkeley DeepDrive 100K]
category: "video"
year: 2020
---

# BDD100K

## Description
BDD100K is a large-scale, diverse driving video dataset from the Berkeley DeepDrive project, featuring 100,000 videos captured from more than 50,000 rides across New York, San Francisco Bay Area, and other regions. It provides annotations for multiple tasks including scene tagging, object detection, lane marking, drivable area segmentation, semantic/instance segmentation, and multi-object tracking, making it one of the most richly annotated driving datasets available.

## Format
720p video at 30fps, approximately 40 seconds per clip. Accompanied by JSON annotation files for multiple tasks including bounding boxes, segmentation masks, and lane markings.

## Size
100,000 videos (70K training, 10K validation, 20K test). Multiple annotation types covering diverse weather, time-of-day, and geographic conditions.

## License
Available for research use. Requires agreeing to the BDD100K license upon download.

## How to Download
Official website: https://www.vis.xyz/bdd100k/. Data also available at https://dl.cv.ethz.ch/bdd100k/data/. Documentation: https://doc.bdd100k.com/download.html. GitHub toolkit: https://github.com/bdd100k/bdd100k

## Papers Using This Dataset
- [[NVIDIA Cosmos]] — used as a driving video data source and part of TokenBench evaluation
