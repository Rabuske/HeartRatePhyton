from Authorization import Authorization
from AppConfig     import AppConfig
import requests
import json

class Fitbit(object):

    authorization = None
    database = None

    def __init__(self, database):
        self.authorization = Authorization()
        self.database = database

    def getHeartRate(self, startDate, endDate = None):
        uri = AppConfig().get("uri_heart")
        uri = uri.replace("[date]", startDate)
        if endDate != None:
            uri = uri.replace("[end-date]", endDate)
        else:
            uri = uri.replace("[end-date]//", "")

        authorizationHeader = self.authorization.getAuthorizationHeader(self.authorization.getToken(self.database))
        response = requests.get(uri, headers={ "Authorization" : authorizationHeader })
        responseJson = response.json()
        outfile = open('data.txt', 'w') 
        json.dump(responseJson, outfile)
        
