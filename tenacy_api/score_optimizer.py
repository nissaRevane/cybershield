from tenacy_api.api_player import ApiPlayer
from tenacy_api.measures_data import MeasuresData

class ScoreOptimizer:
    BUDGET_LIMIT = 100

    def __init__(self, token):
        self.token = token
        self.best_measures = []
        self.best_score = 0
        self.computation_metric = { "api_calls": 0 }
        self.status = { "error": False, "message": "ok" }
    
    def call(self):
        self.__optimize(MeasuresData().all_combinations_of_3_measures())

        if self.status["error"]:
            return {
                "error": True,
                "message": self.status["message"]
            }
        
        return {
            "error": False,
            "best_measures": self.best_measures,
            "best_score": self.best_score,
            "computation_metric": self.computation_metric
        }
    
    def __optimize(self, measures_data_collection):
        for measures_data in measures_data_collection:
            if self.status["error"]:
                break
            if self.__is_over_budget(measures_data):
                continue

            self.computation_metric["api_calls"] += 1
            self.__try_measure(measures_data)
    
    def __is_over_budget(self, measures_data):
        cost = sum(map(lambda measures_data: measures_data["cost"], measures_data))
        return cost > self.BUDGET_LIMIT
    
    def __try_measure(self, measures_data):
        measures_data_identifiers = list(
            map(lambda measures_data: measures_data["identifier"], measures_data)
        )

        try:
            api_response = ApiPlayer(self.token, measures_data_identifiers).call()
            
            score = api_response["score"]

            if score > self.best_score:
                self.best_measures = list(
                    map(lambda measures_data: measures_data["identifier"], measures_data)
                )
                self.best_score = score
        except Exception as e:
            self.status = {
                "error": True,
                "message": "measures {}: {}".format(measures_data_identifiers, e)
            }
