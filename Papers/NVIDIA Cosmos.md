---
tags: [paper, video-planning]
title: "Cosmos World Foundation Model Platform for Physical AI"
authors: [Niket Agarwal, Arslan Ali, Maciej Bala, Yogesh Balaji, Erik Barker, Tiffany Cai, Prithvijit Chattopadhyay, Yongxin Chen, Yin Cui, Yifan Ding, Daniel Dworakowski, Jiaojiao Fan, Michele Fenzi, Francesco Ferroni, Sanja Fidler, Dieter Fox, Songwei Ge, Yunhao Ge, Jinwei Gu, Siddharth Gururani, Ethan He, Jiahui Huang, Jacob Huffman, Pooya Jannaty, Jingyi Jin, Seung Wook Kim, Gergely Klar, Grace Lam, Shiyi Lan, Laura Leal-Taixe, Anqi Li, Zhaoshuo Li, Chen-Hsuan Lin, Tsung-Yi Lin, Huan Ling, Ming-Yu Liu, Xian Liu, Alice Luo, Qianli Ma, Hanzi Mao, Kaichun Mo, Arsalan Mousavian, Seungjun Nah, Sriharsha Niverty, David Page, Despoina Paschalidou, Zeeshan Patel, Lindsey Pavao, Morteza Ramezanali, Fitsum Reda, Xiaowei Ren, Vasanth Rao Naik Sabavat, Ed Schmerling, Stella Shi, Bartosz Stefaniak, Shitao Tang, Lyne Tchapmi, Przemek Tredak, Wei-Cheng Tseng, Jibin Varghese, Hao Wang, Haoxiang Wang, Heng Wang, Ting-Chun Wang, Fangyin Wei, Xinyue Wei, Jay Zhangjie Wu, Jiashu Xu, Wei Yang, Lin Yen-Chen, Xiaohui Zeng, Yu Zeng, Jing Zhang, Qinsheng Zhang, Yuxuan Zhang, Qingqing Zhao, Artur Zolkowski]
year: 2025
arxiv: "https://arxiv.org/abs/2501.03575"
repo: "https://github.com/NVIDIA/Cosmos"
group: "Video Generation / Planning"
importance: 
aliases: [Cosmos, NVIDIA Cosmos, Cosmos WFM, Cosmos-Predict1, Cosmos Tokenizer]
---

![[PDFs/NVIDIA Cosmos.pdf]]


# Cosmos World Foundation Model Platform for Physical AI

## Summary

NVIDIA Cosmos is a comprehensive platform for building world foundation models (WFMs) designed for Physical AI applications such as robotics and autonomous driving. The platform provides an end-to-end pipeline encompassing video data curation, novel video tokenizers (Cosmos Tokenizer), pre-trained world foundation models in both diffusion-based and autoregressive families, and post-training recipes for downstream tasks including camera control, robotic manipulation, and autonomous driving. The platform was trained on approximately 20 million hours of video data processed into ~100 million curated video clips using a GPU-accelerated curation pipeline achieving 89x speedup over CPU baselines.

The paper introduces the Cosmos Tokenizer, a causal visual tokenizer supporting both continuous and discrete tokenization for images and videos jointly -- the first tokenizer to achieve all of these capabilities simultaneously. The tokenizer achieves +4 dB [[PSNR]] improvement in reconstruction quality on [[DAVIS-2017|DAVIS]] videos while running up to 12x faster than competing approaches. Two families of world foundation models are presented: diffusion-based (7B and 14B parameter variants) and autoregressive (4B/5B and 12B/13B parameter variants), both trained on 10,000 NVIDIA H100 GPUs over 3 months on 9,000 trillion tokens.

Post-training demonstrates that the pre-trained WFMs can be fine-tuned for camera-controllable world generation, action-conditioned robotic manipulation, and autonomous driving video prediction. The entire platform, including models and benchmark datasets ([[TokenBench]], [[ShotBench]]), is released as open source under a permissive license to accelerate Physical AI research.

## Key Contributions

