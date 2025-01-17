sample_answers = ["""```json
[
  {
    "subject": "Anders Osborne",
    "object": "Rock music",
    "relationship": "exponent"
  },
  {
    "subject": "Anders Osborne",
    "object": "Billy Iuso",
    "relationship": "associated"
  },
  {
    "subject": "Anders Osborne",
    "object": "Tab Benoit",
    "relationship": "associated"
  },
  {
    "subject": "Anders Osborne",
    "object": "Galactic",
    "relationship": "associated"
  }
]
```""",
"""
```json
{
  "subject": "Audi e-tron",
  "object": "Audi",
  "relationship": "division"
}
```""",
"""Given this list of phrases: 
1. Allan Shivers, who worked as a member of the Texas State Senate from District 4 (Port Arthur), served in the Democratic Party in the US, where he was succeeded by Price Daniel.
2. Allan Shivers, a member of the Democratic Party in the United States, worked as a member of the Texas State Senate from District 4 (Port Arthur) and was succeeded by Price Daniel.
3. Democratic, Texas State Senate District 4 for Port Arthur member Allan Shivers was succeeded by Price Daniel.
 and using these entities: 
1. Allan Shivers
2. Texas State Senate
3. District 4
4. Port Arthur
5. Democratic Party
6. US
7. Price Daniel
, I want you to describe the relation between each one of them. 

Additional instructions that you have to follow:
Each relation between entities should use only 1 word
Your output should follow the format: {"object":"Entity 1", "relationship":"Relationship Description", "subject":"Entity 2"}

**Example:**
{"object":"Texas State Senate", "relationship":"Location", "subject":"Allan Shivers"}

**Your task:**

```json
[
  {"object":"Allan Shivers", "relationship":"Member", "subject":"Texas State Senate"},
  {"object":"Texas State Senate", "relationship":"Location", "subject":"District 4"},
  {"object":"District 4", "relationship":"Location", "subject":"Port Arthur"},
  {"object":"Democratic Party", "relationship":"Political Party", "subject":"Allan Shivers"},
  {"object":"US", "relationship":"Location", "subject":"Allan Shivers"},
  {"object":"Price Daniel", "relationship":"Successor", "subject":"Allan Shivers"}
]
```

**Please provide the output in the same format.**
""",
"""
Failed to process response: Given this list of phrases: 
1. Adam McQuaid was originally drafted to the Columbus Blue Jackets out of Columbus, Ohio. He nows plays with the Boston Bruins whose general manager is Don Sweeney.
2. Don Sweeney is general manager for the Boston Bruins, the team Adam McQuaid played for. McQuaid was drafted to the Columbus Blue Jackets, from Columbus, Ohio.
3. Adam McQuaid was drafted with the Columbus Blue Jackets in Columbus, Ohio. He played for the Boston Bruins whose manager is Don Sweeney.
 and using these entities: 
1. Adam McQuaid
2. Columbus Blue Jackets
3. Boston Bruins
4. Don Sweeney
5. Columbus, Ohio
6. Boston
, I want you to describe the relation between each one of them. 

Additional instructions that you have to follow:
Each relation between entities should use only 1 word
Your output should follow the format: {"object":"Entity 1", "relationship":"Relationship Description", "subject":"Entity 2"}

**Example:**
{"object":"Columbus Blue Jackets", "relationship":"Drafted", "subject":"Adam McQuaid"}

**Your task:**

```json
[
  {"object": "Adam McQuaid", "relationship": "Drafted", "subject": "Columbus Blue Jackets"},
  {"object": "Columbus Blue Jackets", "relationship": "Drafted", "subject": "Adam McQuaid"},
  {"object": "Boston Bruins", "relationship": "Team", "subject": "Adam McQuaid"},
  {"object": "Don Sweeney", "relationship": "Manager", "subject": "Boston Bruins"},
  {"object": "Columbus, Ohio", "relationship": "Location", "subject": "Adam McQuaid"},
  {"object": "Boston", "relationship": "Location", "subject": "Adam McQuaid"},
  {"object": "Don Sweeney", "relationship": "General Manager", "subject": "Boston Bruins"},
  {"object": "Columbus Blue Jackets", "relationship": "Team", "subject": "Adam McQuaid"}
]
```

**Your output:**

```json
[
  {"object": "Adam McQuaid", "relationship": "Drafted", "subject": "Columbus Blue Jackets"},
  {"object": "Columbus Blue Jackets", "relationship": "Drafted", "subject": "Adam McQuaid"},
  {"object": "Boston Bruins", "relationship": "Team", "subject": "Adam McQuaid"},
  {"object": "Don Sweeney", "relationship": "Manager", "subject": "Boston Bruins"},
  {"object": "Columbus, Ohio", "relationship": "Location", "subject": "Adam McQuaid"},
  {"object": "Boston", "relationship": "Location", "subject": "Adam McQuaid"},
  {"object": "Don Sweeney", "relationship": "General Manager", "subject": "Boston Bruins"},
  {"object": "Columbus Blue Jackets", "relationship": "Team", "subject": "Adam McQuaid"}
]
```

**Explanation:**

The provided phrases describe the career of Adam McQuaid, his draft, his team, and his manager. 

Here's a breakdown of the relationships:

* **Adam McQuaid** was **Drafted** by the **Columbus Blue Jackets**.
* **Columbus Blue Jackets** drafted **Adam McQuaid**.
* **Adam McQuaid** plays for the **Boston Bruins**.
""",
"""
Your output should follow the format: ***Entity | Relationship | Entity 2 ***

Here's the output for the given phrases:

**1. Aleksandr Prudnikov | Played for | FC Spartak Moscow**
**2. Aleksandr Prudnikov | Is attached to | FC Spartak Moscow**
**3. Aleksandr Prudnikov | Played for | FC Spartak Moscow**
**4. Aleksandr Prudnikov | Plays for | FC Kuban Krasnodar** 
"""]

