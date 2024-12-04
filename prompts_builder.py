prompt_base_with_example = """ 

I want you to identify the object, subject and relationship between them from a set of sentences.

Using the following sentence as an example:

1. The Andrews County Airport is owned by Andrews County, Texas.

The object would be Andrews_County,_Texas, the subject Andrews_County_Airport and the relationship would be owner. Note that the
object and subject must be different entities!

Now for the next sentences, output a JSON object following the same process, creating AT MOST {num} triples, even if there is more than one sentence:

{sent}
"""

entity_extraction_prompt = """You are working in an Entity Identification Task. 
I want you to list  all entities from the following sentences: {sent}. 
Your output should be a JSON array"""

relation_extraction_prompt = """You are working in an Entity Relation Identification Task.
Given this list of phrases: {sent} and using these entities: {ents}, I want you to describe the relation between each one of them. 

Additional instructions that you have to follow:
Each relation between entities should at most 3 word
Your output should follow the format: ***Entity | Relationship | Entity 2 ***"""

class PromptBuilder:
    def concatenate_sentences(sentences):
        concat_sentence = "\n"
        idx = 1

        for sentence in sentences:
            concat_sentence += f"{idx}. " + sentence + "\n"
            idx += 1
        
        return concat_sentence

    def gen_prompt_for_relations(self, sentences, entities):
        concatenated_sentences = PromptBuilder.concatenate_sentences(sentences)
        concatenated_entities = PromptBuilder.concatenate_sentences(entities)

        return relation_extraction_prompt.format(sent=concatenated_sentences, ents=concatenated_entities)

    def gen_prompt_for_extraction(self, sentences):
        return entity_extraction_prompt.format(sent=PromptBuilder.concatenate_sentences(sentences))

    def gen_prompt_with_example(self, sentences, num_triplets):        
        formated_prompt = prompt_base_with_example.format(sent=PromptBuilder.concatenate_sentences(sentences), num=num_triplets)

        return [
            {"role": "user", "content": formated_prompt}
        ]