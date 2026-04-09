---
tags: [metric]
aliases: [Learned Perceptual Image Patch Similarity, Perceptual Loss]
category: "generation-quality"
higher_is_better: false
---

# LPIPS

## Definition
Learned Perceptual Image Patch Similarity (LPIPS) measures the perceptual distance between two images using deep features extracted from a pretrained neural network (typically AlexNet, VGG, or SqueezeNet). Unlike PSNR and SSIM, LPIPS is learned from human perceptual judgments and correlates significantly better with how humans perceive image similarity. It computes the weighted L2 distance between feature activations at multiple layers.

## Formula
$$\text{LPIPS}(x, y) = \sum_{l} \frac{1}{H_l W_l} \sum_{h,w} \| w_l \odot (\hat{\phi}_l^x(h,w) - \hat{\phi}_l^y(h,w)) \|_2^2$$

where $\hat{\phi}_l^x$ and $\hat{\phi}_l^y$ are the unit-normalized feature activations at layer $l$ for images $x$ and $y$, $w_l$ are learned per-channel weights, and $H_l, W_l$ are the spatial dimensions at layer $l$.

## Interpretation
- LPIPS is a distance metric: lower values indicate more perceptually similar images.
- A value of 0 indicates perceptually identical images.
- Typical values range from 0.0 to 1.0, with values below 0.1 indicating very high perceptual similarity.
- Lower is better.

## Common Usage
LPIPS is the standard learned perceptual metric for evaluating image and video generation, reconstruction, super-resolution, and style transfer. It is preferred over PSNR/SSIM when perceptual fidelity matters more than pixel-level accuracy. In world model evaluation, LPIPS captures whether generated frames "look right" to a human observer, even if individual pixels differ.

## Papers Using This Metric
- [[Hunyuan World 1.5]] — used to evaluate perceptual quality of generated video frames
- [[NVIDIA Cosmos]] — used to evaluate tokenizer reconstruction perceptual quality
- [[Learning Latent Action World Models In The Wild]] — used to evaluate perceptual fidelity of video predictions
