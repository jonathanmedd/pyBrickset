"""
 This module is a wrapper for the Brickset API v3
"""

# import logging - enable if logging required
import json
import requests
from errors import InvalidRequest, InvalidApiKey, InvalidLoginCredentials, InvalidSetId

# These two lines enable debugging at httplib level (requests->urllib3->http.client)
# You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
# The only thing missing will be the response.body which is not logged.
# try:
#     import http.client as http_client
# except ImportError:
#     # Python 2
#     import httplib as http_client
# http_client.HTTPConnection.debuglevel = 1

# # You must initialize logging, otherwise you'll not see debug output.
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True

class Client:
    '''
    A wrapper for Brickset.com's API v3.
    All endpoints require an API key. Inventory functions require a login to have been processed
    :param str apiKey: The API key you got from Brickset.
    :raises pyBrickset.errors.InvalidApiKey: If the key provided is invalid.
    '''

    baseUrl = 'https://brickset.com/api/v3.asmx{}'

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
                raise InvalidRequest(
                    f'Brickset error was {jsonResponse["message"]}')
            return None

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
            response = requests.post(url, data=payload, timeout=10)
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
            raise InvalidSetId(
                f'SetId {setId} was not found so is invalid')

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
        url = self.baseUrl.format('/checkKey')

        response = self.processHttpRequest(url, payload)

        jsonResponse = response.json()
        if jsonResponse["status"] == 'error':
            raise InvalidApiKey(
                f'The provided API key {apiKey} was invalid.')
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
        url = self.baseUrl.format('/login')

        response = self.processHttpRequest(url, payload)

        jsonResponse = response.json()
        if jsonResponse["status"] == 'error':
            raise InvalidLoginCredentials(f'{jsonResponse["message"]}')

        self.userHash = jsonResponse["hash"]
        return True

    def getSets(self, pageSize=500, **kwargs):
        '''
        Gets a list Lego sets.
        :param str theme: The theme of the set.
        :param str subtheme: The subtheme of the set.
        :param str setNumber: The LEGO set number.
        :param str year: The year in which the set came out.
        :param str orderBy: How you want the set ordered. Accepts 'Number', 'YearFrom', 'Pieces',
        'Minifigs', 'Rating', 'UKRetailPrice', 'USRetailPrice', 'CARetailPrice', 'DERetailPrice',
        'FRRetailPrice','UKPricePerPiece', 'USPricePerPiece', 'CAPricePerPiece', 'DEPricePerPiece',
        'FRPricePerPiece', 'Theme', 'Subtheme', 'Name', 'Random', 'QtyOwned', 'OwnCount',
        'WantCount', 'UserRating', 'CollectionID'.
        :param str owned: Set to 1 to retrieve a user's owned sets.
        :param str wanted: Set to 1 to retrieve a user's wanted sets.
        :param int pageSize: How many results are on a page. Defaults to 500.
        :returns: A list of sets.
        :rtype: list
        '''

        params = {
            'pageSize': pageSize,
            'theme': kwargs.get('theme', ''),
            'subtheme':   kwargs.get('subtheme', ''),
            'setNumber':  kwargs.get('setNumber', ''),
            'year':  kwargs.get('year', ''),
            'orderBy':  kwargs.get('orderBy', ''),
            'owned':  kwargs.get('owned', ''),
            'wanted':  kwargs.get('wanted', '')
        }

        payload = {
            'apiKey': self.apiKey,
            'userHash': self.userHash,
            'params': json.dumps(params)
        }
        url = self.baseUrl.format('/getSets')

        response = self.processHttpRequest(url, payload)
        self.checkResponse(response)

        jsonResponse = response.json()
        return jsonResponse["sets"]

    def getAdditionalImages(self, setId):
        '''
        Get a list of URLs of additional set images for the specified set.
        :param str setId: The ID for the set you want to get the additional set images of.
        :returns: A list of URLs to additional set images.
        :rtype: List[`dict`]
        '''

        payload = {
            'apiKey': self.apiKey,
            'setID': setId
        }
        url = self.baseUrl.format('/getAdditionalImages')

        response = self.processHttpRequest(url, payload)
        self.checkResponse(response)
        self.checkSetId(response, setId)

        jsonResponse = response.json()
        return jsonResponse["additionalImages"]

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
        url = self.baseUrl.format('/getInstructions')

        response = self.processHttpRequest(url, payload)
        self.checkResponse(response)
        self.checkSetId(response, setId)

        jsonResponse = response.json()
        return jsonResponse["instructions"]

    def getReviews(self, setId):
        '''
        Get user reviews for the specified set.
        :param str setId: The ID for the set you want to get the reviews of.
        :returns: A list of reviews of the set.
        :rtype: List[`dict`]
        '''

        payload = {
            'apiKey': self.apiKey,
            'setID': setId
        }
        url = self.baseUrl.format('/getReviews')

        response = self.processHttpRequest(url, payload)
        self.checkResponse(response)
        self.checkSetId(response, setId)

        jsonResponse = response.json()
        return jsonResponse["reviews"]

    def getThemes(self):
        '''
        Gets a list Lego themes.
        :returns: A list of themes.
        :rtype: list
        '''
        payload = {
            'apiKey': self.apiKey
        }
        url = self.baseUrl.format('/getThemes')

        response = self.processHttpRequest(url, payload)
        self.checkResponse(response)

        jsonResponse = response.json()
        return jsonResponse["themes"]

    def getSubthemes(self, Theme): # pylint: disable=invalid-name
        '''
        Get a list of subthemes for a given theme, with the total number of sets in each.
        :param str Theme: Theme to find subthemes for.
        :returns: A list of subthemes for the theme.
        :rtype: list
        '''
        payload = {
            'apiKey': self.apiKey,
            'Theme': Theme
        }
        url = self.baseUrl.format('/getSubthemes')

        response = self.processHttpRequest(url, payload)
        self.checkResponse(response)

        jsonResponse = response.json()
        return jsonResponse["subthemes"]

    def getYears(self, Theme): # pylint: disable=invalid-name
        '''
        Get a list of years for a given theme, with the total number of sets in each.
        :param str Theme: Theme to find years for.
        :returns: A list of years for the theme.
        :rtype: list
        '''
        payload = {
            'apiKey': self.apiKey,
            'Theme': Theme
        }
        url = self.baseUrl.format('/getYears')

        response = self.processHttpRequest(url, payload)
        self.checkResponse(response)

        jsonResponse = response.json()
        return jsonResponse["years"]

    def setCollection(self, setId, **kwargs):
        '''
        Set a user's collection details
        :param str own: 1 or 0. If 0 then qtyOwned is automatically set to 0.
        :param str want: 1 or 0.
        :param str qtyOwned: 0-999. If > 0 then own is automatically set to 1.
        :param str notes: User notes, max 1000 characters.
        :param str rating: User rating 1-5.
        :returns: API result.
        :rtype: String
        '''

        params = {
            'own': kwargs.get('own', ''),
            'want':   kwargs.get('want', ''),
            'qtyOwned':  kwargs.get('qtyOwned', ''),
            'notes':  kwargs.get('notes', ''),
            'rating':  kwargs.get('rating', '')
        }

        payload = {
            'apiKey': self.apiKey,
            'userHash': self.userHash,
            'setID': setId,
            'params': json.dumps(params)
        }
        url = self.baseUrl.format('/setCollection')

        response = self.processHttpRequest(url, payload)
        self.checkResponse(response)

        jsonResponse = response.json()
        return jsonResponse["status"]

    def getUserNotes(self):
        '''
        Get all of a user's set notes.
        :returns: A list of a user's set notes.
        :rtype: list
        '''
        payload = {
            'apiKey': self.apiKey,
            'userHash': self.userHash
        }
        url = self.baseUrl.format('/getUserNotes')

        response = self.processHttpRequest(url, payload)
        self.checkResponse(response)

        jsonResponse = response.json()
        return jsonResponse["userNotes"]

    def getMinifigCollection(self, **kwargs):
        '''
        Get a list of minifigs owned by a user
        :param str own: 1 or 0. If 0 then qtyOwned is automatically set to 0.
        :param str want: 1 or 0.
        :param str query: This can be a minifig number or name. Wildcards are added before and
        after. If omitted, all minifigs owned are returned.
        :returns: A list of owned minifigs.
        :rtype: List[`dict`]
        '''

        params = {
            'owned': kwargs.get('owned', ''),
            'wanted':   kwargs.get('wanted', ''),
            'query':  kwargs.get('query', '')
        }

        payload = {
            'apiKey': self.apiKey,
            'userHash': self.userHash,
            'params': json.dumps(params)
        }
        url = self.baseUrl.format('/getMinifigCollection')

        response = self.processHttpRequest(url, payload)
        self.checkResponse(response)

        jsonResponse = response.json()
        return jsonResponse["minifigs"]

    def setMinifigCollection(self, minifigNumber, **kwargs):
        '''
        Add/change a user's 'loose' minifig collection.
        :param str minifigNumber: BrickLink minifig number.
        :param str own: 1 or 0. If 0 then qtyOwned is automatically set to 0.
        :param str want: 1 or 0.
        :param str qtyOwned: 0-999. If > 0 then own is automatically set to 1.
        :param str notes: User notes, max 1000 characters.
        :returns: API result.
        :rtype: String
        '''

        params = {
            'own': kwargs.get('own', ''),
            'want':   kwargs.get('want', ''),
            'qtyOwned':  kwargs.get('qtyOwned', ''),
            'notes':  kwargs.get('notes', '')
        }

        payload = {
            'apiKey': self.apiKey,
            'userHash': self.userHash,
            'minifigNumber': minifigNumber,
            'params': json.dumps(params)
        }
        url = self.baseUrl.format('/setMinifigCollection')

        response = self.processHttpRequest(url, payload)
        self.checkResponse(response)

        jsonResponse = response.json()
        return jsonResponse["status"]

    def getUserMinifigNotes(self):
        '''
        Get all of a user's minifigure notes.
        :returns: A list of a user's minifigure notes.
        :rtype: list
        '''
        payload = {
            'apiKey': self.apiKey,
            'userHash': self.userHash
        }
        url = self.baseUrl.format('/getUserMinifigNotes')

        response = self.processHttpRequest(url, payload)
        self.checkResponse(response)

        jsonResponse = response.json()
        return jsonResponse["userMinifigNotes"]
