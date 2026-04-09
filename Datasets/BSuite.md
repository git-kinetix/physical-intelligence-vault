---
tags: [dataset]
aliases: [bsuite, Behaviour Suite]
category: "reinforcement-learning"
year: 2019
---

# BSuite

## Description
BSuite (Behaviour Suite for Reinforcement Learning) is a collection of carefully-designed experiments from Google DeepMind that investigate core capabilities of RL agents, including credit assignment, exploration, generalization, memory, and noise robustness. It provides clear, informative, and scalable diagnostic problems for evaluating and comparing learning algorithms.

## Format
Simulated environments following the OpenAI Gym / dm_env interface. Each experiment produces structured evaluation metrics and radar plots for agent comparison.

## Size
23 core experiments, each with multiple difficulty levels (hundreds of configurations total).

## License
Apache 2.0

## How to Download
- GitHub: https://github.com/google-deepmind/bsuite
- Install via pip: `pip install bsuite`
- Documentation: https://deepmind.com/research/open-source/bsuite

## Papers Using This Dataset
- [[DreamerV3]] — used for diagnostic evaluation of world model capabilities
