import torch
import time
import logging

from prompts_builder import PromptBuilder
from parsers.gemma_parser import GemmaParser
from transformers import pipeline
from datasets import load_dataset
from results.result_file_builder import ResultsBuilder

ENTRIES_TO_USE = 3
BATCH_SIZE = 1

model_names = {
#  "qwen": "Qwen/Qwen2.5-1.5B-Instruct",
 "gemma-2" : "google/gemma-2-2b-it",
#  "llama-3.2" : "meta-llama/Llama-3.2-1B-Instruct"
}

dataset = load_dataset("webnlg-challenge/web_nlg", "release_v3.0_en", split="dev", trust_remote_code=True)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

random_entries = dataset.shuffle().select(range(ENTRIES_TO_USE))

prompt_builder = PromptBuilder()

entries_metadata = []

def entities_prompts_generator():
    for entry in random_entries:
        sentences = entry["lex"]["text"]
        number_triplets = entry["size"]
        
        logger.debug(">>>>")
        logger.debug(f"Testing sentences: {sentences}, with model {model_key}")
        logger.debug("---")
        logger.debug(f"Number of triplets expected: {number_triplets}")
        logger.debug("---")
        
        entries_metadata.append({"eid":entry["eid"], "category": entry["category"], "modified_triplets":entry["modified_triple_sets"]["mtriple_set"] })

        yield prompt_builder.gen_prompt_for_extraction(sentences)

def relation_prompts_generator(entities_list, processed_entries):
    
    for idx in range(0, len(entities_list)):
        entry = random_entries[processed_entries[idx]]
        sentences = entry["lex"]["text"]
        entities = entities_list[idx]
        
        logger.debug(">>>>")
        logger.debug(f"Testing sentences: {sentences}, with model {model_key}")
        logger.debug("---")
        logger.debug(f"Entities: {entities}")
        logger.debug("---")

        yield prompt_builder.gen_prompt_for_relations(sentences, entities)

for model_key in model_names:

    pipe = pipeline(
        "text-generation",
        model=model_names[model_key],
        model_kwargs={"torch_dtype": torch.bfloat16},
        device="cuda",  # replace with "mps" to run on a Mac device
    )
    
    results = ResultsBuilder(model_key, "multi")
    sentence_count = 0    

    start_time = time.time()    
    
    entities_array = []
    processed_entities = []
    entities_errors = 0

    for outputs in pipe(entities_prompts_generator(), max_new_tokens=512, batch_size=BATCH_SIZE):
        logger.info(f"Processing entities from {sentence_count} of {ENTRIES_TO_USE}")
        generated_response = outputs[0]["generated_text"].strip()
        
        logger.debug("---")
        logger.debug(generated_response)
        
        try:
            entities_array.append(GemmaParser.extract_entities(generated_response))
            processed_entities.append(sentence_count)
            logger.debug(entities_array[-1])
        except:
            logging.exception(f">>> Failed to process entities <<<\n{generated_response}")
            entities_errors += 1

        sentence_count += 1

    sentence_count = 0
    extract_errors = 0
    for outputs in pipe(relation_prompts_generator(entities_array, processed_entities), max_new_tokens=512, batch_size=BATCH_SIZE):
        logger.info(f"Processing relations from {sentence_count} of {ENTRIES_TO_USE}")
        generated_response = outputs[0]["generated_text"].strip()
        
        logger.debug("---")
        logger.debug(generated_response)
        
        try:
            generated_triplets = GemmaParser.extract_triples_from_lines(generated_response)

            logger.debug(generated_triplets)

            results.add_result(generated_triplets, entries_metadata[sentence_count]["category"], entries_metadata[sentence_count]["eid"])
            results.add_modified_triplets(entries_metadata[sentence_count]["modified_triplets"], entries_metadata[sentence_count]["category"], entries_metadata[sentence_count]["eid"])
        except:
            logging.exception(f"Failed to process response: {generated_response}")
            extract_errors += 1

        sentence_count += 1
    logger.info(f"Total processing time: {time.time() - start_time}s")
    logger.info(f"Total of {extract_errors + entities_errors} entries failed to be processed")
    results.write_results_files()

