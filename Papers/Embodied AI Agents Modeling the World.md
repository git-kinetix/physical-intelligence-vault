---
tags: [paper, domain/robotics, domain/ssl, method/masked-prediction, lineage/jepa, lineage/fair]
title: "Embodied AI Agents: Modeling the World"
authors: [Pascale Fung, Yoram Bachrach, Asli Celikyilmaz, Kamalika Chaudhuri, Delong Chen, Willy Chung, Emmanuel Dupoux, Hongyu Gong, Hervé Jégou, Alessandro Lazaric, Arjun Majumdar, Andrea Madotto, Franziska Meier, Florian Metze, Louis-Philippe Morency, Théo Moutakanni, Juan Pino, Basile Terver, Joseph Tighe, Paden Tomasello, Jitendra Malik]
year: 2025
arxiv: "https://arxiv.org/abs/2506.22355"
repo: ""
group: "JEPA Family"
venue: "arXiv 2025"
domain: [robotics, ssl]
method: [masked-prediction]
lineage: [jepa, fair]
predecessor: ["[[V-JEPA 2]]", "[[I-JEPA]]"]
importance: 
aliases: [Embodied AI Agents, Modeling the World]
---

![[PDFs/Embodied AI Agents Modeling the World.pdf]]

# Embodied AI Agents: Modeling the World

## Summary

This Meta AI position paper presents a comprehensive framework for embodied AI agents -- systems with visual, virtual, or physical forms (avatars, wearables, robots) that interact with users and environments. The authors argue that world models are the central organizing principle for embodied AI, enabling agents to understand and predict their environment, interpret user intentions, and reason about social contexts. The framework integrates multimodal perception, reasoning-based planning, action and control, and memory systems.

The paper classifies embodied agents into three types: Type I (virtual embodied agents such as avatars and conversational agents), Type II (wearable agents such as Meta smart glasses), and Type III (robotic agents). For each type, the authors describe how physical world models and mental world models work together to enable perception, planning, and action. Physical world models capture object properties, spatial relationships, dynamics, and causal structures, while mental world models represent human beliefs, goals, intentions, and emotions (Theory of Mind).

A key theme is the adoption of Joint-Embedding Predictive Architectures ([[I-JEPA]], [[V-JEPA]], [[V-JEPA 2]]) for building world models that predict in abstract latent space rather than pixel space, enabling efficient planning. The paper also introduces and evaluates several world model benchmarks (MVP, IntPhys 2, CausalVQA, WorldPrediction) that reveal substantial gaps between current AI systems and human physical reasoning capabilities.

## Key Contributions

- Comprehensive framework for embodied AI centered on world modeling, integrating multimodal perception, physical and mental world models, memory, and action/control
- Three-type taxonomy of embodied agents: virtual (avatars), wearable (smart glasses), and robotic
- Introduction of four world model benchmarks: Minimal Video Pairs (MVP), IntPhys 2, CausalVQA, and WorldPrediction
- Demonstration that current state-of-the-art models dramatically underperform humans on physical reasoning benchmarks (e.g., 40.2% vs 92.9% human accuracy on MVP)
- Advocacy for JEPA-based latent-space world models over generative pixel-space approaches for efficient planning and control
- Discussion of memory architectures (fixed, working, external, episodic) for embodied agents
- Integration of mental world models (Theory of Mind) for human-agent collaboration

## Architecture / Method

The paper proposes a modular architecture for embodied AI agents with five interconnected components:

**Multimodal Perception:**
- Vision: Perception Encoder (PE) and Perception Language Model (PLM) for image and video understanding
- Audio/Speech: Seamless Interaction system trained on over 4,000 hours of dyadic interactions for natural turn-taking
- Touch: Tactile sensing for robotic manipulation

**Physical [[World Models]]:**
- Capture object properties, spatial relationships, environment dynamics, and causal relationships
- Low-level motion planning using visual world models that predict future states
- High-level action planning through abstract reasoning
- Joint-Embedding Predictive Architectures (JEPA) predict in latent space rather than pixel space, enabling more efficient planning
- Model-predictive control: "a World Model rolls the world forward under candidate actions" and a cost module evaluates hypothetical futures

**Mental [[World Models]]:**
- Theory of Mind representations capturing user beliefs, goals, intentions, and emotions
- Social dynamics modeling for multi-agent interactions
- Enable agents to understand and predict human behavior for collaboration

