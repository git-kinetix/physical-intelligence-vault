---
tags: [paper, jepa]
title: "Self-Supervised Learning from Images with a Joint-Embedding Predictive Architecture"
authors: [Mahmoud Assran, Quentin Duval, Ishan Misra, Piotr Bojanowski, Pascal Vincent, Michael Rabbat, Yann LeCun, Nicolas Ballas]
year: 2023
arxiv: "https://arxiv.org/abs/2301.08243"
repo: "https://github.com/facebookresearch/ijepa"
group: "JEPA Family"
importance: 
aliases: [I-JEPA, Image JEPA]
---

![[PDFs/I-JEPA.pdf]]


# Self-Supervised Learning from Images with a Joint-Embedding Predictive Architecture

## Summary

I-JEPA (Image-based Joint-Embedding Predictive Architecture) is a non-generative self-supervised learning method for images that predicts representations of target image blocks from a context block in a learned latent space. Proposed by Meta/FAIR, I-JEPA is the foundational instantiation of Yann LeCun's Joint-Embedding Predictive Architecture vision, preceding [[V-JEPA]] (video) and later variants like [[TD-JEPA]] and [[Le-JEPA]].

The core idea is to avoid pixel-level reconstruction (as in MAE) and instead predict abstract feature representations. By using a multi-block masking strategy that samples sufficiently large-scale target blocks and spatially distributed context blocks, I-JEPA learns semantic representations without relying on hand-crafted data augmentations (crops, color jitter, etc.) that methods like DINO and iBOT require. This makes I-JEPA conceptually cleaner and significantly more computationally efficient.

Pretraining a ViT-H/14 on ImageNet with I-JEPA requires fewer than 1,200 GPU hours, which is over 2.5x faster than iBOT with a ViT-S/16 and over 10x more efficient than MAE with a ViT-H/14, while achieving competitive or superior linear probing accuracy. The paper was published at CVPR 2023.

## Key Contributions

- Introduces I-JEPA, the first image-based Joint-Embedding Predictive Architecture, establishing the JEPA paradigm for self-supervised representation learning
- Demonstrates that predicting representations in latent space (rather than pixels) yields strong visual representations without hand-crafted view augmentations
- Proposes a multi-block masking strategy critical for learning semantic (rather than low-level) features from images
- Achieves highly competitive ImageNet linear probing results with dramatically lower computational cost than prior methods
- Shows strong transfer learning performance across diverse downstream tasks (object counting, depth prediction, classification)
- Provides the conceptual and architectural foundation for subsequent JEPA models including [[V-JEPA]] and [[V-JEPA 2]]

## Architecture / Method

I-JEPA uses a Vision Transformer (ViT) encoder-predictor framework within a joint-embedding predictive architecture:

1. **Context Encoder**: A ViT encodes the visible (unmasked) patches of an image into feature representations.
2. **Predictor**: A smaller transformer takes the context encoder's output along with positional embeddings of the masked target regions, and predicts the feature representations of those target patches.
3. **Target Encoder**: An exponential moving average (EMA) of the context encoder provides the target representations for the masked patches.
4. **Multi-Block Masking**: The masking strategy samples multiple target blocks of sufficiently large spatial scale (e.g., large rectangular regions), while using an informative, spatially distributed context block. This encourages the model to learn high-level semantic features rather than local textures.

The training loss is an L2 regression loss between the predictor output and the EMA target encoder representation:

$$\mathcal{L} = \| f_\theta(\text{context}) - \text{sg}(f_{\bar{\theta}}(\text{target})) \|^2$$

Key design choices:
- **No hand-crafted augmentations**: Unlike contrastive methods (DINO, iBOT), I-JEPA does not use crops, color jitter, or other view augmentations
- **Prediction in representation space**: Avoids pixel-level reconstruction, focusing on abstract semantic prediction
- **Asymmetric architecture**: The predictor is a lightweight transformer, keeping computational cost low

## Results

### Table 1: [[ImageNet-1K]] Linear Probing ([[Top-1 Accuracy]])

| Method | Architecture | Epochs | [[Top-1 Accuracy]]. |
|--------|-------------|--------|------------|
| **I-JEPA** | ViT-B/16 | 600 | 72.9% |
| **I-JEPA** | ViT-L/16 | 600 | 77.5% |
| **I-JEPA** | ViT-H/14 | 300 | 79.3% |
| **I-JEPA** | ViT-H/16 (448) | 300 | 81.1% |
| MAE | ViT-B/16 | 1600 | 68.0% |
| MAE | ViT-L/16 | 1600 | 76.0% |
| MAE | ViT-H/14 | 1600 | 77.2% |
| data2vec | ViT-L/16 | 1600 | 77.3% |
| iBOT | ViT-L/16 | 250 | 81.0% |
| DINO | ViT-B/8 | 300 | 80.1% |

I-JEPA ViT-H/14 achieves 79.3% with only 300 epochs, outperforming MAE ViT-H/14 (77.2% at 1600 epochs) with over 10x less compute.

### Table 2: Low-Shot [[ImageNet-1K]] (1% Labels, [[Top-1 Accuracy]])

| Method | Architecture | Epochs | [[Top-1 Accuracy]]. |
|--------|-------------|--------|------------|
| **I-JEPA** | ViT-L/16 | 600 | 69.4% |
| **I-JEPA** | ViT-H/14 | 300 | 73.3% |
| **I-JEPA** | ViT-H/16 (448) | 300 | 77.3% |
| MAE | ViT-L/16 | 1600 | 67.1% |
| MAE | ViT-H/14 | 1600 | 71.5% |
| data2vec | ViT-L/16 | 1600 | 73.3% |
| MSN | ViT-B/4 | 300 | 75.7% |

### Table 3: Transfer Learning ([[Linear Probe Accuracy|Linear Probe]], [[Top-1 Accuracy]])

| Method | Architecture | [[CIFAR-100]] | [[Places205]] | iNat18 |
|--------|-------------|-----------|-----------|--------|
| **I-JEPA** | ViT-H/14 | 87.5% | 58.4% | 47.6% |
| MAE | ViT-H/14 | 77.3% | 55.0% | 32.9% |
| data2vec | ViT-L/16 | 81.6% | 54.6% | 28.1% |
| iBOT | ViT-L/16 | 88.3% | 60.4% | 57.3% |
| DINO | ViT-B/8 | 84.9% | 57.9% | 55.9% |

I-JEPA substantially outperforms MAE on all transfer benchmarks. iBOT and DINO achieve higher scores on iNat18, but they rely on hand-crafted augmentations and are significantly more expensive to train.

## Metrics Used

- [[Top-1 Accuracy]] -- ImageNet linear probing and low-shot evaluation
- [[GPU Hours]] -- computational efficiency comparison (I-JEPA ViT-H/14: <1,200 GPU hours)
- [[Transfer Learning Accuracy]] -- linear probe on [[CIFAR-100]], [[Places205]], iNat18

## Datasets Used

- [[ImageNet-1K]] -- pretraining and linear evaluation
- [[CIFAR-100]] -- transfer learning evaluation
- [[Places205]] -- transfer learning evaluation
- [[iNaturalist 2018]] -- transfer learning evaluation

## Related Papers

- [[V-JEPA]] -- extends I-JEPA's feature prediction paradigm to video, using spatiotemporal masking
- [[V-JEPA 2]] -- scaled successor to [[V-JEPA]] with improved video understanding
- [[TD-JEPA]] -- temporal difference variant of JEPA
- [[Le-JEPA]] -- further extension of the JEPA framework
- [[Le-World-Model]] -- world model building on JEPA representations
