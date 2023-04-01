import sys
import os
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from fastapi import Request, FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# allow cors
origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the model
if "models" not in os.listdir():
    print("models not found. Downloading...")
    os.system("mkdir models")
    # download models

scifi_model = GPT2LMHeadModel.from_pretrained("models/scifi-speculative")
print("scifi model loaded")
philosophy_model = GPT2LMHeadModel.from_pretrained("models/philosophy")
print("philosophy model loaded")
academia_model = GPT2LMHeadModel.from_pretrained("models/academia")
print("academia model loaded")
litreature_model = GPT2LMHeadModel.from_pretrained("models/litreature")
print("litreature model loaded")

# Load the pre-trained GPT2 tokenizer
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

# Generate text from a prompt
@app.post("/")
async def generate(request: Request):
    req = await request.json()

    print(req)

    length = req["length"]
    model = req["model"]
    prompt = req["prompt"]

    
    if length > 100:
        length = 100
    if length < 0 or length < 10:
        length = 10

    input_ids = tokenizer.encode(prompt, return_tensors='pt')

    generated_text = ""

    if model == "scifi":
        output = scifi_model.generate(input_ids, max_length=length, do_sample=True, pad_token_id=tokenizer.eos_token_id)
        generated_text = tokenizer.decode(output[0], skip_special_tokens=True)

    elif model == "philosophy":
        output = philosophy_model.generate(input_ids, max_length=length, do_sample=True, pad_token_id=tokenizer.eos_token_id)
        generated_text = tokenizer.decode(output[0], skip_special_tokens=True)

    elif model == "academia":
        output = academia_model.generate(input_ids, max_length=length, do_sample=True, pad_token_id=tokenizer.eos_token_id)
        generated_text = tokenizer.decode(output[0], skip_special_tokens=True)

    elif model == "litreature":
        output = litreature_model.generate(input_ids, max_length=length, do_sample=True, pad_token_id=tokenizer.eos_token_id)
        generated_text = tokenizer.decode(output[0], skip_special_tokens=True)

    return {
        "prompt": prompt,
        "completion": generated_text
    }
