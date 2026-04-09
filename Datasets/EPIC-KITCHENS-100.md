---
tags: [dataset]
aliases: [EPIC-KITCHENS, Epic-Kitchens]
category: "egocentric"
year: 2021
---

# EPIC-KITCHENS-100

## Description
EPIC-KITCHENS-100 is the largest egocentric kitchen activity dataset, containing 100 hours of unscripted cooking activities across 45 kitchens captured with head-mounted cameras. It features 20 million frames, 90,000 action segments in 700 variable-length videos with dense annotations for action recognition, detection, anticipation, and retrieval tasks.

## Format
Egocentric video (RGB frames and optical flow) with temporal action annotations including verb-noun pairs, narrations, and segment boundaries.

## Size
100 hours, 20M frames, 90K action annotations, 700 videos, 45 kitchens. ~1+ TB download with all modalities.

## License
CC-BY-NC 4.0

## How to Download
- Official website: https://epic-kitchens.github.io/
- Annotations: https://github.com/epic-kitchens/epic-kitchens-100-annotations
- Download scripts provided for videos, RGB frames, and flow frames.

## Papers Using This Dataset
- [[V-JEPA 2]] — used for egocentric action anticipation evaluation
- [[V-JEPA 2.1]] — used for egocentric video understanding
- [[GR00T]] — used for kitchen activity pretraining
- [[Dream Dojo]] — used as source of egocentric manipulation data
