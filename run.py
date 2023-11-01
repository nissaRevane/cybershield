import random

from tenacy_api.token_generator import TokenGenerator
from tenacy_api.score_optimizer import ScoreOptimizer

name = "player{}".format(random.randint(0, 1000))
email = "{}@email.io".format(name)

token = TokenGenerator(name, email).call()
optimizer_response = ScoreOptimizer(token).call()

if optimizer_response["error"]:
    print("Error: {}".format(optimizer_response["message"]))
    exit()

best_measures = optimizer_response["best_measures"]
best_score = optimizer_response["best_score"]
computation_metric = optimizer_response["computation_metric"]

print("The best solution have a score of {}".format(best_score))
print("It uses the following measures: {}".format(", ".join(best_measures)))
print("The computation have been done in {} API requests".format(computation_metric["api_calls"]))
