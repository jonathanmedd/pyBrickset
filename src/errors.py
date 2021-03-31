"""
 Errors
"""

class InvalidRequest(Exception):
    '''
    The request that was sent to the server was invalid.
    '''

class InvalidApiKey(Exception):
    '''
    The API key provided was invalid and cannot be used.
    '''

class InvalidLoginCredentials(Exception):
    '''
    The login credentials used were invalid.
    '''

class InvalidSetId(Exception):
    '''
    The set ID that was passed is invalid - eg it doesn't exist.
    '''