- **Cosmos Tokenizer**: A causal visual tokenizer supporting continuous and discrete tokenization for both images and videos jointly, with state-of-the-art reconstruction quality (+4 dB [[PSNR]]) and 12x faster runtime
- **Video curation pipeline**: GPU-accelerated pipeline processing 20M hours of video with 89x speedup over CPU baselines, including shot detection, motion filtering, quality filtering, deduplication, and annotation
- **Two WFM families**: Diffusion-based (7B/14B) and autoregressive (4B-13B) world foundation models pre-trained on ~100M video clips
- **Post-training recipes**: Demonstrations of fine-tuning for camera control, robotic manipulation, and autonomous driving
- **WFM-based policy evaluation**: Framework for evaluating Physical AI policies in simulation rather than the real world
- **Open-source release**: Models, tokenizers, and benchmark datasets ([[TokenBench]], [[ShotBench]]) released under permissive license
- **Guardrails**: Pre-guard (keyword blocking, Aegis classifier) and post-guard (content safety, face blur) safety systems

## Architecture / Method

### Cosmos Tokenizer

The Cosmos Tokenizer employs a wavelet-based encoder-decoder architecture with temporally causal spatio-temporal convolutions and self-attention. Key design choices:

- **Causal architecture**: Enables joint image-video training and aligns with physical causality (future frames depend only on past)
- **Wavelet space processing**: Operates on wavelet-transformed representations to reduce redundancy
- **Temporally factorized attention**: Captures both spatial and long-range temporal dependencies efficiently
- **Adaptive layer normalization**: Uses learnable scale-shift-gate modulation
- **FSQ quantization**: For discrete tokens, uses Finite Scalar Quantization with vocabulary size of 64,000
- **Compression ratios**: Supports 4x8x8, 8x8x8, and 8x16x16 for video; 8x8 and 16x16 for images

### Diffusion World Foundation Model

The diffusion WFM is a transformer-based latent diffusion model (3D DiT) operating on continuous latent tokens:

- **Patchification**: Converts tokenized video latents into patch sequences
- **FPS-aware 3D RoPE**: Rotary positional embeddings aware of frame rate for temporal consistency
- **Cross-attention text conditioning**: T5-XXL text embeddings incorporated via cross-attention
- **Query-key normalization**: Stabilizes attention computations at scale
- **AdaLN-LoRA**: Adaptive layer normalization with low-rank adaptation for parameter-efficient conditioning
- **Progressive training**: Three stages -- low-resolution pre-training (512p, 57 frames), high-resolution pre-training (720p, 121 frames), and high-quality fine-tuning (720p, 121 frames)

### Autoregressive World Foundation Model

The autoregressive WFM uses a GPT-style (Llama3-based) transformer operating on discrete tokens:

- **Discrete token prediction**: Next-token prediction on FSQ-quantized tokens from DV8x16x16 tokenizer
- **Cross-attention for text**: T5 text embeddings incorporated via cross-attention layers
- **Diffusion decoder**: Upsamples from DV8x16x16 to CV8x8x8 continuous tokens for final high-quality output
- **Prompt upsampler**: Mistral-NeMo-12B-Instruct model enhances input text prompts

### Post-Training

- **Camera control**: Fine-tunes diffusion WFM with camera pose as conditioning input
- **Robotic manipulation**: Fine-tunes on video-action sequence datasets for action-conditioned future state prediction
- **Autonomous driving**: Fine-tunes for driving scenario generation and prediction

## Results

### Table 1: Shot Detection Algorithm Comparison (F1 Scores)

| Dataset | PySceneDetect | [[Panda-70M]] | TransNetV2 | AutoShot |
|---------|---------------|----------|------------|----------|
| BBC | 0.889 | 0.777 | 0.967 | 0.952 |
| RAI | 0.831 | 0.829 | 0.919 | 0.906 |
| SHOT | 0.718 | 0.622 | 0.821 | 0.834 |
| ClipShots | 0.477 | 0.513 | 0.726 | 0.711 |

TransNetV2 achieves the best F1 scores on most benchmarks and is adopted as the default shot detection algorithm in the Cosmos curation pipeline.

### Table 2: Transcoding Performance

| Method | GPU | Codec | Batch | [[FPS]] (videos/s) |
|--------|-----|-------|-------|-----------------------|
| ffmpeg | H100 | libx264 | 1 | 0.0574 |
| ffmpeg | L40S | h264_nvenc | 1 | 0.0674 |
| ffmpeg | L40S | h264_nvenc | 16 | 0.1026 |
| pynvc+ffmpeg | L40S | h264_nvenc | 1 | 0.3702 |

Using PyNvideoCodec with ffmpeg on L40S achieves a 6.5x throughput improvement over the CPU-based H100 baseline, enabling efficient processing of the 20M hour video corpus.

### Table 3: VILA Annotation Inference [[FPS|Throughput]]

