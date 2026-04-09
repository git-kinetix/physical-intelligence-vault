---
tags: [metric]
aliases: [Search Time, Planning Latency]
category: "efficiency"
higher_is_better: false
---

# Planning Time

## Definition
Planning Time measures the computational time required for a model-based agent to perform planning or search using its learned world model before committing to an action. This includes the time spent on forward simulation, tree search, trajectory optimization, or other planning procedures within the model's latent or observation space.

## Formula
N/A — typically measured directly as wall-clock time for the planning computation, reported in milliseconds or seconds. May also be characterized by the number of planning steps or rollouts:

$$\text{Planning Time} \propto K \times T \times C_{\text{model}}$$

where $K$ is the number of candidate trajectories, $T$ is the planning horizon, and $C_{\text{model}}$ is the cost of a single model forward pass.

## Interpretation
- Low planning time enables faster decision making and higher control frequencies, critical for real-time robotic systems.
- High planning time may yield better decisions (more thorough search) but limits real-time applicability.
- The tradeoff between planning depth and computational cost is a central design consideration in model-based RL and robotics.
- Lower is better (for deployment); however, some additional planning time may improve decision quality.

## Common Usage
Used in model-based reinforcement learning and robotic planning to evaluate the computational overhead of the planning process. It is especially relevant when comparing methods that use different amounts of search (e.g., MPC with varying horizons, tree search with different branching factors) or when assessing real-time deployment feasibility.

## Papers Using This Metric
- [[V-JEPA 2]] — measuring planning overhead in world model-based robotic control
- [[Le-World-Model]] — evaluating the computational cost of model-based planning approaches
