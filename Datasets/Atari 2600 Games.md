---
tags: [dataset]
aliases: [Atari 100K, ALE]
category: "reinforcement-learning"
year: 2013
---

# Atari 2600 Games

## Description
The Arcade Learning Environment (ALE) provides a standardized interface to hundreds of Atari 2600 game environments for reinforcement learning research. It enables automatic extraction of game scores and end-of-game signals across 100+ games, serving as the most widely-used discrete-action RL benchmark. The Atari 100K variant restricts agents to 100K environment steps (roughly 2 hours of real-time play) to evaluate sample efficiency.

## Format
Simulated environment. Observations are 210x160 RGB frames (typically downsampled to 84x84 grayscale), with 18 discrete actions (joystick + button combinations). Frame-skip of 4 is standard.

## Size
57 standard benchmark games; 100+ total games available.

## License
GPL-2.0

## How to Download
- GitHub (Farama Foundation): https://github.com/Farama-Foundation/Arcade-Learning-Environment
- Install via pip: `pip install ale-py`
- Documentation: https://ale.farama.org/

## Papers Using This Dataset
- [[DreamerV2]] — evaluated on Atari 100K sample-efficiency benchmark
- [[DreamerV3]] — evaluated across 57 Atari games
