---
tags: [dataset]
aliases: [Atomic Visual Actions, AVA v2.2, AVA Actions]
category: "video"
year: 2018
---

# AVA

## Description
AVA (Atomic Visual Actions) is a video dataset created by Google that provides spatio-temporally localized annotations of atomic visual actions. It densely annotates 80 atomic visual actions in movie clips, with actions localized in both space and time, enabling evaluation of action detection models that must identify what action is happening, where in the frame, and when.

## Format
Video clips extracted from movies (15-minute annotated segments), with CSV annotation files providing bounding boxes and action labels at 1-second intervals.

## Size
430 movie clips (235 training, 64 validation, 131 test), each with 15 minutes annotated. 1.62M action labels across 80 action classes.

## License
Creative Commons Attribution 4.0 International (CC BY 4.0).

## How to Download
Videos hosted by CVDF on AWS S3: https://s3.amazonaws.com/ava-dataset/. Annotations and download instructions at https://research.google.com/ava/download.html. GitHub: https://github.com/cvdfoundation/ava-dataset

## Papers Using This Dataset
- [[V-JEPA 2.1]] — used for spatio-temporal action detection evaluation
