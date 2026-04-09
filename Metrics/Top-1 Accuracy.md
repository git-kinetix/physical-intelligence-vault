---
tags: [metric]
aliases: [Top-1 Acc, Top-1, Classification Accuracy]
category: "classification"
higher_is_better: true
---

# Top-1 Accuracy

## Definition
Top-1 Accuracy measures the fraction of examples for which the model's single highest-confidence prediction exactly matches the ground-truth label. It is the most widely reported classification metric in computer vision and serves as the default measure of model performance on benchmarks such as ImageNet and Kinetics.

## Formula
$$\text{Top-1 Accuracy} = \frac{1}{N} \sum_{i=1}^{N} \mathbb{1}[\hat{y}_i = y_i]$$

where $\hat{y}_i$ is the predicted class with the highest probability for sample $i$, $y_i$ is the ground-truth label, and $N$ is the total number of samples.

## Interpretation
- A high value (close to 1.0 or 100%) indicates the model correctly classifies most examples on its first prediction.
- A low value indicates the model frequently misclassifies examples.
- Typical ranges depend on the dataset: ImageNet top-1 accuracy for state-of-the-art models is 85--92%, while Kinetics-400 typically ranges from 80--90%.
- Higher is better.

## Common Usage
Top-1 Accuracy is the standard evaluation metric for image and video classification tasks. It is used to benchmark pretrained representations (e.g., via linear probing or fine-tuning) on datasets like ImageNet-1K, Kinetics-400/600/700, Something-Something v2, and others. In self-supervised and representation learning, it measures how well learned features transfer to downstream classification.

## Papers Using This Metric
- [[V-JEPA]] — used to evaluate frozen video representations via linear and attentive probes on Kinetics-400 and Something-Something v2
- [[V-JEPA 2]] — used to evaluate video representations on Kinetics-400/600/700 and ImageNet-1K via linear and attentive probing
- [[V-JEPA 2.1]] — used to evaluate video and image classification across Kinetics, Something-Something v2, ImageNet, and other benchmarks
- [[Le-JEPA]] — used to evaluate latent representations on classification tasks
- [[Le-World-Model]] — used to evaluate learned representations on downstream classification
