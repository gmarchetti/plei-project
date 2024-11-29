sample_answers = ["""Here's a breakdown of the triples and the reasoning:

**Understanding the Format**

The output format you provided is:

```json
{
  "object": "object_name",
  "property": "relationship_type",
  "subject": "subject_name"
}
```

* **object:** The entity being described.
* **property:** The relationship between the object and subject.
* **subject:** The entity performing the action or being described.

**Extracting Triples**

Let's analyze the sentences and extract triples:

**Sentence 1:**

* **The main ethnic group in Japan are the Japanese and the leader is Tarō Asō.**
* **object:** "Japanese"
* **subject:** "main ethnic group in Japan"
* **property:** "is" 

**Sentence 2:**

* **Akita Museum of Art is in Akita, Akita which is part of Japan and the Akita Prefecture.**
* **object:** "Akita Museum of Art"
* **subject:** "Akita, Akita"
* **property:** "is located in"

**Sentence 3:**

* **The leader of Japan is Taro Aso and the main ethnic group in Japan is the Japanese.**
* **object:** "Taro Aso"
* **subject:** "leader of Japan"
* **property:** "is"

**Sentence 4:**

* **Akita, Akita is part of Akita Prefecture.**
* **object:** "Akita, Akita"
* **subject:** "Akita Prefecture"
* **property:** "is part of"

**Sentence 5:**

* **Akita Museum of Art is in the city of Akita, Japan.**
* **object:** "Akita Museum of Art"
* **subject:** "Akita, Japan"
* **property:** "is located in"

**Important Notes:**

* **Context is Key:**  The relationship between the subject and object can be complex.  For example, "Akita, Akita is part of Akita Prefecture" implies a spatial relationship.
* **Multiple Triples:**  A single sentence can have multiple triples, depending on the relationships you want to capture. 
* **Ambiguity:**  Some sentences might have multiple interpretations, leading to multiple possible triples. 

Let me know if you'd like to explore more""",
"""
Here's a triple extracted from the provided sentences:

**object": "Greek_New_Democracy_Party",
"relationship": "member",
"subject": "Adonis_Georgiadis" 

**Explanation:**

* **Subject:** Adonis Georgiadis is the subject of the sentence.
* **Object:** The Greek New Democracy Party is the object of the sentence.
* **Relationship:**  "member" indicates that Adonis Georgiadis is a member of the party. 


Let me know if you'd like to extract more triples from the text!
""",
"""
Here are the object, subject, and relationship triples extracted from the provided sentences:

1. **Estádio Municipal Coaracy da Mata Fonseca** - **Agremiação Sportiva Arapiraquense** - **ground** 
2. **Agremiação Sportiva Arapiraquense** - **play in the Campeonato Brasileiro Série C league** - **participant**
3. **Vila Nova Futebol Clube** - **have been champions of Campeonato Brasileiro Série C** - **champion**
4. **Estádio Municipal Coaracy da Mata Fonseca** - **located in Alagoas** - **location**
5. **Agremiação Sportiva Arapiraquense** - **play in the Campeonato Brasileiro Série C league** - **team** 


**Explanation:**

* **Object:** The entity that receives the action or is acted upon.
* **Subject:** The entity performing the action or initiating the relationship.
* **Relationship:** The connection or association between the subject and object. 


Let me know if you'd like me to elaborate on any of these relationships or provide further analysis!
"""]
import re

class GemmaParser:
    
    def extract_triples(answer):
        triples = []
        
        object_pattern = r'.+object.+\"'
        subject_pattern = r'.+subject.+\"'
        relation_pattern = r'(.+property.+\")|(.+relationship.+\")'
        
        objects_found = re.findall(object_pattern, answer)
        subjects_found = re.findall(subject_pattern, answer)
        relations_found = re.findall(relation_pattern, answer)

        print(objects_found)
        print(subjects_found)
        print(relations_found)

        for i in range(len(objects_found)):
            object_string = objects_found[i].split(" ", 1)[1].strip()
            subject_string = subjects_found[i].split(" ", 1)[1].strip()
            relation_string = relations_found[i].split(" ", 1)[1].strip()

            triplet_string = f"{object_string} | {relation_string} | {subject_string}"
            triples.append(triplet_string)

        return triples
    

if __name__ == '__main__':
    print(GemmaParser.extract_triples(sample_answers[0]))