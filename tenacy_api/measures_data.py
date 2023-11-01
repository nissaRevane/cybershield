import json

# From a json file, it returns a collection of list of measures
class MeasuresData:
    def __init__(self):
        with open("tenacy_api/measures_data.json", "r") as measures_file:
            self.measures = json.load(measures_file)
        measures_file.close()
    
    def all_combinations_of_3_measures(self):
        coverage_measures = self.__coverage_measures()
        measure_length = len(coverage_measures)
        combinations = []

        for i in range(measure_length):
            for j in range(i + 1, measure_length):
                if i == j:
                    continue
                for k in range(j + 1, measure_length):
                    if i == k or j == k:
                        continue
                    combinations.append(
                        [coverage_measures[i], coverage_measures[j],coverage_measures[k]]
                    )
        
        return combinations
    
    def __coverage_measures(self):
        return list(filter(lambda measure: self.__is_a_coverage_measure(measure), self.measures))
    
    def __is_a_coverage_measure(self, measure):
        return any(map(lambda risk: risk["coverage"] > 0, measure["riskCoverage"]))