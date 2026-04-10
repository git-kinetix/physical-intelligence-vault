---
tags: [paper, domain/video-generation, method/transformer]
title: "Learning Latent Action World Models In The Wild"
authors: [Quentin Garrido, Tushar Nagarajan, Basile Terver, Nicolas Ballas, Yann LeCun, Michael Rabbat]
year: 2026
arxiv: "https://arxiv.org/abs/2601.05230"
group: "Video Generation / Planning"
venue: "arXiv 2026"
domain: [video-generation]
method: [transformer]
lineage: []
predecessor: []
importance: 3
aliases: [LAWM, Latent Action World Models]
---

!PDFs/Learning Latent Action World Models In The Wild.pdf


# Learning Latent Action World Models In The Wild

## Summary

This paper from FAIR (Meta) addresses a fundamental bottleneck in world model research: the scarcity of action-labeled video data. While abundant unlabeled video exists on the internet, most world models require paired video-action data for training, limiting their scale. The authors propose learning latent action world models (LAMs) directly from uncurated, in-the-wild video data ([[YouTube-Temporal-1B]]) without any explicit action labels, extending prior work beyond controlled settings such as robotics simulations and video games.

The key finding is that continuous, constrained latent action spaces -- regularized via sparsity constraints or noise addition (VAE-like) -- significantly outperform the discrete vector quantization (VQ) approach used in prior work like Genie when dealing with complex, real-world scene dynamics. The authors discover that without a unified embodiment across diverse footage, learned actions become spatially localized relative to the camera perspective, representing an important insight about representation constraints in uncurated video.

To bridge the gap between latent actions and real-world control, the authors train a lightweight controller that maps known robot actions to the learned latent action space. This enables a world model trained purely on YouTube videos to solve planning tasks on robotics benchmarks ([[DROID]] for manipulation, [[RECON]] for navigation) with performance comparable to models trained with ground-truth actions. This demonstrates that latent actions can serve as a universal interface between internet-scale video understanding and physical robot control.

## Key Contributions

- **In-the-wild latent action learning**: First demonstration of training latent action world models on uncurated YouTube videos ([[YouTube-Temporal-1B]]) at scale, moving beyond controlled environments
- **Continuous over discrete**: Empirical evidence that continuous latent action spaces with regularization (sparsity or noise) significantly outperform vector quantization (VQ) for complex real-world dynamics
- **Spatial localization insight**: Discovery that without unified embodiment, learned actions become spatially localized relative to camera perspective
- **Cross-video action transfer**: Demonstration that learned actions transfer meaningfully across different videos, capturing environment-specific changes (e.g., humans entering rooms)
- **Universal action interface**: Training lightweight controllers to map real robot actions to latent actions, enabling YouTube-trained models to solve robotics planning tasks
- **Competitive robotics performance**: Achieving planning performance on [[DROID]] and [[RECON]] comparable to action-conditioned baselines trained with ground-truth actions

## Architecture / Method

### Latent Action Model (LAM)

The model architecture follows an encoder-decoder design for video prediction conditioned on discovered latent actions:

1. **Video Encoder**: A causal Vision Transformer (ViT) processes input video frames to extract visual representations
2. **Action Encoder**: A separate encoder infers latent actions from pairs of consecutive frames, capturing the "change" between timesteps
3. **World Model Decoder**: Conditioned on the current frame(s) and a latent action, the decoder predicts the next frame(s)

The latent action vector has dimension 128 and represents the abstract transformation between consecutive frames.

### Latent Action Regularization

Three approaches are compared for controlling information flow through the latent action bottleneck:

1. **Sparsity constraints (Sparse)**: Simultaneous L1, L2, mean, variance, and covariance penalties on the 128-dimensional latent vectors. The lambda_l1 parameter (ranging 0.001 to 0.1) controls constraint severity. Higher values produce more constrained (more abstract) actions.

2. **Noise addition (VAE-like / Noise)**: KL divergence regularization toward a standard normal distribution N(0,1). The beta parameter controls the constraint severity. Lower beta values preserve fine-grained motion details.

3. **Vector Quantization (VQ / Discrete)**: Standard VQ with codebook sizes of 512 and 2,048 learned vectors. This is the approach used by prior work (Genie) but found to degrade significantly on complex in-the-wild scenes.

### Controller for Robot Action Mapping

A lightweight neural network controller is trained to map real robot actions (e.g., joint velocities, end-effector positions) to the learned latent action space. This enables using the YouTube-trained world model for planning in robotics domains:

- The controller is trained on a small amount of robot data with action labels
- At inference time, a planner searches over real actions, maps them through the controller to latent actions, and uses the world model for rollout evaluation
- Classical planning protocols (e.g., visual model-predictive control toward a goal image) are applied

### Training Details

- **Training data**: [[YouTube-Temporal-1B]] (in-the-wild uncurated videos)
- **Batch size**: 1,024
- **Training iterations**: 30,000
- **Latent action dimension**: 128

