import random

from tenacy_api.token_generator import TokenGenerator
from tenacy_api.score_optimizer import ScoreOptimizer
from tenacy_api.measures_data import MeasuresData

name = "player{}".format(random.randint(0, 1000))
email = "{}@email.io".format(name)

token = TokenGenerator(name, email).call()
best_solution = ScoreOptimizer(token).call()

best_measures = best_solution["best_measures"]
best_score = best_solution["best_score"]
computation_metric = best_solution["computation_metric"]

print("The best solution have a score of {}".format(best_score))
print("It uses the following measures: {}".format(", ".join(best_measures)))
print("The computation have been done in {} API requests".format(computation_metric))
