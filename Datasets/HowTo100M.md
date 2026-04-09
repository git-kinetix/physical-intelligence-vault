---
tags: [dataset]
aliases: [HowTo100M, HT100M]
category: "video"
year: 2019
---

# HowTo100M

## Description
HowTo100M is a large-scale dataset of narrated instructional videos sourced from YouTube, where content creators explain visual content on screen. It was designed for learning text-video embeddings from naturally occurring narration, covering 23,000 activities across domains such as cooking, crafting, personal care, gardening, and fitness.

## Format
YouTube video clips paired with automatically extracted narration captions (via ASR). Provided as video IDs and timestamps with associated text; actual videos must be downloaded from YouTube.

## Size
136 million video clips from 1.2 million YouTube videos, totaling approximately 15 years of video. Requires approximately 12 TB of storage for all video files.

## License
Unknown. Access requires filling out a form to receive credentials for downloading.

## How to Download
Official page: https://www.di.ens.fr/willow/research/howto100m/. Requires registration to obtain download credentials. Also referenced on Hugging Face: https://huggingface.co/datasets/HuggingFaceM4/howto100m

## Papers Using This Dataset
- [[V-JEPA 2]] — used as part of pre-training video data
- [[V-JEPA 2.1]] — used as part of VideoMix22M pre-training data mixture
