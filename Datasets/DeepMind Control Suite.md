---
tags: [dataset]
aliases: [DMC, ExoRL / DMC]
category: "reinforcement-learning"
year: 2018
---

# DeepMind Control Suite

## Description
The DeepMind Control Suite (DMC) is a set of continuous control benchmark tasks built on the MuJoCo physics engine, providing standardized environments for reinforcement learning research. It includes locomotion, manipulation, and balancing tasks with varying difficulty levels, serving as the primary evaluation benchmark for model-based and model-free RL algorithms.

## Format
Simulated environment (not a static dataset). Provides observations (proprioceptive states or pixel renders), continuous actions, and rewards via the dm_control Python API.

## Size
30+ task domains with multiple difficulty variants. The DMC Vision Benchmark offline dataset is ~950 GB.

## License
Apache 2.0

## How to Download
- GitHub: https://github.com/google-deepmind/dm_control
- Install via pip: `pip install dm-control`
- DMC Vision Benchmark data: `gcloud storage cp -r gs://dmc_vision_benchmark $DATA_DIR`

## Papers Using This Dataset
- [[DreamerV1]] — primary evaluation benchmark for world model-based RL
- [[DreamerV2]] — primary evaluation benchmark for world model-based RL
- [[DreamerV3]] — primary evaluation benchmark for world model-based RL
- [[TD-JEPA]] — used for continuous control evaluation