import re
import json
import logging

class GemmaParser:
  
  def __build_json_object(answer):
    json_section_pattern = r'```json[^`]*```'
    json_section = re.findall(json_section_pattern, answer)[0] 

    logging.debug("--->>> JSON Section")
    logging.debug(json_section)

    json_pattern = r'[\{\[][.\w\W]*[\W]*[\]\}]'
    json_string = re.findall(json_pattern, json_section)
    
    logging.debug("--->>> JSON String")
    logging.debug(json_string[0])

    json_object = json.loads(json_string[0])

    return json_object
  
  def extract_entities(answer):
    json_object = GemmaParser.__build_json_object(answer)

    entities_dict = {}

    for entry in json_object:
      entity_name = None
      
      if isinstance(entry, dict):
        entity_name = entry["entity"]
      elif isinstance(entry, str):
        entity_name = entry
      
      if entity_name != None:
        entities_dict[entity_name] = 1

    entity_list = list(entities_dict.keys())

    return entity_list

  def extract_triples_from_lines(answer):
    line_pattern = r'^[*]+.*'
    triples_line = re.findall(line_pattern, answer, re.RegexFlag.M)

    logging.debug("--->>> Lines section")
    logging.debug(triples_line)

    triples = []
    for line in triples_line:
      edge_pattern = r'[*]+\d?\.?'
      cleaned_line = re.sub(edge_pattern, "", line)
      
      logging.debug(cleaned_line)
      composite_word_patter = r'\b\ \b'
      space_for_underscore = re.sub(composite_word_patter, "_", cleaned_line)

      logging.debug(space_for_underscore)

      triples.append(space_for_underscore)
    
    return triples

  def extract_triples(answer):
    triples_objects = GemmaParser.__build_json_object(answer)

    triples = []

    if isinstance(triples_objects, list):
      for triple in triples_objects:
        triples.append(f"{triple["object"].replace(" ", "_")} | {triple["relationship"].replace(" ", "_")} | {triple["subject"].replace(" ", "_")}")
    elif isinstance(triples_objects, dict) and "sentences" in triples_objects.keys():
      for triple in triples_objects["sentences"]:
        triples.append(f"{triple["object"].replace(" ", "_")} | {triple["relationship"].replace(" ", "_")} | {triple["subject"].replace(" ", "_")}")
    else:
      triples.append(f"{triples_objects["object"].replace(" ", "_")} | {triples_objects["relationship"].replace(" ", "_")} | {triples_objects["subject"].replace(" ", "_")}")
    return triples
  
  def extract_relationship(answer):
    relationship_array = GemmaParser.__build_json_object(answer)

    logging.debug("--->>> JSON Object")
    logging.debug(relationship_array)

    relationships = []

    for relationship_dict in relationship_array:
      for relationship in iter(relationship_dict.values()):
        relationships.append(relationship)

    return relationships

  def extract_pruned_relationships(answer):    
    pruned_relations = []
    final_list_pattern = r'[`]+LIST_START[`]*\s^[\d]*[\W\w.]+[`]'
    final_list_region = re.findall(final_list_pattern, answer, re.RegexFlag.M)[0]

    logging.debug("--->>> LIST REGION")
    logging.debug(final_list_region)

    list_of_matches_pattern = r'^[\d]*\.*[\w\ \_\-]*\|[\w\ \_\-]*\|[\w\ \_\-]*$'
    list_of_matches = re.findall(list_of_matches_pattern, final_list_region, re.RegexFlag.M)

    logging.debug(f"List of matched lines: {list_of_matches}")

    for line in list_of_matches:
      logging.debug(f"Parsing relationship from line: {line}")
      relationship = re.sub(r'[\d]+\.\s', "", line)
      pruned_relations.append(relationship)

    return pruned_relations

  def extract_non_json_entities(answer):
    entities_dict = {}

    entities_line_pattern = r'^[\d]*\. [\w\W\.]*?$'
    entities_lines = re.findall(entities_line_pattern, answer, re.RegexFlag.M)
    
    entity_name_pattern = r'[\d]\.\ [\W\w]*?$'

    logging.debug(f"Lines of entities: {entities_lines}")
    for line in entities_lines:
      entity_name = re.findall(entity_name_pattern, line, re.RegexFlag.M)[0]
      entity_name = re.sub(r'[\d]\.\ +', "", entity_name) #remove number and space from beginning
      entity_name = re.sub(r'\*', "", entity_name) #remove * surrounding names
      logging.debug(f"Entities: {entity_name}")
      entities_dict[entity_name] = 1

    entity_list = list(entities_dict.keys())

    return entity_list