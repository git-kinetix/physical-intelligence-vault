---
tags: [dataset]
aliases: [RH20T, Robot-Human 20T]
category: "robotics"
year: 2023
---

# RH20T-Human

## Description
RH20T is a comprehensive robotic dataset for learning diverse manipulation skills in one-shot, containing over 110,000 contact-rich robot manipulation sequences. Each sequence includes visual, force, audio, and action information along with a corresponding human demonstration video, enabling one-shot robot learning through human-robot paired demonstrations across diverse skills and contexts.

## Format
Multimodal trajectory data with RGB video (multiple views), depth, force/torque sensing, audio, and action labels. Both robot execution and paired human demonstration videos.

## Size
110,000+ manipulation sequences. RGB version: ~5 TB; RGBD version: ~10 TB (resized from 40 TB original).

## License
Unknown (publicly available at project website)

## How to Download
- Official website: https://rh20t.github.io/
- Hugging Face: https://huggingface.co/datasets/hainh22/rh20t
- Data split into configuration-specific tar.gz files for incremental download.

## Papers Using This Dataset
- [[GR00T]] — human demonstration subset used for humanoid robot policy pretraining
