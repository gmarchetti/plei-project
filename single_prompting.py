import torch
import time
from prompts_builder import PromptBuilder
from parsers.gemma_parser import GemmaParser
from transformers import pipeline
from datasets import load_dataset
from results.result_file_builder import ResultsBuilder

ENTRIES_TO_USE = 100
BATCH_SIZE = 16

model_names = {
#  "qwen": "Qwen/Qwen2.5-1.5B-Instruct",
 "gemma-2" : "google/gemma-2-2b-it",
#  "llama-3.2" : "meta-llama/Llama-3.2-1B-Instruct"
}

dataset = load_dataset("webnlg-challenge/web_nlg", "release_v3.0_en", split="dev", trust_remote_code=True)

LOG_DEBUG = False
LOG_INFO = True
LOG_ERROR = False

random_entries = dataset.shuffle().select(range(ENTRIES_TO_USE))

prompt_builder = PromptBuilder()

entries_metadata = []

def logDebug(msg):
    if LOG_DEBUG:
        print(msg)

def logInfo(msg):
    if LOG_INFO:
        print(msg)

def logError(msg):
    if LOG_ERROR:
        print(msg)

def promptsGenerator():
    for entry in random_entries:
        sentences = entry["lex"]["text"]
        number_triplets = entry["size"]
        
        logDebug(">>>>")
        logDebug(f"Testing sentences: {sentences}, with model {model_key}")
        logDebug("---")
        logDebug(f"Number of triplets expected: {number_triplets}")
        logDebug("---")
        
        entries_metadata.append({"eid":entry["eid"], "category": entry["category"], "modified_triplets":entry["modified_triple_sets"]["mtriple_set"] })

        yield prompt_builder.gen_prompt_with_example(sentences, number_triplets)[0]["content"]

for model_key in model_names:

    pipe = pipeline(
        "text-generation",
        model=model_names[model_key],
        model_kwargs={"torch_dtype": torch.bfloat16},
        device="cuda",  # replace with "mps" to run on a Mac device
    )
    
    results = ResultsBuilder(model_key)
    sentence_count = 0    

    start_time = time.time()    

    for outputs in pipe(promptsGenerator(), max_new_tokens=512, batch_size=BATCH_SIZE):
        logInfo(f"Processing sentence {sentence_count} of {ENTRIES_TO_USE}")
        generated_response = outputs[0]["generated_text"].strip()
        
        logDebug("---")
        logDebug(generated_response)
        try:
            generated_triplets = GemmaParser.extract_triples(generated_response)

            logDebug(generated_triplets)

            results.add_result(generated_triplets, entries_metadata[sentence_count]["category"], entries_metadata[sentence_count]["eid"])
            results.add_modified_triplets(entries_metadata[sentence_count]["modified_triplets"], entries_metadata[sentence_count]["category"], entries_metadata[sentence_count]["eid"])
        except:
            logError(f"Failed to process response: {generated_response}")

        sentence_count += 1

    logInfo(f"Total processing time: {time.time() - start_time}s")
    results.write_results_files()
