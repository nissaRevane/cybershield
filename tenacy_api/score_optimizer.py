from tenacy_api.api_player import ApiPlayer
from tenacy_api.measures_data import MeasuresData
from tenacy_api.coverage_computer import CoverageComputer

class ScoreOptimizer:
    BUDGET_LIMIT = 100

    def __init__(self, token):
        self.token = token
        self.best_measures = []
        self.best_score = 0
        self.best_coverage = {}
        self.computation_metric = { "api_calls": 0 }
        self.status = { "error": False, "message": "ok" }
    
    def call(self):
        measures_data_collection = self.__ordered_collection_of_measures_data()
        self.__optimize(measures_data_collection)

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

            if not self.__can_increase_coverage(measures_data):
                continue

            self.computation_metric["api_calls"] += 1
            self.__try_measure(measures_data)
    
    def __ordered_collection_of_measures_data(self):
        raw_collection = MeasuresData().all_combinations_of_3_measures()
        on_budget_collection = list(
            filter(lambda measures_data: self.__on_budget(measures_data), raw_collection)
        )

        return sorted(
            on_budget_collection,
            key=lambda measures_data: self.__estimated_impact(measures_data),
            reverse=True
        )

    def __estimated_impact(self, measures_data):
        coverage_by_risk = CoverageComputer(measures_data).call()
        risks_severity = dict(
            map(
                lambda risk: (risk["risk"], risk["severity"]),
                measures_data[0]["riskCoverage"]
            )
        )

        return sum(
            map(lambda risk: coverage_by_risk[risk] * risks_severity[risk], coverage_by_risk)
        )
    
    def __on_budget(self, measures_data):
        cost = sum(map(lambda measures_data: measures_data["cost"], measures_data))
        return cost <= self.BUDGET_LIMIT
    
    def __can_increase_coverage(self, measures_data):
        coverage_by_risk = CoverageComputer(measures_data).call()

        for risk in coverage_by_risk:
            if risk not in self.best_coverage:
                return True

            if coverage_by_risk[risk] > self.best_coverage[risk]:
                return True

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
                self.best_coverage = api_response["risks"]
        except Exception as e:
            self.status = {
                "error": True,
                "message": "measures {}: {}".format(measures_data_identifiers, e)
            }
