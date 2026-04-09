---
tags: [dataset]
aliases: [YT-Temporal-1B, YTTemporal1B]
category: "video"
year: 2022
---

# YouTube-Temporal-1B

## Description
YouTube-Temporal-1B (YT-Temporal-1B) is a massive-scale video dataset consisting of approximately 20 million YouTube videos spanning over 1 billion frames. It was originally curated for training MERLOT Reserve, a multi-modal model handling video, audio, and text. The dataset provides temporally dense video data at scale for self-supervised video representation learning.

## Format
YouTube video IDs with temporal metadata. Videos must be downloaded from YouTube using the provided IDs. Originally hosted on Google Cloud Storage.

## Size
Approximately 20 million videos with over 1 billion frames total.

## License
Unknown. The original Google Cloud Storage bucket has been shut down. Video IDs were publicly released.

## How to Download
Video IDs were released at gs://merlot/yttemporal1b/ (now unavailable). The dataset is referenced at https://rowanzellers.com/merlotreserve/. A subset is available on Hugging Face: https://huggingface.co/datasets/HuggingFaceM4/yttemporal180m. See also: https://opendatalab.com/OpenDataLab/YT-Temporal-1B

## Papers Using This Dataset
- [[V-JEPA 2.1]] — curated subset used as part of VideoMix22M pre-training data
- [[NVIDIA Cosmos]] — used as a video data source
