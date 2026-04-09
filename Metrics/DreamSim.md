---
tags: [metric]
aliases: [Dream Similarity, DreamSim Perceptual Similarity]
category: "generation-quality"
higher_is_better: false
---

# DreamSim

## Definition
DreamSim is a learned perceptual similarity metric that combines features from multiple vision foundation models (DINO, CLIP, and OpenCLIP) to measure image similarity in a way that aligns with human perceptual judgments. Unlike LPIPS, which uses features from a single classification network, DreamSim ensembles self-supervised and language-supervised features and is fine-tuned on human similarity judgments from the NIGHTS dataset. This makes it more robust to semantic and structural variations.

## Formula
$$\text{DreamSim}(x, y) = d\left(f_{\text{ens}}(x),\; f_{\text{ens}}(y)\right)$$

where $f_{\text{ens}}$ is an ensemble of LoRA-adapted DINO, CLIP, and OpenCLIP ViT features, and $d$ is a learned distance function. The final score is a weighted combination of per-model cosine distances fine-tuned on human perceptual judgments.

## Interpretation
- DreamSim is a distance metric: lower values indicate images are more perceptually similar.
- It captures both low-level visual similarity and higher-level semantic similarity better than LPIPS.
- Values are typically in the range [0, 1], with values near 0 indicating very similar images.
- Lower is better.

## Common Usage
DreamSim is used as a perceptual quality metric for image generation, reconstruction, and style transfer. It is particularly suited for evaluating world models and video generation systems where both semantic content and visual appearance matter. Its alignment with human judgments makes it a strong complement to LPIPS, PSNR, and SSIM.

## Papers Using This Metric
- [[NVIDIA Cosmos]] — used to evaluate perceptual quality of tokenizer reconstructions and generated content
