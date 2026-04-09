---
tags: [paper, vla]
title: "pi*0.6: a VLA That Learns From Experience"
authors: [Ali Amin, Raichelle Aniceto, Ashwin Balakrishna, Kevin Black, Ken Conley, Grace Connors, James Darpinian, Karan Dhabalia, Jared DiCarlo, Danny Driess, Michael Equi, Adnan Esmail, Yunhao Fang, Chelsea Finn, Catherine Glossop, Thomas Godden, Ivan Goryachev, Lachy Groom, Hunter Hancock, Karol Hausman, Gashon Hussein, Brian Ichter, Szymon Jakubczak, Rowan Jen, Tim Jones, Ben Katz, Liyiming Ke, Chandra Kuchi, Marinda Lamb, Devin LeBlanc, Sergey Levine, Adrian Li-Bell, Yao Lu, Vishnu Mano, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Allen Z. Ren, Charvi Sharma, Lucy Xiaoyang Shi, Laura Smith, Jost Tobias Springenberg, Kyle Stachowicz, Will Stoeckle, Alex Swerdlow, James Tanner, Marcel Torne, Quan Vuong, Anna Walling, Haohuan Wang, Blake Williams, Sukwon Yoo, Lili Yu, Ury Zhilinsky, Zhiyuan Zhou]
year: 2025
arxiv: "https://arxiv.org/abs/2511.14759"
group: "VLA Models"
importance: 
aliases: [pi0.6, pi-zero-point-six, pi_0.6, pi*0.6, RECAP]
---

!PDFs/Pi0.6.pdf


# pi*0.6: a VLA That Learns From Experience

## Summary

pi*0.6 is Physical Intelligence's third-generation VLA model that introduces reinforcement learning from real-world experience to improve generalist robot policies. The paper presents RECAP (RL with Experience and Corrections via Advantage-conditioned Policies), a general-purpose method for training VLAs with RL via advantage conditioning. RECAP incorporates heterogeneous data sources -- demonstrations, on-policy autonomous rollouts, and expert teleoperated interventions (corrections) -- into a unified self-improvement process.

The key insight is that VLAs can improve through iterative real-world deployment rather than relying solely on curated demonstration data. pi*0.6 builds on the [[Pi0|pi0]] architecture with a Gemma 3 4B VLM backbone and an 860M parameter action expert. The model is first pre-trained with offline RL across multiple tasks, then specialized through RECAP iterations involving autonomous data collection, distributional value function training, and advantage-conditioned policy extraction.

RECAP more than doubles task throughput and roughly halves the task failure rate on challenging tasks. The resulting pi*0.6 model can fold laundry in real homes, reliably assemble boxes, and make espresso drinks using professional equipment -- tasks that were previously unreliable or impossible for prior [[Pi0|pi0]] variants.

## Key Contributions

- RECAP method: A general-purpose RL framework for VLAs using advantage conditioning with heterogeneous data (demonstrations + on-policy rollouts + expert corrections)
- Distributional value function for estimating advantages from mixed-quality data sources
- Advantage-conditioned policy extraction using a binarized improvement indicator
- Demonstration that offline RL pre-training followed by online RECAP iterations enables significant real-world performance gains
- Deployment-ready results: reliable laundry folding in real homes, box assembly, and espresso making
- RECAP outperforms alternative RL methods (AWR, PPO) when applied to VLAs

## Architecture / Method

**Model Architecture:**
- VLM backbone: Gemma 3 4B
- Action expert: 860M parameters
- Discretized action bins: 201
- Action chunk frequency: 50 Hz

**Value Function:**
- 670M parameter VLM backbone
- Distributional value function p_phi(V | o_t, l) mapping observations and language to a distribution over B discretized value bins
- Trained with cross-entropy loss on discretized returns

**RECAP Method (three iterated steps):**

1. **Data Collection:** Autonomous rollouts with optional expert teleoperated interventions (corrections). Heterogeneous data includes demonstrations, on-policy episodes, and correction episodes.

2. **Value Function Training:** Learn distributional value function using all collected data. Reward structure:
   - Success: 0 at terminal step
   - Failure: -C_fail (large constant penalty)
   - Each step: -1 (time penalty)
   - Values normalized to (-1, 0) range per task

