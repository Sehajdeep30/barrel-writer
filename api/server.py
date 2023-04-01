import sys
import os
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from fastapi import FastAPI

app = FastAPI()

# Load the model
if "models" not in os.listdir():
    print("models not found. Downloading...")
    os.system("mkdir models")
    # download models

scifi_model = GPT2LMHeadModel.from_pretrained("models/scifi-speculative")
print("scifi model loaded")
philosophy_model = GPT2LMHeadModel.from_pretrained("models/philosophy")
print("philosophy model loaded")

# Load the pre-trained GPT2 tokenizer 
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

OUTPUT_LENGTH = 50

# Generate text from a prompt
@app.get("/completion/{model}/{prompt}")
async def generate(prompt: str, model: str) -> dict:
    input_ids = tokenizer.encode(prompt, return_tensors='pt')

    if model == "scifi":
        output = scifi_model.generate(input_ids, max_length=OUTPUT_LENGTH, do_sample=True, pad_token_id=tokenizer.eos_token_id)
        generated_text = tokenizer.decode(output[0], skip_special_tokens=True)

    elif model == "philosophy":
        output = philosophy_model.generate(input_ids, max_length=OUTPUT_LENGTH, do_sample=True, pad_token_id=tokenizer.eos_token_id)
        generated_text = tokenizer.decode(output[0], skip_special_tokens=True)

    return {
        "prompt": prompt,
        "completion": generated_text
    }
