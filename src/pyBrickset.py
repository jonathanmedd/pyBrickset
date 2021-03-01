import requests
import json
import sys
from errors import InvalidRequest, InvalidApiKey, InvalidLoginCredentials, InvalidSetID

# params = {"words": 10, "paragraphs": 1, "format": "json"}

class Client:

    BASEURL = 'https://brickset.com/api/v3.asmx/{}'

    def __init__(self, apiKey, raiseError=True):
        self.apiKey = apiKey
        self.userHash = ''

        # Check the provided key
        if not self.checkApiKey() and raiseError:
            raise InvalidApiKey('The provided API key `{}` was invalid.'.format(apiKey))

    @staticmethod
    def checkResponse(request):

        # Check API status code, if 200 then check payload response for error
        if request.status_code == 200:
            jsonResponse = request.json()

            if jsonResponse["status"] == 'error':
                raise InvalidRequest('Brickset error was {}'.format(jsonResponse["status"]))
            return
        else:
            raise InvalidRequest('HTTP error was {}'.format(request.status_code))


    def checkApiKey(self, apiKey=None):
        if not apiKey: apiKey = self.apiKey

        payload = {
            'apiKey': apiKey or self.apiKey
        }
        url = self.BASEURL.format('/checkKey')

        response = requests.post(url,data=payload)
        self.checkResponse(response)

        jsonResponse = response.json()
        if jsonResponse["status"] == 'success':
            return True
        raise InvalidApiKey('The provided API key {} was invalid.'.format(apiKey))


    def getThemes(self):
        # Add check for this variable
        payload = {
            'apiKey': self.apiKey
        }
        url = self.BASEURL.format('/getTheme')

        response = requests.post(url,data=payload)
        self.checkResponse(response)

        jsonResponse = response.json()
        return jsonResponse["themes"]

    def getInstructions(self, setId):
        # Add check for this variable
        payload = {
            'apiKey': self.apiKey,
            'setID': setId
        }
        url = self.BASEURL.format('/getInstructions')

        response = requests.post(url,data=payload)
        self.checkResponse(response)

        jsonResponse = response.json()
        return jsonResponse["instructions"]