| Engine | [[Precision]] | Batch Size | [[FPS]] (clips/s) | [[FPS]] (tokens/s) |
|--------|-----------|------------|----------------------|-----------------------|
| PyTorch | FP16 | 1 | 0.21 | 49.6 |
| TRT-LLM | FP16 | 1 | 0.40 | 95.6 |
| TRT-LLM | FP16 | 16 | 1.09 | 260.9 |
| TRT-LLM | FP8 | 16 | 1.96 | 470.6 |

TensorRT-LLM with FP8 quantization and batch size 16 achieves 9.3x throughput improvement over the PyTorch FP16 baseline for video annotation.

### Table 4: Visual Tokenizer Capabilities Comparison

| Model | Causal | Image | Video | Joint | Discrete | Continuous |
|-------|--------|-------|-------|-------|----------|------------|
| FLUX-Tokenizer | - | Yes | No | No | No | Yes |
| Open-MAGVIT2 | - | Yes | No | No | Yes | No |
| LlamaGen-Tokenizer | - | Yes | No | No | Yes | No |
| VideoGPT-Tokenizer | No | No | Yes | No | Yes | No |
| Omni-Tokenizer | No | Yes | Yes | Yes | Yes | Yes |
| CogVideoX-Tokenizer | Yes | Yes | Yes | Yes | No | Yes |
| Cosmos-Tokenizer | Yes | Yes | Yes | Yes | Yes | Yes |

Cosmos Tokenizer is the only tokenizer to support all capabilities: causal, image, video, joint training, discrete, and continuous tokenization.

### Table 5: Continuous Video Tokenizer Evaluation

| Tokenizer | Frames | [[PSNR]] ([[DAVIS-2017]]) | [[SSIM]] ([[DAVIS-2017]]) | [[rFVD]] ([[DAVIS-2017]]) | [[PSNR]] ([[TokenBench]]) | [[SSIM]] ([[TokenBench]]) | [[rFVD]] ([[TokenBench]]) |
|-----------|--------|--------------|--------------|--------------|--------------------|--------------------|--------------------|
| CogVideoX 4x8x8 | 17 | 29.29 | 0.864 | 19.58 | 32.06 | 0.909 | 6.97 |
| Omni-Tokenizer 4x8x8 | 17 | 22.23 | 0.713 | 117.66 | 24.48 | 0.830 | 35.86 |
| Cosmos-0.1-CV 4x8x8 | 49 | 32.80 | 0.900 | 15.93 | 35.45 | 0.928 | 6.85 |
| Cosmos-0.1-CV 8x8x8 | 49 | 30.61 | 0.856 | 30.16 | 34.44 | 0.917 | 11.62 |
| Cosmos-0.1-CV 8x16x16 | 49 | 27.60 | 0.779 | 93.82 | 31.61 | 0.875 | 43.08 |
| Cosmos-1.0-CV 8x8x8 | 121 | 31.28 | 0.868 | 23.49 | 35.13 | 0.926 | 9.82 |

Cosmos continuous video tokenizers outperform all baselines on both [[DAVIS-2017|DAVIS]] and [[TokenBench]]. The Cosmos-0.1-CV 4x8x8 model achieves +3.5 dB [[PSNR]] improvement over CogVideoX on [[DAVIS-2017|DAVIS]] while processing 49 frames versus 17.

### Table 6: Discrete Video Tokenizer Evaluation

| Tokenizer | Frames | Quantization | [[PSNR]] ([[DAVIS-2017]]) | [[SSIM]] ([[DAVIS-2017]]) | [[rFVD]] ([[DAVIS-2017]]) | [[PSNR]] ([[TokenBench]]) | [[SSIM]] ([[TokenBench]]) | [[rFVD]] ([[TokenBench]]) |
|-----------|--------|--------------|--------------|--------------|--------------|--------------------|--------------------|---------------------|
| VideoGPT 4x4x4 | - | VQ | 28.17 | 0.850 | 72.33 | 33.66 | 0.914 | 13.85 |
| Omni-Tokenizer 4x8x8 | 17 | VQ | 20.02 | 0.703 | 188.60 | 25.31 | 0.827 | 53.55 |
| Cosmos-0.1-DV 4x8x8 | 17 | FSQ | 28.81 | 0.818 | 37.36 | 31.97 | 0.888 | 19.67 |
| Cosmos-0.1-DV 8x8x8 | 17 | FSQ | 27.51 | 0.789 | 100.15 | 30.95 | 0.873 | 43.86 |
| Cosmos-0.1-DV 8x16x16 | 17 | FSQ | 25.09 | 0.714 | 241.52 | 28.91 | 0.829 | 113.48 |
| Cosmos-1.0-DV 8x16x16 | 49 | FSQ | 25.49 | 0.719 | 259.33 | 29.33 | 0.838 | 107.43 |

