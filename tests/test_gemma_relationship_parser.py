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
""",
"""
You are working in an Information Extraction Task.
Given this list of phrases:
1. Baymax is a character from the film Big Hero 6 starring Scott Adsit. He was created by Steven T Seagle and the American, Duncan Rouleau.
2. American Duncan Rouleau and Steven T. Seagle created Baymax. Baymax is a character in Big Hero 6 which starred Scott Adsit.
3. Baymax was created by American Duncan Rouleau and Steven T. Seagle. Baymax is a character in Big Hero 6 which stars Scott Adsit.
 what are the relationship between the following pairs of entities:
1. Baymax and Big Hero 6
2. Baymax and Scott Adsit
3. Baymax and Steven T Seagle
4. Baymax and Duncan Rouleau
5. Baymax and American
6. Big Hero 6 and Scott Adsit
7. Big Hero 6 and Steven T Seagle
8. Big Hero 6 and Duncan Rouleau
9. Big Hero 6 and American
10. Scott Adsit and Steven T Seagle
11. Scott Adsit and Duncan Rouleau
12. Scott Adsit and American
13. Steven T Seagle and Duncan Rouleau
14. Steven T Seagle and American
15. Duncan Rouleau and American


Additional instructions that you have to follow:
The relationship should be described in a single word
Each entity of the pair should not contain the word AND
If no relationship can be established between the entities based on the phrase, mark it as NONE
Your output should follow the format: {"Entity | Entity 2" : ***Relationship***} inside a JSON array.


```json
[
  {"Baymax | Big Hero 6": "CHARACTER"},
  {"Baymax | Scott Adsit": "CHARACTER"},
  {"Baymax | Steven T Seagle": "CREATOR"},
  {"Baymax | Duncan Rouleau": "CREATOR"},
  {"Big Hero 6 | Scott Adsit": "STARRED"},
  {"Big Hero 6 | Steven T Seagle": "CREATOR"},
  {"Big Hero 6 | Duncan Rouleau": "CREATOR"},
  {"Big Hero 6 | American": "ORIGIN"},
  {"Scott Adsit | Steven T Seagle": "CREATOR"},
  {"Scott Adsit | Duncan Rouleau": "CREATOR"},
  {"Scott Adsit | American": "STARRED"},
  {"Steven T Seagle | Duncan Rouleau": "CREATOR"},
  {"Steven T Seagle | American": "CREATOR"},
  {"Duncan Rouleau | American": "CREATOR"}
]
```

**Explanation:**

Here's the breakdown of the relationships extracted from the provided phrases:

* **{"Baymax | Big Hero 6": "CHARACTER"}**:  Baymax is a character within the film Big Hero 6.
* **{"Baymax | Scott Adsit": "CHARACTER"}**:  Scott Adsit voices the character Baymax.
* **{"Baymax | Steven T Seagle": "CREATOR"}**:  Steven T. Seagle created the character Baymax.
* **{"Baymax | Duncan Rouleau": "CREATOR"}**:  Duncan Rouleau co-created the character Baymax.
* **{"Big Hero 6 | Scott Adsit": "STARRED"}**: Scott Adsit starred in the film Big Hero 6.
* **{"Big Hero 6 | Steven T Seagle": "CREATOR"}**: Steven T. Seagle created the film Big Hero 6.
* **{"Big Hero 6 | Duncan Rouleau": "CREATOR"}**: Duncan Rouleau co-created the film Big Hero 6.
* **{"Big Hero 6 | American": "ORIGIN"}**:  The film Big Hero 6 originated in America.
* **{"Scott Adsit | Steven T Seagle": "CREATOR"}**:  Scott Adsit and Steven T. Seagle are both creators of the film Big Hero 6.
* **{"Scott Adsit |
""",
"""
You are working in an Information Extraction Task.
Given this list of phrases:
1. California, where some parts speak Chinese, is home to Antioch, which covers 75.324 square kilometres of Contra Costa County in the San Francisco Bay area.
2. Antioch and the San Francisco bay area are parts of Contra Costa County in California. The total area of Antioch is 75.324 square km and Chinese is one of the spoken languages in California.
3. With a total area of 75.324 square km, Antioch is part of Contra Costa County. This county is part of the San Francisco Bay area, in California, where, in some parts, Chinese is spoken.
 what are the relationship between the following pairs of entities:
1. California and Antioch
2. California and Contra Costa County
3. California and San Francisco Bay area
4. California and Chinese
5. Antioch and Contra Costa County
6. Antioch and San Francisco Bay area
7. Antioch and Chinese
8. Contra Costa County and San Francisco Bay area
9. Contra Costa County and Chinese
10. San Francisco Bay area and Chinese


Additional instructions that you have to follow:
The relationship should be described in a single word
Each entity of the pair should not contain the word AND
If no relationship can be established between the entities based on the phrase, mark it as NONE
Your output should follow the format: {"Entity | Entity 2" : ***Relationship***} inside a JSON array.

**Answer:**
```json
[
{"California | Antioch": "home to", "California | Contra Costa County": "part of", "California | San Francisco Bay area": "part of", "California | Chinese": "where spoken", "Antioch | Contra Costa County": "part of", "Antioch | San Francisco Bay area": "part of", "Antioch | Chinese": "spoken in", "Contra Costa County | San Francisco Bay area": "part of", "San Francisco Bay area | Chinese": "where spoken"}
]
```


**Explanation:**

Here's a breakdown of the relationships extracted from the phrases:

* **California | Antioch:**  "home to" -  California is the location where Antioch is situated.
* **California | Contra Costa County:** "part of" -  California encompasses Contra Costa County.
* **California | San Francisco Bay area:** "part of" -  California includes the San Francisco Bay area.
* **California | Chinese:** "where spoken" -  Chinese is spoken in California.
* **Antioch | Contra Costa County:** "part of" -  Antioch is located within Contra Costa County.
* **Antioch | San Francisco Bay area:** "part of" -  Antioch is within the San Francisco Bay area.
* **Antioch | Chinese:** "spoken in" -  Chinese is spoken in Antioch.
* **Contra Costa County | San Francisco Bay area:** "part of" -  Contra Costa County is a part of the San Francisco Bay area.
* **San Francisco Bay area | Chinese:** "where spoken" -  Chinese is spoken in the San Francisco Bay area.


Let me know if you have any other text you'd like me to analyze!
"""
]

expected_responses = [
    ["BORN_IN","PLAYS_WITH","ASSOCIATED_WITH","ASSOCIATED_WITH","ASSOCIATED_WITH","ASSOCIATED_WITH"],
    ["BORN_IN", "FROM", "LEADER_OF"],
    ["CHARACTER","CHARACTER","CREATOR","CREATOR","STARRED","CREATOR","CREATOR","ORIGIN","CREATOR","CREATOR","STARRED","CREATOR","CREATOR","CREATOR"],
    ["home to", "part of", "part of", "where spoken", "part of", "part of", "spoken in", "part of", "where spoken"]
]

import logging
import sys
from parsers.gemma_parser import GemmaParser

logging.basicConfig(level=logging.DEBUG)

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