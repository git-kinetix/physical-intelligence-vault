---
tags: [dataset]
aliases: [Crafter Benchmark]
category: "reinforcement-learning"
year: 2021
---

# Crafter

## Description
Crafter is a procedurally generated 2D survival game benchmark that tests a broad spectrum of agent capabilities including exploration, resource gathering, tool crafting, combat, and long-horizon planning. Each episode generates a new randomized open world where the agent must forage, build shelter, defend against monsters, and craft progressively advanced tools, all from image observations.

## Format
Simulated environment following the OpenAI Gym interface. Observations are 64x64x3 RGB images; action space is 17 categorical actions. Evaluates 22 achievement milestones.

## Size
Single environment with procedurally generated episodes (no static dataset). 22 tracked achievements serve as the evaluation metric.

## License
MIT

## How to Download
- GitHub: https://github.com/danijar/crafter
- Install via pip: `pip install crafter`
- Project page: https://danijar.com/project/crafter/

## Papers Using This Dataset
- [[DreamerV3]] — used as a challenging open-ended exploration benchmark