Cosmos discrete tokenizers with FSQ quantization significantly outperform Omni-Tokenizer with VQ at the same compression ratio (4x8x8), achieving +8.8 dB [[PSNR]] on [[DAVIS-2017|DAVIS]].

### Table 7: Continuous Image Tokenizer Evaluation

**[[MS-COCO 2017]]:**

| Tokenizer | [[PSNR]] | [[SSIM]] | [[rFID]] |
|-----------|------|------|------|
| FLUX-Tokenizer 8x8 | 24.00 | 0.682 | 2.501 |
| Cosmos-0.1-CI 8x8 | 28.66 | 0.836 | 1.760 |
| Cosmos-0.1-CI 16x16 | 23.63 | 0.663 | 3.823 |

**[[ImageNet-1K]]:**

| Tokenizer | [[PSNR]] | [[SSIM]] | [[rFID]] |
|-----------|------|------|------|
| FLUX-Tokenizer 8x8 | 20.09 | 0.518 | 1.229 |
| Cosmos-0.1-CI 8x8 | 28.83 | 0.837 | 0.689 |
| Cosmos-0.1-CI 16x16 | 23.72 | 0.655 | 1.031 |

Cosmos continuous image tokenizer at 8x8 compression outperforms FLUX-Tokenizer by +4.7 dB [[PSNR]] on [[MS-COCO 2017|MS-COCO]] and +8.7 dB on [[ImageNet-1K]].

### Table 8: Discrete Image Tokenizer Evaluation

**[[MS-COCO 2017]]:**

| Tokenizer | Quantization | [[PSNR]] | [[SSIM]] | [[rFID]] |
|-----------|--------------|------|------|------|
| Open-MAGVIT2 16x16 | LFQ | 19.50 | 0.502 | 6.649 |
| LlamaGen 8x8 | VQ | 21.99 | 0.616 | 4.123 |
| LlamaGen 16x16 | VQ | 19.11 | 0.491 | 6.077 |
| Cosmos-0.1-DI 8x8 | FSQ | 24.40 | 0.704 | 3.710 |
| Cosmos-0.1-DI 16x16 | FSQ | 20.45 | 0.529 | 7.234 |

**[[ImageNet-1K]]:**

| Tokenizer | Quantization | [[PSNR]] | [[SSIM]] | [[rFID]] |
|-----------|--------------|------|------|------|
| Open-MAGVIT2 16x16 | LFQ | 17.00 | 0.398 | 2.701 |
| LlamaGen 8x8 | VQ | 19.64 | 0.498 | 1.403 |
| LlamaGen 16x16 | VQ | 18.38 | 0.448 | 1.657 |
| Cosmos-0.1-DI 8x8 | FSQ | 24.48 | 0.701 | 1.265 |
| Cosmos-0.1-DI 16x16 | FSQ | 20.49 | 0.518 | 2.518 |

Cosmos discrete image tokenizers with FSQ consistently outperform both VQ (LlamaGen) and LFQ (Open-MAGVIT2) baselines in [[PSNR]] and [[SSIM]] across both datasets.

### Table 9: Tokenizer Runtime Performance (A100 80GB GPU)

| Tokenizer | Type | Resolution | Frames | Parameters | Time (ms) |
|-----------|------|------------|--------|------------|-----------|
| FLUX-Tokenizer 8x8 | Continuous-Image | 1024x1024 | - | 84M | 242 |
| Cosmos-0.1-CI 8x8 | Continuous-Image | 1024x1024 | - | 77M | 62.7 |
| LlamaGen 8x8 | Discrete-Image | 1024x1024 | - | 70M | 475 |
| Cosmos-0.1-DI 8x8 | Discrete-Image | 1024x1024 | - | 79M | 64.2 |
| CogVideoX 4x8x8 | Continuous-Video | 720x1280 | 17 | 216M | 414 |
| Omni-Tokenizer 4x8x8 | Continuous-Video | 720x1280 | 17 | 54M | 82.9 |
| Cosmos-0.1-CV 4x8x8 | Continuous-Video | 720x1280 | 49 | 105M | 34.8 |
| Omni-Tokenizer 4x8x8 | Discrete-Video | 720x1280 | 17 | 54M | 53.2 |
| Cosmos-0.1-DV 4x8x8 | Discrete-Video | 720x1280 | 17 | 105M | 51.5 |

