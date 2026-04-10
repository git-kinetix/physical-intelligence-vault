---
tags: [paper, jepa, motion]
title: "Revisiting Feature Prediction for Learning Visual Representations from Video"
authors: [Adrien Bardes, Quentin Garrido, Jean Ponce, Xinlei Chen, Michael Rabbat, Yann LeCun, Mahmoud Assran, Nicolas Ballas]
year: 2024
arxiv: "https://arxiv.org/abs/2404.08471"
repo: "https://github.com/facebookresearch/jepa"
group: "JEPA Family"
importance: 
aliases: [V-JEPA, Video JEPA]
---

!PDFs/V-JEPA.pdf


# Revisiting Feature Prediction for Learning Visual Representations from Video

## Summary

V-JEPA (Video Joint-Embedding Predictive Architecture) is a self-supervised method for learning visual representations from video by predicting features in a latent space rather than reconstructing raw pixels. The approach is trained solely through a feature prediction objective applied to video data, without relying on pretrained image encoders, text supervision, negative examples, human annotations, or pixel-level reconstruction. Models are pretrained on [[VideoMix2M]], a dataset of 2 million videos collected from public datasets.

The key insight is that predicting in representation space (rather than pixel space) leads to versatile visual representations that perform well on both motion-based and appearance-based tasks without adapting the model's parameters (i.e., using a frozen backbone). V-JEPA demonstrates that feature prediction from video alone can match or exceed methods that rely on pixel reconstruction, image-text supervision, or significantly more data and parameters. The largest V-JEPA model (ViT-H/16) achieves 81.9% on [[Kinetics-400]], 72.2% on [[Something-Something v2|Something-Something-v2]], and 77.4% on [[ImageNet-1K]] under frozen evaluation with an attentive probe.

## Key Contributions

- Introduces V-JEPA, a self-supervised video representation learning method based purely on feature prediction in latent space
- Demonstrates that feature prediction outperforms pixel prediction for video representation learning
- Shows that a single video-pretrained model can perform well on both motion-heavy ([[Something-Something v2|SSv2]]) and appearance-heavy (ImageNet) tasks using a frozen backbone
- Achieves strong label efficiency, outperforming prior methods in low-shot evaluation settings (5%, 10%, 50% labels)
- Introduces the [[VideoMix2M]] pretraining dataset combining [[Kinetics-710]], [[HowTo100M]], and [[Something-Something v2|SSv2]]
- Provides a comprehensive ablation study on masking strategies, pooling, and data distribution

## Architecture / Method

V-JEPA uses a Vision Transformer (ViT) encoder-predictor architecture within a Joint-Embedding Predictive Architecture framework. The method operates as follows:

1. **Context Encoder**: A ViT encodes the visible (unmasked) patches of a video clip into feature representations.
2. **Predictor**: A smaller transformer takes the context encoder's output and positional embeddings of the masked regions, and predicts the feature representations of the masked patches.
3. **Target Encoder**: An exponential moving average (EMA) of the context encoder provides the target representations for the masked patches.
4. **Multi-block Masking**: The masking strategy samples multiple target blocks of sufficiently large spatiotemporal scale, while using an informative, spatially distributed context block. This is critical for learning semantic (rather than low-level) representations.

The training loss is a simple L2 regression loss between the predictor's output and the target encoder's representation of the masked regions:

$$\mathcal{L} = \| f_\theta(\text{context}) - \text{sg}(f_{\bar{\theta}}(\text{target})) \|^2$$

where $f_\theta$ is the context encoder + predictor, $f_{\bar{\theta}}$ is the EMA target encoder, and sg denotes stop-gradient.

Key design choices:
- **Attentive probing** (rather than average pooling) significantly improves frozen evaluation
- **Multi-block masking** outperforms random-tube and causal multi-block masking strategies
- Training on a diverse video mixture ([[VideoMix2M]]) yields the best average performance

## Results

### Table 1: Feature Prediction vs. Pixel Prediction (ViT-L/16, Frozen Eval)

| Target Type | Arch. | [[Kinetics-400]] | [[Something-Something v2]] | IN1K | [[Kinetics-400]]-ft |
|-------------|-------|------|------|------|---------|
| Pixels | ViT-L/16 | 68.6 | 66.0 | 73.3 | 85.4 |
| Features | ViT-L/16 | 73.7 | 66.2 | 74.8 | 85.6 |

Feature prediction consistently outperforms pixel prediction on frozen evaluation benchmarks, especially on [[Kinetics-400]] (+5.1 points), while maintaining comparable fine-tuning performance.

