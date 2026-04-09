---
tags: [dataset]
aliases: [RealEstate10K, RE10K, Real Estate 10K]
category: "video"
year: 2018
---

# RealEstate10K

## Description
RealEstate10K is a large-scale camera pose dataset created by Google, containing approximately 80,000 video clips extracted from roughly 10,000 YouTube real estate walkthrough videos. Camera poses are estimated using Structure from Motion (SfM), providing ground-truth trajectories for each clip. It is widely used for novel view synthesis, 3D scene reconstruction, and camera motion understanding research.

## Format
Text files (one per clip) specifying timestamps and 6-DOF camera poses for sampled frames. Videos must be downloaded from YouTube using the provided video IDs and timestamps.

## Size
Approximately 80,000 video clips from ~10,000 YouTube videos, totaling roughly 10 million frames.

## License
Creative Commons Attribution 4.0 International (CC BY 4.0).

## How to Download
Official project page: https://google.github.io/realestate10k/. Downloader scripts available at https://github.com/cashiwamochi/RealEstate10K_Downloader

## Papers Using This Dataset
- [[Hunyuan World 1.5]] — used for 3D-aware video generation and novel view synthesis
