sample_answers = [
"""
```json
[
  {"Alex Day | London Borough of Havering": "BORN_IN"},
  {"Alex Day | Chameleon Circuit": "PLAYS_WITH"},
  {"Alex Day | Charlie McDonnell": "ASSOCIATED_WITH"},
  {"London Borough of Havering | Chameleon Circuit": "ASSOCIATED_WITH"},
  {"London Borough of Havering | Charlie McDonnell": "ASSOCIATED_WITH"},
  {"Chameleon Circuit | Charlie McDonnell": "ASSOCIATED_WITH"}
]
```

**Explanation:**

Here's the breakdown of the relationships based on the provided phrases:

1. **Alex Day | London Borough of Havering:**  **BORN_IN** - The phrase explicitly states Alex Day was born in the London Borough of Havering.
2. **Alex Day | Chameleon Circuit:** **PLAYS_WITH** - The phrase mentions Alex Day plays with the band Chameleon Circuit.
3. **Alex Day | Charlie McDonnell:** **ASSOCIATED_WITH** - The phrase states Alex Day is associated with Charlie McDonnell.
4. **London Borough of Havering | Chameleon Circuit:** **ASSOCIATED_WITH** - The phrase states the London Borough of Havering is associated with Chameleon Circuit.
5. **London Borough of Havering | Charlie McDonnell:** **ASSOCIATED_WITH** - The phrase states the London Borough of Havering is associated with Charlie McDonnell.
6. **Chameleon Circuit | Charlie McDonnell:** **ASSOCIATED_WITH** - The phrase states Chameleon Circuit is associated with Charlie McDonnell.


**Therefore, the JSON array you provided is correct.**
""",
"""
```json
[
  {"Alfredo Zitarrosa | Tabaré Vázquez": "BORN_IN"},
  {"Alfredo Zitarrosa | Uruguay": "FROM"},
  {"Tabaré Vázquez | Uruguay": "LEADER_OF"}
]
```

**Explanation:**

Here's the breakdown of the relationships based on the provided phrases:

* **Alfredo Zitarrosa | Tabaré Vázquez:**  The phrases strongly suggest a connection between these two.  "Alfredo Zitarrosa was born in Tabaré Vázquez led Uruguay" implies a direct link.
    * **Relationship:** BORN_IN
* **Alfredo Zitarrosa | Uruguay:**  The phrase "Alfredo Zitarrosa's birthplace was Uruguay" indicates a connection between him and the country.
    * **Relationship:** FROM
* **Tabaré Vázquez | Uruguay:** The phrase "Tabaré Vázquez is the leader of Uruguay" clearly establishes a leadership role for him within the country.
    * **Relationship:** LEADER_OF


Let me know if you have any other information extraction tasks you'd like to work on!
"""
]

expected_responses = [
    ["BORN_IN","PLAYS_WITH","ASSOCIATED_WITH","ASSOCIATED_WITH","ASSOCIATED_WITH","ASSOCIATED_WITH"],
    ["BORN_IN", "FROM", "LEADER_OF"],
]

from parsers.gemma_parser import GemmaParser


def test_same_length():
    for idx in range(len(sample_answers)):
        parsed_response = GemmaParser.extract_relationship(sample_answers[idx])
        assert len(parsed_response) == len(expected_responses[idx])

def test_all_relationships_are_expected():
    for idx in range(len(sample_answers)):
        parsed_response = GemmaParser.extract_relationship(sample_answers[idx])
        for pr in parsed_response:
            assert pr in expected_responses[idx]

def test_all_expected_relationships_exists():
    for idx in range(len(sample_answers)):
        parsed_response = GemmaParser.extract_relationship(sample_answers[idx])
        for er in expected_responses[idx]:
            assert er in parsed_response