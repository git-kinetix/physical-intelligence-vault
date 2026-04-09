---
tags: [dataset]
aliases: [Galaxy10 DECaLS, Galaxy10]
category: "image"
year: 2022
---

# Galaxy10

## Description
Galaxy10 is a galaxy morphology classification dataset inspired by CIFAR-10, containing galaxy images from the DESI Legacy Imaging Surveys (DECaLS) with labels sourced from Galaxy Zoo volunteer classifications. It covers 10 broad morphological classes including spirals, ellipticals, mergers, and edge-on galaxies, serving as a benchmark for applying deep learning to astronomical image classification.

## Format
256x256 pixel color images in HDF5 format (.h5), with integer class labels for 10 galaxy morphology types.

## Size
17,736 galaxy images across 10 classes. Relatively compact dataset suitable for rapid experimentation.

## License
Unknown. Data sourced from DESI Legacy Imaging Surveys with labels from Galaxy Zoo.

## How to Download
Official documentation: https://astronn.readthedocs.io/en/latest/galaxy10.html. GitHub: https://github.com/henrysky/Galaxy10. Also available on Hugging Face: https://huggingface.co/datasets/matthieulel/galaxy10_decals

## Papers Using This Dataset
- [[Le-JEPA]] — used for domain-specific image classification evaluation
