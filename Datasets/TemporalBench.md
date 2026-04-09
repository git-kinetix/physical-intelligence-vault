---
tags: [dataset]
aliases: [TemporalBench Benchmark]
category: "evaluation-benchmark"
year: 2024
---

# TemporalBench

## Description
TemporalBench is a benchmark from Microsoft for evaluating fine-grained temporal understanding in multimodal video models, published at NeurIPS 2024. It consists of ~10,000 video question-answer pairs derived from ~2,000 high-quality human annotations detailing temporal dynamics, covering action frequency, motion magnitude, event order, and more. State-of-the-art models like GPT-4o achieve only 38.5% accuracy vs. ~70% human performance.

## Format
Video QA benchmark with multiple-choice questions. Videos sourced from ActivityNet, Charades, COIN, EgoExo4D, FineGym, and short video collections.

## Size
~10,000 QA pairs from ~2,000 annotated video clips.

## License
Academic research only (non-commercial, no redistribution).

## How to Download
- GitHub: https://github.com/mu-cai/TemporalBench
- Hugging Face: https://huggingface.co/datasets/microsoft/TemporalBench
- Project page: https://temporalbench.github.io/

## Papers Using This Dataset
- [[V-JEPA 2]] — evaluated on fine-grained temporal understanding
