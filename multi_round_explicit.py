import torch
import time
import logging

from tqdm import tqdm
from prompts_builder import PromptBuilder
from parsers.gemma_parser import GemmaParser
from transformers import pipeline
from datasets import load_dataset
from results.result_file_builder import ResultsBuilder

ENTRIES_TO_USE = 16
BATCH_SIZE = 8

model_names = {
#  "qwen": "Qwen/Qwen2.5-1.5B-Instruct",
 "gemma-2" : "google/gemma-2-2b-it",
#  "llama-3.2" : "meta-llama/Llama-3.2-1B-Instruct"
}

dataset = load_dataset("webnlg-challenge/web_nlg", "release_v3.0_en", split="dev", trust_remote_code=True)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)


random_entries = dataset.shuffle().select(range(ENTRIES_TO_USE))
entries = [random_entries[idx] for idx in range(ENTRIES_TO_USE)]

prompt_builder = PromptBuilder()

def safe_list_get (l, idx, default):
  try:
    return l[idx]
  except IndexError:
    return default


def build_triplets(entities_list, relationships_list):
    triplets_set = []
    extra_triplets = []

    logger.debug(f"Building triplets with Entities: {entities_list} and Relationships: {relationships_list}")
    for i in range(len(entities_list)):
        for j in range(i, len(entities_list)):
            if i != j:
                relationship = safe_list_get(relationships_list, len(triplets_set), "NONE")
                triplet = f"{entities_list[i]} | {relationship} | {entities_list[j]}"
                triplets_set.append(triplet)
                if relationship == "NONE":
                    extra_triplets.append(triplet)
    

    for triplet in extra_triplets:
        triplets_set.remove(triplet)

    return triplets_set

def entities_prompts_generator():
    for entry in entries:
        sentences = entry["lex"]["text"]
        number_triplets = entry["size"]
        
        logger.debug(">>>>")
        logger.debug(f"Testing sentences:\n{sentences}")                

        yield prompt_builder.gen_prompt_for_extraction(sentences)

def relation_prompts_generator(entities_list):
    
    for idx in range(0, len(entities_list)):
        entities = entities_list[idx]
        entry = entries[idx]
        
        sentences = entry["lex"]["text"]
        
        logger.debug(">>>>")
        logger.debug(f"Testing sentences: {sentences}, with model {model_key}")
        logger.debug("---")
        logger.debug(f"Entities: {entities}")
        logger.debug("---")

        yield prompt_builder.gen_prompt_for_explicit_relations(sentences, entities)

def pruning_prompts_generator(relationship_list):
    for idx in range(0, len(relationship_list)):
        entry = entries[idx]
        sentences = entry["lex"]["text"]
        relationship = relationship_list[idx]
        
        logger.debug(">>>>")
        logger.debug(f"Testing sentences: {sentences}, with model {model_key}")
        logger.debug("---")
        logger.debug(f"Relationships: {relationship}")
        logger.debug("---")

        yield prompt_builder.gen_prompt_for_relationship_pruning(sentences, relationship)

def remove_entries_that_failed(list_of_failed):
    logger.info(f">>> Removing {len(list_of_failed)} entries that failed to process")
    
    for idx in reversed(list_of_failed):
        del entries[idx]

for model_key in model_names:

    pipe = pipeline(
        "text-generation",
        model=model_names[model_key],
        model_kwargs={"torch_dtype": torch.bfloat16},
        device="cuda",  # replace with "mps" to run on a Mac device
    )
    
    results = ResultsBuilder(model_key, "explicit")
    sentence_count = 0    

    start_time = time.time()    
    
    extracted_entities_array = []
    entities_errors = 0
    failed_entries = []

    logger.info(f">>>> Extracting Entities from sentences <<<<")
    for outputs in pipe(entities_prompts_generator(), max_new_tokens=256, batch_size=BATCH_SIZE, return_full_text = False, do_sample=True, top_k=3):
        generated_response = outputs[0]["generated_text"].strip()
        
        logger.debug(f">>> Response from entity extraction prompt:\n{generated_response}")
        
        try:
            extracted_entities_array.append(GemmaParser.extract_entities(generated_response))
            logger.debug(f"Extracted entities: {extracted_entities_array[-1]}")
        except:
            logging.exception(f">>> Failed to process entities <<<\n{generated_response}")
            failed_entries.append(sentence_count)
            entities_errors += 1

        sentence_count += 1

    remove_entries_that_failed(failed_entries)
        
    sentence_count = 0
    extract_errors = 0
    
    processed_relationships = []
    
    failed_entries = []
    logger.info(f">>>> Extracting Relationship from sentences <<<<")
    for outputs in pipe(relation_prompts_generator(extracted_entities_array), max_new_tokens=512, batch_size=BATCH_SIZE, return_full_text = True):
        generated_response = outputs[0]["generated_text"].strip()
        
        logger.debug(f">>> Response for Relationship Extraction:\n{generated_response}")
        
        try:
            extracted_relationships = GemmaParser.extract_relationship(generated_response)
            logger.debug(f">> Relationships:\n {extracted_relationships}")
            generated_triplets = build_triplets(extracted_entities_array[sentence_count], extracted_relationships)
            logger.debug(f">> Triplets:\n {generated_triplets}")
            processed_relationships.append(generated_triplets)
        except:
            logging.exception(f">>>Failed to process response:\n {generated_response}")
            failed_entries.append(sentence_count)
            extract_errors += 1

        sentence_count += 1
    
    remove_entries_that_failed(failed_entries)
    sentence_count = 0
    prune_errors = 0
    
    logger.info(f">>>> Pruning extracted Relationship from sentences <<<<")
    for outputs in pipe(pruning_prompts_generator(processed_relationships), max_new_tokens=512, batch_size=BATCH_SIZE, return_full_text = False):
        generated_response = outputs[0]["generated_text"].strip()
        
        logger.debug(f"--->>> Generated Response for Relationship Pruning\n{generated_response}")
        
        try:
            extracted_pruned_triplets = GemmaParser.extract_pruned_relationships(generated_response)
            logger.debug(f"Final Triplets: {extracted_pruned_triplets}")

            current_entry = entries[sentence_count]

            logger.debug(f"Saving results for entry {current_entry}")
            results.add_result(extracted_pruned_triplets, current_entry["category"], current_entry["eid"])
            results.add_modified_triplets(current_entry["modified_triple_sets"]["mtriple_set"], current_entry["category"], current_entry["eid"])
        except:
            logging.exception(f">>>Failed to process response:\n {generated_response}")
            prune_errors += 1

        sentence_count += 1
    
    logger.info(f"Total processing time: {time.time() - start_time}s")
    logger.info(f"Total of {extract_errors + entities_errors + prune_errors} entries failed to be processed")
    results.write_results_files()

