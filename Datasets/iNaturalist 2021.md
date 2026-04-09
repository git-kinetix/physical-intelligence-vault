---
tags: [dataset]
aliases: [iNat2021, iNaturalist-2021, iNat 2021]
category: "image"
year: 2021
---

# iNaturalist 2021

## Description
iNaturalist 2021 is a large-scale fine-grained species classification dataset featuring community-curated, research-grade images from the iNaturalist citizen science platform. It covers 10,000 species with rich taxonomic metadata, presenting a long-tailed distribution challenge where some species have many more images than others. Annotations are 85-95% accurate through community verification.

## Format
JPEG images of variable resolution depicting plants, animals, fungi, and other organisms in natural settings. Accompanied by JSON annotation files with species labels and taxonomic hierarchy.

## Size
Approximately 2.7 million training images across 10,000 species, 100K validation images (10 per species), and 500K test images. A "mini" split of 500K images (50 per species) is also provided.

## License
Creative Commons Attribution 4.0 (CC BY 4.0).

## How to Download
Competition page with download links: https://github.com/visipedia/inat_comp/tree/master/2021. Also available via TensorFlow Datasets and torchvision.

## Papers Using This Dataset
- [[V-JEPA]] — used for fine-grained classification evaluation
