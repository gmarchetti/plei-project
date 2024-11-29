prompt_base_with_example = """ 

I want you to identify the object, subject and relationship between them from a set of sentences.

Using the following sentence as an example:

1. The Andrews County Airport is owned by Andrews County, Texas.

The object would be Andrews_County,_Texas, the subject Andrews_County_Airport and the relationship would be owner. Note that the
object and subject must be different entities!

Now do the same process for the following sentences, creating AT MOST {num} triples, even if there is more than one sentence:

{sent}
"""

zero_shot = [
    {"role": "user",
     "content": """I want to create a Knowledge Graph, so extract the triplet object, property and subject from the sentence {}
The output should be in json format and there should be no white spaces between the tokens."""}
]

class PromptBuilder:
    
    def gen_prompt_with_example(self, sentences, num_triplets):
        concat_sentence = ""
        
        for sentence in sentences:
            concat_sentence += sentence + "\n"
        
        formated_prompt = prompt_base_with_example.format(sent=concat_sentence, num=num_triplets)

        return [
            {"role": "user", "content": formated_prompt}
        ]