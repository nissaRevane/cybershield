# cybershield
In a defense game, players manage a company facing cyber-security risks. They select up to 3 cost-limited measures to minimize risks and earn scores.

## Installation

Install requests module with pip:
```bash
python3 -m pip install requests
```

run the script:
```bash
python3 run.py
```

## API

The game server exposes a RESTfull JSON API. The root url is https://technical-test.tools.tenacy.io. The API implements CORS, and will only allow request with origin localhost (any port).

To access API endpoint a token is mandatory (either in Authorization header or as a get parameter of the request). To get the token, we have to register a player with it's name and email.

## Ideas

### 1 - Try everything in your head but only ask for the smart ones

The first idea is to try every combinaition of 3 measures. But we only sent a request if the cost constraint is respected and if at least one measure risk have a better coverage than the best. If this new combinaison is better than the best, we update the best combinaison.

There is 15 measures, so there is 455(3 out of 15) combinations of 3 measures. But we can reduce this number by removing the combinations with a cost higher than 100k. We can also remove the combinations with a risk coverage lower than the best coverage for every risk.

### 2 - Try to be smart and present the bests candidates first

To optimized the number of calls, we can organized the measures from the "best" to the "worst" by sorting them by approximation of their value based on the coverage and the cost. So the best will increase quickly and there will be less calls.

### 3 - Remenber the good ones even if they are not the best

We can also remember the combinations that are not the best but beat other champions in at least on risk. Doing so it will be harder and harder to find a better combination.