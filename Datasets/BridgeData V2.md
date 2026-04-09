---
tags: [dataset]
aliases: [BridgeV2, Bridge Data V2]
category: "robotics"
year: 2023
---

# BridgeData V2

## Description
BridgeData V2 is a large-scale robot manipulation dataset containing 60,096 trajectories collected across 24 environments on a low-cost WidowX robot arm. It includes 50,365 teleoperated demonstrations and 9,731 scripted rollouts covering 13 manipulation skills, designed for scalable robot learning research.

## Format
Trajectory data consisting of JPEG/PNG images and pickle (pkl) files containing observations, actions, and proprioceptive states.

## Size
60,096 trajectories across 24 environments and 13 skills.

## License
CC-BY 4.0

## How to Download
- Official website: https://rail-berkeley.github.io/bridgedata/
- GitHub: https://github.com/rail-berkeley/bridge_data_v2
- Download raw data as zip files (demos*.zip for demonstrations, scripted*.zip for scripted data).

## Papers Using This Dataset
- [[Learning Latent Action World Models]] — used for learning latent action representations from manipulation data