**Memory Systems:**
- Fixed memory: model weights encoding long-term knowledge
- Working memory: activations and KV-cache for in-context processing
- External memory: retrieval-augmented generation (RAG) for accessing stored information
- Proposed episodic memory: for continuous learning from agent experiences

**Actions and Control:**
- Hierarchical planning from high-level abstract actions to low-level motor commands
- Type-specific implementations: dialogue generation (virtual), proactive assistance (wearable), physical manipulation (robotic)

## Results

### [[MVP|MVP Benchmark]]: State-of-the-Art vs Human Physical Reasoning

| Model | Accuracy |
|-------|----------|
| State-of-the-art multimodal models | 40.2% |
| Human baseline | 92.9% |
| Random chance | 25.0% |

The MVP benchmark comprises 55,000 multiple-choice video QA pairs using minimal-change video pairs to test physical and spatio-temporal reasoning. The 52.7 percentage point gap between SOTA and human performance highlights the inadequacy of current models for physical world understanding.

### WorldPrediction Benchmark

| Task | Current SOTA | Human Performance |
|------|-------------|-------------------|
| WorldPrediction-WM (World Modeling) | 57% | Near perfect |
| WorldPrediction-PP (Procedural Planning) | 38% | Near perfect |

The WorldPrediction benchmark uses a POMDP framework to evaluate world modeling and procedural planning capabilities. Current models fall far short of human-level performance on both tasks.

### IntPhys 2 Benchmark

| Physics Principle | Model Performance | Human Performance |
|------------------|-------------------|-------------------|
| Permanence | Chance level | Ceiling |
| Immutability | Chance level | Ceiling |
| Spatio-Temporal Continuity | Chance level | Ceiling |
| Solidity | Chance level | Ceiling |

IntPhys 2 uses a violation-of-expectation paradigm to test four core physics principles. Contemporary vision models perform at chance level across all complex test cases while humans approach ceiling performance.

### CausalVQA Benchmark

| Question Type | Model vs Human |
|--------------|----------------|
| Counterfactual | Models significantly underperform |
| Hypothetical | Models significantly underperform |
| Anticipation | Weakest model performance |
| Planning | Models significantly underperform |
| Descriptive | Models significantly underperform |

CausalVQA evaluates causal reasoning on real-world video scenarios. State-of-the-art multimodal models significantly underperform humans, with particular weakness in anticipation and hypothetical reasoning.

## Metrics Used

- [[Top-1 Accuracy]] — multiple-choice accuracy on MVP benchmark (40.2% SOTA vs 92.9% human)
- Violation-of-Expectation Score — IntPhys 2 evaluation of intuitive physics across four principles
- Video QA Accuracy — CausalVQA evaluation across five causal reasoning question types
- World Modeling Accuracy — WorldPrediction-WM task measuring environment state prediction (57% SOTA)
- Procedural Planning Accuracy — WorldPrediction-PP task measuring action sequence prediction (38% SOTA)

## Datasets Used

- [[MVP]] (Minimal Video Pairs) — 55,000 multiple-choice video QA pairs for physical reasoning evaluation
- IntPhys 2 — violation-of-expectation video benchmark for four core physics principles
- CausalVQA — video QA dataset for causal reasoning with five question types
- WorldPrediction — POMDP-based benchmark for world modeling and procedural planning
- Seamless Interaction Dataset — over 4,000 hours of dyadic interactions for audiovisual model training
- ToMI — Theory of Mind benchmark for mental state reasoning
- Hi-ToM — higher-order Theory of Mind evaluation
- ExploreToM — adversarially generated belief-reasoning tasks for Theory of Mind

## Related Papers

- [[V-JEPA 2]] — key exemplar of JEPA-based world models; [[V-JEPA 2]]-AC demonstrates latent-space robotic planning advocated in this paper
- [[I-JEPA]] — foundational image-based JEPA architecture underlying the proposed world modeling approach
- [[V-JEPA]] — video JEPA predecessor that demonstrated self-supervised video representation learning
- [[V-JEPA 2.1]] — dense-feature JEPA variant relevant to the multimodal perception component
- [[JEPA-WMs]] — concurrent work (co-authored by Basile Terver) studying what drives success in JEPA-based world models for physical planning
- [[NVIDIA Cosmos]] — video generation world model; contrasted with JEPA latent-space approach
- [[Octo]] — generalist robot policy baseline compared against [[V-JEPA 2]]-AC in the paper
- [[RT-2]] — VLA model representing the language-conditioned robotics approach discussed
