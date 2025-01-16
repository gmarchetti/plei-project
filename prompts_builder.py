prompt_base_with_example = """ 
I want you to identify the object, subject and relationship between them from a set of sentences.

Using the following sentence as an example:

1. The Andrews County Airport is owned by Andrews County, Texas.

The object would be Andrews_County,_Texas, the subject Andrews_County_Airport and the relationship would be owner. Note that the
object and subject must be different entities!

Now for the next sentences, output a JSON object following the same process, creating AT MOST {num} triples, even if there is more than one sentence:

{sent}
"""

entity_extraction_prompt = """
You are working in an Entity Identification Task. 
I want you to list  all entities from the following sentences: {sent}. 
Your output should be a JSON array"""

relation_extraction_prompt = """
You are working in an Entity Relation Identification Task.
Given this list of phrases: {sent} and using these entities: {ents}, I want you to describe the relation between each one of them. 

Additional instructions that you have to follow:
Each relation between entities should at most 3 word
Your output should follow the format: ***Entity | Relationship | Entity 2 ***"""

explicit_relation_prompt = """
You are working in an Information Extraction Task.
Given this list of phrases: {sent} what are the relationship between the following pairs of entities: {ents}

Additional instructions that you have to follow:
The relationship should be described in a single word
Each entity of the pair should not contain the word AND
If no relationship can be established between the entities based on the phrase, mark it as NONE
Your output should follow the format: {{"Entity | Entity 2" : ***Relationship***}} inside a JSON array"""

relationship_pruning_prompt = """
You are working in an Information Extraction Task.
Given this list of phrases:
{sent}

Remove the least relevant relationships from the following list
{rels}

Additional instructions that you have to follow:
Each entity of the pair should not contain the word AND
No new relationship should be added
The list should be smaller than the original one
The output format should be inside a JSON object
"""

class PromptBuilder:
    def concatenate_sentences(sentences):
        concat_sentence = "\n"
        idx = 1

        for sentence in sentences:
            concat_sentence += f"{idx}. " + sentence + "\n"
            idx += 1
        
        return concat_sentence
    def gen_prompt_for_relationship_pruning(self, sentences, relations):
        concatenated_sentences = PromptBuilder.concatenate_sentences(sentences)
        concatenated_relationships = PromptBuilder.concatenate_sentences(relations)

        return relationship_pruning_prompt.format(sent=concatenated_sentences, rels=concatenated_relationships)
    
    def gen_prompt_for_explicit_relations(self, sentences, entities):
        entities_pairs = []
        for i in range(len(entities)):
            for j in range(i, len(entities)):
                if i != j:
                    entities_pairs.append(f"{entities[i]} and {entities[j]}")

        concatenated_sentences = PromptBuilder.concatenate_sentences(sentences)
        concatenated_entities = PromptBuilder.concatenate_sentences(entities_pairs)

        return explicit_relation_prompt.format(sent=concatenated_sentences, ents=concatenated_entities)

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