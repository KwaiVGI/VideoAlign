import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
import glob
import pandas as pd
from tqdm import tqdm

import torch

from inference import VideoVLMRewardInference
from calc_accuracy import calc_accuracy_with_ties, calc_accuracy_without_ties


def convert_pair_to_single(df_pair_anno):
    df_A = df_pair_anno[['path_A', 'A_model', 'prompt', 'fps_A', 'num_frames_A']]
    df_A.columns = ['path', 'model', 'prompt', 'fps', 'num_frames']

    df_B = df_pair_anno[['path_B', 'B_model', 'prompt', 'fps_B', 'num_frames_B']]
    df_B.columns = ['path', 'model', 'prompt', 'fps', 'num_frames']

    df_single = pd.concat([df_A, df_B], axis=0)
    df_single = df_single.drop_duplicates(subset=['path'])
    df_single = df_single.sort_values(by=['path'])

    df_single = df_single.reset_index(drop=True)

    return df_single

def convert_single_to_pair(df_pair_anno, df_single_pred):
    score_dict = {}
    keys_to_store = ["reward_VQ", "reward_MQ", "reward_TA", "reward_Overall"]

    for i, row in df_single_pred.iterrows():
        score_dict[row["path"]] = {k: row[k] for k in keys_to_store}

    for key in keys_to_store:
        df_pair_anno[f"{key}_A"] = 0.0
        df_pair_anno[f"{key}_B"] = 0.0

    for i, row in df_pair_anno.iterrows():
        for key in keys_to_store:
            df_pair_anno.at[i, f"{key}_A"] = score_dict[row["path_A"]][key]
            df_pair_anno.at[i, f"{key}_B"] = score_dict[row["path_B"]][key]


    return df_pair_anno
    

def main():
    ## 1. load the model
    load_from_pretrained = "./checkpoints"

    device = torch.device("cuda:0")
    dtype = torch.bfloat16

    inferencer = VideoVLMRewardInference(load_from_pretrained, 
                                         device=device, dtype=dtype)

    ## 2. load the data and preprocess
    data_dir = "datasets/eval"
    anno_path = "datasets/eval/videogen-rewardbench.csv"
    out_dir = "videogen-rewardbench-output"
    os.makedirs(out_dir, exist_ok=True)

    df_pair_anno = pd.read_csv(anno_path)

    """
    We first convert the pair annotation to single prompt-video items
    Then we infer to get the reward for each prompt-video item and merge them back to the pair annotation
    This is because inference is done on single prompt-video items
    And many prompt-video items are shared between the pair annotation
    """
    df_single_pred = convert_pair_to_single(df_pair_anno)

    # add new columns
    df_single_pred["reward_VQ"] = 0.0
    df_single_pred["reward_MQ"] = 0.0
    df_single_pred["reward_TA"] = 0.0
    df_single_pred["reward_Overall"] = 0.0

    ## 3. infer the reward

    batch_size = 8
    batch_video_paths = []
    batch_prompts = []
    batch_indices = []
        
    for idx, row in tqdm(df_single_pred.iterrows(), total=len(df_single_pred)):
        prompt = row["prompt"]
        # import pdb; pdb.set_trace()
        video_path = os.path.join(data_dir, row['path'])
        
        # Accumulate the data for the current batch
        batch_video_paths.append(video_path)
        batch_prompts.append(prompt)
        batch_indices.append(idx)

        if len(batch_video_paths) == batch_size or idx == len(df_single_pred) - 1:

            # try:
            with torch.no_grad():
                rewards = inferencer.reward(batch_video_paths, batch_prompts)

            # Store the results in the dataframe
            for i, batch_idx in enumerate(batch_indices):
                df_single_pred.loc[batch_idx, 'reward_VQ'] = rewards[i]['VQ']
                df_single_pred.loc[batch_idx, 'reward_MQ'] = rewards[i]['MQ']
                df_single_pred.loc[batch_idx, 'reward_TA'] = rewards[i]['TA']
                df_single_pred.loc[batch_idx, 'reward_Overall'] = rewards[i]['Overall']

            # Reset the batch lists
            batch_video_paths = []
            batch_prompts = []
            batch_indices = []     

    df_single_pred.to_csv(os.path.join(out_dir, "out_single.csv"), index=False)

    ## 4. merge the single prediction back to the pair annotation and calc accuracy
    df_pair_pred = convert_single_to_pair(df_pair_anno, df_single_pred)
    df_pair_pred.to_csv(os.path.join(out_dir, "out_pair.csv"), index=False)

    # calculate the accuracy
    reward_attributes = ["VQ", "MQ", "TA", "Overall"]
    results = {}
    for reward_attr in reward_attributes:
        df_pair_pred[f'reward_{reward_attr}'] = df_pair_pred[f"reward_{reward_attr}_A"] - df_pair_pred[f"reward_{reward_attr}_B"]
        df_pair_pred[f"{reward_attr}"] = df_pair_pred[f"{reward_attr}"].map({'A': 1, 'B': -1, 'same': 0})

        results[f"{reward_attr} Accuracy"] = {
            "with_ties": calc_accuracy_with_ties(df_pair_pred[f"{reward_attr}"], df_pair_pred[f"reward_{reward_attr}"]),
            "without_ties": calc_accuracy_without_ties(df_pair_pred[f"{reward_attr}"], df_pair_pred[f"reward_{reward_attr}"])
        }
        print(f"{reward_attr} Accuracy: ", end="")
        print(f"With ties: {results[f'{reward_attr} Accuracy']['with_ties']}, ", end="")
        print(f"Without ties: {results[f'{reward_attr} Accuracy']['without_ties']}")

        
    with open(os.path.join(out_dir, "accuracy.json"), "w") as f:
        json.dump(results, f, indent=4)


if __name__ == "__main__":
    main()


