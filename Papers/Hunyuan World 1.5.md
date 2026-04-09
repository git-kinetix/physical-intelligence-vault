---
tags: [paper, world-model]
title: "WorldPlay: Towards Long-Term Geometric Consistency for Real-Time Interactive World Modeling"
authors: [Wenqiang Sun, Haiyu Zhang, Haoyuan Wang, Junta Wu, Zehan Wang, Zhenwei Wang, Yunhong Wang, Jun Zhang, Tengfei Wang, Chunchao Guo]
year: 2025
arxiv: "https://arxiv.org/abs/2512.14614"
repo: "https://github.com/Tencent-Hunyuan/HY-WorldPlay"
group: "World Models"
importance: 
aliases: [HY-World 1.5, WorldPlay, Hunyuan World 1.5]
---

![[PDFs/Hunyuan World 1.5.pdf]]


# WorldPlay: Towards Long-Term Geometric Consistency for Real-Time Interactive World Modeling

## Summary
HY-World 1.5 (WorldPlay) is Tencent Hunyuan's interactive world model that achieves real-time, long-horizon video generation with geometric consistency -- addressing the fundamental trade-off between speed and memory that limits current methods. The system generates 720p streaming video at 24 FPS while maintaining 3D geometric consistency over extended time horizons, supporting first-person and third-person perspectives in both real-world and stylized environments.

The framework introduces three core innovations: (1) a Dual Action Representation that handles both keyboard and mouse inputs for responsive real-time control, (2) a Reconstituted Context Memory mechanism that dynamically rebuilds context from previous frames using temporal reframing to keep geometrically important but temporally distant frames accessible, and (3) Context Forcing, a novel distillation technique that preserves the student model's capacity to use long-range information while enabling real-time inference speeds. Additionally, the system incorporates WorldCompass, a reinforcement learning post-training framework designed to directly improve action-following and visual quality of the autoregressive video model. WorldPlay achieves state-of-the-art results across both short-term generation quality and long-term geometric consistency benchmarks, significantly outperforming prior methods.

## Key Contributions
- First open-source real-time interactive world model with long-term geometric consistency
- Dual Action Representation enabling robust control from both discrete (keyboard) and continuous (mouse) inputs
- Reconstituted Context Memory with temporal reframing that dynamically rebuilds context to maintain geometric consistency over long horizons
- Context Forcing distillation method that preserves long-range memory while achieving real-time speed
- WorldCompass reinforcement learning post-training framework for improving action-following and visual quality
- 24 FPS streaming 720p video generation with strong geometric consistency

## Architecture / Method
WorldPlay is a streaming video diffusion model built on large-scale video generation backbones.

**Backbone Options:**
- HunyuanVideo-8B (recommended, higher quality)
- WAN-5B (lightweight alternative)

**Dual Action Representation:**
The model accepts two forms of user input simultaneously:
- Discrete actions from keyboard (forward, backward, left, right, jump, etc.)
- Continuous actions from mouse (camera rotation angles)
This dual representation is injected into the diffusion model's conditioning pipeline, enabling responsive real-time control during interactive world exploration.

**Reconstituted Context Memory:**
Rather than using a fixed sliding window of past frames (which loses long-range geometric information), the system dynamically reconstructs context by:
1. Selecting geometrically important frames from the full history based on camera pose diversity
2. Applying temporal reframing via modified RoPE (Rotary Position Embeddings) to place these frames into the model's context window
3. This ensures the model can reference distant but geometrically relevant frames even as the horizon grows

**Context Forcing (Distillation):**
A novel distillation technique designed for memory-aware models:
- The teacher model generates high-quality outputs using full context
- The student model is trained to match teacher outputs while using compressed context
- Key innovation: the distillation explicitly preserves the student's capacity for long-range information use, preventing the error drift that plagues naive distillation approaches

