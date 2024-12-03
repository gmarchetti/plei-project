import torch
import random
from prompts_builder import PromptBuilder
from parsers.gemma_parser import GemmaParser
from transformers import pipeline
from datasets import load_dataset
from results.result_file_builder import ResultsBuilder

model_names = {
#  "qwen": "Qwen/Qwen2.5-1.5B-Instruct",
 "gemma-2" : "google/gemma-2-2b-it",
#  "llama-3.2" : "meta-llama/Llama-3.2-1B-Instruct"
}

dataset = load_dataset("webnlg-challenge/web_nlg", "release_v3.0_en", split="dev", trust_remote_code=True)



random_entries = dataset.shuffle().select(range(3))

prompt_builder = PromptBuilder()

for model_key in model_names:
    

    pipe = pipeline(
        "text-generation",
        model=model_names[model_key],
        model_kwargs={"torch_dtype": torch.bfloat16},
        device="cuda",  # replace with "mps" to run on a Mac device
    )
    
    results = ResultsBuilder(model_key)

    for entry in random_entries:
        sentences = entry["lex"]["text"]
        original_triple = entry["original_triple_sets"]["otriple_set"]
        modified_triple = entry["modified_triple_sets"]["mtriple_set"]
        number_triplets = entry["size"]
        
        print(">>>>")
        print(f"Testing sentences: {sentences}, with model {model_key}")
        print("---")
        print(f"Number of triplets expected: {number_triplets}")
        print("---")
        
        chat_messages = prompt_builder.gen_prompt_with_example(sentences, number_triplets)

        outputs = pipe(chat_messages, max_new_tokens=512)
        generated_response = outputs[0]["generated_text"][-1]["content"].strip()
        chat_messages.append({"role" : "assistant", "content": generated_response})
        chat_messages.append({"role": "user", "content": "Now format the your answer into a JSON"})
        
        print("---")
        outputs = pipe(chat_messages, max_new_tokens=512)
        generated_response = outputs[0]["generated_text"][-1]["content"].strip()
        print(generated_response)
        generated_triplets = GemmaParser.extract_triples(generated_response)

        print(generated_triplets)
        print("---")
        print(f"Original triple was: {original_triple}")
        print(f"Modified triple was: {modified_triple}")
        print("---\n")

        results.add_result(generated_triplets, entry["category"], entry["eid"])
        results.add_modified_triplets(modified_triple, entry["category"], entry["eid"])

    results.write_results_files()

