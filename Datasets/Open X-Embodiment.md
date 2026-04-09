---
tags: [dataset]
aliases: [Open-X Embodiment, OXE]
category: "robotics"
year: 2023
---

# Open X-Embodiment

## Description
Open X-Embodiment is Google DeepMind's large-scale robot learning dataset that integrates data from 21 institutions across 22 robot platforms (manipulators, bimanual arms, quadrupeds) and 60+ pre-existing datasets. It encompasses 527 distinct manipulation skills and over 1 million demonstration trajectories, serving as a unified resource for cross-embodiment robot learning research.

## Format
Trajectory data stored in RLDS (Reinforcement Learning Datasets) format via TensorFlow Datasets, including observations (images, proprioception), actions, and rewards.

## Size
1M+ real robot trajectories spanning 22 robot embodiments.

## License
Apache 2.0 for software; CC-BY 4.0 for data and other materials. Some subsets have non-commercial restrictions per original contributor terms.

## How to Download
- Official project website: https://robotics-transformer-x.github.io/
- GitHub: https://github.com/google-deepmind/open_x_embodiment
- Also available on Hugging Face: https://huggingface.co/datasets/jxu124/OpenX-Embodiment

## Papers Using This Dataset
- [[V-JEPA 2.1]] — used for cross-embodiment robot pretraining
- [[GR00T]] — used for humanoid robot foundation model training
- [[Pi0]] — used for generalist robot policy pretraining
- [[Pi0.5]] — used for generalist robot policy pretraining
