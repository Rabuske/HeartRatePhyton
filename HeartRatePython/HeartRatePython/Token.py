import datetime

class Token(object):
    accessToken = None
    refreshToken = None
    generationDate = None
    expiresIn = None # in seconds
    type = None
    userId  = None
    
    def __init__(self, userId, accessToken, refreshToken, type, expiresIn, generationDate=None):
        self.userId = userId
        self.accessToken = accessToken
        self.refreshToken = refreshToken
        self.type = type
        self.expiresIn = expiresIn
        self.generationDate = generationDate
        if self.generationDate == None:
            self.generationDate = datetime.datetime.utcnow().timestamp()

    def isExpired(self):
        expirationDate = float(self.generationDate) + float(self.expiresIn)
        if datetime.datetime.utcnow().timestamp() > expirationDate:
            return True
        else:
            return False

    # Create an object of the type Token based on a response from the Requests package
    def createFromDDIC(dictionary):
        try:
            return Token(dictionary[0], dictionary[1], dictionary[2], dictionary[3], dictionary[4], dictionary[5])
        except KeyError as e:
            return Token(dictionary["user_id"], dictionary["access_token"], dictionary["refresh_token"], dictionary["token_type"], dictionary["expires_in"])        
    