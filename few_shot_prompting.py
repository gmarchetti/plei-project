import torch
import random
from prompts_builder import PromptBuilder
from transformers import pipeline
from datasets import load_dataset

model_names = {
#  "qwen": "Qwen/Qwen2.5-1.5B-Instruct",
 "gemma-2" : "google/gemma-2-2b-it",
#  "llama-3.2" : "meta-llama/Llama-3.2-1B-Instruct"
}

dataset = load_dataset("webnlg-challenge/web_nlg", "release_v3.0_en", split="dev", trust_remote_code=True)



random_entries = dataset.shuffle().select(range(4))

prompt_builder = PromptBuilder()

for model_key in model_names:
    

    pipe = pipeline(
        "text-generation",
        model=model_names[model_key],
        model_kwargs={"torch_dtype": torch.bfloat16},
        device="cuda",  # replace with "mps" to run on a Mac device
    )
    
    for entry in random_entries:
        sentences = entry["lex"]["text"]
        original_triple = entry["original_triple_sets"]["otriple_set"]
        modified_triple = entry["modified_triple_sets"]["mtriple_set"]
        
        print(f"Testing sentences: {sentences}, with model {model_key}")
        # print(prompt_builder.gen_prompt_with_example(sentences)[0]["content"])
        outputs = pipe(prompt_builder.gen_prompt_with_example(sentences), max_new_tokens=256)
        generated_response = outputs[0]["generated_text"][-1]["content"].strip()
        
        print(generated_response)

        print(f"Original triple was: {original_triple}")
        print(f"Modified triple was: {modified_triple}")
