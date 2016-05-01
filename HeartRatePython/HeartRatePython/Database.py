import sqlite3 as externalDb
from AppConfig import AppConfig
import datetime
from Token import Token

class Database(object):    

#   == Database definition
    version = "0.1" 

#   == Database connection variables
    connection = None

#   When creating the object, already connect to the database and initialize/update it
    def __init__(self):
        self.connection = externalDb.connect(AppConfig().get("database_name"))       
        cursor = self.connection.cursor()
        
        # Check if the database has been initialized, by looking for the 'version' table
        cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'version'")
        result = cursor.fetchone()
        if result == None:
            self.initDb()
        # Check if database is updated
        else:
            cursor.execute("SELECT version FROM version ORDER BY date DESC Limit 1")
            result = cursor.fetchone()
            self.updateDb(result)        
        cursor.close()   

    # Initialization routines that must always contain the most recent database version
    def initDb(self):    
        cursor = self.connection.cursor()
        cursor.execute("CREATE TABLE version (version, date)")
        cursor.execute("CREATE TABLE heart_zone (date, min, max, calories, minutes, name)")
        cursor.execute("CREATE TABLE heart_intraday (date, time, value)")
        cursor.execute("CREATE TABLE token (user_id, access_token, refresh_token, token_type, expires_in, request_time)")
        cursor.execute("INSERT  INTO version values (?,?)", (self.version, datetime.datetime.now()))
        cursor.close()
        self.connection.commit()

    # Update routines that migrates the database from version to newVersion
    def updateDb(self, newVersion):    
        if newVersion == self.version:
            return
        cursor = self.connection.cursor()
        cursor.close()
        self.connection.commit()

#---Token Operations
    def storeToken(self, token):
        cursor = self.connection.cursor()
        # Delete the existing token for this user 
        cursor.execute("DELETE FROM token WHERE user_id=?", (token.userId,))
        # Insert the new token
        tokenData = token.getData()
        cursor.execute("INSERT INTO token VALUES (?, ?, ?, ?, ?, ?)",  tokenData)
        cursor.close()
        self.connection.commit()
            
    # For now, we only support one user
    def readToken(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM token")
        result = cursor.fetchone()
        cursor.close()
        if result == None:
            return None
        return Token.createFromDDIC(result)

#---Heart Rate
    def saveHeartData(self, heartDataJson):
        cursor = self.connection.cursor()
        date = None
        for activity in heartDataJson["activities-heart"]:
            date = activity["dateTime"]
            for zone in activity["value"]["heartRateZones"]:
                cursor.execute("INSERT INTO heart_zone VALUES (?,?,?,?,?,?)", (date, zone["max"],zone["min"], zone["caloriesOut"], zone["minutes"], zone["name"]))
        for intraday in heartDataJson["activities-heart-intraday"]["dataset"]:
            cursor.execute("INSERT INTO heart_intraday VALUES (?,?,?)", (date, intraday["time"], intraday["value"]))
        self.connection.commit()
        cursor.close()

    def getLastHeartInfo(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM heart_intraday ORDER BY date DESC, time DESC Limit 1")
        result = cursor.fetchone()
        cursor.close()
        return result

    def getIntradayData(self, date):
        cursor = self.connection.cursor()
        cursor.execute("SELECT time, value FROM heart_intraday WHERE date=? ORDER BY time", (date,))
        result = cursor.fetchall()
        cursor.close()
        return result