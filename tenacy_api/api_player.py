import requests
import json

from tenacy_api.config import API_URL

# Calls the API to get the score and risks coverage from a list of measures
class ApiPlayer:
    URL = "{}/play".format(API_URL)

    def __init__(self, token, measures_data):
        self.token = token
        self.measures_data = measures_data
    
    def call(self):
        response = requests.post(self.URL, headers=self.__headers(), data=self.__data())

        if response.status_code == 200:
            return {
                "score": response.json()["score"],
                "risks": self.__risks_coverage(response.json()["risks"])
            }

        raise Exception("Error on API call: {}".format(response.json()["error"]))

    def __headers(self):
        return({
            "Content-Type": "application/json",
            "Origin": "http://localhost:8080",
            "Authorization": "Bearer {}".format(self.token)
        })
    
    def __data(self):
        return json.dumps({ "measures": self.measures_data })

    def __risks_coverage(self, risks):
        list_covergae_risk = list(map(lambda risk: (risk["identifier"], risk["coverage"]), risks))
        return dict(list_covergae_risk)
