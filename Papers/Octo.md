---
tags: [paper, domain/robotics, method/transformer, method/diffusion]
title: "Octo: An Open-Source Generalist Robot Policy"
authors: [Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, Jianlan Luo, You Liang Tan, Lawrence Yunliang Chen, Pannag Sanketi, Quan Vuong, Ted Xiao, Dorsa Sadigh, Chelsea Finn, Sergey Levine]
year: 2024
arxiv: "https://arxiv.org/abs/2405.12213"
repo: "https://github.com/octo-models/octo"
group: "VLA Models"
venue: "RSS 2024"
domain: [robotics]
method: [transformer, diffusion]
lineage: []
predecessor: []
importance: 3
aliases: [Octo, Octo-Base, Octo-Small]
---

!PDFs/Octo.pdf


# Octo: An Open-Source Generalist Robot Policy

## Summary

Octo is an open-source generalist robot policy developed by UC Berkeley and collaborators, trained on 800,000 robot trajectories from the [[Open X-Embodiment]] dataset. It is designed as a flexible foundation for robot learning that can be instructed via language commands or goal images, and can be effectively fine-tuned to new robot setups with different sensory inputs and action spaces within a few hours on consumer GPUs.

The model uses a transformer-based architecture that reads tokenized robot observations (images, language, proprioception) and predicts actions via a diffusion-based action head. Two model sizes are released: Octo-Small (27M parameters) and Octo-Base (93M parameters). Despite being orders of magnitude smaller than [[RT-2]]-X (55B), Octo achieves comparable or superior performance when conditioned on language, and outperforms the next best baseline by 52% on average across six evaluation setups when fine-tuned to new domains.

Octo represents a significant milestone as the first open-source, broadly capable generalist robot policy that can serve as an effective initialization for fine-tuning to diverse downstream robot platforms, including those with new observation modalities and action spaces not seen during pretraining. It was published at RSS 2024.

## Key Contributions

- First widely adopted open-source generalist robot policy trained on the [[Open X-Embodiment]] dataset (800K trajectories)
- Demonstrates effective cross-embodiment transfer: a single model serves as a versatile initialization across 9 different robot platforms
- Achieves comparable performance to [[RT-2]]-X (55B) with only 93M parameters when using language conditioning on WidowX tasks
- Goal image conditioning yields 25% higher success rates than language conditioning, revealing modality-specific strengths
- Efficient fine-tuning: adapts to new observation inputs and action spaces in a few hours on consumer GPUs
- Comprehensive ablation study on data mixtures, action representations, and architecture choices

## Architecture / Method

**Transformer Backbone:** Octo uses a transformer that processes tokenized inputs from multiple modalities:
- **Image observations**: Encoded into patch tokens via a lightweight CNN encoder
- **Language instructions**: Tokenized using a pretrained language model encoder
- **Goal images**: Processed through the same image encoder as observations
- **Proprioceptive state**: Projected into token space via an MLP

**Action Head:** Octo uses a diffusion-based action head that generates continuous action chunks, conditioned on the transformer's output tokens. This avoids discretization artifacts of autoregressive token-based approaches.

**Readout Tokens:** Special readout tokens are appended to the input sequence. The transformer attends over all observation and task tokens, and the readout token representations are used to condition the diffusion action head.

**Data Mixture:** Training uses a curated subset of the [[Open X-Embodiment]] dataset spanning multiple robot embodiments (WidowX, Franka, Kuka, Google Robot, etc.) with diverse tasks and environments.

**Model Sizes:**
- **Octo-Small**: 27M parameters
- **Octo-Base**: 93M parameters

**Fine-Tuning:** The full model can be fine-tuned end-to-end on target domain data, including support for new observation modalities (e.g., wrist cameras) and action spaces (e.g., different robot morphologies) not present in pretraining.

## Results

### Table 1: Fine-Tuning to New Robot Setups (~100 Target Demonstrations)

| Task | Octo | ResNet+Transformer (Scratch) | VC-1 |
|------|------|------------------------------|------|
| Berkeley Insertion (new obs.) | 70% | 10% | 5% |
| Stanford Coffee | 75% | 45% | 0% |
| CMU Baking | 50% | 25% | 30% |
| Berkeley Pick-Up (new action) | 60% | 0% | 0% |
| Berkeley Coke | 100% | 20% | 10% |
| Berkeley Bimanual (new action) | 80% | 20% | 50% |
| **Average** | **72%** | **20%** | **15%** |

Octo dramatically outperforms from-scratch training and VC-1 initialization when fine-tuned on small target domain datasets, achieving 72% average success vs. 20% and 15% for the baselines.

### Table 2: Architecture Ablation on WidowX Tasks

| Configuration | Aggregate Success |
|--------------|-------------------|
| Octo-Small (full model) | 83% |
| RT-X dataset mix | 60% |
| Single robot dataset | 43% |
| Discretized actions | 18% |
| MSE continuous actions | 35% |
| ResNet-50 + Transformer | 70% |

The full Octo configuration with diffusion action head and diverse data mixture significantly outperforms all ablated variants.

### Table 3: Zero-Shot Cross-Embodiment Performance

| Conditioning | Octo | RT-1-X | [[RT-2]]-X (55B) |
|-------------|------|--------|--------------|
| Language (WidowX) | ~comparable to [[RT-2]]-X | lower | baseline |
| Goal Image (WidowX) | +25% vs language | N/A | N/A |

Octo matches the 55B-parameter [[RT-2]]-X on language-conditioned WidowX tasks despite being ~600x smaller, and achieves 25% higher success with goal image conditioning.

## Metrics Used

- [[Success Rate]] -- primary metric for task completion across robot platforms
- Fine-Tuning Efficiency -- hours to adapt to new robot setups on consumer GPUs
- Cross-Embodiment Transfer -- zero-shot and fine-tuned performance on robots not seen during pretraining

## Datasets Used

- [[Open X-Embodiment]] -- 800K robot trajectories spanning multiple embodiments and tasks, the largest open robot manipulation dataset
- WidowX data -- subset used for primary evaluation
- Bridge V2 -- subset of cross-embodiment data

## Related Papers

- [[RT-2]] -- the closed-source VLA model (55B) that Octo matches on language-conditioned tasks at 600x smaller scale
- [[OpenVLA]] -- a larger open-source VLA (7B) that outperforms Octo on several benchmarks
- [[Pi0]] -- Physical Intelligence's VLA that uses a similar diffusion action head but with a much larger VLM backbone
- [[Pi0.5]] -- successor to [[Pi0]] with improved multi-task capabilities
- [[GR00T]] -- NVIDIA's humanoid robot foundation model, another approach to generalist robot control
