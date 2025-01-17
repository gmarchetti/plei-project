sample_answers = [
"""
---
1. **3 Arena**
2. **Críona Ní Dhálaigh**
3. **Dublin**
4. **Republic of Ireland**
5. **Live Nation Entertainment**

---

**Explanation:**

The named entities are the important terms in the text. They can be people, locations, organizations, or other entities that need to be recognized and extracted.


Please let me know if you have any questions.
""",
"""
---
1.  **Indianapolis**
2.  **Anderson**
3.  **Indiana**
4.  **United States**
5.  **Lafayette Township**
6.  **Madison County**
7.  **Indiana**
8.  **Anderson**
9.  **Lafayette Township**
10. **Madison County**
11. **United States**
12. **Indianapolis**


**Please note:**  I want to identify the entities that appear in all the sentences, not necessarily the most frequent.


Let me know what your answer is.
""",
"""
---
1. **Andra**
2. **Rhythm and blues**

---

Please let me me know if you need any more information.
""",
"""
---
***
1. Lemper
2. Arem-Arem
3. Javanese
4. Banana Leaf
5. Rice
6. Vegetables
7. Minced meat


***


**Explanation:**

The named entities in this task are:

- **Lemper:** This is named as a dish variation.
- **Arem-Arem:**  This is a dish name.
- **Javanese:** This refers to a cuisine, a cultural and geographic region.
- **Banana Leaf:** This is a type of leaf commonly used in cooking, especially for certain dishes like Lemper.
- **Rice:** This is a type of grain commonly used in cooking.
- **Vegetables:** This is a general category of food.
- **Minced meat:** This is a type of meat preparation.


Let me know if you have any other questions!
"""
]

expected_responses = [
    ["3 Arena","Críona Ní Dhálaigh","Dublin","Republic of Ireland", "Live Nation Entertainment"],
    ["Indianapolis", "Anderson", "Indiana", "United States", "Lafayette Township", "Madison County"],
    ["Andra", "Rhythm and blues"],
    [ "Lemper", "Arem-Arem", "Javanese", "Banana Leaf", "Rice", "Vegetables", "Minced meat"]
]

import logging
from parsers.gemma_parser import GemmaParser

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("GemmaParser").setLevel(logging.DEBUG)

def test_same_length():
    for idx in range(len(sample_answers)):
        parsed_response = GemmaParser.extract_non_json_entities(sample_answers[idx])
        assert len(parsed_response) == len(expected_responses[idx])

def test_all_relationships_are_expected():
    for idx in range(len(sample_answers)):
        parsed_response = GemmaParser.extract_non_json_entities(sample_answers[idx])
        for pr in parsed_response:
            assert pr in expected_responses[idx]

def test_all_expected_relationships_exists():
    for idx in range(len(sample_answers)):
        parsed_response = GemmaParser.extract_non_json_entities(sample_answers[idx])
        for er in expected_responses[idx]:
            assert er in parsed_response