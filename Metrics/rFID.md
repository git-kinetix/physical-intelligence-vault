---
tags: [metric]
aliases: [Reconstruction FID, Reconstruction Frechet Inception Distance]
category: "generation-quality"
higher_is_better: false
---

# rFID

## Definition
Reconstruction FID (rFID) is a variant of Frechet Inception Distance computed on images that have been encoded and then decoded (reconstructed) by a tokenizer or autoencoder. It measures the distributional distance between original and reconstructed image sets using Inception network features. Like rFVD for video, rFID isolates the quality loss introduced by the tokenizer from the downstream generation model.

## Formula
$$\text{rFID} = \|\mu_{\text{orig}} - \mu_{\text{recon}}\|^2 + \text{Tr}\left(\Sigma_{\text{orig}} + \Sigma_{\text{recon}} - 2(\Sigma_{\text{orig}} \Sigma_{\text{recon}})^{1/2}\right)$$

where $(\mu_{\text{orig}}, \Sigma_{\text{orig}})$ and $(\mu_{\text{recon}}, \Sigma_{\text{recon}})$ are the mean and covariance of Inception-v3 features extracted from original and reconstructed image sets, respectively.

## Interpretation
- Lower rFID indicates the tokenizer better preserves the statistical properties of original images during encode-decode.
- A value of 0 would indicate perfect reconstruction at the distributional level.
- rFID is typically lower than generation FID, since reconstruction is an easier task than generation from scratch.
- Lower is better.

## Common Usage
rFID is used to evaluate image and video tokenizers (VQ-VAEs, autoencoders) that serve as the compression backbone for generation models. By measuring reconstruction fidelity at the distributional level, it captures perceptual quality degradation that per-pixel metrics might miss. It is commonly reported alongside rFVD, PSNR, and SSIM for tokenizer evaluation.

## Papers Using This Metric
- [[NVIDIA Cosmos]] — used to evaluate the Cosmos image/video tokenizer reconstruction quality
