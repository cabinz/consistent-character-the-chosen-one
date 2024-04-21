from diffusers import DiffusionPipeline
import torch
import os
import argparse

from utils.common import config2args, log_print
from utils.logger import get_logger


cmd_parser = argparse.ArgumentParser(description="Process running command.")
cmd_parser.add_argument('-c', '--config_file', type=str) 
cmd_parser.add_argument('-p', '--prompt_postfix', type=str, default="sitting on a rocket.") 
cmd_parser.add_argument('-l', '--loop_id', type=int, default=0) 
cmd_args = cmd_parser.parse_args()

args = config2args(cmd_args.config_file)

model_path = os.path.join(args.output_dir, args.character_name, str(cmd_args.loop_id))
pipe = DiffusionPipeline.from_pretrained(model_path, torch_dtype=torch.float16)
pipe.to("cuda")
pipe.load_lora_weights(os.path.join(model_path, f"checkpoint-{args.checkpointing_steps * args.num_train_epochs}"))

image_postfix = args.prompt_postfix.replace(" ", "_")

# create folder
output_folder = f"./inference_results/{args.character_name}"
os.makedirs(output_folder, exist_ok=True)

# remember to use the place holader here
prompt = f"A photo of {args.placeholder_token}{args.prompt_postfix}."
image = pipe(prompt, num_inference_steps=35, guidance_scale=7.5).images[0]
image.save(os.path.join(output_folder, f"{args.character_name}_{image_postfix}.png"))
