---
tags: [paper, domain/character-animation, method/vae, method/rl]
title: "MuscleVAE: Model-Based Controllers of Muscle-Actuated Characters"
authors: [Yusen Feng, Xiyan Xu, Libin Liu]
year: 2023
arxiv: "https://arxiv.org/abs/2312.07340"
repo: "https://github.com/PKU-MoCCA/MuscleVAE"
group: "World Models"
venue: "SIGGRAPH 2023"
domain: [character-animation]
method: [vae, rl]
lineage: []
predecessor: ["[[MVAE]]"]
importance: 3
aliases: [MuscleVAE, Muscle VAE]
---

!PDFs/MuscleVAE.pdf

# MuscleVAE: Model-Based Controllers of Muscle-Actuated Characters

## Summary
MuscleVAE presents a simulation and control framework for generating biomechanically plausible motion for muscle-actuated characters. The core contribution is extending the [[ControlVAE]] paradigm from torque-driven to muscle-actuated characters by integrating Hill-type muscle models with fatigue dynamics. A key innovation is a novel muscle-space PD control strategy that operates directly on muscle target lengths rather than raw activation signals, dramatically improving training convergence for the high-dimensional musculoskeletal control problem.

The framework incorporates the 3CC-r (Three-Compartment Controller revised) fatigue dynamics model into the Hill-type muscle model, enabling the simulation of realistic fatigue development and recovery during prolonged activities. This creates a natural evolution of motion style as muscles fatigue, with the character automatically adapting its movement patterns. The musculoskeletal character model has 23 rigid bodies actuated by 284 muscles, simulated at 120 Hz for muscle dynamics and 20 Hz for policy updates.

Published at SIGGRAPH Asia 2023 by researchers at Peking University and the National Key Lab of General AI, MuscleVAE demonstrates that a VAE-based generative model can learn rich latent representations encoding not only motion features but also muscle control and fatigue properties from unstructured motion capture data. The model-based training approach using a differentiable world model enables efficient gradient-based optimization, producing high-fidelity motions across tasks including motion tracking, random motion generation, velocity-conditioned locomotion, and fatigue-aware control.

## Key Contributions
- Integrates the 3CC-r fatigue dynamics model into Hill-type muscle simulation, enabling realistic fatigue development and recovery that naturally alters motion style during prolonged activities
- Proposes a muscle-space PD control strategy where actions specify target muscle lengths rather than raw activation signals, with target lengths computed as l_M = (a + 1.0) * l_M^tpose, substantially improving training convergence over vanilla activation control
- Develops MuscleVAE, a generative model that learns latent representations encoding motion features, muscle control signals, and fatigue properties jointly from unstructured motion capture data
- Employs a differentiable world model to approximate musculoskeletal dynamics, enabling efficient model-based training via gradient backpropagation through the learned dynamics
- Demonstrates downstream tasks including motion tracking, random motion sampling, velocity-conditioned locomotion, and fatigue-aware motion generation on a 23-body, 284-muscle character

## Architecture / Method
The MuscleVAE framework consists of four main components: musculoskeletal simulation, muscle-space control, the MuscleVAE generative model, and a differentiable world model.

**Musculoskeletal Simulation:**

The character model comprises 23 rigid bodies connected by joints with a total of 284 muscles. Each muscle is modeled using the Hill-type muscle model with three elements: a contractile element (CE), a parallel elastic element (PE), and a series elastic tendon. Muscle force is computed as:

F_M = F_max * (f_L(l_CE) * f_V(v_CE) * alpha + f_PE(l_CE))

where F_max is maximum isometric force, f_L and f_V are force-length and force-velocity functions, and alpha is the activation level. The simulation runs at 120 Hz for muscle dynamics and 480 Hz for rigid body physics.

**Fatigue Dynamics (3CC-r Model):**

The fatigue model tracks three compartments of muscle actuator state: Active (M_A), Resting (M_R), and Fatigued (M_F), with M_A + M_R + M_F = 1. The compartment transitions are governed by differential equations with fatigue coefficient F and recovery coefficient R_r. The effective maximum activation is clamped to M_A, so fatigued muscles cannot produce their full force, leading to natural motion degradation under sustained effort.

**Muscle-Space PD Control:**

Rather than directly outputting activation signals (which leads to training instability), the policy outputs actions that specify target muscle lengths:

l_M_target = (a + 1.0) * l_M^tpose

A PD controller then computes the desired muscle force to track this target length. The resulting force is clipped to the feasible range [0, F_max * M_A], ensuring physical plausibility and fatigue-awareness. This approach converts the high-dimensional muscle control problem into a more tractable length-tracking problem.

