import requests
import json

from tenacy_api.config import API_URL

# Generate a token from a name and an email to access the API
class TokenGenerator:
    URL = "{}/register".format(API_URL)
    HEADERS = {
        "Content-Type": "application/json",
        "Origin": "http://localhost:8080"
    }

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def call(self):
        response = requests.post(self.URL, headers=self.HEADERS, data=self.__data())
        if response.status_code == 200:
            return response.json()["token"]
        
        raise Exception("Failed to register player: {}".format(response.text))
    
    def __data(self):
        return json.dumps({
            "name": self.name,
            "email": self.email
        })
