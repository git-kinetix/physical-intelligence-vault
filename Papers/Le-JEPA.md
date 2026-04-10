---
tags: [paper, jepa, motion]
title: "LeJEPA: Provable and Scalable Self-Supervised Learning Without the Heuristics"
authors: [Randall Balestriero, Yann LeCun]
year: 2025
arxiv: "https://arxiv.org/abs/2511.08544"
repo: "https://github.com/galilai-group/lejepa"
group: "JEPA Family"
importance: 
aliases: [LeJEPA, Le-JEPA]
---

!PDFs/Le-JEPA.pdf


# LeJEPA: Provable and Scalable Self-Supervised Learning Without the Heuristics

## Summary

LeJEPA provides the first comprehensive theoretical framework for Joint-Embedding Predictive Architectures, identifying the isotropic Gaussian distribution as the optimal target distribution for JEPA embeddings and introducing a novel regularizer called Sketched Isotropic Gaussian Regularization (SIGReg) to enforce this distribution. The resulting method, LeJEPA, combines the standard JEPA predictive loss with SIGReg, eliminating common heuristics that plague existing self-supervised methods -- including stop-gradient operations, teacher-student (EMA) mechanisms, and complex hyperparameter schedulers.

LeJEPA is remarkably simple (approximately 50 lines of code for distributed training), requires only a single trade-off hyperparameter, and has linear time and memory complexity. Despite this simplicity, it achieves 79% top-1 accuracy on [[ImageNet-1K]] with a ViT-H/14 using frozen backbone linear evaluation. The method is validated across 10+ datasets and 60+ architectures spanning ViTs, ConvNeXts, ResNets, MaxViTs, and Swin Transformers, demonstrating exceptional stability and architecture-agnostic performance. A key practical benefit is that the training loss correlates strongly with downstream linear probe performance, enabling model selection without supervised probing.

## Key Contributions

- Identifies the isotropic Gaussian as the optimal target distribution for JEPA embeddings (theoretical result)
- Introduces SIGReg (Sketched Isotropic Gaussian Regularization), a principled regularizer with linear time/memory complexity
- Eliminates the need for stop-gradient, EMA teacher-student, and hyperparameter schedulers
- Achieves competitive self-supervised performance with a single hyperparameter and ~50 lines of code
- Validates across 60+ architectures (ViTs, ConvNeXts, ResNets, MaxViTs, Swin) and 10+ datasets
- Demonstrates stable training even on 1.8B parameter ViT-g models without heuristics
- Shows training loss correlates with downstream performance, enabling unsupervised model selection
- Provides theoretical guarantees against representation collapse

## Architecture / Method

LeJEPA combines two components:

**1. JEPA Predictive Loss:**
Given a context view $x$ and target view $y$ from an augmented image, the encoder produces representations $z_x = f_\theta(x)$ and $z_y = f_\theta(y)$. A predictor $g_\phi$ maps the context representation to predict the target:

$$\mathcal{L}_{\text{pred}} = \| g_\phi(z_x) - z_y \|^2$$

Unlike standard JEPA methods, there is no stop-gradient on the target and no EMA teacher -- both branches use the same encoder with shared weights.

**2. SIGReg (Sketched Isotropic Gaussian Regularization):**
SIGReg constrains the embedding distribution to be an isotropic Gaussian $\mathcal{N}(0, I)$ by matching the characteristic function of the embedding distribution to that of the Gaussian:

$$\mathcal{L}_{\text{SIGReg}} = \sum_{k=1}^{K} \left| \hat{\varphi}(\omega_k) - \exp(-\|\omega_k\|^2/2) \right|^2$$

where $\hat{\varphi}(\omega_k) = \frac{1}{B}\sum_{i=1}^{B} \exp(j \omega_k^\top z_i)$ is the empirical characteristic function evaluated at random frequency slices $\omega_k$, and $\exp(-\|\omega_k\|^2/2)$ is the characteristic function of $\mathcal{N}(0,I)$.

