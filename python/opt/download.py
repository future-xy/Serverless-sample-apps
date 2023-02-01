from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

import os
import json
import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name", type=str, default="opt-125m")   # default is the smallest model
    args = parser.parse_args()
    return args


args = get_args()
model_name = args.model_name

# always use fp16 on GPU
model = AutoModelForCausalLM.from_pretrained(f"facebook/{model_name}", device_map="auto", torch_dtype=torch.float16)
model.eval()
tokenizer = AutoTokenizer.from_pretrained(f"facebook/{model_name}")

prompt = "Whatever you want "
inputs = tokenizer(prompt, return_tensors="pt")
output = model.generate(**inputs)
print(tokenizer.decode(output[0]))