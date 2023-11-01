from tenacy_api.score_computer import ScoreComputer
from tenacy_api.measures_data import MeasuresData

class ScoreOptimizer:
    def __init__(self, token):
        self.token = token
        self.best_measures = []
        self.best_score = 0
        self.computation_metric = 0
    
    def call(self):
        for measures_data in MeasuresData().all_combinations_of_3_measures():
            self.computation_metric += 1
            self.__try_measure(measures_data)
        
        return {
            "best_measures": self.best_measures,
            "best_score": self.best_score,
            "computation_metric": self.computation_metric
        }
    
    def __try_measure(self, measures_data):
        measures_data_identifiers = list(
            map(lambda measures_data: measures_data["identifier"], measures_data)
        )
        score = ScoreComputer(self.token, measures_data_identifiers).call()

        if score > self.best_score:
            self.best_measures = list(
                map(lambda measures_data: measures_data["identifier"], measures_data)
            )
            self.best_score = score
