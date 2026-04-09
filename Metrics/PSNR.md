---
tags: [metric]
aliases: [Peak Signal-to-Noise Ratio]
category: "generation-quality"
higher_is_better: true
---

# PSNR

## Definition
Peak Signal-to-Noise Ratio (PSNR) measures the ratio between the maximum possible signal power and the power of distortion (noise) affecting the quality of a reconstructed or generated image. It is derived from the Mean Squared Error (MSE) between the original and reconstructed images. PSNR is one of the most widely used pixel-level image quality metrics.

## Formula
$$\text{PSNR} = 10 \cdot \log_{10}\left(\frac{MAX^2}{\text{MSE}}\right) = 20 \cdot \log_{10}\left(\frac{MAX}{\sqrt{\text{MSE}}}\right)$$

where $MAX$ is the maximum possible pixel value (e.g., 255 for 8-bit images) and:

$$\text{MSE} = \frac{1}{N} \sum_{i=1}^{N} (y_i - \hat{y}_i)^2$$

## Interpretation
- PSNR is measured in decibels (dB). Higher values indicate better reconstruction quality.
- Typical ranges: 20--25 dB is considered low quality; 30--40 dB is considered good; above 40 dB is excellent.
- PSNR does not always correlate well with human perceptual quality, as it only measures pixel-level differences.
- Higher is better.

## Common Usage
PSNR is a standard metric for image and video compression, super-resolution, denoising, inpainting, and generation. In world models and video generation, PSNR measures how faithfully generated or reconstructed frames match ground-truth frames at the pixel level. It is almost always reported alongside SSIM and perceptual metrics like LPIPS.

## Papers Using This Metric
- [[Hunyuan World 1.5]] — used to evaluate video generation quality
- [[NVIDIA Cosmos]] — used to evaluate tokenizer reconstruction quality
- [[Learning Latent Action World Models In The Wild]] — used to evaluate video prediction fidelity
