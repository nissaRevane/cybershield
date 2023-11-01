import json

class MeasuresData:
    def __init__(self):
        with open("tenacy_api/measures_data.json", "r") as measures_file:
            self.measures = json.load(measures_file)
        measures_file.close()

    def identifiers(self):
        return list(map(lambda measure: measure["identifier"], self.measures))
