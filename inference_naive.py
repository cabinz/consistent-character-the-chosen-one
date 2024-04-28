from diffusers import DiffusionPipeline
import torch
import os
import argparse

from utils.common import config2args, log_print, get_timestamp
from utils.logger import get_logger


rum_timstamp = get_timestamp()

cmd_parser = argparse.ArgumentParser(description="Process running command.")
cmd_parser.add_argument('-m', '--model_path', type=str, default='stabilityai/stable-diffusion-xl-base-1.0')
cmd_parser.add_argument('-o', '--output_base', type=str, default='./out/naive_gen') 
cmd_parser.add_argument('-p', '--prompts', 
                        action='append', help='A single or a more prompt postfix strings.')
cmd_parser.add_argument('-n', '--num_images_per_prompt', type=int, default=1) 
cmd_args = cmd_parser.parse_args()

# Load models
pipe = DiffusionPipeline.from_pretrained(cmd_args.model_path, torch_dtype=torch.float16)
pipe.to("cuda")

# Set up output directory
output_dir = os.path.join(cmd_args.output_base, rum_timstamp)
os.makedirs(output_dir)

# Infer
for prompt in cmd_args.prompts:
    img_filename_prefix = prompt.replace(" ", "_")
    imgs = pipe(prompt, 
                num_inference_steps=35, 
                guidance_scale=7.5, 
                num_images_per_prompt=cmd_args.num_images_per_prompt
            ).images
    for sampling_id, img in enumerate(imgs):
        img_path = os.path.join(
            output_dir, f"{img_filename_prefix}_{sampling_id}.png")
        img.save(img_path)
