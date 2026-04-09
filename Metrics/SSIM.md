---
tags: [metric]
aliases: [Structural Similarity Index, Structural Similarity Index Measure]
category: "generation-quality"
higher_is_better: true
---

# SSIM

## Definition
The Structural Similarity Index Measure (SSIM) assesses image quality by comparing luminance, contrast, and structural information between a reference image and a distorted/generated image. Unlike PSNR, SSIM is designed to model perceived changes in structural information, making it better aligned with human visual perception. It operates on local image patches and combines three comparison functions.

## Formula
$$\text{SSIM}(x, y) = \frac{(2\mu_x \mu_y + C_1)(2\sigma_{xy} + C_2)}{(\mu_x^2 + \mu_y^2 + C_1)(\sigma_x^2 + \sigma_y^2 + C_2)}$$

where $\mu_x, \mu_y$ are the mean intensities, $\sigma_x^2, \sigma_y^2$ are the variances, $\sigma_{xy}$ is the covariance, and $C_1, C_2$ are small constants for numerical stability (typically $C_1 = (k_1 L)^2$, $C_2 = (k_2 L)^2$ with $L$ the dynamic range).

## Interpretation
- SSIM ranges from -1 to 1, where 1 indicates identical images.
- In practice, values are typically between 0 and 1, with values above 0.9 indicating high structural similarity.
- SSIM captures perceptual quality better than PSNR, especially for blur, compression, and noise artifacts.
- Higher is better.

## Common Usage
SSIM is a standard metric for image and video quality assessment, used alongside PSNR in compression, super-resolution, denoising, generation, and reconstruction tasks. In world models and video generation, SSIM measures how well generated frames preserve the structural content of ground-truth frames.

## Papers Using This Metric
- [[Hunyuan World 1.5]] — used to evaluate video generation quality
- [[NVIDIA Cosmos]] — used to evaluate tokenizer reconstruction quality
- [[Learning Latent Action World Models In The Wild]] — used to evaluate video prediction fidelity