**WorldCompass RL Framework:**
Post-training with reinforcement learning to directly optimize:
- Action-following accuracy (does the generated video match the user's input?)
- Visual quality and consistency of long-horizon autoregressive generation

**Training Pipeline:**
1. Pre-training on large-scale video data
2. Middle-training for interactive conditioning
3. RL post-training with WorldCompass
4. Memory-aware model distillation via Context Forcing

## Results

### Table 1: Quantitative Comparison — Short-Term and Long-Term Generation Quality

| Method | Real-time | Short [[PSNR]] | Short [[SSIM]] | Short [[LPIPS]] | Short [[Rdist]] | Short [[Tdist]] | Long [[PSNR]] | Long [[SSIM]] | Long [[LPIPS]] | Long [[Rdist]] | Long [[Tdist]] |
|--------|-----------|-----------|-----------|------------|------------|------------|----------|----------|-----------|-----------|-----------|
| CameraCtrl | No | 17.93 | 0.569 | 0.298 | 0.037 | 0.341 | 10.09 | 0.241 | 0.549 | 0.733 | 1.117 |
| SEVA | No | 19.84 | 0.598 | 0.313 | 0.047 | 0.223 | 10.51 | 0.301 | 0.517 | 0.721 | 1.893 |
| ViewCrafter | No | 19.91 | 0.617 | 0.327 | 0.029 | 0.543 | 9.32 | 0.277 | 0.661 | 1.573 | 3.051 |
| Gen3C | No | 21.68 | 0.635 | 0.278 | 0.024 | 0.477 | 15.37 | 0.431 | 0.483 | 0.357 | 0.979 |
| VMem | No | 19.97 | 0.587 | 0.316 | 0.048 | 0.219 | 12.77 | 0.335 | 0.542 | 0.748 | 1.547 |
| Matrix-Game-2.0 | Yes | 17.26 | 0.505 | 0.383 | 0.287 | 0.843 | 9.57 | 0.205 | 0.631 | 2.125 | 2.742 |
| GameCraft | No | 21.05 | 0.639 | 0.341 | 0.151 | 0.617 | 10.09 | 0.287 | 0.614 | 2.497 | 3.291 |
| WorldPlay (w/o CF) | No | 21.27 | 0.669 | 0.261 | 0.033 | 0.157 | 16.27 | 0.425 | 0.495 | 0.611 | 0.991 |
| **WorldPlay (full)** | **Yes** | **21.92** | **0.702** | **0.247** | **0.031** | **0.121** | **18.94** | **0.585** | **0.371** | **0.332** | **0.797** |

WorldPlay achieves the best scores on nearly every metric for both short-term and long-term generation. Critically, it is the only real-time method that achieves competitive quality -- Matrix-Game-2.0, the only other real-time method, scores significantly lower across all metrics. The long-term [[PSNR]] of 18.94 far exceeds the next best (Gen3C at 15.37), demonstrating the effectiveness of the Reconstituted Context Memory. Lower [[Rdist]] and [[Tdist]] values indicate better camera pose accuracy.

### Table 2: Action Representation Ablation

| Action Type | [[PSNR]] | [[SSIM]] | [[LPIPS]] | [[Rdist]] | [[Tdist]] |
|-------------|------|------|-------|-------|-------|
| Discrete only | 21.47 | 0.661 | 0.248 | 0.103 | 0.615 |
| Continuous only | 21.93 | 0.665 | 0.231 | 0.038 | 0.287 |
| **Dual (full)** | **22.09** | **0.687** | **0.219** | **0.028** | **0.113** |

The dual action representation combining both discrete and continuous inputs achieves the best performance, particularly for camera pose accuracy ([[Rdist]], [[Tdist]]), validating the design choice.

### Table 3: RoPE Design Ablation (Long-Term Generation)

| Positional Encoding | [[PSNR]] | [[SSIM]] | [[LPIPS]] | [[Rdist]] | [[Tdist]] |
|---------------------|------|------|-------|-------|-------|
| Standard RoPE | 14.03 | 0.358 | 0.534 | 0.805 | 1.341 |
| **Reframed RoPE** | **16.27** | **0.425** | **0.495** | **0.611** | **0.991** |

Temporal reframing of RoPE (the core of Reconstituted Context Memory) provides a substantial improvement in long-term generation quality, with [[PSNR]] improving from 14.03 to 16.27 and geometric consistency ([[Rdist]], [[Tdist]]) improving significantly.

## Metrics Used
- [[PSNR]] — [[PSNR|Peak Signal-to-Noise Ratio]]; measures pixel-level reconstruction quality (higher is better)
- [[SSIM]] — [[SSIM|Structural Similarity Index]]; measures structural similarity between generated and ground truth frames (higher is better)
- [[LPIPS]] — [[LPIPS|Learned Perceptual Image Patch Similarity]]; measures perceptual distance (lower is better)
- [[Rdist]] — Rotation distance; measures camera rotation accuracy between generated and ground truth poses (lower is better)
- [[Tdist]] — Translation distance; measures camera translation accuracy (lower is better)
- [[Human Evaluation Score]] — human assessments of visual quality, control accuracy, and long-term consistency (300 cases, 30 assessors)

## Datasets Used
- [[RealEstate10K]] — real estate walkthrough videos for training and evaluation of novel view synthesis
- [[DL3DV]] — large-scale 3D vision dataset for diverse scene understanding
- [[Tanks and Temples]] — benchmark for 3D reconstruction with indoor and outdoor scenes
- [[Custom Tencent Dataset]] — proprietary video data for pre-training the video diffusion backbone

## Related Papers
- [[CameraCtrl]] — camera-conditioned video generation baseline
- [[SEVA]] — single-image novel view synthesis baseline
- [[ViewCrafter]] — view synthesis from single images
- [[Gen3C]] — generative 3D-consistent video synthesis
- [[Matrix-Game-2.0]] — real-time interactive world model baseline
- [[GameCraft]] — game-oriented world generation
- [[DreamerV3]] — model-based RL world model (different paradigm: latent state world models for RL vs. video generation world models)
