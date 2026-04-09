---
tags: [metric]
aliases: [Reconstruction FVD, Reconstruction Frechet Video Distance]
category: "generation-quality"
higher_is_better: false
---

# rFVD

## Definition
Reconstruction FVD (rFVD) is a variant of Frechet Video Distance computed specifically on videos that have been encoded and then decoded (reconstructed) by a video tokenizer. Rather than measuring the quality of generated content, rFVD measures how much information is lost during the tokenization process by comparing the distribution of reconstructed videos against the original videos. It isolates tokenizer quality from generation model quality.

## Formula
$$\text{rFVD} = \|\mu_{\text{orig}} - \mu_{\text{recon}}\|^2 + \text{Tr}\left(\Sigma_{\text{orig}} + \Sigma_{\text{recon}} - 2(\Sigma_{\text{orig}} \Sigma_{\text{recon}})^{1/2}\right)$$

where $(\mu_{\text{orig}}, \Sigma_{\text{orig}})$ and $(\mu_{\text{recon}}, \Sigma_{\text{recon}})$ are the mean and covariance of I3D features extracted from original and reconstructed video sets, respectively.

## Interpretation
- Lower rFVD indicates the tokenizer preserves more of the original video distribution during encode-decode.
- A value of 0 would indicate lossless tokenization (never achieved with lossy compression).
- rFVD is essential for evaluating tokenizers independently of the downstream generation model.
- Lower is better.

## Common Usage
rFVD is used to evaluate video tokenizers (autoencoders, VQ-VAEs, continuous VAEs) for world models and video generation pipelines. It provides a distributional measure of reconstruction fidelity that complements per-frame metrics like rPSNR and rSSIM. It is particularly important when comparing tokenizer architectures for video generation systems.

## Papers Using This Metric
- [[NVIDIA Cosmos]] — used to evaluate the Cosmos video tokenizer reconstruction quality
