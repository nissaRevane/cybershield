import json

class MeasuresData:
    def __init__(self):
        with open("tenacy_api/measures_data.json", "r") as measures_file:
            self.measures = json.load(measures_file)
        measures_file.close()

    def get_measures(self):
        return self.measures

    def identifiers(self):
        return list(map(lambda measure: measure["identifier"], self.measures))
    
    def all_combinations_of_3_measures(self):
        measure_length = len(self.measures)
        combinations = []

        for i in range(measure_length):
            for j in range(i + 1, measure_length):
                if i == j:
                    continue
                for k in range(j + 1, measure_length):
                    if i == k or j == k:
                        continue
                    combinations.append([self.measures[i], self.measures[j], self.measures[k]])
        
        return combinations
