---
tags: [metric]
aliases: [kNN Accuracy, k-Nearest Neighbors Accuracy, KNN Accuracy]
category: "representation"
higher_is_better: true
---

# k-NN Accuracy

## Definition
k-Nearest Neighbors (k-NN) Accuracy measures the classification accuracy of a non-parametric k-NN classifier applied to learned feature representations. For each test sample, the k most similar training samples in the feature space are retrieved, and the majority class label among those neighbors is assigned as the prediction. This metric evaluates representation quality without introducing any additional trainable parameters, making it a pure test of feature discriminability and clustering structure.

## Formula
$$\text{k-NN Accuracy} = \frac{1}{N_{\text{test}}} \sum_{i=1}^{N_{\text{test}}} \mathbb{1}\left[\text{mode}\left(\{y_j : j \in \mathcal{N}_k(x_i)\}\right) = y_i\right]$$

where $\mathcal{N}_k(x_i)$ is the set of $k$ nearest neighbors of test sample $x_i$ in the training feature space, $y_j$ are their labels, and $y_i$ is the ground-truth label.

## Interpretation
- A high k-NN accuracy indicates that the learned representations form well-separated clusters aligned with semantic classes.
- A low k-NN accuracy suggests the feature space does not organize samples by class membership.
- k-NN accuracy is typically lower than linear probe accuracy, as the linear probe can learn decision boundaries; k-NN relies solely on neighborhood structure.
- Common values of k are 10 or 20. Higher is better.

## Common Usage
k-NN Accuracy is a standard evaluation protocol for self-supervised and unsupervised representation learning. It is used to assess the quality of features learned by models like DINO, MAE, JEPA variants, and other pretraining methods. Because it requires no training, it provides the most direct measure of intrinsic feature quality.

## Papers Using This Metric
- [[Le-JEPA]] — used to evaluate the quality of latent representations learned by the model
