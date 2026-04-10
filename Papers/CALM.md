---
tags: [paper, domain/character-animation, method/adversarial, method/rl, lineage/peng]
title: "CALM: Conditional Adversarial Latent Models for Directable Virtual Characters"
authors: [Chen Tessler, Yoni Kasten, Yunrong Guo, Shie Mannor, Gal Chechik, Xue Bin Peng]
year: 2023
arxiv: "https://arxiv.org/abs/2305.02195"
repo: "https://github.com/NVlabs/CALM"
group: "World Models"
venue: "SIGGRAPH 2023"
domain: [character-animation]
method: [adversarial, rl]
lineage: [peng]
predecessor: ["[[ASE]]"]
importance: 4
aliases: [CALM, Conditional Adversarial Latent Models]
---

!PDFs/CALM.pdf

# CALM: Conditional Adversarial Latent Models for Directable Virtual Characters

## Summary
CALM extends [[ASE]]'s adversarial skill embedding framework with two critical additions: a conditional discriminator and a learned motion encoder, enabling users to directly specify which style of motion a physically simulated character should perform. Where [[ASE]] learns a latent skill space that maps codes to behaviors but provides no mechanism for selecting a particular behavior by description, CALM closes this gap by jointly training a motion encoder that maps reference motion clips to latent codes on a hyperspherical latent space. The conditional discriminator then ensures that the policy, when given a particular latent code, produces motion that matches the reference clip associated with that code.

The result is a directable latent space with clear semantic structure: similar motions (e.g., different walking styles) cluster together, dissimilar motions (e.g., running vs. crouching) are well-separated, and interpolation between codes produces smooth, physically plausible motion blends. This semantic structure is quantified by Fisher's concentration coefficient (0.23 for CALM vs. 0.68 for [[ASE]], lower is better separation) and demonstrated through a user study where human raters correctly matched CALM's generated motions to textual descriptions 78% of the time, compared to only 35% for [[ASE]].

CALM's directable latent space enables a qualitatively new capability: zero-shot task composition, where a high-level controller can specify both what to do (reach a location, strike a target) and how to do it (run, walk, crouch-walk, kick, use shield, use sword) without any additional training for new style combinations. The paper demonstrates this on heading control, location tasks with three ending styles, and strike tasks with three attack styles, achieving high success rates across all combinations. The approach was developed at NVIDIA Research with affiliations at Technion, Bar-Ilan University, and Simon Fraser University.

## Key Contributions
- Introduces a conditional discriminator that conditions adversarial training on latent codes, forcing the policy to produce motion matching the specific reference clip encoded by each code, eliminating [[ASE]]'s mode collapse problem
- Proposes a learned motion encoder that maps motion sequences to a 64-dimensional latent vector on an L2 unit hypersphere, creating a semantically structured latent space without external supervision
- Achieves directable control: users specify both the task objective and the desired motion style via latent conditioning, enabling zero-shot composition of locomotion styles with downstream tasks
- Demonstrates superior latent space quality: Fisher's concentration of 0.23 (vs. [[ASE]]'s 0.68), Inception Score of 19.8 (vs. 18.6), and 78% human classification accuracy (vs. 35% for [[ASE]])
- Shows zero-shot generalization to unseen task-style combinations (e.g., reach a location while crouch-walking, then celebrate) without additional fine-tuning

## Architecture / Method
CALM builds on [[ASE]]'s hierarchical LLC/HLC architecture but replaces [[ASE]]'s unconditional adversarial training with a conditional framework centered on two new components.

**Motion Encoder:**

The encoder E(M) maps a motion sequence M (a window of state transitions from the mocap dataset) to a 64-dimensional latent vector z on the L2 unit hypersphere. Key design choices:

- **Spherical constraint:** Latent codes are projected onto the unit hypersphere (||z|| = 1), improving training stability and preventing out-of-distribution sampling during inference
- **Alignment loss:** Overlapping subsequences from the same motion clip should map to similar latent codes, encouraging local temporal consistency
- **Uniformity loss:** Latent codes should be spread across the hypersphere to prevent collapse, encouraging maximal use of the latent space
- **No auxiliary supervision:** The encoder is trained end-to-end via policy gradients; semantic structure emerges purely from the dynamics of adversarial training

**Conditional Discriminator:**

The discriminator D(s, s' | z) receives state transitions (s, s') and a conditioning latent code z. During training:

- **Real samples:** A motion clip is sampled from the dataset, encoded to z via the motion encoder, and paired with a transition from that same clip. The discriminator should classify these as real.
- **Fake samples:** The policy generates a transition conditioned on the same z. The discriminator should classify these as fake.
- **Effect:** The policy must produce motion that matches the specific clip encoded by z, not just any plausible motion. This is the key mechanism that creates the directable, semantically meaningful latent space.

**Negative Samples (Contrastive Training):**

CALM additionally trains the discriminator with negative samples: real transitions paired with mismatched latent codes (from different clips). This teaches the discriminator to reject plausible-but-wrong style matches, further sharpening the latent space's semantic structure.

**High-Level Controller (HLC):**

For downstream tasks, an HLC selects both a latent code z (specifying motion style) and timing for skill transitions. The HLC can be trained with RL for precision tasks (e.g., heading control with a specific locomotion style) or used in zero-shot mode via a simple finite state machine (FSM) that sequences motion styles for compound tasks (e.g., run to a location, then celebrate).

**Character and Simulation:**

