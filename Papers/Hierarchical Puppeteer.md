---
tags: [paper, domain/robotics, domain/character-animation, method/masked-prediction, method/rl, lineage/jepa]
title: "Hierarchical World Models as Visual Whole-Body Humanoid Controllers"
authors: [Nicklas Hansen, Jyothir S V, Vlad Sobal, Yann LeCun, Xiaolong Wang, Hao Su]
year: 2024
arxiv: "https://arxiv.org/abs/2405.18418"
repo: "https://github.com/nicklashansen/puppeteer"
group: "World Models"
venue: "arXiv 2025"
domain: [robotics, character-animation]
method: [masked-prediction, rl]
lineage: [jepa]
predecessor: ["[[V-JEPA 2]]"]
importance: 3
aliases: [Puppeteer, Hierarchical Puppeteer, RL Puppeteer]
---

!PDFs/Hierarchical Puppeteer.pdf


# Hierarchical World Models as Visual Whole-Body Humanoid Controllers

## Summary
Puppeteer proposes a hierarchical world model for visual whole-body humanoid control that produces natural, human-like motions while solving diverse locomotion and navigation tasks. The key insight is to decompose the problem into two levels: a low-level proprioceptive tracking agent that follows reference motions via joint-level control, and a high-level visual puppeteer agent that synthesizes reference motions for the tracker based on visual observations and task rewards. Both agents are JEPA-style (Joint-Embedding Predictive Architecture) world models trained with model-based RL.

Evaluated on 8 tasks with a simulated 56-degree-of-freedom humanoid, Puppeteer achieves reward performance comparable to [[TD-MPC2]] on most tasks while producing motions that are overwhelmingly preferred by humans (97.6% preference rate in a user study with 46 participants). In contrast, end-to-end methods like SAC and [[DreamerV3]] fail to achieve meaningful performance within the same computational budget (3M environment steps). The hierarchical decomposition, combined with pretraining the low-level tracker on motion capture data, enables both efficient learning and natural motion quality. Published at ICLR 2025.

## Key Contributions
- Hierarchical world model architecture separating visual task planning (puppeteer) from motor execution (tracker)
- Data-driven approach using large-scale motion capture data to bootstrap natural motion generation without reward shaping or hand-crafted primitives
- First demonstration of visual whole-body humanoid control with natural motions using model-based RL
- 97.6% human preference rate over [[TD-MPC2]] in naturalness evaluation, while matching task performance
- Open-sourced model checkpoints for both hierarchical levels

## Architecture / Method
Puppeteer uses a two-level hierarchical architecture, where both levels are JEPA-style world models:

**Low-Level: Proprioceptive Tracking Agent**
- Input: 212-dimensional proprioceptive state (joint positions, velocities, etc.) + 15-dimensional reference command
- Output: joint torques for the 56-DoF humanoid
- Architecture: 5M parameter world model with 256-dim encoder, 512-dim MLP, 512-dim latent state
- Training: pretrained on large-scale MoCap dataset to track diverse human motions
- The tracker learns to follow any reference motion by imitating joint-level trajectories from motion capture data

**High-Level: Visual Puppeteer Agent**
- Input: 64x64 RGB images + proprioceptive state
- Output: 15-dimensional command vectors in [-1, 1] that serve as reference motions for the tracker
- Architecture: 5M parameter world model with same dimensions as tracker
- Training: trained with model-based RL using task rewards, with the low-level tracker frozen
- The puppeteer learns to synthesize reference commands that, when executed by the tracker, accomplish the downstream task

**Command Space:**
The 15-dimensional command vector is a compact representation of desired body motion, learned end-to-end. The puppeteer discovers how to use this interface to communicate task-relevant motions to the tracker.

**Q-Functions:**
Both agents use an ensemble of 5 Q-functions for value estimation, following [[TD-MPC2]]'s approach.

**Key Design Choices:**
- Hierarchical decomposition enables leveraging MoCap data without restricting the policy to a fixed set of skills
- The frozen tracker ensures motion naturalness is preserved during high-level task learning
- JEPA-style world models enable efficient imagination-based planning

## Results

