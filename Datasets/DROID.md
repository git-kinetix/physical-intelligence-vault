---
tags: [dataset]
aliases: [Droid Dataset]
category: "robotics"
year: 2024
---

# DROID

## Description
DROID (Distributed Robot Interaction Dataset) is a large-scale, in-the-wild robot manipulation dataset consisting of 76,000 demonstration trajectories (350 hours of interaction data) collected across 564 scenes, 52 buildings, and 86 tasks. It provides diverse real-world manipulation data for training generalizable robot policies.

## Format
Trajectory data with RGB images (multiple camera views including wrist cameras), depth, proprioceptive states, and actions. Stored in RLDS format.

## Size
76,000 trajectories, 350 hours of interaction data, 564 scenes, 52 buildings, 86 tasks.

## License
CC-BY 4.0

## How to Download
- Official website: https://droid-dataset.github.io/
- GitHub: https://github.com/droid-dataset/droid
- Includes interactive dataset visualizer and policy training code.

## Papers Using This Dataset
- [[V-JEPA 2.1]] — used for robot manipulation pretraining
- [[Dream Dojo]] — used for world model training data
- [[Learning Latent Action World Models]] — used for learning latent action representations
