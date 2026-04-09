---
tags: [metric]
aliases: [Frechet Video Distance, Fréchet Video Distance]
category: "generation-quality"
higher_is_better: false
---

# FVD

## Definition
Frechet Video Distance (FVD) measures the distributional similarity between generated and real video clips by comparing statistics of features extracted from a pretrained video classification network (typically I3D). It is the video extension of the Frechet Inception Distance (FID) used for images. FVD captures both the quality and temporal coherence of generated videos by operating on spatiotemporal features.

## Formula
$$\text{FVD} = \|\mu_r - \mu_g\|^2 + \text{Tr}\left(\Sigma_r + \Sigma_g - 2(\Sigma_r \Sigma_g)^{1/2}\right)$$

where $(\mu_r, \Sigma_r)$ and $(\mu_g, \Sigma_g)$ are the mean and covariance of the I3D feature distributions for real and generated video sets, respectively.

## Interpretation
- FVD is a distance metric: lower values indicate the generated video distribution is closer to the real video distribution.
- A value of 0 would indicate identical distributions (never achieved in practice).
- Typical FVD values vary widely by dataset and resolution, but state-of-the-art models often achieve FVD in the range of 50--300 on standard benchmarks.
- FVD captures both visual quality and temporal consistency, unlike frame-level metrics.
- Lower is better.

## Common Usage
FVD is the primary distributional quality metric for video generation, video prediction, and world models. It is used to compare the overall quality of generated video distributions against real data, complementing per-frame metrics like PSNR, SSIM, and LPIPS. FVD is standard on benchmarks such as UCF-101, Kinetics, and various robotics video prediction tasks.

## Papers Using This Metric
- [[Learning Latent Action World Models In The Wild]] — used to evaluate the quality of generated video predictions in world model evaluation
