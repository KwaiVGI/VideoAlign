## Data Organization Guidelines
Your training data should include a CSV file and a video folder structured as follows:

```
├── example.csv
└── videos/
    ├── example_1_A.mp4
    ├── example_1_B.mp4
    ├── example_2_A.mp4
    ├── example_2_B.mp4
    └── ...
```

### CSV File Format
The CSV file must contain the following columns with exact header names:
* `path_A`: Path to video A (e.g., ./videos/example_1_A.mp4).
* `path_B`: Path to video B (e.g., ./videos/example_1_B.mp4).
* `prompt`: Text description outlining the video content or scene.
* `VQ`: Visual quality preference label (possible values: A, B, same).
* `MQ`: Motion quality preference label (possible values: A, B, same).
* `TA`: Text alignment preference label (possible values: A, B, same).
* `fps_A`: Frame rate of video A.
* `num_frames_A`: Number of frames in video A.
* `fps_B`: Frame rate of video B.
* `num_frames_B`: Number of frames in video B.

We provide an example [here](example.csv)


## Training Script Parameters

The following table summarizes the parameters used in the training script. You can adjust these values as needed for your experiments.

| Parameter                         | Description                                                        | Example Value                                  |
| --------------------------------- | ------------------------------------------------------------------ | ---------------------------------------------- |
| `--lora_enable`                   | Enable LoRA tuning for the model.                                  | `True`                                         |
| `--vision_lora`                   | Enable LoRA tuning for the vision component.                       | `False`                                        |
| `--freeze_vision_tower`           | Freeze the vision tower parameters during training.                | `False`                                        |
| `--freeze_llm`                    | Freeze the language model parameters during training.              | `False`                                        |
| `--tune_merger`                   | Enable tuning for the merger module(between the vision encoder and the LLM).                               | `True`                                         | 
| `--fps`                           | FPS to sample from the video.                                      | `2`                                            | 
| `--max_frame_pixels`              | Maximum number of pixels per frame allowed.                        | `200704`(448*448)                              | 
| `--sample_type`                   | Frame sampling strategy.                                           | `"uniform"`                                    | 
| `--lora_r`                        | LoRA Rank                                                          | `64`                                           | 
| `--lora_alpha`                    | LoRA Alpha                                                         | `128`                                          | 
| `--lora_namespan_exclude`         | Model parts to exclude from LoRA tuning.                           | `"['lm_head', 'rm_head', 'embed_tokens']"`     |
| `--bf16`                          | Use bfloat16 precision training.                                   | `True`                                         | 
| `--torch_dtype`                   | Torch data type to use during training.                            | `"bfloat16"`                                   | 
| `--num_lora_modules`              | Number of LoRA modules to apply (-1 for all available modules).    | `-1`                                           | 
| `--model_name_or_path`            | Identifier or path for the pre-trained model.                      | `Qwen/Qwen2-VL-2B-Instruct`                    | 
| `--meta_data`                     | Path to the training metadata CSV file.                            | `"./datasets/train/example.csv"`                | 
| `--meta_data_test`                | Path to the valid metadata CSV file.                                | `"./datasets/train/example.csv"`                | 
| `--data_dir`                      | Directory of the training data.                                    | `"./datasets/train"`                            | 
| `--output_dir`                    | Directory where model outputs will be saved.                       | `rm_output`                                    | 
| `--eval_dim`                      | Evaluation dimensions (single dimension or multiple dimensions).   | `"VQ" "MQ" "TA"`                    |
| `--output_dim`                    | Number of output dimensions.                                       | `1`                                            | 
| `--use_special_tokens`            | Enable the use of special tokens during training.                  | `True`                                         | 
| `--reward_token`                  | The token used to indicate reward in the text.                     | `"special"`                                    | 
| `--loss_type`                     | Specifies the loss function type.                                  | `"btt"`                                        | 
| `--use_tied_data`                 | Use tied data for training.                                        | `True`                                         | 
| `--prompt_template_type`          | The template type for input template.                              | `"detailed_special"`                           | 
| `--per_device_train_batch_size`   | Batch size per device for training.                                | `1`                                            | 
| `--per_device_eval_batch_size`    | Batch size per device for evaluation.                              | `4`                                            | 
| `--gradient_accumulation_steps`   | Number of gradient accumulation steps.                             | `4`                                            | 
| `--num_train_epochs`              | Total number of training epochs.                                   | `3`                                            | 
| `--learning_rate`                 | Base learning rate for training.                                   | `2e-6`                                         | 
| `--merger_lr`                     | Learning rate for the merger module.                               | `2e-6`                                         | 
| `--vision_lr`                     | Learning rate for the vision components.                           | `2e-6`                                         | 
| `--special_token_lr`              | Learning rate for the special tokens.                              | `2e-6`                                         | 
| `--report_to`                     | Logging backend for training reports.                              | `tensorboard`                                  | 
| `--warmup_ratio`                  | Warmup ratio for the learning rate scheduler.                      | `0.05`                                         | 
| `--lr_scheduler_type`             | Type of learning rate scheduler.                                   | `"constant_with_warmup"`                       | 
| `--eval_strategy`                 | Strategy for evaluation during training.                           | `"steps"`                                      | 
| `--logging_epochs`                | Frequency of logging (in terms of epochs).                        | `0.01`                                         | 
| `--eval_epochs`                   | Frequency of evaluation (in terms of epochs).                     | `0.1`                                          | 
| `--save_epochs`                   | Frequency of saving the model (in terms of epochs).               | `0.25`                                         | 
| `--max_length`                    | Maximum sequence length(just to avoid OOM).                        | `6144`                                         | 
| `--gradient_checkpointing`        | Enable gradient checkpointing to save memory.                      | `False`                                        | 
| `--deepspeed`                     | Path to the DeepSpeed configuration file.(zero0, zero2, zero3)    | `ds_config/zero0.json`                         | 
| `--save_only_model`               | Save only the model weights.                                      | `True`                                         | 
| `--save_full_model`               | Save the full model (including optimizer states, etc.).           | `False`                                        | 
| `--dataloader_num_workers`        | Number of workers for data loading.                               | `8`                                            | 

By following these guidelines and understanding the parameters, you can customize the training process to suit your specific needs.
