import torch
import time
from prompts_builder import PromptBuilder
from parsers.gemma_parser import GemmaParser
from transformers import pipeline
from datasets import load_dataset
from results.result_file_builder import ResultsBuilder

ENTRIES_TO_USE = 5
BATCH_SIZE = 1

model_names = {
#  "qwen": "Qwen/Qwen2.5-1.5B-Instruct",
 "gemma-2" : "google/gemma-2-2b-it",
#  "llama-3.2" : "meta-llama/Llama-3.2-1B-Instruct"
}

dataset = load_dataset("webnlg-challenge/web_nlg", "release_v3.0_en", split="dev", trust_remote_code=True)

LOG_DEBUG = True
LOG_INFO = True
LOG_ERROR = True

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

def entities_prompts_generator():
    for entry in random_entries:
        sentences = entry["lex"]["text"]
        number_triplets = entry["size"]
        
        logDebug(">>>>")
        logDebug(f"Testing sentences: {sentences}, with model {model_key}")
        logDebug("---")
        logDebug(f"Number of triplets expected: {number_triplets}")
        logDebug("---")
        
        entries_metadata.append({"eid":entry["eid"], "category": entry["category"], "modified_triplets":entry["modified_triple_sets"]["mtriple_set"] })

        yield prompt_builder.gen_prompt_for_extraction(sentences)

def relation_prompts_generator(entities_list):
    entity_index = 0
    for entry in random_entries:
        sentences = entry["lex"]["text"]
        entities = entities_list[entity_index]
        entity_index += 1
        logDebug(">>>>")
        logDebug(f"Testing sentences: {sentences}, with model {model_key}")
        logDebug("---")
        logDebug(f"Entities: {entities}")
        logDebug("---")

        yield prompt_builder.gen_prompt_for_relations(sentences, entities)

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
    
    entities_array = []

    for outputs in pipe(entities_prompts_generator(), max_new_tokens=512, batch_size=BATCH_SIZE):
        logInfo(f"Processing sentence {sentence_count} of {ENTRIES_TO_USE}")
        generated_response = outputs[0]["generated_text"].strip()
        
        logDebug("---")
        logDebug(generated_response)
        
        entities_array.append(GemmaParser.extract_entities(generated_response))

        logDebug(entities_array[sentence_count])

        sentence_count += 1

    sentence_count = 0 
    for outputs in pipe(relation_prompts_generator(entities_array), max_new_tokens=512, batch_size=BATCH_SIZE):
        logInfo(f"Processing sentence {sentence_count} of {ENTRIES_TO_USE}")
        generated_response = outputs[0]["generated_text"].strip()
        
        logDebug("---")
        logDebug(generated_response)
        
        # entities_array.append(GemmaParser.extract_entities(generated_response))

        sentence_count += 1
    logInfo(f"Total processing time: {time.time() - start_time}s")
    # results.write_results_files()