Cosmos continuous video tokenizer achieves 11.9x speedup over CogVideoX while processing nearly 3x more frames. Cosmos image tokenizer achieves 3.8x speedup over FLUX and 7.4x over LlamaGen.

### Table 10: Cosmos WFM 1.0 Release Map

| Type | Base Models | Video2World Models | Tokenizer | Enhancer |
|------|-------------|-------------------|-----------|----------|
| Diffusion | Cosmos-1.0-Diffusion-7B-Text2World | Cosmos-1.0-Diffusion-7B-Video2World | Cosmos-1.0-Tokenizer-CV8x8x8 | Cosmos-1.0-PromptUpsampler-12B |
| Diffusion | Cosmos-1.0-Diffusion-14B-Text2World | Cosmos-1.0-Diffusion-14B-Video2World | Cosmos-1.0-Tokenizer-CV8x8x8 | Cosmos-1.0-PromptUpsampler-12B |
| Autoregressive | Cosmos-1.0-Autoregressive-4B | Cosmos-1.0-Autoregressive-5B-Video2World | Cosmos-1.0-Tokenizer-DV8x16x16 | Cosmos-1.0-Diffusion-7B-Decoder |
| Autoregressive | Cosmos-1.0-Autoregressive-12B | Cosmos-1.0-Autoregressive-13B-Video2World | Cosmos-1.0-Tokenizer-DV8x16x16 | Cosmos-1.0-Diffusion-7B-Decoder |

### Table 11: Diffusion Model Configuration Details

| Configuration | 7B-Text2World | 14B-Text2World | 7B-Video2World | 14B-Video2World |
|---------------|---------------|----------------|----------------|-----------------|
| Number of Layers | 28 | 36 | 28 | 36 |
| Model Dimension | 4,096 | 5,120 | 4,096 | 5,120 |
| FFN Hidden Dimension | 16,384 | 20,480 | 16,384 | 20,480 |
| AdaLN-LoRA Dimension | 256 | 256 | 256 | 256 |
| Attention Heads | 32 | 40 | 32 | 40 |
| Key/Value Heads | 32 | 40 | 32 | 40 |
| MLP Activation | GELU | GELU | GELU | GELU |
| Positional Embedding | Hybrid | Hybrid | Hybrid | Hybrid |
| Conditional Info | Text; FPS | Text; FPS | Text; FPS; Frames | Text; FPS; Frames |
| Base Learning Rate | 2^-15 | 2^-16 | 2^-15 | 2^-16 |
| Weight Decay | 0.1 | 0.2 | 0.1 | 0.2 |

### Table 12: Progressive Training Stages

| Stage | Resolution | Frames | Context Length | FSDP Size | CP Size |
|-------|------------|--------|----------------|-----------|---------|
| Low-resolution Pre-training | 512p (640x512) | 57 | 10,240 | 64 | 2 |
| High-resolution Pre-training | 720p (1280x704) | 121 | 56,320 | 64 | 8 |
| High-quality Fine-tuning | 720p (1280x704) | 121 | 56,320 | 64 | 8 |

### 3D Consistency Evaluation (Post-Training)

| Model | [[Sampson Error]] | [[Pose Success Rate]] | [[PSNR]] | [[SSIM]] | [[LPIPS]] |
|-------|---------------|-------------------|------|------|-------|
| VideoLDM | 0.841 | 4.40% | 26.23 | 0.783 | 0.135 |
| Cosmos Diffusion Text2World 7B | 0.355 | 62.60% | 33.02 | 0.939 | 0.070 |
| Cosmos Diffusion Video2World 7B | 0.473 | 68.40% | 30.66 | 0.929 | 0.085 |
| Cosmos Autoregressive 4B | 0.433 | 35.60% | 32.56 | 0.933 | 0.090 |
| Real videos (reference) | 0.431 | 56.40% | 35.38 | 0.962 | 0.054 |

Cosmos models dramatically outperform the VideoLDM baseline on 3D consistency, with the Diffusion Video2World 7B model achieving 68.4% pose success rate compared to 4.4% for VideoLDM. The Cosmos Diffusion models even surpass the pose success rate of real videos (56.4%).

### Physics Alignment Evaluation (Post-Training)

