import torch
import time
import logging
from prompts_builder import PromptBuilder
from parsers.gemma_parser import GemmaParser
from transformers import pipeline
from datasets import load_dataset
from results.result_file_builder import ResultsBuilder

ENTRIES_TO_USE = 20
BATCH_SIZE = 1

model_names = {
#  "qwen": "Qwen/Qwen2.5-1.5B-Instruct",
#  "gemma-2" : "google/gemma-2-2b-it",
#  "gemma-2-9" : "google/gemma-2-9b-it",
 "llama-3.2" : "meta-llama/Llama-3.2-3B-Instruct"
}

dataset = load_dataset("webnlg-challenge/web_nlg", "release_v3.0_en", split="dev", trust_remote_code=True)

logger = logging.getLogger(__name__)

random_entries = dataset.shuffle().select(range(ENTRIES_TO_USE))

prompt_builder = PromptBuilder()

entries_metadata = []

def promptsGenerator():
    for entry in random_entries:
        sentences = entry["lex"]["text"]
        number_triplets = entry["size"]
        
        logger.debug(">>>>")
        logger.debug(f"Testing sentences: {sentences}, with model {model_key}")
        logger.debug("---")
        logger.debug(f"Number of triplets expected: {number_triplets}")
        logger.debug("---")
        
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
        logger.info(f"Processing sentence {sentence_count} of {ENTRIES_TO_USE}")
        generated_response = outputs[0]["generated_text"].strip()
        
        logger.debug("---")
        logger.debug(generated_response)
        try:
            generated_triplets = GemmaParser.extract_triples(generated_response)

            logger.debug(generated_triplets)

            results.add_result(generated_triplets, entries_metadata[sentence_count]["category"], entries_metadata[sentence_count]["eid"])
            results.add_modified_triplets(entries_metadata[sentence_count]["modified_triplets"], entries_metadata[sentence_count]["category"], entries_metadata[sentence_count]["eid"])
        except:
            logger.error(f"Failed to process response: {generated_response}")

        sentence_count += 1

    logger.info(f"Total processing time: {time.time() - start_time}s")
    results.write_results_files()

