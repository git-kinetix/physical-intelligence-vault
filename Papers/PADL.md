---
tags: [paper, domain/character-animation, method/rl, method/language-conditioned, lineage/peng]
title: "PADL: Language-Directed Physics-Based Character Control"
authors: [Jordan Juravsky, Yunrong Guo, Sanja Fidler, Xue Bin Peng]
year: 2022
arxiv: "https://arxiv.org/abs/2301.13868"
repo: "https://github.com/nv-tlabs/PADL"
group: "World Models"
venue: "SIGGRAPH Asia 2022"
domain: [character-animation]
method: [rl, language-conditioned]
lineage: [peng]
predecessor: ["[[ASE]]"]
importance: 3
aliases: [PADL, Physics-based Animation Directed with Language]
---

!PDFs/PADL.pdf

# PADL: Language-Directed Physics-Based Character Control

## Summary

PADL (Physics-based Animation Directed with Language) introduces a framework for controlling physically simulated characters through natural language commands, published at SIGGRAPH Asia 2022. The system allows users to specify both high-level task objectives (e.g., "go to location") and low-level motion skills (e.g., "while running" or "while sneaking") using free-form text. PADL bridges the gap between language understanding and physics-based character animation by combining a learned motion-language embedding space with adversarial reinforcement learning policies.

The method operates in two stages. First, a skill embedding stage trains a motion encoder (bidirectional transformer) and a language encoder (pre-trained CLIP text encoder with a 2-layer FC head) to map motions and captions into a shared 128-dimensional latent space. Second, a policy training stage uses PPO with an adversarial skill reward (joint discriminator over state transitions and skill embeddings) alongside task-specific rewards to train controllers that execute language-specified skills while completing goals. A multi-task aggregation module based on a fine-tuned BERT multiple-choice QA model determines which high-level task a user command refers to.

Unlike [[ASE]], which can suffer from mode collapse when scaling to many motions, PADL assigns a distinct learned motion latent to every clip in the dataset, guaranteeing full coverage of the reference motion repertoire. The system is demonstrated on a 37-DOF humanoid character with a sword and shield, performing a diverse array of locomotion, combat, and interaction skills directed by natural language.

## Key Contributions

- First framework for language-directed physics-based character control that supports both high-level task specification and low-level skill selection via natural language
- A motion-language embedding space using a bidirectional transformer motion encoder paired with a CLIP-based language encoder, achieving superior dataset coverage compared to raw CLIP embeddings
- An adversarial imitation learning approach using a joint discriminator over state transitions and skill embeddings that mitigates mode collapse compared to marginal discriminators used in [[ASE]]
- A multi-task aggregation method leveraging language-based multiple-choice QA (fine-tuned BERT on SWAG) to extract task objectives from free-form commands
- Demonstration on 131 motion clips with 265 text captions, training at a scale of ~7 billion samples (~2.5 days on a single A100 GPU)

## Architecture / Method

**Skill Embedding Stage:**
- **Motion encoder**: Bidirectional transformer that maps variable-length motion clips to 128D latent embeddings
- **Language encoder**: Pre-trained CLIP text encoder followed by a 2-layer fully connected projection head mapping to 128D
- **Motion decoder**: Bidirectional transformer with a learned query sequence for motion reconstruction
- Training objective: Contrastive loss aligning motion and language embeddings in the shared space

**Policy Training Stage:**
- **Policy network**: MLP with hidden layers [1024, 1024, 512]
- **Value function**: Same architecture as the policy
- **Discriminator**: Joint discriminator over (state transition, skill embedding) pairs, same MLP architecture, trained with gradient penalty
- **Optimization**: PPO with 4,096 parallel environments on a single A100 GPU
- **Reward**: Weighted combination of task reward (goal-conditioned) and skill reward (adversarial imitation), with adaptive task weight initialized at lambda_0 = 3 and clamped to [0.5, 3]
- Simulation at 120 Hz, policy at 30 Hz

**Multi-Task Aggregation:**
- Fine-tuned BERT model on the SWAG dataset for multiple-choice QA
- Given a user command, selects the most appropriate high-level task from a predefined set
- Enables a single interface for directing diverse behaviors

**Character**: 37-DOF humanoid with sword and shield, trained on 131 motion clips (~9 minutes total) with 265 captions (1-4 per clip).

## Results

PADL results are primarily demonstrated qualitatively through interactive character animations. The paper evaluates skill embedding quality via a dataset coverage metric.

### Dataset Coverage Analysis

| Embedding Method | Dimensionality | Coverage at Threshold |
|-----------------|---------------|----------------------|
| **PADL (learned)** | 128D | **Best across all thresholds** |
| Raw CLIP | 512D | Lower coverage |
| PCA-reduced CLIP | 128D | Lower coverage |

The learned 128D motion-language embeddings achieve superior dataset coverage compared to both raw 512D CLIP text embeddings and PCA-reduced 128D CLIP embeddings, indicating that the learned space better preserves motion-relevant semantic structure.

### Qualitative Demonstrations

PADL successfully demonstrates:
- Locomotion tasks (walk, run, sneak, hop) directed by language
- Combat skills (sword attacks, shield blocks) selected via text
- Combined task + skill commands (e.g., "go to the target while sneaking")
- Dynamic skill switching based on changing language instructions

### Training Scale

| Configuration | Value |
|--------------|-------|
| Parallel environments | 4,096 |
| Total training samples | ~7 billion |
| Simulated time | ~7 years |
| Wall-clock training time | ~2.5 days (single A100) |

## Metrics Used

- Coverage — fraction of motion dataset states within a threshold distance in the embedding space
- [[Episode Return]] — cumulative reward combining task and skill objectives
- Adversarial skill reward — discriminator-based measure of motion naturalness relative to reference clips

## Datasets Used

- Custom motion capture dataset — 131 clips (~9 minutes), 265 text captions, 37-DOF humanoid with sword and shield

## Related Papers

- [[DeepMimic]] — foundational work on physics-based motion imitation by Peng et al.; PADL extends this paradigm with language conditioning
- [[ASE]] — adversarial skill embeddings predecessor; PADL addresses [[ASE]]'s mode collapse via per-clip latent assignment and joint discriminator
- [[CALM]] — conditional adversarial latent models for directable characters; shares the goal of controllable physics-based animation
- [[MaskedMimic]] — unified physics-based character control through masked motion inpainting; concurrent work on versatile control interfaces
- [[LeVERB]] — language-conditioned humanoid whole-body control; applies similar language-to-motion ideas to real humanoid robots
- [[SuperPADL]] — direct successor that scales PADL to 5,000+ motions via progressive distillation
