---
tags: [dataset]
aliases: [OGBench Dataset]
category: "reinforcement-learning"
year: 2024
---

# OGBench

## Description
OGBench is a comprehensive benchmark for offline goal-conditioned reinforcement learning, offline unsupervised RL, and standard offline RL. It features 85 datasets for goal-conditioned tasks and 410 tasks for standard offline RL across 8 diverse environment types: PointMaze, AntMaze, HumanoidMaze, AntSoccer, Cube, Scene, Puzzle, and Powderworld (drawing).

## Format
Offline trajectory datasets with observations, actions, and goals. Pip-installable with Gymnasium-based APIs. JAX-based reference implementations of 6 algorithms included.

## Size
85 goal-conditioned datasets + 410 standard offline RL tasks across 8 environment types. Datasets auto-download on first run.

## License
MIT

## How to Download
- GitHub: https://github.com/seohongpark/ogbench
- Install via pip: `pip install ogbench`
- Datasets auto-download to `~/.ogbench/data` on first run.
- Project page: https://seohong.me/projects/ogbench/

## Papers Using This Dataset
- [[TD-JEPA]] — used for offline goal-conditioned RL evaluation
