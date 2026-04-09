---
tags: [dataset]
aliases: [MineRL, Minecraft Diamond]
category: "reinforcement-learning"
year: 2019
---

# Minecraft

## Description
The Minecraft environment for RL, primarily accessed through the MineRL platform, provides a complex 3D open-world setting for reinforcement learning research. MineRL includes over 60 million automatically annotated state-action pairs of human demonstrations across various Minecraft tasks. The flagship Diamond challenge requires agents to navigate, gather resources, craft tools, and ultimately obtain a diamond -- one of the hardest long-horizon RL challenges.

## Format
Simulated 3D environment. Observations are 64x64 RGB frames with inventory information. Actions include movement, camera control, and crafting commands. Human demonstrations available as paired state-action trajectories.

## Size
60M+ annotated state-action pairs of human demonstrations. The environment itself generates unlimited procedural episodes.

## License
MIT (MineRL package)

## How to Download
- MineRL: https://github.com/minerllabs/minerl
- Install via pip: `pip install minerl`
- Diamond environment: https://github.com/danijar/diamond_env
- Competition page: https://minerl.io/diamond/

## Papers Using This Dataset
- [[DreamerV3]] — first algorithm to collect diamonds in Minecraft from scratch without human data
