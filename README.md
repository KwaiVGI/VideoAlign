# VideoReward

<p align="center"> <strong> Improving Video Generation with Human Feedback </strong> </p>

<div align="center">
<p align="center">
   📃 <a href="https://arxiv.org/abs/2501.13918" target="_blank">[Paper]</a> • 🌐 <a href="https://gongyeliu.github.io/videoalign/" target="_blank">[Project Page]</a> • 🤗<a href="https://huggingface.co/datasets/KwaiVGI/VideoGen-RewardBench" target="_blank">[VideoGen-RewardBench]</a>
</p>
</div>


## 📖 Introduction


This repository, **VideoAlign**, open-sources the **VideoReward** component -- our VLM-based reward model introduced in the paper [Improving Video Generation with Human Feedback](https://arxiv.org/abs/2501.13918). VideoReward evaluates generated videos across three critical dimensions:
* Visual Quality (VQ): The clarity, aesthetics, and single-frame reasonableness.
* Motion Quality (MQ): The dynamic stability, dynamic reasonableness, naturalness, and dynamic degress.
* Text Alignment (TA): The relevance between the generated video and the text prompt.

This versatile reward model can be used for data filtering, guidance, reject sampling, DPO, and other RL methods. <br>

<img src=https://gongyeliu.github.io/videoalign/pics/overview.png width="100%"/>



## 📝 Updates
- __[2025.02.08]__: 🔥 Release the [VideoGen-RewardBench](https://huggingface.co/datasets/KwaiVGI/VideoGen-RewardBench).
- __[2025.02.08]__: 🔥 Release the [Code](#) and [Checkpoints](https://huggingface.co/KwaiVGI/VideoReward) of VideoReward.
- __[2025.01.23]__: Release the [Paper](https://arxiv.org/abs/2501.13918) and [Project Page](https://gongyeliu.github.io/videoalign/).


##  🚀 Quick Started

### 1. Environment Set Up
Clone this repository and install packages.
```bash
git clone https://github.com/KwaiVGI/VideoAlign
cd VideoAlign
conda env create -f environment.yaml
```

### 2. Download Pretrained Weights

Please download our checkpoints from [Huggingface](https://huggingface.co/KwaiVGI/VideoReward) and put it in `./checkpoints/`.

```bash
cd checkpoints
git lfs install
git clone https://huggingface.co/KwaiVGI/VideoReward
cd ..
```

### 3. Scoring for a single prompt-video item.

```bash
python inference.py
```


## 🏁 Eval the Performance on VideoGen-RewardBench


### 1. Download the VideoGen-RewardBench and put it in `./datasets/`.

```bash
cd dataset
git lfs install
git clone https://huggingface.co/datasets/KwaiVGI/VideoGen-RewardBench
cd ..
```

### 2. Start inference

```bash
python eval_videogen_rewardbench.py
```

## 🏁 Train RM on Your Own Data
### 1. Prepare your own data as the [instruction](./datasets/train/README.md) stated.

### 2. Start training!
```bash
sh train.sh
```



## 🤗 Acknowledgments

Our reward model is based on [QWen2-VL-2B-Instruct](https://huggingface.co/Qwen/Qwen2-VL-2B-Instruct), and our code is build upon [TRL](https://github.com/huggingface/trl) and [Qwen2-VL-Finetune](https://github.com/2U1/Qwen2-VL-Finetune), thanks to all the contributors!


## ⭐ Citation

Please leave us a star ⭐ if you find our work helpful.
```bibtex
@misc{liu2025improving,
      title={Improving Video Generation with Human Feedback},
      author={Jie Liu and Gongye Liu and Jiajun Liang and Ziyang Yuan and Xiaokun Liu and Mingwu Zheng and Xiele Wu and Qiulin Wang and Wenyu Qin and Menghan Xia and Xintao Wang and Xiaohong Liu and Fei Yang and Pengfei Wan and Di Zhang and Kun Gai and Yujiu Yang and Wanli Ouyang},
      year={2025},
      eprint={2501.13918},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/2501.13918}, 
}