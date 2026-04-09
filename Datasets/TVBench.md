---
tags: [dataset]
aliases: [TVBench Benchmark]
category: "evaluation-benchmark"
year: 2024
---

# TVBench

## Description
TVBench is an open-source video multiple-choice QA benchmark designed to rigorously evaluate temporal understanding in video-language models. It addresses known shortcomings of existing benchmarks where single frames or text-only cues suffice for correct answers, by ensuring that temporal video information is genuinely required. Videos are sourced from Perception Test, CLEVRER, STAR, MoVQA, Charades-STA, NTU RGB+D, FunQA, and CSV.

## Format
Video multiple-choice question-answering. Each question requires temporal reasoning across multiple frames to answer correctly.

## Size
Multiple-choice QA pairs sourced from 8 existing video datasets.

## License
Permissive (evaluation code); video licenses vary by source dataset.

## How to Download
- GitHub: https://github.com/daniel-cores/tvbench
- Hugging Face: https://huggingface.co/datasets/FunAILab/TVBench
- Most videos included; NTU RGB+D videos must be downloaded separately.
- Project page: https://daniel-cores.github.io/tvbench/

## Papers Using This Dataset
- [[V-JEPA 2]] — evaluated on temporal video understanding
