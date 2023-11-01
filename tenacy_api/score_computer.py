import requests
import json

from tenacy_api.config import API_URL

class ScoreComputer:
    URL = "{}/play".format(API_URL)

    def __init__(self, token, measures_data):
        self.token = token
        self.measures_data = measures_data
    
    def call(self):
        response = requests.post(self.URL, headers=self.__headers(), data=self.__data())
        if response.status_code == 200:
            return response.json()["score"]
        
        return 0

    def __headers(self):
        return({
            "Content-Type": "application/json",
            "Origin": "http://localhost:8080",
            "Authorization": "Bearer {}".format(self.token)
        })
    
    def __data(self):
        return json.dumps({ "measures": self.measures_data })