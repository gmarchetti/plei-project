prompt_base_with_example = """ 
Using the following example of a sentences:

1. The Andrews County Airport is owned by Andrews County, Texas.

and this output example:

"object": "Andrews_County,_Texas",
"property": "owner",
"subject": "Andrews_County_Airport"


extract a single triple with the object, subject and relation from the following sentences:

{}
"""

zero_shot = [
    {"role": "user",
     "content": """I want to create a Knowledge Graph, so extract the triplet object, property and subject from the sentence {}
The output should be in json format and there should be no white spaces between the tokens."""}
]

class PromptBuilder:
    
    def gen_prompt_with_example(self, sentences):
        concat_sentence = ""
        
        for sentence in sentences:
            concat_sentence += sentence + "\n"
        
        formated_prompt = prompt_base_with_example.format(concat_sentence)

        return [{"role": "user", "content": formated_prompt}
]