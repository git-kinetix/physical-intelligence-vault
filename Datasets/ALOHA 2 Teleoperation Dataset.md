---
tags: [dataset]
aliases: [ALOHA Unleashed Dataset, ALOHA 2 Dataset]
category: "robotics"
year: 2024
---

# ALOHA 2 Teleoperation Dataset

## Description
The ALOHA 2 Teleoperation Dataset is a bimanual robot manipulation dataset collected on the ALOHA 2 platform from Google DeepMind. It contains over 26,000 real-world demonstrations across five challenging tasks (hanging a shirt, tying shoelaces, replacing a robot finger, inserting gears, stacking kitchen items) and 2,000 demonstrations for three simulated tasks, collected via puppeteering-based teleoperation.

## Format
Trajectory data with synchronized bimanual joint positions, RGB images from multiple camera views, and end-effector actions from two 6-DoF arms with parallel-jaw grippers.

## Size
26,000+ real-world demonstrations (5 tasks) and 2,000 simulated demonstrations (3 tasks).

## License
Unknown

## How to Download
- Project website: https://aloha-unleashed.github.io/
- ALOHA 2 hardware: https://aloha-2.github.io/
- Related datasets available on TensorFlow Datasets and Hugging Face under ALOHA variants.

## Papers Using This Dataset
- [[Gemini Robotics]] — used for bimanual dexterous manipulation evaluation and training
