---
tags: [dataset]
aliases: [SSv2, Something-Something-v2, 20BN-Something-Something V2, SSV2]
category: "video"
year: 2017
---

# Something-Something v2

## Description
Something-Something v2 is a large-scale video dataset of fine-grained hand gestures and object manipulations, originally created by TwentyBN (now Qualcomm AI Research). It requires temporal reasoning to classify actions, as the same object can appear in many different action categories. This makes it a key benchmark for evaluating motion and temporal understanding rather than static appearance bias.

## Format
WebM video files using the VP9 codec, approximately 2-6 seconds per clip. Accompanied by JSON annotation files with action labels.

## Size
220,847 videos total: 168,913 training, 24,777 validation, and 27,157 test videos across 174 action categories. Approximately 19.4 GB compressed download.

## License
Free for academic research. Commercial use requires a separate license from Qualcomm. CC BY-NC-ND 4.0 for academic use.

## How to Download
Available from Qualcomm: https://www.qualcomm.com/developer/software/something-something-v-2-dataset. Also referenced at https://20bn.com/datasets/something-something/v2

## Papers Using This Dataset
- [[V-JEPA]] — used for temporal action recognition evaluation
- [[V-JEPA 2]] — used for temporal action recognition evaluation
- [[V-JEPA 2.1]] — used for temporal action recognition evaluation and as part of VideoMix pre-training data