3. **Advantage-Conditioned Policy Extraction:** Train policy with binary improvement indicator:
   I_t = 1(A^{pi_ref}(o_t, a_t, l) > epsilon_l)
   
   Policy objective minimizes: -log pi_theta(a_t | o_t, l) - alpha * log pi_theta(a_t | I_t, o_t, l)

**Hyperparameters:**
- Advantage dropout: 30%
- Advantage threshold percentile: 30% (pre-training), 40% (fine-tuning)
- N-step lookahead for advantage: 50 steps

**Data Collection Per Task:**
- 300-600 autonomous episodes per RECAP iteration
- 280-360 correction episodes per task

## Results

### Table 1: RECAP Performance Improvements

| Task | Metric | Improvement with RECAP |
|------|--------|----------------------|
| Diverse laundry | [[FPS]] | >2x |
| Espresso making | [[FPS]] | >2x |
| T-shirt folding | [[FPS]] | ~50% improvement across iterations |
| All hard tasks | Failure rate | Roughly halved |

RECAP more than doubles task throughput on the most challenging tasks while approximately halving the failure rate.

### Table 2: Baseline Comparison ([[Pi0|pi0]].6 out-of-the-box capabilities)

| Task | [[Pi0]].6 Baseline | pi*0.6 (with RECAP) |
|------|:--------------:|:-------------------:|
| Laundry folding in real homes | Reliable | More reliable + faster |
| Box assembly | ~20% success | Significantly improved |
| Espresso making | Limited | Reliable |

The base [[Pi0|pi0]].6 model (without RECAP) can fold laundry reliably and assemble boxes ~20% of the time. RECAP training dramatically improves both reliability and speed.

### Table 3: RL Method Comparison

| Method | Relative [[FPS]] (Laundry) |
|--------|:----------------------------:|
| [[Pi0.5]] (no RL) | Baseline |
| [[Pi0]].6 (supervised only, no advantage) | Improved |
| AWR (advantage-weighted regression) | Moderate improvement |
| PPO variant (with SPO constraints) | Moderate improvement |
| **pi*0.6 (RECAP)** | **Highest throughput by far** |

RECAP applied to pi*0.6 achieves the highest throughput for the laundry task compared to AWR and PPO, demonstrating that advantage conditioning with heterogeneous data outperforms standard RL approaches for VLAs.

### Table 4: Evaluation Task Details

| Task | Items | Time Limit | Description |
|------|:-----:|:----------:|-------------|
| Laundry folding | 11 item types | 200-600 sec | Fold diverse clothing items (t-shirts, shorts, etc.) |
| Espresso making | Multi-step | 200-600 sec | Full espresso preparation with professional equipment |
| Box assembly | Single box | 200-600 sec | Fold and assemble cardboard box from flat |

### Table 5: Data Sources

| Source | Description |
|--------|-------------|
| Pre-training demonstrations | Tens of thousands of hours across multiple tasks and robots |
| On-policy autonomous episodes | 300-600 per task per RECAP iteration |
| Expert correction episodes | 280-360 per task per RECAP iteration |

The training pipeline combines massive pre-training data with relatively modest amounts of online interaction data, making the approach practical for real-world deployment.

## Metrics Used

- [[Task Throughput]] -- primary metric combining success rate and speed, measured as tasks completed per hour
- [[Success Rate]] -- proportion of successful episodes out of total attempts
- [[Failure Rate]] -- proportion of failed episodes, roughly halved by RECAP
- [[Task Completion Time]] -- time to complete each task, used in throughput calculation
- Advantage Value -- estimated advantage used for conditioning policy training via the distributional value function

## Datasets Used

- Physical Intelligence Pre-training Dataset -- tens of thousands of hours of multi-task, multi-robot demonstrations used for offline RL pre-training
- RECAP On-Policy Data -- autonomous rollout data collected during iterative deployment (300-600 episodes per task per iteration)
- RECAP Expert Corrections -- teleoperated intervention data collected during autonomous execution (280-360 episodes per task)

## Related Papers

- [[Pi0]] -- foundational VLA architecture that pi*0.6 builds upon
- [[Pi0.5]] -- predecessor model with open-world generalization but without RL
- [[GR00T]] -- NVIDIA's VLA for humanoid robots, uses imitation learning without RL self-improvement
- [[Gemini Robotics]] -- Google DeepMind's VLA model, evaluated on similar manipulation tasks
