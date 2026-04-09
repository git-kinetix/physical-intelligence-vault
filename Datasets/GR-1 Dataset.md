---
tags: [dataset]
aliases: [GR1 Dataset, Fourier GR-1 Dataset, PhysicalAI-Robotics-GR00T-GR1]
category: "robotics"
year: 2025
---

# GR-1 Dataset

## Description
The GR-1 Dataset is a collection of teleoperated manipulation trajectories from the Fourier GR-1 humanoid robot, released by NVIDIA as part of the GR00T N1 open foundation model initiative. It contains video recordings of the GR1-T2 robot performing various manipulation tasks in lab environments from third-person perspectives, designed for training generalist humanoid robot policies.

## Format
Trajectory data with RGB video, proprioceptive states (joint positions), and action labels. Available in LeRobot-compatible format on Hugging Face.

## Size
92 videos of Fourier GR1-T2 robot tasks (subset released publicly). Full internal dataset scale undisclosed.

## License
CC-BY 4.0

## How to Download
- Hugging Face: https://huggingface.co/datasets/nvidia/PhysicalAI-Robotics-GR00T-GR1
- GR00T GitHub: https://github.com/NVIDIA/Isaac-GR00T
- Part of NVIDIA's open-source Physical AI dataset collection.

## Papers Using This Dataset
- [[GR00T]] — primary training data for the GR00T N1 humanoid foundation model
- [[Dream Dojo]] — used for robot world model post-training
