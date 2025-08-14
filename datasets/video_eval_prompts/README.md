This folder contains the prompt sets we use to evaluate video generation performance in the paper. It includes curated subsets from public benchmarks and a challenging set we constructed with GPT-4o. Chinese translations are provided for readability.

- VBench: 946 prompts curated from the [VBench](https://github.com/Vchitect/VBench) benchmark.

- VideoGen-Eval: 400 prompts curated from [VideoGen-Eval](https://github.com/AILab-CVC/VideoGen-Eval) for general-purpose evaluation.

- TA-Hard: 72 prompts generated with GPT-4o. This set emphasizes challenging cases, typically combining two subjects and incorporating uncommon actions.


For VBench and VideoGen-Eval, we rewrite the prompts to better align with our video model’s input format while preserving the original intent and difficulty.

Each prompt is available in both English and Chinese. The Chinese versions help bilingual annotators and readers.
