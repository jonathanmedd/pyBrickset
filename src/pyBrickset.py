import requests
import json
import sys
from errors import InvalidRequest, InvalidApiKey, InvalidLoginCredentials, InvalidSetId

# params = {"words": 10, "paragraphs": 1, "format": "json"}

class Client:
    '''
    A wrapper for Brickset.com's API v3.
    All endpoints require an API key. Inventory functions require a login to have been processed
    :param str apiKey: The API key you got from Brickset.
    :raises pyBrickset.errors.InvalidApiKey: If the key provided is invalid.
    '''

    BASEURL = 'https://brickset.com/api/v3.asmx{}'

    def __init__(self, apiKey):
        self.apiKey = apiKey
        self.userHash = ''

        # Check the provided key
        self.checkApiKey()

    @staticmethod
    def checkResponse(request):

        # Check API status code, if 200 then check payload response for error
        if request.status_code == 200:
            jsonResponse = request.json()

            if jsonResponse["status"] == 'error':
                raise InvalidRequest('Brickset error was {}'.format(jsonResponse["message"]))
            return

    @staticmethod
    def processHttpRequest(url, payload):
        try:
            r = requests.post(url,data=payload)
            r.raise_for_status()
            return r
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

    @staticmethod
    def checkSetId(request, setId):

        # Check response matches property, if 0 then setId was not found so is invalid
        jsonResponse = request.json()

        if jsonResponse["matches"] == 0:
            raise InvalidSetId('SetId {} was not found so is invalid'.format(setId))
        return

    def checkApiKey(self, apiKey=None):
        '''
        Checks that an API key is valid.
        :param str apiKey: (optional) A key that you want to check the validity of. Defaults to the one provided on initialization.
        :returns: If the key is valid, this method will return ``True``.
        :rtype: `bool`
        :raises: :class:`pyBrickset.errors.InvalidApiKey`
        '''

        if not apiKey: apiKey = self.apiKey

        payload = {
            'apiKey': apiKey or self.apiKey
        }
        url = self.BASEURL.format('/checkKey')

        response = self.processHttpRequest(url, payload)

        jsonResponse = response.json()
        if jsonResponse["status"] == 'error':
            raise InvalidApiKey('The provided API key {} was invalid.'.format(apiKey))
        return True

    def getThemes(self):
        payload = {
            'apiKey': self.apiKey
        }
        url = self.BASEURL.format('/getThemes')

        response = self.processHttpRequest(url, payload)
        self.checkResponse(response)

        jsonResponse = response.json()
        return jsonResponse["themes"]

    def getInstructions(self, setId):
        payload = {
            'apiKey': self.apiKey,
            'setID': setId
        }
        url = self.BASEURL.format('/getInstructions')

        response = self.processHttpRequest(url, payload)
        self.checkResponse(response)
        self.checkSetId(response, setId)

        jsonResponse = response.json()
        return jsonResponse["instructions"]
