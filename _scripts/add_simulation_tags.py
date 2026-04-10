#!/usr/bin/env python3
"""
Add physics-simulation or motion tag to paper frontmatter.

physics-simulation: papers that run a physics engine (MuJoCo, Bullet, IsaacGym)
                    to simulate character/robot body dynamics with forces/torques
motion:            papers about motion understanding/generation/prediction
                    without a physics engine (video-based, kinematic, learned simulators)
"""

import re
from pathlib import Path

VAULT = Path("/home/omar/Repos/physical-intelligence-vault")

# Papers that use physics engines for character/robot simulation
PHYSICS_SIMULATION = {
    # Character animation (Bullet, MuJoCo, IsaacGym)
    "DeepMimic",          # Bullet physics, character imitation
    "MVAE",               # Physics-simulated character control
    "Hierarchical Puppeteer",  # MuJoCo humanoid
    "Vid2Player3D",       # IsaacGym tennis
    "LeVERB",             # IsaacSim humanoid
    "Eureka",             # Isaac Gym dexterous manipulation
    # Will also apply to: PhysicsVAE, ControlVAE, MuscleVAE, ASE, CALM, MaskedMimic
    "PhysicsVAE",
    "ControlVAE",
    "MuscleVAE",
    "ASE",
    "CALM",
    "MaskedMimic",
    # RL in physics-simulated environments
    "DreamerV1",          # MuJoCo DMC
    "DreamerV2",          # Atari ALE
    "DreamerV3",          # MuJoCo, Atari, Crafter, Minecraft
    "TD-MPC2",            # MuJoCo
    "TD-JEPA",            # MuJoCo DMC
    "IRIS",               # Atari
    "DIAMOND",            # Atari
    "PLDM",              # MuJoCo
    "Le-World-Model",     # MuJoCo Push-T
    "Stable World Model", # MuJoCo evaluation
    "ACT-JEPA",           # MuJoCo Push-T, ManiSkill
}

# Papers about motion/video without physics engine
MOTION = {
    "V-JEPA",             # Video representation learning
    "V-JEPA 2",           # Video understanding + planning (no physics sim)
    "V-JEPA 2.1",         # Dense video features
    "I-JEPA",             # Image representation learning
    "Le-JEPA",            # Image/video SSL
    "PEVA",               # Egocentric video prediction from body motion
    "Dream Dojo",         # Video world model from human video
    "Hunyuan World 1.5",  # Video world model with 3D
    "Genie 2",            # Generative interactive environments (neural, no physics)
    "NVIDIA Cosmos",      # Video generation world model
    "UniPi",              # Video generation as planning
    "UniSim",             # Neural simulator (learned, not physics engine)
    "Learning Latent Action World Models In The Wild",  # Latent action from video
    "Pi0",                # VLA (real robot, no physics sim in method)
    "Pi0.5",
    "Pi0.6",
    "GR00T",              # VLA (trains in sim but method is motion/vision)
    "Gemini Robotics",    # VLA
    "RT-2",               # VLA
    "Octo",               # Robot policy
    "OpenVLA",            # VLA
}

def add_tag(filepath, tag):
    content = filepath.read_text()

    # Find the tags line in frontmatter
    match = re.search(r'^tags:\s*\[([^\]]*)\]', content, re.MULTILINE)
    if not match:
        return False

    existing_tags = match.group(1)

    # Don't add if already present
    if tag in existing_tags:
        return False

    new_tags = existing_tags.rstrip() + ", " + tag
    new_line = f"tags: [{new_tags}]"
    content = content[:match.start()] + new_line + content[match.end():]

    filepath.write_text(content)
    return True

count = 0
for f in sorted((VAULT / "Papers").glob("*.md")):
    name = f.stem
    if name in PHYSICS_SIMULATION:
        if add_tag(f, "physics-simulation"):
            count += 1
            print(f"  +physics-simulation: {name}")
    elif name in MOTION:
        if add_tag(f, "motion"):
            count += 1
            print(f"  +motion: {name}")
    else:
        print(f"  (untagged): {name}")

print(f"\nTagged {count} papers")