### Table 2: Impact of Pretraining Data Distribution (Frozen Eval)

| Arch. | Data | #Samples | [[Kinetics-400]] | [[Something-Something v2]] | IN1K | Avg. |
|-------|------|----------|------|------|------|------|
| ViT-L/16 | [[Kinetics-710]] | 700K | 75.8 | 63.2 | 73.7 | 70.9 |
| ViT-L/16 | [[Kinetics-710]]+[[Something-Something v2]] | 900K | 72.9 | 67.4 | 72.8 | 71.0 |
| ViT-L/16 | [[Kinetics-710]]+HT | 1900K | 74.5 | 64.2 | 74.8 | 71.1 |
| ViT-L/16 | [[VideoMix2M]] | 2000K | 73.7 | 66.2 | 74.8 | 71.5 |
| ViT-H/16 | [[Kinetics-710]]+[[Something-Something v2]] | 900K | 75.7 | 66.8 | 73.7 | 72.0 |
| ViT-H/16 | [[VideoMix2M]] | 2000K | 74.0 | 68.5 | 75.9 | 72.8 |

Training on the diverse [[VideoMix2M]] mixture achieves the highest average performance across benchmarks, especially benefiting [[Something-Something v2|SSv2]] and ImageNet evaluations.

### Table 3: Masking Strategy Ablation (ViT-L/16, Frozen Eval)

| Masking Strategy | [[Kinetics-400]] | [[Something-Something v2]] | IN1K |
|------------------|------|------|------|
| random-tube [0.9] | 51.5 | 46.4 | 55.6 |
| causal multi-block [6] | 61.3 | 49.8 | 66.9 |
| causal multi-block [12] | 71.9 | 63.6 | 72.2 |
| multi-block | 72.9 | 67.4 | 72.8 |

Multi-block masking significantly outperforms random-tube and causal masking strategies. Increasing the number of predicted blocks in causal masking improves performance but still falls short of the non-causal multi-block approach.

### Table 4: Comparison with Pixel Prediction Methods (ViT-L/16, Frozen Eval)

| Method | Arch. | #Samples | [[Kinetics-400]] | [[Something-Something v2]] | AVA | IN1K | [[Places205]] | iNat21 | [[Kinetics-400]]-ft | [[Something-Something v2]]-ft |
|--------|-------|----------|------|------|-----|------|-----------|--------|---------|---------|
| OmniMAE | ViT-L/16 | 2400M | 65.6 | 60.6 | 14.4 | 75.1 | 59.8 | 66.1 | 84.0 | 74.2 |
| VideoMAE | ViT-L/16 | 410M | 77.8 | 65.5 | 21.6 | 71.1 | 59.3 | 64.6 | 85.4 | 74.3 |
| Hiera | Hiera-L | 770M | 75.5 | 64.2 | 15.8 | 68.9 | 58.5 | 56.9 | 87.3 | 75.1 |
| V-JEPA | ViT-L/16 | 270M | 80.8 | 69.5 | 25.6 | 74.8 | 60.3 | 67.8 | 85.6 | 75.1 |

V-JEPA outperforms all pixel-prediction baselines on frozen evaluation across video and image tasks, using significantly fewer pretraining samples. It achieves the highest AVA score (25.6) and competitive fine-tuning results.

### Table 5: State-of-the-Art Comparison (Frozen Eval with [[Attentive Probe Accuracy|Attentive Probe]])

