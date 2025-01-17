sample_answers = [
"""
```LIST_START
1. Helena | OBJECT | 101 Helena
LIST_END```


**Explanation:**

The provided phrases describe the characteristics of the object "101 Helena".  The relationship "Helena | OBJECT | 101 Helena" is the most relevant as it directly states the object and its identifier.

The other phrases are redundant and do not provide additional information about the object.
""",
"""
```LIST_START
1. Julia Morgan | BORN_IN | California
2. Julia Morgan | DESIGNED | Asilomar Conference Grounds
3. Julia Morgan | DESIGNED | Los Angeles Herald Examiner building
4. Julia Morgan | DESIGNED | The Riverside Art Museum
5. Julia Morgan | DESIGNED | Hearst Castle
6. California | LOCATED_IN | Asilomar Conference Grounds
7. California | LOCATED_IN | Los Angeles Herald Examiner building
8. California | LOCATED_IN | The Riverside Art Museum
9. California | LOCATED_IN | Hearst Castle
10. Asilomar Conference Grounds | PART_OF | Los Angeles Herald Examiner building
11. Asilomar Conference Grounds | PART_OF | The Riverside Art Museum
12. Asilomar Conference Grounds | PART_OF | Hearst Castle
```
LIST_END


**Explanation:**

The original list contains relationships that are either redundant or not directly relevant to the core information about Julia Morgan.

Here's a breakdown of why some relationships are removed:

* **Relationship 1:**  "Julia Morgan | BORN_IN | California" is a core fact about her.
* **Relationship 2:** "Julia Morgan | DESIGNED | Asilomar Conference Grounds" is a direct design relationship.
* **Relationship 3:** "Julia Morgan | DESIGNED | Los Angeles Herald Examiner building" is a direct design relationship.
* **Relationship 4:** "Julia Morgan | DESIGNED | The Riverside Art Museum" is a direct design relationship.
* **Relationship 5:** "Julia Morgan | DESIGNED | Hearst Castle" is a direct design relationship.
* **Relationship 6:** "California | LOCATED_IN | Asilomar Conference Grounds" is a location relationship.
* **Relationship 7:** "California | LOCATED_IN | Los Angeles Herald Examiner building" is a location relationship.
* **Relationship 8:** "California | LOCATED_IN | The Riverside Art Museum" is a location relationship.
* **Relationship 9:** "California | LOCATED_IN | Hearst Castle" is a location relationship.
* **Relationship 10:** "Asilomar Conference Grounds | PART_OF | Los Angeles Herald Examiner building" is a part-of relationship.
* **Relationship 11:** "Asilomar Conference Grounds | PART_OF | The Riverside Art Museum" is a part-of relationship.
*
""",
"""
```LIST_START
LIST_END
```

**Explanation:**

The goal is to create a list of relationships that are directly extracted from the provided text and are relevant to the entities.

Here's a breakdown of the relationships and why they are relevant:

* **1. Abilene Regional Airport | LOCATION | Abilene:** This is a direct relationship extracted from the text.
* **2. Abilene Regional Airport | PART_OF | Taylor County:** This is a direct relationship extracted from the text.
* **3. Abilene Regional Airport | STATE | Texas:** This is a direct relationship extracted from the text.
* **4. Abilene Regional Airport | COUNTRY | United States:** This is a direct relationship extracted from the text.
* **5. Abilene | PART_OF | Taylor County:** This is a direct relationship extracted from the text.
* **6. Abilene | STATE | Texas:** This is a direct relationship extracted from the text.
* **7. Abilene | COUNTRY | United States:** This is a direct relationship extracted from the text.
* **8. Taylor County | PART_OF | Texas:** This is a direct relationship extracted from the text.
* **9. Taylor County | COUNTRY | United States:** This is a direct relationship extracted from the text.
* **10. Texas | COUNTRY | United States:** This is a direct relationship extracted from the text.


**Final List:**

```LIST_START
1. Abilene Regional Airport | LOCATION | Abilene
2. Abilene Regional Airport | PART_OF | Taylor County
3. Abilene Regional Airport | STATE | Texas
4. Abilene Regional Airport | COUNTRY | United States
5. Abilene | PART_OF | Taylor County
6. Abilene | STATE | Texas
7. Abilene | COUNTRY | United States
8. Taylor County | PART_OF | Texas
9. Taylor County | COUNTRY | United States
10. Texas | COUNTRY | United States
LIST_END
```
"""
]

expected_responses = [
    ["Helena | OBJECT | 101 Helena"],
    ["Julia Morgan | BORN_IN | California", "Julia Morgan | DESIGNED | Asilomar Conference Grounds", "Julia Morgan | DESIGNED | Los Angeles Herald Examiner building","Julia Morgan | DESIGNED | The Riverside Art Museum", "Julia Morgan | DESIGNED | Hearst Castle", "California | LOCATED_IN | Asilomar Conference Grounds", "California | LOCATED_IN | Los Angeles Herald Examiner building","California | LOCATED_IN | The Riverside Art Museum", "California | LOCATED_IN | Hearst Castle", "Asilomar Conference Grounds | PART_OF | Los Angeles Herald Examiner building", "Asilomar Conference Grounds | PART_OF | The Riverside Art Museum", "Asilomar Conference Grounds | PART_OF | Hearst Castle"],
    [ "Abilene Regional Airport | LOCATION | Abilene", "Abilene Regional Airport | PART_OF | Taylor County", "Abilene Regional Airport | STATE | Texas", "Abilene Regional Airport | COUNTRY | United States", "Abilene | PART_OF | Taylor County", "Abilene | STATE | Texas", "Abilene | COUNTRY | United States", "Taylor County | PART_OF | Texas", "Taylor County | COUNTRY | United States", "Texas | COUNTRY | United States"]
]

import logging
from parsers.gemma_parser import GemmaParser

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("GemmaParser").setLevel(logging.DEBUG)

def test_same_length():
    for idx in range(len(sample_answers)):
        parsed_response = GemmaParser.extract_pruned_relationships(sample_answers[idx])
        assert len(parsed_response) == len(expected_responses[idx])

def test_all_relationships_are_expected():
    for idx in range(len(sample_answers)):
        parsed_response = GemmaParser.extract_pruned_relationships(sample_answers[idx])
        for pr in parsed_response:
            assert pr in expected_responses[idx]

def test_all_expected_relationships_exists():
    for idx in range(len(sample_answers)):
        parsed_response = GemmaParser.extract_pruned_relationships(sample_answers[idx])
        for er in expected_responses[idx]:
            assert er in parsed_response