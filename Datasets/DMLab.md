---
tags: [dataset]
aliases: [DeepMind Lab, DmLab]
category: "reinforcement-learning"
year: 2016
---

# DMLab

## Description
DeepMind Lab (DMLab) is a customizable 3D learning environment for agent-based AI research, providing challenging navigation and puzzle-solving tasks. Built on a modified Quake III Arena engine, it offers first-person perspective environments for testing deep reinforcement learning agents on spatial reasoning, memory, and exploration.

## Format
Simulated 3D environment. Observations include first-person RGB frames, depth maps, and agent velocity. Actions are continuous movement and discrete look directions.

## Size
30+ predefined levels with configurable difficulty. Source code only (must be built from source with Bazel).

## License
GPL-2.0

## How to Download
- GitHub: https://github.com/google-deepmind/lab
- Build from source: `git clone https://github.com/deepmind/lab && cd lab && bazel build ...`
- Linux x86 only (BUILD files need modification for other platforms).

## Papers Using This Dataset
- [[DreamerV3]] — used for 3D navigation and exploration evaluation
