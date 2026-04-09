---
tags: [moc, metric]
aliases: [Metrics MOC]
---

# Metrics Index

All evaluation metrics used across papers in this vault.

## Classification & Accuracy
- [[Top-1 Accuracy]] — Standard classification accuracy
- [[Mean Average Precision (mAP)]] — Detection/retrieval metric
- [[Recall@5]] — Top-5 retrieval recall
- [[F1 Score]] — Harmonic mean of precision and recall
- [[Precision]] — True positive rate among predictions
- [[Recall]] — True positive rate among actual positives
- [[k-NN Accuracy]] — Nearest-neighbor classification on features
- [[Linear Probe Accuracy]] — Linear classifier on frozen representations
- [[Attentive Probe Accuracy]] — Attentive pooling + linear probe
- [[VQA Accuracy]] — Visual Question Answering accuracy
- [[ERQA Accuracy]] — Embodied Reasoning QA accuracy

## Generation Quality
- [[PSNR]] — Peak Signal-to-Noise Ratio
- [[SSIM]] — Structural Similarity Index
- [[LPIPS]] — Learned Perceptual Image Patch Similarity
- [[FVD]] — Frechet Video Distance
- [[rFVD]] — Reconstruction FVD
- [[rFID]] — Reconstruction FID
- [[DreamSim]] — Perceptual similarity via DINO/CLIP features

## Segmentation & Dense Prediction
- [[mIoU]] — Mean Intersection over Union
- [[IoU]] — Intersection over Union
- [[J&F Mean]] — Video object segmentation metric
- [[RMSE]] — Root Mean Square Error (depth)

## Geometric / Trajectory
- [[Absolute Trajectory Error (ATE)]] — Global trajectory error
- [[Relative Trajectory Error (RTE)]] — Local trajectory error
- [[Sampson Error]] — Epipolar geometry error
- [[Euclidean Distance to Goal]] — L2 distance to target
- [[Rdist]] — Rotational distance
- [[Tdist]] — Translational distance
- [[Pose Success Rate]] — Viewpoint estimation success

## Reinforcement Learning
- [[Episode Return]] — Cumulative RL reward
- [[Gamer Normalized Median]] — Atari score vs human gamer (median)
- [[Gamer Normalized Mean]] — Atari score vs human gamer (mean)
- [[Human Normalized Median]] — Score vs human performance (median)
- [[Human Normalized Mean]] — Score vs human performance (mean)
- [[Record Normalized Mean]] — Score vs SOTA record
- [[Crafter Score]] — Crafter environment achievement score
- [[BSuite Score]] — Behavior Suite aggregate
- [[Diamond Collection Rate]] — Minecraft diamond metric
- [[Normalized Zero-Shot Returns]] — Zero-shot RL transfer
- [[Probability of Improvement]] — Statistical RL comparison

## Robotics & Task Performance
- [[Success Rate]] — Task completion rate
- [[Task Progress Score]] — Partial credit for incomplete tasks
- [[Normalized Task Score]] — Performance normalized to baseline
- [[Failure Rate]] — Proportion of failed tasks
- [[Task Completion Time]] — Time to complete task
- [[Task Throughput]] — Tasks per unit time
- [[Language Following Rate]] — Instruction following accuracy
- [[2D Pointing Accuracy]] — 2D spatial prediction accuracy
- [[3D Object Detection AP]] — 3D detection average precision

## Representation Quality
- [[Linear Probe MSE]] — Linear probe regression error
- [[MLP Probe MSE]] — MLP probe regression error
- [[Pearson Correlation]] — Linear correlation coefficient
- [[Surprise Score]] — Novelty in representations
- [[Temporal Straightening]] — Linearity of temporal trajectories
- [[Prediction Error]] — Model prediction vs ground truth
- [[Mean Maximum Rank Violation]] — Ranking consistency

## Human Evaluation
- [[Human Preference Rate]] — Human rater preference
- [[Human Evaluation Score]] — Numerical human score
- [[Motion Naturalness]] — Natural-looking motion quality

## Efficiency
- [[Data Efficiency]] — Performance per data consumed
- [[Inference Latency]] — Model inference time
- [[Planning Time]] — Planning/search time
- [[FPS]] — Frames per second
