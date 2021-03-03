"""
 This module is a wrapper for the Brickset API v3
"""

import requests
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
        '''
        Returns if a Brickset request has no error in the response, otherwise raises InvalidRequest.
        '''

        # Check API status code, if 200 then check payload response for error
        if request.status_code == 200:
            jsonResponse = request.json()

            if jsonResponse["status"] == 'error':
                raise InvalidRequest('Brickset error was {}'.format(jsonResponse["message"]))
            return

    @staticmethod
    def processHttpRequest(url, payload):
        '''
        Processes an HTTP request, raises a SystemExit exception on failure
        :param str url: API url
        :param str payload: JSON payload
        :returns: If the HTTP response is good, this method will return the ``request``.
        :rtype: `request`
        :raises: :class:`pyBrickset.errors.InvalidApiKey`
        '''

        try:
            response = requests.post(url,data=payload)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err) from err

    @staticmethod
    def checkSetId(request, setId):
        '''
        Checks that a Brickset SetId is valid.
        :param request request: Returned API request
        :param str setId:
        :returns: If the key is valid, this method will return ``True``.
        :rtype: `bool`
        :raises: :class:`pyBrickset.errors.InvalidApiKey`
        '''

        # Check response matches property, if 0 then setId was not found so is invalid
        jsonResponse = request.json()

        if jsonResponse["matches"] == 0:
            raise InvalidSetId('SetId {} was not found so is invalid'.format(setId))

    def checkApiKey(self, apiKey=None):
        '''
        Checks that an API key is valid.
        :param str apiKey: (optional) A key that you want to check the validity of.
           Defaults to the one provided on initialization.
        :returns: If the key is valid, this method will return ``True``.
        :rtype: `bool`
        :raises: :class:`pyBrickset.errors.InvalidApiKey`
        '''

        if not apiKey:
            apiKey = self.apiKey

        payload = {
            'apiKey': apiKey or self.apiKey
        }
        url = self.BASEURL.format('/checkKey')

        response = self.processHttpRequest(url, payload)

        jsonResponse = response.json()
        if jsonResponse["status"] == 'error':
            raise InvalidApiKey('The provided API key {} was invalid.'.format(apiKey))
        return True

    def login(self, username, password):
        '''
        Logs into Brickset as a user, returning a userhash, which can be used in other methods.
        The user hash is stored inside the client (:attr:`userHash`).
        :param str username: Your Brickset username.
        :param str password: Your Brickset password.
        :returns: If the login is valid, this will return ``True``.
        :rtype: `bool`
        :raises: :class:`pyBrickset.errors.InvalidLoginCredentials`
        '''
        payload = {
            'apiKey': self.apiKey,
            'username': username,
            'password': password,
        }
        url = self.BASEURL.format('/login')

        response = self.processHttpRequest(url, payload)

        jsonResponse = response.json()
        if jsonResponse["status"] == 'error':
            raise InvalidLoginCredentials('{}'.format(jsonResponse["message"]))

        self.userHash = jsonResponse["hash"]
        return True

    def getThemes(self):
        '''
        Gets a list Lego themes.
        :returns: A list of themes.
        :rtype: list
        '''
        payload = {
            'apiKey': self.apiKey
        }
        url = self.BASEURL.format('/getThemes')

        response = self.processHttpRequest(url, payload)
        self.checkResponse(response)

        jsonResponse = response.json()
        return jsonResponse["themes"]

    def getInstructions(self, setId):
        '''
        Get the instructions for a set.
        :param str setId: The ID for the set you want to get the instructions of.
        :returns: A list of URLs to instructions.
        :rtype: List[`dict`]
        '''

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