| Method | Arch. | Params | Data | [[Kinetics-400]] | [[Something-Something v2]] | AVA | IN1K | [[Places205]] | iNat21 |
|--------|-------|--------|------|------|------|-----|------|-----------|--------|
| [[I-JEPA]] | ViT-H/16_512 | 630M | IN22K | 79.7 | 50.0 | 19.8 | 84.4 | 66.5 | 85.7 |
| OpenCLIP | ViT-G/14 | 1800M | [[LAION]] | 81.8 | 34.8 | 23.2 | 85.3 | 70.2 | 83.6 |
| DINOv2 | ViT-g/14 | 1100M | [[LVD-142M]] | 83.4 | 50.6 | 24.3 | 86.2 | 68.4 | 88.8 |
| MVD | ViT-L/16 | 200M | IN1K+[[Kinetics-400]] | 79.4 | 66.5 | 19.7 | 73.3 | 59.4 | 65.7 |
| OmniMAE | ViT-H/16 | 630M | IN1K+[[Something-Something v2]] | 71.4 | 65.4 | 16.0 | 76.3 | 60.6 | 72.4 |
| VideoMAE | ViT-H/16 | 630M | [[Kinetics-400]] | 79.8 | 66.2 | 20.7 | 72.3 | 59.1 | 65.5 |
| VideoMAEv2 | ViT-g/14 | 1100M | Un.Hybrid | 71.2 | 61.2 | 12.9 | 71.4 | 60.6 | 68.3 |
| Hiera | Hiera-H | 670M | [[Kinetics-400]] | 77.0 | 64.7 | 17.5 | 71.4 | 59.5 | 61.7 |
| V-JEPA | ViT-L/16 | 200M | [[VideoMix2M]] | 80.8 | 69.5 | 25.6 | 74.8 | 60.3 | 67.8 |
| V-JEPA | ViT-H/16 | 630M | [[VideoMix2M]] | 82.0 | 71.4 | 25.8 | 75.9 | 61.7 | 67.9 |
| V-JEPA | ViT-H/16_384 | 630M | [[VideoMix2M]] | 81.9 | 72.2 | 25.0 | 77.4 | 62.8 | 72.6 |

V-JEPA achieves the best [[Something-Something v2|SSv2]] performance (72.2%) among all methods by a large margin, demonstrating superior motion understanding. While image-pretrained methods (DINOv2, OpenCLIP) lead on appearance-heavy benchmarks (IN1K, [[Places205]], iNat21), V-JEPA provides the best balance across video and image tasks trained from video alone.

### Table 6: Low-Shot Label Efficiency

| Method | Arch. | [[Kinetics-400]] 5% | [[Kinetics-400]] 10% | [[Kinetics-400]] 50% | [[Something-Something v2]] 5% | [[Something-Something v2]] 10% | [[Something-Something v2]] 50% |
|--------|-------|---------|----------|----------|---------|----------|----------|
| MVD | ViT-L/16 | 62.6 | 68.3 | 77.2 | 42.9 | 49.5 | 61.0 |
| VideoMAE | ViT-H/16 | 62.3 | 68.5 | 78.2 | 41.4 | 48.1 | 60.5 |
| VideoMAEv2 | ViT-g/14 | 37.0 | 48.8 | 67.8 | 28.0 | 37.3 | 54.0 |
| V-JEPA | ViT-H/16 | 67.0 | 72.1 | 80.2 | 51.9 | 57.5 | 67.3 |
| V-JEPA | ViT-H/16_384 | 68.2 | 72.8 | 80.6 | 54.0 | 59.3 | 67.9 |

V-JEPA shows exceptional label efficiency, outperforming all baselines across all low-shot settings. The gap is especially large on [[Something-Something v2|SSv2]] at 5% labels (+12.0 points over VideoMAE), highlighting the quality of frozen representations.

## Metrics Used

- [[Top-1 Accuracy]] — primary evaluation metric for classification on [[Kinetics-400|K400]], [[Something-Something v2|SSv2]], IN1K, [[Places205]], iNat21
- [[Mean Average Precision (mAP)]] — used for AVA action localization
- [[Attentive Probe Accuracy]] — frozen evaluation protocol using a learned attention-based probe on top of frozen features
- [[Linear Probe Accuracy]] — alternative frozen evaluation using a linear classifier

## Datasets Used

- [[VideoMix2M]] — pretraining dataset combining [[Kinetics-710]], [[HowTo100M]], and [[Something-Something v2|SSv2]] (2M videos)
- [[Kinetics-400]] — action recognition benchmark (400 classes)
- [[Kinetics-710]] — extended Kinetics dataset used in pretraining
- [[Something-Something v2]] — fine-grained motion understanding benchmark
- [[AVA]] — spatiotemporal action localization benchmark
- [[ImageNet-1K]] — image classification benchmark (1000 classes)
- [[Places205]] — scene classification benchmark
- [[iNaturalist 2021]] — fine-grained species classification benchmark
- [[HowTo100M]] — instructional video dataset used in pretraining
- [[ImageNet-22K]] — used by baseline [[I-JEPA]]

## Related Papers

- [[I-JEPA]] — the image-based JEPA that inspired V-JEPA's approach to feature prediction
- [[V-JEPA 2]] — successor work scaling V-JEPA to larger models and data, adding action-conditioned capabilities
- VideoMAE — pixel-prediction baseline that V-JEPA outperforms on frozen evaluation
- DINOv2 — strong image self-supervised baseline; leads on appearance tasks but lags on motion understanding
- OpenCLIP — image-text contrastive baseline for comparison
