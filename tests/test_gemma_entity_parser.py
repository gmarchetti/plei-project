sample_answers = [
"""
You are working in an Entity Identification Task.
I want you to list  all entities from the following sentences:
1. Elliot See, a graduate of University of Texas at Austin, was born in Dallas on July 23, 1927, and died in St. Louis.
.
Your output should be a JSON array:

```json
["Elliot See", "University of Texas at Austin", "Dallas", "St. Louis"]
```

**Explanation:**

The task is to identify and extract named entities from the given text.  Named entities are important for tasks like information extraction, knowledge graph construction, and information retrieval.

Here's how we break down the process:

1. **Sentence Analysis:** We read the sentence carefully to understand the context.
2. **Entity Recognition:** We identify key elements that represent real-world entities.
3. **Entity Extraction:** We extract the entities and their corresponding types.

**Applying this to your example:**

```json
["Elliot See", "University of Texas at Austin", "Dallas", "St. Louis"]
```

**Explanation of Entities:**

* **Elliot See:** Person
* **University of Texas at Austin:** Organization
* **Dallas:** Location
* **St. Louis:** Location


Let me know if you have any other sentences you'd like me to analyze!
"""
]

expected_responses = [
    ["Elliot See","University of Texas at Austin","Dallas","St. Louis"],
]

import logging
from parsers.gemma_parser import GemmaParser

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("GemmaParser").setLevel(logging.DEBUG)

def test_same_length():
    for idx in range(len(sample_answers)):
        parsed_response = GemmaParser.extract_entities(sample_answers[idx])
        assert len(parsed_response) == len(expected_responses[idx])

def test_all_relationships_are_expected():
    for idx in range(len(sample_answers)):
        parsed_response = GemmaParser.extract_entities(sample_answers[idx])
        for pr in parsed_response:
            assert pr in expected_responses[idx]

def test_all_expected_relationships_exists():
    for idx in range(len(sample_answers)):
        parsed_response = GemmaParser.extract_entities(sample_answers[idx])
        for er in expected_responses[idx]:
            assert er in parsed_response