---
tags: [dataset]
aliases: [Push-T Benchmark, Push-T Task]
category: "robotics"
year: 2023
---

# Push-T

## Description
Push-T is a robotic manipulation benchmark task introduced alongside the Diffusion Policy paper, where an agent must push a T-shaped block into a target position using a circular end-effector. It serves as a standard evaluation environment for visuomotor policy learning methods, with success measured by the intersection-over-union (IoU) between the final block position and the target.

## Format
Trajectory data with 2D image observations (96x96) and continuous end-effector position actions. Demonstration data stored in Zarr format.

## Size
~200 expert demonstrations (relatively small-scale benchmark dataset).

## License
MIT

## How to Download
- Part of the Diffusion Policy codebase: https://github.com/real-stanford/diffusion_policy
- Demonstration data is downloaded automatically via the training scripts.
- Project page: https://diffusion-policy.cs.columbia.edu/

## Papers Using This Dataset
- [[Le-World-Model]] — used as a manipulation benchmark for world model evaluation
