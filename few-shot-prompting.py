import torch
from transformers import pipeline
from datasets import load_dataset

model_names = {
#  "qwen": "Qwen/Qwen2.5-1.5B-Instruct",
 "gemma-2" : "google/gemma-2-2b-it",
#  "llama-3.2" : "meta-llama/Llama-3.2-1B-Instruct"
}

dataset = load_dataset("webnlg-challenge/web_nlg", "release_v3.0_en", split="dev", trust_remote_code=True)

sentence = dataset[40]["lex"]["text"]

original_triple = dataset[40]["original_triple_sets"]["otriple_set"]
modified_triple = dataset[40]["modified_triple_sets"]["mtriple_set"]

zero_shot = [
    {"role": "user",
     "content": f"""I want to create a Knowledge Graph, so extract the triplet object, property and subject from the sentence {sentence}
The output should be in json format and there should be no white spaces between the tokens."""}
]

few_shot = [
    {"role": "user", "content": 
     f""" 
Using the following example of a sentences:

1. The Andrews County Airport is owned by Andrews County, Texas.

and this output example:

{{
    "object": "Andrews_County,_Texas",
    "property": "owner",
    "subject": "Andrews_County_Airport"
}}

extract the object, subject and relation from the following sentence:

1. {sentence}

The output should be in JSON format
"""}
]


for model_key in model_names:
    print(f"Testing sentence: {sentence}, with model {model_key}")

    pipe = pipeline(
        "text-generation",
        model=model_names[model_key],
        model_kwargs={"torch_dtype": torch.bfloat16},
        device="cuda",  # replace with "mps" to run on a Mac device
    )

    outputs = pipe(few_shot, max_new_tokens=256)
    generated_response = outputs[0]["generated_text"][-1]["content"].strip()
    
    print(generated_response)

    print(f"Original triple was: {original_triple}")
    print(f"Modified triple was: {modified_triple}")