**MuscleVAE Model:**

The generative model follows the [[ControlVAE]] architecture adapted for muscle-actuated characters:
- **State representation:** Skeleton state (joint positions, velocities, orientations) plus muscle state (muscle lengths, activations, fatigue compartment values M_A, M_R, M_F)
- **Policy:** pi(a|s, z) maps current state s and latent code z to muscle-space actions
- **Posterior encoder:** q(z|s, s_skeleton_next) encodes the next-state transition into the latent space
- **Prior:** p(z|s) state-dependent prior for latent code sampling at inference

**Differentiable World Model:**

A learned neural network omega approximates the musculoskeletal dynamics, mapping (state, action) pairs to next states. This enables gradient-based optimization by backpropagating through the world model during training, avoiding the need for expensive simulation rollouts during policy updates. The world model is iteratively refined alongside the policy.

**Training Procedure:**

Training alternates between: (1) extracting short motion clips from the dataset, (2) encoding them via the posterior to get latent codes, (3) decoding latent codes with the policy and rolling out via the world model, (4) minimizing reconstruction error (skeleton state + muscle length) and KL divergence, and (5) updating the world model with new simulation data. Training runs for approximately 20,000 iterations on the LaFAN motion dataset.

## Results

MuscleVAE's evaluation is primarily qualitative, demonstrated through motion tracking fidelity, random motion generation diversity, velocity-conditioned control, and fatigue dynamics visualization. The paper does not include traditional numerical comparison tables but instead presents results through motion sequences and learning curves.

### Ablation: Muscle-Space Control vs. Vanilla Activation Control (Figure 12)

| Control Strategy | Outcome |
|---|---|
| MuscleVAE + Muscle-Space PD Control (proposed) | Successful convergence; character learns stable locomotion and dynamic motions |
| MuscleVAE + Vanilla Activation Control | Fails to converge; character cannot maintain balance; reward plateaus early with no growth |

The ablation study demonstrates that the proposed muscle-space PD control strategy is critical for training feasibility. With vanilla activation control (directly outputting muscle activations), the system struggles to find a feasible MuscleVAE and the character is unable to maintain balance.

### Task Demonstrations

| Task | Description |
|---|---|
| Motion Tracking | Accurately reconstructs walking, running, jumping, hopping, and turning from reference clips |
| Random Motion Generation | Samples diverse, natural-looking motions by randomly sampling latent codes from the prior |
| Velocity Control | Generates locomotion at user-specified target velocities with smooth transitions |
| Fatigue Simulation | Motion style naturally degrades under sustained effort; character adapts gait as muscles fatigue |
| Jump Spin Kick | Tracks highly dynamic motion from the SFU Motion Capture Database |

### Fatigue Analysis (Figures 7-11)

The fatigue dynamics produce observable effects on motion: as the active compartment M_A decreases through sustained effort, the character's stride length shortens, speed decreases, and motion becomes less energetic. Recovery occurs when muscles are rested, with natural transitions between fatigued and recovered states.

## Metrics Used
- Reconstruction Loss — combined skeleton state error and muscle length error with discount factor, used as the primary training objective
- [[Episode Return]] — cumulative reward used to evaluate training convergence in the ablation study comparing muscle-space vs. activation control
- KL Divergence — measures posterior-prior distribution gap in the VAE latent space
- Activation Regularization — L1 and L2 norms on muscle activation levels to encourage efficient muscle usage
- [[Motion Naturalness]] — qualitative assessment of generated motions through visual inspection and fatigue-induced style changes

## Datasets Used
- LaFAN (Ubisoft La Forge Animation) — approximately 25 minutes of motion capture data including walking, running, turning, hopping, and jumping at 30 Hz, used to train the MuscleVAE generative model
- SFU Motion Capture Database — used for the "Jump Spin Kick" demonstration sequence to show tracking of highly dynamic motions

## Related Papers
- [[MVAE]] — original [[MVAE|Motion VAE]] predecessor; MuscleVAE extends the VAE-based motion generation paradigm from torque-driven to muscle-actuated characters
- [[DeepMimic]] — foundational motion imitation framework using physics-based RL; MuscleVAE tackles the same motion tracking problem but with biologically plausible muscle actuation
- [[Hierarchical Puppeteer]] — hierarchical world model for humanoid control; both approaches use learned latent spaces for character control but MuscleVAE operates at the muscle level
- [[DreamerV3]] — general model-based RL with learned world models; MuscleVAE similarly uses a differentiable world model but specialized for musculoskeletal dynamics
- [[TD-MPC2]] — scalable model-based continuous control; MuscleVAE's model-based training shares the principle of learning dynamics for policy optimization
