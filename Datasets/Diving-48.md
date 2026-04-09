---
tags: [dataset]
aliases: [Diving48, Diving-48]
category: "video"
year: 2018
---

# Diving-48

## Description
Diving-48 is a fine-grained video dataset of competitive diving, containing trimmed clips of 48 unambiguous dive sequences standardized by FINA (International Swimming Federation). Each dive class is defined by four attributes (takeoff, somersaults, twists, and dive position), making it a strong test of temporal reasoning since static frames alone are insufficient to distinguish dive types.

## Format
Video clips of competitive diving sequences with action class labels. Can be processed into RGB frames or optical flow.

## Size
Approximately 18,000 trimmed video clips across 48 dive classes (~15K training, ~2K test).

## License
Unknown. The dataset is publicly available for research purposes.

## How to Download
Official website: http://www.svcl.ucsd.edu/projects/resound/dataset.html. Also available via OpenDataLab: https://opendatalab.com/OpenDataLab/diving48/download. MMAction2 supports automated download: https://mmaction2.readthedocs.io/en/stable/dataset_zoo/diving48.html

## Papers Using This Dataset
- [[V-JEPA]] — used for fine-grained temporal action recognition evaluation