**Total Loss:**
$$\mathcal{L} = \mathcal{L}_{\text{pred}} + \lambda \cdot \mathcal{L}_{\text{SIGReg}}$$

where $\lambda$ is the single trade-off hyperparameter.

**Key design properties:**
- Linear time and memory in batch size and embedding dimension (unlike VICReg's quadratic covariance)
- Number of frequency slices controls the approximation quality (default: 2048-4096)
- Integration range [-3, 3] or [-5, 5] works well across settings
- Multi-view strategy with 2+ global views and optional local views

## Results

### Table 1a: SIGReg Hyperparameter [[Recall|Sensitivity]] — Integration Range and Frequency Slices (ViT-L/14, [[ImageNet-1K]], 100 epochs)

| Integration Range | num_slices | 5 points | 17 points | 41 points |
|-------------------|-----------|----------|-----------|-----------|
| [-1, 1] | 512 | 71.82 | 72.13 | 72.04 |
| [-1, 1] | 2048 | 72.88 | 72.30 | 72.69 |
| [-3, 3] | 512 | 73.95 | 74.16 | 74.04 |
| [-3, 3] | 2048 | 75.02 | 74.68 | 74.77 |
| [-5, 5] | 512 | 73.71 | 74.21 | 74.15 |
| [-5, 5] | 2048 | 74.50 | 74.80 | 74.77 |

Performance is robust across integration ranges and number of points. [-3, 3] with 2048 slices achieves the best result (75.02%). The wider range [-5, 5] is slightly worse, likely due to higher variance in the characteristic function estimates.

### Table 1b: View Configuration (ViT-L/14, [[ImageNet-1K]])

| Global Views (Vg) | V=2 Total | V=6 Total | V=8 Total | V=10 Total |
|--------------------|-----------|-----------|-----------|------------|
| 1 | 53.06 | 58.65 | 64.46 | 68.97 |
| 2 | 72.26 | 73.07 | 73.68 | — |
| 4 | — | 73.68 | 73.94 | 75.08 |

Two global views are essential (53.06% with 1 global view vs. 72.26% with 2). Additional local views provide marginal gains; 4 global + 6 local views (V=10) yields the best result at 75.08%.

### Table 1c: Batch Size [[Recall|Sensitivity]] (ViT-L/14, [[ImageNet-1K]])

| Batch Size | 128 | 256 | 512 | 1024 |
|-----------|-----|-----|-----|------|
| Accuracy | 72.20 | 74.15 | 74.72 | 74.07 |

Performance is relatively robust to batch size, peaking at 512. Unlike contrastive methods, LeJEPA does not require very large batch sizes.

### Table 1d: Embedding and Projector Dimensions (ViT-L/14, [[ImageNet-1K]])

| Proj Dim | Emb 512 / Slices 1024 | Emb 512 / Slices 4096 | Emb 2048 / Slices 1024 | Emb 2048 / Slices 4096 |
|----------|----------------------|----------------------|------------------------|------------------------|
| 64 | 75.29 | 75.32 | 75.50 | 75.65 |
| 128 | 74.77 | 75.09 | 75.26 | 75.47 |
| 256 | 74.56 | 74.66 | 75.08 | 75.02 |
| 512 | 73.94 | 74.11 | 74.81 | 74.65 |
| 1024 | 73.65 | 73.94 | 74.71 | 74.79 |

Smaller projector dimensions (64) consistently outperform larger ones. Higher embedding dimensions (2048) and more slices (4096) provide marginal improvements. Best result: 75.65% with Emb=2048, Slices=4096, Proj=64.

### Table 1e: Register Tokens (ViT-L/14, [[ImageNet-1K]])

| Register Tokens | 0 | 1 | 2 | 4 | 8 |
|----------------|---|---|---|---|---|
| num_slices 1024 | 75.14 | 75.18 | 75.08 | 75.34 | 75.23 |
| num_slices 4096 | 75.61 | 75.58 | 75.67 | 75.63 | 75.84 |

Register tokens provide small but consistent improvements. The best result (75.84%) uses 8 register tokens with 4096 slices. Performance is robust to the number of registers.

### Table 2: [[Galaxy10]] In-Domain Results (Domain-Specific Pretraining)

| Method | Setting | 1-shot | Full |
|--------|---------|--------|------|
| DINOv2 ViT-S/16 (transfer) | Frozen | 21.05 | 78.34 |
| DINOv3 ViT-S/16 (transfer) | Frozen | 24.71 | 81.60 |
| LeJEPA ConvNeXt-V2 Nano (in-domain) | Frozen | 28.74 | 76.52 |
| LeJEPA ResNet-34 (in-domain) | Frozen | 31.08 | 78.17 |
| LeJEPA ConvNeXt-V2 Nano (in-domain) | Full FT | 29.42 | 82.72 |
| LeJEPA ResNet-34 (in-domain) | Full FT | 24.27 | 83.28 |

LeJEPA with in-domain pretraining on [[Galaxy10]] outperforms transfer learning from DINOv2/DINOv3 frontier models, especially on 1-shot evaluation (31.08% vs. 24.71%) and full fine-tuning (83.28% vs. 81.60%). This demonstrates LeJEPA's value for domain-specific self-supervised learning with small architectures.

### Key Headline Results

| Model | Dataset | Metric | Score |
|-------|---------|--------|-------|
| ViT-H/14 | [[ImageNet-1K]] | [[Linear Probe Accuracy]] (frozen) | 79.0% |
| ViT-L/14 | [[ImageNet-1K]] | [[Linear Probe Accuracy]] (100 ep) | ~75% |
| 50 timm models | ImageNet-10 | [[Linear Probe Accuracy]] (frozen) | 91.5–95.0% |
| ViT-g (1.8B) | — | Training stability | Stable (no divergence) |

LeJEPA achieves 79% linear probe accuracy on [[ImageNet-1K]] with ViT-H/14, competitive with methods that use far more complex training pipelines. Across 50 diverse architectures from the timm library, ImageNet-10 accuracy ranges from 91.5% to 95.0%, demonstrating exceptional architecture-agnostic stability.

## Metrics Used

- [[Linear Probe Accuracy]] — primary metric; frozen backbone with a linear classifier on top
- [[Top-1 Accuracy]] — classification accuracy on [[ImageNet-1K]], ImageNet-100, ImageNet-10, [[Galaxy10]], [[Food101]], [[CIFAR-10]], [[CIFAR-100]]
- [[k-NN Accuracy]] — k-nearest-neighbor evaluation of representation quality
- [[1-shot Accuracy]] — few-shot classification with a single example per class
- Training Loss Correlation — correlation between training loss and downstream linear probe accuracy (practical model selection metric)

## Datasets Used

- [[ImageNet-1K]] — primary benchmark for self-supervised representation learning (1.28M images, 1000 classes)
- ImageNet-100 — 100-class subset of ImageNet for ablation studies
- ImageNet-10 — 10-class subset used for architecture sweep across 50+ models
- [[Galaxy10]] — astronomy dataset for domain-specific pretraining evaluation
- [[Food101]] — food image classification dataset
- [[CIFAR-10]] — small-scale image classification (10 classes)
- [[CIFAR-100]] — small-scale image classification (100 classes)

## Related Papers

- [[I-JEPA]] — the original image JEPA that LeJEPA theoretically grounds and simplifies
- [[V-JEPA]] — video extension of JEPA; could benefit from LeJEPA's SIGReg regularizer
- VICReg — variance-invariance-covariance regularization; SIGReg provides a more principled and efficient alternative
- Barlow Twins — redundancy-reduction SSL method; LeJEPA eliminates the need for covariance computation
- DINOv2 — state-of-the-art image SSL baseline; LeJEPA is competitive with far simpler training
- [[LeWorldModel]] — sister paper applying LeJEPA's SIGReg to world models from pixels
- SimCLR — contrastive learning baseline; LeJEPA avoids the need for negative examples