| Model | Conditioning | [[PSNR]] | [[SSIM]] | [[DreamSim]] | Avg. [[IoU]] |
|-------|-------------|------|------|----------|----------|
| Cosmos Diffusion Video2World 7B | prompt + 9 frames | 21.06 | 0.69 | 0.86 | 0.592 |
| Cosmos Diffusion Video2World 14B | prompt + 9 frames | 20.21 | 0.64 | 0.86 | 0.598 |
| Cosmos Autoregressive Video2World 12B | 9 frames | 18.22 | 0.49 | 0.87 | 0.487 |

Physics alignment is evaluated across eight controlled scenarios testing gravity, collision, and inertia. The 14B diffusion model achieves slightly better [[IoU]] (0.598) than the 7B variant (0.592), while the autoregressive model lags behind in [[PSNR]] and [[SSIM]] but achieves competitive [[DreamSim]] scores.

## Metrics Used

- [[PSNR]] -- [[PSNR|Peak Signal-to-Noise Ratio]], used to evaluate tokenizer reconstruction quality and video generation fidelity
- [[SSIM]] -- [[SSIM|Structural Similarity Index]], used alongside [[PSNR]] for reconstruction and generation quality
- [[rFVD]] -- [[rFVD|Reconstruction Frechet Video Distance]], used to evaluate video tokenizer temporal quality on [[DAVIS-2017|DAVIS]] and [[TokenBench]]
- [[rFID]] -- [[rFID|Reconstruction Frechet Inception Distance]], used to evaluate image tokenizer quality on [[MS-COCO 2017|MS-COCO]] and ImageNet
- [[LPIPS]] -- [[LPIPS|Learned Perceptual Image Patch Similarity]], used in 3D consistency evaluation of generated videos
- [[Sampson Error]] -- Epipolar geometry error, used to measure 3D consistency of generated video
- [[Pose Success Rate]] -- Percentage of successfully estimated camera poses, used for 3D consistency evaluation
- [[DreamSim]] -- Perceptual similarity metric, used in physics alignment evaluation
- [[IoU]] -- [[IoU|Intersection over Union]], averaged across physics scenarios (gravity, collision, inertia)
- [[F1 Score]] -- Used for shot detection algorithm evaluation on [[ShotBench]]
- [[Precision]] -- Used for shot detection evaluation
- [[Recall]] -- Used for shot detection evaluation

## Datasets Used

- [[DAVIS]] -- Dense Annotation Video Segmentation dataset, used for video tokenizer reconstruction evaluation
- [[TokenBench]] -- Custom benchmark of 500 videos from [[BDD100K]], [[Ego-Exo4D|EgoExo-4D]], [[BridgeData V2]], and [[Panda-70M]], created for standardized video tokenizer evaluation
- [[ShotBench]] -- Custom shot detection benchmark combining RAI, BBC Planet Earth, ClipShots, and SHOT datasets
- [[MS-COCO 2017]] -- 5,000 validation images used for image tokenizer evaluation
- [[ImageNet-1K]] -- 50,000 validation images used for image tokenizer evaluation
- [[BDD100K]] -- Driving dataset, part of [[TokenBench]] and training data
- [[EgoExo-4D]] -- Egocentric video dataset, part of [[TokenBench]] and training data
- [[BridgeData V2]] -- Robotic manipulation dataset, part of [[TokenBench]] and used for post-training
- [[Panda-70M]] -- Large-scale web video dataset, part of [[TokenBench]] and training data

## Related Papers

- [[Genie]] -- Google DeepMind's generative interactive environment model using VQ latent actions; Cosmos takes a different approach with continuous tokenization
- [[CogVideoX]] -- Video generation model whose tokenizer is compared against Cosmos Tokenizer
- [[VideoGPT]] -- Early discrete video tokenizer baseline compared in evaluation
- [[FLUX]] -- Image generation model whose tokenizer is compared against Cosmos image tokenizers
- [[Open-MAGVIT2]] -- Discrete image tokenizer using LFQ, compared against Cosmos-DI
- [[LlamaGen]] -- Image generation model with VQ tokenizer, compared against Cosmos-DI
- [[Omni-Tokenizer]] -- Joint image-video tokenizer baseline compared against Cosmos
- [[VideoLDM]] -- Video latent diffusion model used as baseline in 3D consistency evaluation
- [[VILA]] -- Vision-language model used for automated video captioning in the Cosmos pipeline
- [[Learning Latent Action World Models In The Wild]] -- FAIR work on latent action world models from uncurated videos, related approach to action-free video generation
- [[Cosmos-Drive-Dreams]] -- Follow-up work applying Cosmos WFMs specifically to autonomous driving synthetic data generation
