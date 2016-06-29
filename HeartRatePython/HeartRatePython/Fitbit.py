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

    def getHeartIntradayRate(self, date, callback = None):
        data = self.getHeartRateIntradaytDb(date)
        if data == None:
            print("Data not found in database, reaching Fitbit.com")
            data = self.getHeartRateIntradayOnline(date)
        if callback != None:
            callback(data)
        else:
            return data

    def getHeartRateIntradaytDb(self, date):
        return self.database.getIntradayData(date)

    def getHeartRateIntradayOnline(self, date):
        uri = AppConfig().get("uri_heart")
        uri = uri.replace("[date]", date)
        uri = uri.replace("[end-date]", date)
        authorizationHeader = self.authorization.getAuthorizationHeader(self.authorization.getToken(self.database))
        response = requests.get(uri, headers={ "Authorization" : authorizationHeader })
        data = self.formatJson(response.json())
        if data == None:
            return None
        self.database.saveIntraday(data[0])
        self.database.saveZones(data[1])
        return data[0]

    def formatJson(self, json):
        date = None
        intradayData = list()
        zonesData = list()
        for activity in json["activities-heart"]:
            date = activity["dateTime"]
            for zone in activity["value"]["heartRateZones"]:
                if "caloriesOut" not in zone:
                    return None
                zonesData.append((date, zone["name"], zone["max"],zone["min"], zone["caloriesOut"], zone["minutes"]))
        for intraday in json["activities-heart-intraday"]["dataset"]:
            intradayData.append((date, intraday["time"], intraday["value"]))
        return (intradayData, zonesData)        