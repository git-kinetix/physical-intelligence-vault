---
tags: [dataset]
aliases: [ExORL, Exploratory RL]
category: "reinforcement-learning"
year: 2022
---

# ExoRL

## Description
ExoRL (Exploratory Data for Offline Reinforcement Learning) is an offline RL dataset collected by running 9 unsupervised RL exploration algorithms for 10 million steps each across multiple DeepMind Control Suite domains. It demonstrates that the quality of exploratory data matters more than the offline RL algorithm used, providing a standardized way to study the interplay between exploration and offline learning.

## Format
Offline trajectory datasets for DeepMind Control Suite environments. Each domain has datasets from 9 different exploration algorithms, stored as replay buffers with observations, actions, rewards, and next observations.

## Size
10M environment steps per domain per algorithm (9 algorithms x multiple domains).

## License
MIT (majority of code); Apache 2.0 (DeepMind components)

## How to Download
- GitHub: https://github.com/denisyarats/exorl
- Download script: `./download.sh <DOMAIN> <ALGO>`
- Project page: https://sites.google.com/view/exorl

## Papers Using This Dataset
- [[TD-JEPA]] — used for offline RL evaluation with exploratory data