## Results

### Latent Action Regularization Comparison

| Method | Codebook/Parameter | In-the-Wild Quality | Robotics Transfer |
|--------|-------------------|--------------------|--------------------|
| VQ (Discrete) | 512 codes | Poor -- degrades on complex scenes | Limited |
| VQ (Discrete) | 2,048 codes | Poor -- degrades on complex scenes | Limited |
| Sparse (Continuous) | lambda_l1 = 0.001-0.1 | Good -- captures scene complexity | Competitive with action-conditioned baselines |
| Noise/VAE (Continuous) | beta (varying) | Good -- preserves fine-grained motion | Competitive with action-conditioned baselines |

Continuous latent spaces with regularization (sparse or noise) significantly outperform discrete VQ for in-the-wild videos. VQ fails to capture the complexity of real-world scene dynamics, while continuous approaches provide a flexible middle ground.

### Robotics Planning Evaluation ([[DROID]] - Manipulation)

The authors evaluate planning performance on [[DROID]] robotic manipulation tasks by training a controller to map real robot actions to learned latent actions, then using visual model-predictive control toward goal images:

| Method | Action Source | Planning Performance |
|--------|--------------|---------------------|
| Action-conditioned baseline | Ground-truth actions | Baseline reference |
| LAWM + Controller (Sparse) | Latent actions from YouTube | Comparable to baseline |
| LAWM + Controller (Noise) | Latent actions from YouTube | Comparable to baseline |
| LAWM + Controller (VQ) | Latent actions from YouTube | Below baseline |

Models with continuous latent actions (sparse and noise regularization) achieve similar performance to world model and policy baselines that are trained with real actions from the start. The best performing models are those where the latent actions form a middle ground in terms of capacity -- neither too constrained nor too unconstrained.

### Robotics Planning Evaluation ([[RECON]] - Navigation)

| Method | Action Source | Planning Performance |
|--------|--------------|---------------------|
| Action-conditioned baseline | Ground-truth actions | Baseline reference |
| LAWM + Controller (Sparse) | Latent actions from YouTube | Comparable to baseline |
| LAWM + Controller (Noise) | Latent actions from YouTube | Comparable to baseline |

Similar to [[DROID]], the YouTube-trained latent action model with a learned controller achieves competitive navigation performance on [[RECON]], demonstrating that latent actions serve as an effective universal interface for physical control tasks.

### Action Transfer and Spatial Localization

| Experiment | Finding |
|-----------|---------|
| Cross-video transfer | Actions learned from one video (e.g., person walking) transfer to other videos, producing semantically meaningful changes |
| Scene transition detection | Prediction error more than doubles when encountering artificial scene transitions, confirming actions are scene-specific |
| Spatial localization | Without unified embodiment, actions are spatially localized relative to camera -- affecting entities nearest to the original action location |

### Video Prediction Quality

The paper evaluates video prediction quality using standard metrics ([[PSNR]], [[SSIM]], [[LPIPS]], [[FVD]]) on in-the-wild videos. Continuous regularization methods (sparse and noise) produce higher-fidelity predictions than VQ, particularly on videos with complex dynamics and diverse scene content.

## Metrics Used

- [[PSNR]] -- [[PSNR|Peak Signal-to-Noise Ratio]], used to evaluate video prediction quality
- [[SSIM]] -- [[SSIM|Structural Similarity Index]], used to evaluate video prediction quality
- [[LPIPS]] -- [[LPIPS|Learned Perceptual Image Patch Similarity]], used to evaluate perceptual quality of predicted frames
- [[FVD]] -- [[FVD|Frechet Video Distance]], used to evaluate temporal quality and realism of generated video sequences
- [[Prediction Error]] -- Frame-level prediction error, used to detect scene transitions and evaluate action quality

## Datasets Used

- [[YouTube-Temporal-1B]] -- Large-scale uncurated in-the-wild video dataset used for training the latent action world model
- [[DROID]] -- Distributed Robot Interaction Dataset for robotic manipulation, used to evaluate planning with latent actions via a learned controller
- [[RECON]] -- Real-world navigation dataset, used to evaluate planning with latent actions for autonomous navigation tasks

## Related Papers

- Genie -- Google DeepMind's generative interactive environment model that uses discrete VQ latent actions; LAWM shows continuous actions outperform VQ on real-world videos
- [[NVIDIA Cosmos]] -- NVIDIA's world foundation model platform for Physical AI; complementary approach using explicit action-conditioning after pre-training
- [[V-JEPA 2]] -- Meta's self-supervised video model for understanding, prediction, and planning; related FAIR work on learning from video
- AdaWorld -- Adaptable world models with latent actions; concurrent work on latent action learning for world modeling
- Hierarchical Latent Action Model -- HiLAM, follow-up work extending latent action models with hierarchical structure
- Latent Action Pretraining -- LAPA, related approach to pretraining with latent actions for language-action models
