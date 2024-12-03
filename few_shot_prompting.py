import torch
import random
from prompts_builder import PromptBuilder
from parsers.gemma_parser import GemmaParser
from transformers import pipeline
from datasets import load_dataset
from results.result_file_builder import ResultsBuilder

ENTRIES_TO_USE = 30

model_names = {
#  "qwen": "Qwen/Qwen2.5-1.5B-Instruct",
 "gemma-2" : "google/gemma-2-2b-it",
#  "llama-3.2" : "meta-llama/Llama-3.2-1B-Instruct"
}

dataset = load_dataset("webnlg-challenge/web_nlg", "release_v3.0_en", split="dev", trust_remote_code=True)

LOG_DEBUG = False
LOG_INFO = True
LOG_ERROR = True

random_entries = dataset.shuffle().select(range(ENTRIES_TO_USE))

prompt_builder = PromptBuilder()

def logDebug(msg):
    if LOG_DEBUG:
        print(msg)

def logInfo(msg):
    if LOG_INFO:
        print(msg)

def logError(msg):
    if LOG_ERROR:
        print(msg)

for model_key in model_names:

    pipe = pipeline(
        "text-generation",
        model=model_names[model_key],
        model_kwargs={"torch_dtype": torch.bfloat16},
        device="cuda",  # replace with "mps" to run on a Mac device
    )
    
    results = ResultsBuilder(model_key)
    sentence_count = 1

    for entry in random_entries:
        
        logInfo(f"Processing sentence {sentence_count} of {ENTRIES_TO_USE}")

        sentences = entry["lex"]["text"]
        original_triple = entry["original_triple_sets"]["otriple_set"]
        modified_triple = entry["modified_triple_sets"]["mtriple_set"]
        number_triplets = entry["size"]
        
        logDebug(">>>>")
        logDebug(f"Testing sentences: {sentences}, with model {model_key}")
        logDebug("---")
        logDebug(f"Number of triplets expected: {number_triplets}")
        logDebug("---")
        
        chat_messages = prompt_builder.gen_prompt_with_example(sentences, number_triplets)

        outputs = pipe(chat_messages, max_new_tokens=512)
        generated_response = outputs[0]["generated_text"][-1]["content"].strip()
        
        logDebug("---")
        logDebug(generated_response)
        try:
            generated_triplets = GemmaParser.extract_triples(generated_response)

            logDebug(generated_triplets)
            logDebug("---")
            logDebug(f"Original triple was: {original_triple}")
            logDebug(f"Modified triple was: {modified_triple}")
            logDebug("---\n")

            results.add_result(generated_triplets, entry["category"], entry["eid"])
            results.add_modified_triplets(modified_triple, entry["category"], entry["eid"])
        except:
            logError(f"Failed to process response: {generated_response}")

        sentence_count += 1

    results.write_results_files()