### Table 1: Naturalness Metrics (Hurdles Task)

| Metric | [[TD-MPC2]] | Puppeteer |
|--------|---------|-----------|
| Episode Length | 70.7 +/- 5.5 | **100.6 +/- 1.0** |
| Torso Height (cm) | 85.9 +/- 4.7 | **96.0 +/- 0.2** |

Puppeteer maintains a significantly higher torso height (96 cm vs 86 cm), indicating upright, human-like posture, while [[TD-MPC2]] adopts crouched, unnatural gaits. The longer episode length indicates Puppeteer completes tasks more reliably without falling.

### Table 2: Human Preference Study (n=46 participants, 5 visual tasks)

| Task | [[TD-MPC2]] Preferred | Equal | Puppeteer Preferred |
|------|-------------------|-------|---------------------|
| Corridor | 0.0% | 2.2% | **97.8%** |
| Hurdles | 0.0% | 0.0% | **100.0%** |
| Walls | 2.2% | 4.3% | **93.5%** |
| Gaps | 0.0% | 0.0% | **100.0%** |
| Stairs | 2.2% | 6.5% | **91.3%** |
| **Aggregate** | **0.4%** | **2.0%** | **97.6%** |

The human preference results are striking: across all 5 visual tasks, Puppeteer is overwhelmingly preferred for motion naturalness. On Hurdles and Gaps, 100% of participants preferred Puppeteer. Even on Stairs (where [[TD-MPC2]] achieves higher returns), 91.3% still prefer Puppeteer's motion quality. This demonstrates that Puppeteer addresses a fundamental limitation of end-to-end trained world models -- they optimize reward at the expense of natural behavior (reward hacking).

### Table 3: Task Performance Summary

| Task | Type | SAC | [[DreamerV3]] | [[TD-MPC2]] | Puppeteer |
|------|------|-----|-----------|---------|-----------|
| Stand | Proprioceptive | Fails | Fails | Comparable | Comparable |
| Walk | Proprioceptive | Fails | Fails | Comparable | Comparable |
| Run | Proprioceptive | Fails | Fails | Comparable | Comparable |
| Corridor | Visual | Fails | Fails | Comparable | Comparable |
| Hurdles | Visual | Fails | Fails | Comparable | Comparable |
| Walls | Visual | Fails | Fails | Comparable | Comparable |
| Gaps | Visual | Fails | Fails | Comparable | Comparable |
| Stairs | Visual | Fails | Fails | Higher | Lower |

Performance of Puppeteer is comparable to [[TD-MPC2]] across all tasks except Stairs, where [[TD-MPC2]] achieves higher returns by exploiting unnatural crouching behaviors (reward hacking). SAC and [[DreamerV3]] fail to achieve meaningful performance within the 3M step budget on any task, highlighting the difficulty of high-dimensional visual humanoid control for non-hierarchical methods.

## Metrics Used
- [[Episode Return]] — cumulative reward per episode; primary performance metric for all 8 tasks
- [[Human Preference Rate]] — percentage of human evaluators preferring one method's motion quality over another (n=46 participants)
- Episode Length — number of timesteps survived; proxy for stability and task completion
- Torso Height — average height of humanoid torso during locomotion; proxy for posture naturalness
- [[Motion Naturalness]] — qualitative assessment via human evaluation comparing motion quality

## Datasets Used
- [[CMU Motion Capture Database]] — large-scale human motion capture dataset used to pretrain the low-level tracking agent
- Custom Humanoid Simulation Suite — 8 tasks (3 proprioceptive, 5 visual) with a 56-DoF simulated humanoid in MuJoCo

## Related Papers
- [[TD-MPC2]] — scalable world model for continuous control; primary baseline and architectural inspiration for the JEPA-style world model
- [[DreamerV3]] — general-purpose world model; baseline that fails on high-dimensional humanoid control
- SAC — model-free soft actor-critic baseline
- [[DreamerV1]] — earlier [[DreamerV1|Dreamer]] agent
- JEPA — Joint-Embedding Predictive Architecture proposed by LeCun; conceptual foundation for the world model design
- PlaNet — model-based planning agent
