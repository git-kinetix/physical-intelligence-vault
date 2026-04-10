---
tags: [paper, domain/robotics, method/transformer]
title: "OpenVLA: An Open-Source Vision-Language-Action Model"
authors: [Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, Quan Vuong, Thomas Kollar, Benjamin Burchfiel, Russ Tedrake, Dorsa Sadigh, Sergey Levine, Percy Liang, Chelsea Finn]
year: 2024
arxiv: "https://arxiv.org/abs/2406.09246"
repo: "https://github.com/openvla/openvla"
group: "VLA Models"
venue: "CoRL 2024"
domain: [robotics]
method: [transformer]
lineage: []
predecessor: []
importance: 4
aliases: [OpenVLA, OpenVLA-7B]
---

!PDFs/OpenVLA.pdf


# OpenVLA: An Open-Source Vision-Language-Action Model

## Summary

OpenVLA is an open-source 7-billion parameter Vision-Language-Action model developed by researchers at Stanford, UC Berkeley, Toyota Research Institute, Google DeepMind, Physical Intelligence, and MIT. Built on top of the Prismatic VLM architecture, OpenVLA fine-tunes a Llama 2 7B language model backbone with a fused visual encoder (SigLIP + DINOv2) on 970,000 real-world robot demonstrations from the [[Open X-Embodiment]] dataset.

Despite being 7.8x smaller than the closed-source [[RT-2]]-X (55B), OpenVLA outperforms it by 16.5% in absolute task success rate across 29 tasks in the WidowX [[BridgeData V2]] evaluation. OpenVLA also outperforms expressive from-scratch imitation learning methods such as Diffusion Policy by 20.4% when fine-tuned to new robot setups. The model can be fine-tuned on consumer GPUs via LoRA and served efficiently via 4-bit quantization without degradation in success rate, making it practically deployable.

OpenVLA established itself as a key open-source baseline for the VLA community, demonstrating that open models can compete with and surpass much larger closed models. The paper was accepted at ICML 2025.

## Key Contributions

- Releases the first open-source 7B VLA model that outperforms the 55B closed-source [[RT-2]]-X by 16.5% on real robot evaluations
- Demonstrates that a Prismatic VLM (SigLIP + DINOv2 + Llama 2 7B) provides a strong foundation for VLA training
- Shows effective parameter-efficient fine-tuning: LoRA (rank 32) matches full fine-tuning while training only 1.4% of parameters
- Achieves lossless 4-bit quantization, reducing VRAM from 16.8 GB to 7.0 GB without performance degradation
- Trained on 970K real-world robot demonstrations from [[Open X-Embodiment]]
- Provides comprehensive evaluation across 29 [[BridgeData V2]] tasks and fine-tuning experiments on Franka robots

## Architecture / Method

**Visual Encoder:** A fused dual-backbone encoder combining:
- **SigLIP**: Provides strong language-aligned visual features
- **DINOv2**: Provides spatially precise visual features complementary to SigLIP

The two backbones' patch embeddings are concatenated and projected into the LLM's input space via a learned MLP projector.

**Language Model Backbone:** Llama 2 7B serves as the backbone, processing both visual tokens (from the projector) and language tokens (instruction text).

**Action Tokenization:** Robot actions are discretized into 256 bins per dimension (similar to [[RT-2]]) and predicted as text tokens by the language model. The model outputs 7-DoF actions (x, y, z, roll, pitch, yaw, gripper).

**Training Data:** 970K real-world robot demonstrations from the [[Open X-Embodiment]] dataset, spanning multiple robot platforms.

**Fine-Tuning:**
- **Full fine-tuning**: Updates all 7.2B parameters (163.3 GB VRAM)
- **LoRA**: Updates only 97.6M parameters at rank 32 (59.7 GB VRAM), matching full fine-tuning performance
- **Quantization**: 4-bit (int4) inference at 7.0 GB VRAM with no performance loss

**Total Parameters:** 7 billion (7B).

## Results

### Table 1: [[BridgeData V2]] Real Robot Evaluation (WidowX, 29 Tasks)

| Model | Parameters | Average Success |
|-------|-----------|----------------|
| **OpenVLA** | 7B | ~71% |
| [[RT-2]]-X | 55B | ~61% |
| [[Octo]] | 93M | ~35% |
| RT-1-X | 35M | ~25% |

OpenVLA outperforms [[RT-2]]-X in all evaluation categories (language grounding, visual generalization, motion generalization) except semantic generalization, despite being 7.8x smaller.

### Table 2: Fine-Tuning on New Robot Setups (Franka Arms, 7 Tasks)

| Approach | Average Success |
|----------|----------------|
| **OpenVLA (fine-tuned)** | ~67% |
| Diffusion Policy | ~52% |
| [[Octo]] (fine-tuned) | ~48% |
| OpenVLA (from scratch) | ~35% |

OpenVLA is the only approach achieving at least 50% success rate across all tested tasks, demonstrating robust generalization.

### Table 3: Parameter-Efficient Fine-Tuning

| Method | [[Success Rate]] | Trainable Params | VRAM |
|--------|-------------|------------------|------|
| Full Fine-tuning | 69.7% | 7.2B | 163.3 GB |
| LoRA (rank 32) | 68.2% | 97.6M | 59.7 GB |
| LoRA (rank 64) | 68.2% | 195.2M | 60.5 GB |
| Frozen Vision | 47.0% | 6.8B | 156.2 GB |
| Last Layer Only | 30.3% | 465.1M | 51.4 GB |

LoRA matches full fine-tuning while using only 1.4% of trainable parameters and 36% of the VRAM.

### Table 4: Quantization Results

| [[Precision]] | Bridge Success | VRAM |
|-----------|---------------|------|
| bfloat16 | 71.3% | 16.8 GB |
| int8 | 58.1% | 10.2 GB |
| int4 | 71.9% | 7.0 GB |

4-bit quantization matches bfloat16 performance while reducing GPU memory by more than half, enabling deployment on consumer hardware.

## Metrics Used

- [[Success Rate]] -- task completion rate across 29 manipulation tasks
- VRAM Usage -- GPU memory footprint for training and inference
- Trainable Parameters -- efficiency of parameter-efficient fine-tuning methods

## Datasets Used

- [[Open X-Embodiment]] -- 970K real-world robot demonstrations for pretraining
- [[BridgeData V2]] -- WidowX manipulation dataset for primary evaluation (29 tasks)
- [[Franka Demonstration Data]] -- 10-150 demonstrations per task for fine-tuning evaluation

## Related Papers

- [[RT-2]] -- the 55B closed-source VLA that OpenVLA outperforms by 16.5% at 7.8x smaller scale
- [[Octo]] -- the 93M open-source generalist policy that OpenVLA outperforms on most benchmarks
- [[Pi0]] -- Physical Intelligence's 3.3B VLA that further advances the VLA paradigm with flow matching
- [[Pi0.5]] -- successor to [[Pi0]] with improved multi-task performance
- [[GR00T]] -- NVIDIA's humanoid robot foundation model
- [[Gemini Robotics]] -- Google DeepMind's next-generation VLA approach
