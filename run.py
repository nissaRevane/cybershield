import random

from tenacy_api.token_generator import TokenGenerator
from tenacy_api.score_computer import ScoreComputer
from tenacy_api.measures_data import MeasuresData

name = "player{}".format(random.randint(0, 1000))
email = "{}@email.io".format(name)

token = TokenGenerator(name, email).call()
measures_identifiers = MeasuresData().identifiers()

measures = random.sample(measures_identifiers, 3)
score = ScoreComputer(token, measures).call()

print("For measures: {} the score is: {}".format(", ".join(measures), score))
