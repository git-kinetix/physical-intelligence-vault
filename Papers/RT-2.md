---
tags: [paper, domain/robotics, method/transformer, method/language-conditioned]
title: "RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control"
authors: [Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Xi Chen, Krzysztof Choromanski, Tianli Ding, Danny Driess, Avinava Dubey, Chelsea Finn, Pete Florence, Chuyuan Fu, Montse Gonzalez Arenas, Keerthana Gopalakrishnan, Kehang Han, Karol Hausman, Alexander Herzog, Jasmine Hsu, Brian Ichter, Alex Irpan, Nikhil Joshi, Ryan Julian, Dmitry Kalashnikov, Yuheng Kuang, Isabel Leal, Lisa Lee, Tsang-Wei Edward Lee, Sergey Levine, Yao Lu, Henryk Michalewski, Igor Mordatch, Karl Pertsch, Kanishka Rao, Krista Reymann, Michael Ryoo, Grecia Salazar, Pannag Sanketi, Pierre Sermanet, Jaspiar Singh, Anikait Singh, Radu Soricut, Huong Tran, Vincent Vanhoucke, Quan Vuong, Ayzaan Wahid, Stefan Welker, Paul Wohlhart, Jialin Wu, Fei Xia, Ted Xiao, Peng Xu, Sichun Xu, Tianhe Yu, Brianna Zitkovich]
year: 2023
arxiv: "https://arxiv.org/abs/2307.15818"
group: "VLA Models"
venue: "CoRL 2023"
domain: [robotics]
method: [transformer, language-conditioned]
lineage: []
predecessor: []
importance: 5
aliases: [RT-2, Robotics Transformer 2]
---

!PDFs/RT-2.pdf


# RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control

## Summary

RT-2 is a pioneering Vision-Language-Action (VLA) model from Google DeepMind that demonstrates how large vision-language models pretrained on internet-scale data can be directly repurposed for robotic control. The key insight is that robot actions can be expressed as text tokens and incorporated into the training data alongside natural language tokens, enabling a single model to both understand visual-language concepts from the web and output low-level robot actions.

RT-2 is instantiated with two large VLM backbones: PaLI-X (55B parameters) and PaLM-E (12B parameters). By co-fine-tuning these models on both web-scale vision-language data and robot trajectory data, RT-2 achieves strong robotic manipulation performance while inheriting emergent capabilities from web pretraining, including symbol understanding, semantic reasoning, and human recognition. In an extensive evaluation of over 6,000 real-robot trials, RT-2 approximately doubles the generalization performance of its predecessor RT-1 on novel objects and unseen scenarios.

RT-2 represents a paradigm shift in robotics: rather than training robot-specific models from scratch, large pretrained VLMs can serve as powerful foundations for robotic control, transferring broad world knowledge to physical manipulation. This work directly influenced subsequent open-source VLA efforts including [[Octo]], [[OpenVLA]], and [[Pi0]].

## Key Contributions

- Proposes the VLA paradigm: expressing robot actions as text tokens within a vision-language model, enabling end-to-end training on mixed web and robot data
- Demonstrates that web-scale VLM pretraining transfers meaningfully to robotic control, approximately doubling generalization to unseen objects
- Shows emergent semantic reasoning capabilities in robot control: symbol understanding, reasoning about object properties, and multi-step chain-of-thought planning
- Introduces chain-of-thought reasoning for robotics, enabling RT-2 to perform multi-stage semantic reasoning (e.g., selecting an improvised hammer)
- Validates the approach at two model scales: RT-2-PaLI-X-55B and RT-2-PaLM-E-12B
- Provides one of the largest real-robot evaluation studies (6,000+ trials) for a VLA model

## Architecture / Method

**Action Tokenization:** Robot actions (7-DoF: x, y, z, roll, pitch, yaw, gripper) are discretized into 256 bins per dimension and expressed as integer text tokens. Each action becomes a sequence of tokens that can be appended to the VLM's vocabulary. A special token indicates episode termination.

**VLM Backbones:**
- **RT-2-PaLI-X-55B**: Based on PaLI-X, a 55-billion parameter vision-language model with a ViT-22B visual encoder. Co-fine-tuned on web data and robot episodes.
- **RT-2-PaLM-E-12B**: Based on PaLM-E, a 12-billion parameter embodied language model. Co-fine-tuned similarly.

**Training:** The models are co-fine-tuned on a mixture of original web vision-language tasks (e.g., visual question answering, captioning) and robot demonstration data. The robot data comes from a fleet of mobile manipulators performing table-top pick-and-place tasks. The co-fine-tuning preserves the web knowledge while adapting the model to output action tokens.

**Chain-of-Thought (CoT):** RT-2 can be augmented with chain-of-thought reasoning, where the model first outputs a natural language "plan" describing its reasoning before producing action tokens. This enables multi-stage semantic reasoning about which objects to interact with.

**Inference:** At each timestep, the model receives a camera image and a language instruction, and outputs action tokens that are de-tokenized into continuous robot commands.

## Results

### Table 1: Robotic Control Success Rates

| Model | Seen Tasks | Unseen Tasks |
|-------|-----------|-------------|
| RT-2-PaLI-X-55B | 91% | 62% |
| RT-2-PaLM-E-12B | 93% | 62% |
| RT-1 | 92% | 32% |
| VC-1 | 74% | 24% |

RT-2 approximately doubles the generalization performance on unseen tasks compared to RT-1, while maintaining comparable performance on seen tasks.

### Table 2: Emergent Capabilities (Unseen Semantic Categories)

| Capability | RT-2-PaLI-X-55B | RT-1 |
|-----------|-----------------|------|
| Symbol Understanding | ~3x improvement | baseline |
| Reasoning | ~3x improvement | baseline |
| Human Recognition | ~3x improvement | baseline |

RT-2 shows approximately 3x improvement over RT-1 on emergent capability evaluations, demonstrating that web knowledge transfers to robotic reasoning.

### Table 3: Language-Table Benchmark (Simulation)

| Model | [[Success Rate]] |
|-------|-------------|
| RT-2 | 90% |
| Previous SOTA | 77% |

### Table 4: Model Scale Ablation

| Variant | Parameters | Generalization |
|---------|-----------|---------------|
| RT-2-PaLI-X-5B | 5B | Lower |
| RT-2-PaLI-X-55B | 55B | Higher |

Generalization improves with model scale, with the 55B variant showing measurable gains over the 5B variant.

## Metrics Used

- [[Success Rate]] -- primary metric for robotic task completion across seen and unseen tasks
- Generalization Rate -- success rate on novel objects and instructions not seen during robot training
- Emergent Capability Score -- evaluation of symbol understanding, reasoning, and human recognition abilities

## Datasets Used

- Robot Demonstration Data -- table-top pick-and-place demonstrations from a fleet of mobile manipulators
- Web Vision-Language Data -- internet-scale image-text data used for VLM pretraining (VQA, captioning, etc.)
- Language-Table -- simulation benchmark for language-conditioned manipulation

## Related Papers

- [[Pi0]] -- Physical Intelligence's VLA that builds on the VLA paradigm pioneered by RT-2, using flow matching instead of autoregressive action tokens
- [[OpenVLA]] -- open-source VLA that outperforms RT-2-X on multiple benchmarks with a 7B model
- [[Octo]] -- open-source generalist policy achieving comparable performance to RT-2-X with 93M parameters
- [[GR00T]] -- NVIDIA's foundation model for humanoid robots, representing another approach to generalist robot control
- [[Gemini Robotics]] -- Google DeepMind's next-generation robotics model building on insights from RT-2
