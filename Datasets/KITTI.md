---
tags: [dataset]
aliases: [KITTI Vision Benchmark, KITTI Dataset]
category: "multimodal"
year: 2012
---

# KITTI

## Description
KITTI (Karlsruhe Institute of Technology and Toyota Technological Institute) is a comprehensive benchmark suite for autonomous driving, providing real-world sensor data captured from a driving platform equipped with stereo cameras, a Velodyne LiDAR scanner, and GPS/IMU. It covers multiple tasks including stereo vision, optical flow, visual odometry, 3D object detection, and tracking, making it one of the most influential autonomous driving benchmarks.

## Format
Stereo image pairs (PNG), Velodyne LiDAR point clouds (binary), GPS/IMU data, and calibration files. Annotations include 3D bounding boxes, 2D bounding boxes, and difficulty labels.

## Size
7,481 training images with 3D object annotations, 389 stereo/optical flow pairs, and 39.2 km of visual odometry sequences. Multiple sub-benchmarks with varying sizes.

## License
Creative Commons Attribution-NonCommercial-ShareAlike 3.0 (CC BY-NC-SA 3.0).

## How to Download
Official website: https://www.cvlibs.net/datasets/kitti/. Also available via AWS Open Data: https://registry.opendata.aws/kitti/

## Papers Using This Dataset
- [[V-JEPA 2.1]] — used for autonomous driving scene understanding evaluation
