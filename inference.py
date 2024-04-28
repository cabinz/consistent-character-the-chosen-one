from diffusers import DiffusionPipeline
import torch
import os
import argparse

from utils.common import config2args, log_print
from utils.logger import get_logger


cmd_parser = argparse.ArgumentParser(description="Process running command.")
cmd_parser.add_argument('-c', '--config_file', type=str)
cmd_parser.add_argument('-p', '--prompt_postfixes', 
                        action='append', help='A single or a more prompt postfix strings.')
# cmd_parser.add_argument('-i', '--prompt_img_type', type=str, default='photo')
cmd_parser.add_argument('-l', '--loop_id', type=int, default=0) 
cmd_parser.add_argument('-o', '--output_dir', type=str, default='./out/inference_results') 
cmd_parser.add_argument('-n', '--num_images_per_prompt', type=int, default=5) 
cmd_args = cmd_parser.parse_args()

args = config2args(cmd_args.config_file)


# Set up output directory
output_dir = os.path.join(cmd_args.output_dir, args.character_name, f"loop={cmd_args.loop_id}")
os.makedirs(output_dir, exist_ok=True)

# Load models
model_path = os.path.join(args.output_dir, args.character_name, str(cmd_args.loop_id))
pipe = DiffusionPipeline.from_pretrained(model_path, torch_dtype=torch.float16)
pipe.to("cuda")
pipe.load_lora_weights(os.path.join(model_path, f"checkpoint-{args.checkpointing_steps * args.num_train_epochs}"))

# Infer
for prompt_postfix in cmd_args.prompt_postfixes:
    img_filename_postfix = prompt_postfix.replace(" ", "_")
    
    prompt = f"A photo of {args.placeholder_token} {prompt_postfix}."
    # prompt = f"{args.validation_prompt} {prompt_postfix}." # "A photo of <placeholder> ..."
    
    
    # image = pipe(prompt, num_inference_steps=35, guidance_scale=7.5).images[0]
    imgs = pipe(prompt, 
                num_inference_steps=35, 
                guidance_scale=7.5, 
                num_images_per_prompt=cmd_args.num_images_per_prompt
            ).images
    for sampling_id, img in enumerate(imgs):
        img_path = os.path.join(
            output_dir, f"{args.character_name}_{img_filename_postfix}_{sampling_id}.png")
        img.save(img_path)
