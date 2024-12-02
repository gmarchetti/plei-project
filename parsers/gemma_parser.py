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
```"""]

import re
import json

class GemmaParser:
    
  def extract_triples(answer):
    json_pattern = r'[\{\[][.\w\W]*[\]\}]'
    json_string = re.findall(json_pattern, answer)
    
    triples_objects = json.loads(json_string[0])
    triples = []

    if isinstance(triples_objects, list):
      for triple in triples_objects:
        triples.append(f"{triple["subject"]} ! {triple["relationship"]} | {triple["object"]}")
    else:
      triples.append(f"{triples_objects["subject"]} | {triples_objects["relationship"]} | {triples_objects["object"]}")
    return triples
    

if __name__ == '__main__':
  print(GemmaParser.extract_triples(sample_answers[1]))