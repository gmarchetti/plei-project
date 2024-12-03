parsed_test_triple = ['Julia Morgan | is | architect', 'Julia Morgan | designed | Asilomar Conference Grounds', 'Julia Morgan | designed | The Riverside Art Museum', 'Julia Morgan | designed | Hearst Castle', 'Julia Morgan | designed | The Los Angeles Herald Examiner building']

import xml.etree.ElementTree as ElementTree

class ResultsBuilder:
    def __init__(self, model_name) -> None:
        self.__model_name = model_name
        self.__sample_root = ElementTree.fromstring("<benchmark> </benchmark>")
        self.__result_root = ElementTree.fromstring("<benchmark> </benchmark>")

        results_entries_element = ElementTree.Element("entries")
        samples_entries_element = ElementTree.Element("entries")

        self.__result_root.append(results_entries_element)
        self.__sample_root.append(samples_entries_element)

    def add_result(self, list_of_results, category, eid):
        entry_element = self.__result_root.find("entries")

        new_entry = ElementTree.Element("entry")
        new_entry.set("category", category)
        new_entry.set("eid", str(eid))
        
        generated_triples = ElementTree.Element("generatedtripleset")
        for entry in list_of_results:
            new_gtriple = ElementTree.Element("gtriple")
            new_gtriple.text = entry
            generated_triples.append(new_gtriple)

        new_entry.append(generated_triples)
        entry_element.append(new_entry)

    def add_modified_triplets(self, list_of_modified_triplets, category, eid):
        entry_element = self.__sample_root.find("entries")

        new_entry = ElementTree.Element("entry")
        new_entry.set("category", category)
        new_entry.set("eid", str(eid))
        
        generated_triples = ElementTree.Element("modifiedtripleset")
        for entry_set in list_of_modified_triplets:
            for entry in entry_set:
                new_mtriple = ElementTree.Element("mtriple")
                new_mtriple.text = entry
                generated_triples.append(new_mtriple)

        new_entry.append(generated_triples)
        entry_element.append(new_entry)

    def print_results(self):
        print(ElementTree.tostring(results.__sample_root))
        # print(ElementTree.tostring(results.__result_root))

    def write_results_files(self):
        result_tree = ElementTree.ElementTree(self.__result_root)
        samples_tree = ElementTree.ElementTree(self.__sample_root)
        result_tree.write(f"./results/{self.__model_name}-candidates.xml")
        samples_tree.write(f"./results/{self.__model_name}-references.xml")

if __name__ == '__main__':
    results = ResultsBuilder("sample")
    
    results.add_result(parsed_test_triple, "Airport", 40)
    results.add_modified_triplets(parsed_test_triple, "Airport", 40)


    results.write_results_files()
    # results.print_results()