- Same 37-DOF humanoid with sword and shield as [[ASE]]
- IsaacGym GPU-based parallel simulation
- Motion dataset: Reallusion mocap library with locomotion, combat, and idle behaviors

## Results

### Table 1: Pre-Training Evaluation
| Metric | CALM | [[ASE]] |
|--------|:----:|:---:|
| Encoder Quality (Fisher's Concentration) (lower is better) | **0.23** | 0.68 |
| Diversity (Inception Score) (higher is better) | **19.8 +/- 0.1** | 18.6 +/- 0.4 |
| Controllability (Generation Accuracy) (higher is better) | **78%** | 35% |

CALM achieves substantially better latent space quality across all three metrics. Fisher's concentration of 0.23 (vs. 0.68) indicates that motion categories are far more tightly clustered and well-separated in CALM's latent space. The Inception Score of 19.8 confirms that randomly sampled latent codes produce diverse motions. Most strikingly, human raters correctly identified the intended motion from CALM's generations 78% of the time vs. only 35% for [[ASE]], demonstrating that CALM's latent space is genuinely directable.

### Table 2: Zero-Shot Task Composition ([[Success Rate]])
| Motion Style | Heading | Location (Idle) | Location (Celebrate) | Location (Crouch) | Strike (Kick) | Strike (Shield) | Strike (Sword) |
|-------------|:-------:|:---------------:|:-------------------:|:-----------------:|:-------------:|:--------------:|:--------------:|
| Run | 0.92 | 0.98 | 0.96 | 0.99 | 1.0 | 0.96 | 0.99 |
| Walk | 0.81 | 0.92 | 0.99 | 0.98 | 1.0 | 1.0 | 0.97 |
| Crouch Walk | 0.94 | 0.91 | 0.98 | 0.99 | 0.99 | 1.0 | 0.97 |

Zero-shot task composition achieves high success rates (0.81-1.0) across all combinations of locomotion style and task objective, without any task-specific fine-tuning for these combinations. The character can run/walk/crouch-walk to a location, then seamlessly transition to idle/celebrate/crouch, or approach and strike with kick/shield/sword, all controlled via latent code selection.

### Table 3: Ablation Study
| Configuration | Concentration (lower is better) | Inception Score (higher is better) | Accuracy (higher is better) |
|---------------|:------:|:------:|:------:|
| CALM (full) | **0.23** | **19.8 +/- 0.11** | **78%** |
| w/o negative samples | 0.24 | 15.7 +/- 0.07 | 62% |
| w/o negative samples, w/o regularization | 0.35 | 12.8 +/- 0.05 | 61% |

Removing negative samples from discriminator training reduces Inception Score from 19.8 to 15.7 and generation accuracy from 78% to 62%, confirming that contrastive training is critical for sharp latent space semantics. Further removing alignment/uniformity regularization degrades Fisher's concentration from 0.24 to 0.35, showing the regularization prevents latent space collapse.

## Metrics Used
- [[Motion Naturalness]] — enforced via the conditional adversarial discriminator; the style reward ensures generated motions are indistinguishable from the reference mocap dataset
- [[Success Rate]] — used for zero-shot task composition evaluation (Table 2), measuring whether the character successfully completes the task (heading, location, strike) with the specified motion style
- [[Human Preference Rate]] — 78% generation accuracy in the user study where human raters classified generated motions against textual descriptions (40 reference motions, 3 generations each)
- Fisher's Concentration Coefficient — measures class separability of motion categories in the latent space (lower = better separation); 0.23 for CALM vs. 0.68 for [[ASE]]
- Inception Score — measures diversity of motions generated from randomly sampled latent codes (higher = more diverse)

## Datasets Used
- [[CMU Motion Capture Database]] — the Reallusion mocap library with locomotion (run, walk, crouch-walk), sword/shield combat, acrobatics, and idle behaviors for the 37-DOF humanoid character; same dataset as [[ASE]], no segmentation or labeling required

## Related Papers
- [[ASE]] — direct predecessor; CALM extends [[ASE]] by replacing the unconditional discriminator with a conditional one and adding a motion encoder, solving [[ASE]]'s mode collapse and enabling directable control
- [[DeepMimic]] — foundational motion imitation work that both [[ASE]] and CALM build upon; [[DeepMimic]] tracks a single reference clip, while CALM learns a directable latent space over an entire motion dataset
- [[MVAE]] — VAE-based alternative for character control; CALM's GAN-based approach avoids the posterior collapse issues of VAEs and achieves sharper, more diverse motion generation
- [[Hierarchical Puppeteer]] — hierarchical visual humanoid control with tracker/puppeteer architecture; CALM's LLC/HLC hierarchy is conceptually similar but operates in a semantically structured adversarial latent space rather than visual observation space
- [[Vid2Player3D]] — Peng's tennis simulation using similar physics-based skills; CALM's directable latent space could enable style-conditioned athletic movements
- [[Eureka]] — automated reward design for locomotion and manipulation; CALM demonstrates that complex behaviors emerge from simple task rewards when combined with a pre-trained directable skill space
- [[DreamerV3]] — general model-based RL; both learn latent representations, but CALM's is specifically structured for physics-based character animation with adversarial motion priors
- [[AMP]] — foundational predecessor in the [[DeepMimic]] -> [[AMP]] -> [[ASE]] -> CALM lineage; introduces the adversarial motion prior that CALM's conditional discriminator extends with latent code conditioning
