---
tags: [dataset]
aliases: [Tanks and Temples, TanksAndTemples, T&T, T2]
category: "evaluation-benchmark"
year: 2017
---

# Tanks and Temples

## Description
Tanks and Temples is a benchmark for large-scale 3D reconstruction from images, featuring real-world indoor and outdoor scenes captured with high-resolution video and ground-truth geometry obtained via industrial laser scanning. It evaluates the end-to-end quality of image-based 3D reconstruction pipelines under realistic, non-laboratory conditions, and is divided into training, intermediate, and advanced difficulty tiers.

## Format
High-resolution video sequences (input) with ground-truth 3D point clouds from laser scanning (evaluation). Includes 21 scenes across three difficulty levels. A Python downloader script is provided for selective download.

## Size
21 scenes split into Training (7 scenes: Barn, Caterpillar, Church, Courthouse, Ignatius, Meetingroom, Truck), Intermediate (8 scenes: Family, Francis, Horse, Lighthouse, M60, Panther, Playground, Train), and Advanced (6 scenes: Auditorium, Ballroom, Courtroom, Museum, Palace, Temple).

## License
Creative Commons license (free to share and adapt, including for commercial use, with attribution). Python scripts are under MIT License.

## How to Download
Official website with Python downloader: https://www.tanksandtemples.org/. GitHub toolkit: https://github.com/isl-org/TanksAndTemples. Example download command: `python download_t2_dataset.py --modality video --group both`

## Papers Using This Dataset
- [[Hunyuan World 1.5]] — used for 3D reconstruction evaluation
