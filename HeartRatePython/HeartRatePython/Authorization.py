import webbrowser
from AppConfig      import AppConfig
from Token          import Token
import urllib.parse as urlparse
import requests
import base64
import json
import sqlite3

class Authorization(object):
    
    token = None

    def launchAuthorizationPage(self):
        # OAuth2 parameters
        parameters = { "client_id" : AppConfig().get("client_id"), "response_type" : "code", "scope" : "heartrate", "redirect_uri" : AppConfig().get("uri_redirect")}
        # Break URL in parts
        url_parts = list(urlparse.urlparse(AppConfig().get("uri_authorization")))

        # Parse the parameters list and update the URL parts 
        query = dict(urlparse.parse_qsl(url_parts[4]))
        query.update(parameters)
        url_parts[4] = urlparse.urlencode(query)

        # Generate the final URL 
        final_uri = urlparse.urlunparse(url_parts)

        # Open browser to get the code
        print("Openning the browser to connect to fitbit.com")
        webbrowser.open(final_uri,new=2)
        
    def getToken(self, database):
        if self.token == None:
            self.token = database.readToken()            
        if self.token == None:
            print("No valid authorization token found in the database. A new one will be requested.")
            self.token = self.requestNewToken(database)
        elif self.token.isExpired():
            print("Authorization token has been found in database. But it is expired.")
            self.token = self.refreshToken(self.token.refreshToken, database)
        return self.token         

    def requestNewToken(self, database):
        # 1) Lauch the browser to get the authorization code
        self.launchAuthorizationPage( )
        # 2) Ask the user to enter the authorization code
        authorization_code = input("Authorization Code: ")
        # 3) Post request for the token
        post_data = { "code" : authorization_code, "grant_type" : "authorization_code", "client_id" : AppConfig().get("client_id"), "redirect_uri" : AppConfig().get("uri_redirect")}
        authorization = self.getAuthorizationHeader()
        attempts = 0
        while True:
            attempts = attempts + 1
            if attempts > 5:
                print("Number of max attempts reached. Failed to obtain the authorization token.")
                break            
            print("Requesting a new authorization token. Attempt number: %d" % attempts)
            response = requests.post(url=AppConfig().get("uri_token"), data=post_data, headers={ "Authorization" : authorization })
            if response.status_code == 200:
                print("Authorization token obtained from fitbit.com")
                break

        # 4) Save the new token in the database
        return self.storeToken(response, database)

    def storeToken(self, response, database):
        print("Updating authorization token in the database.")
        token = Token.createFromDDIC(response.json())
        database.storeToken(token)
        return token

    def refreshToken(self, refreshToken, database):
        post_data = { "grant_type" : "refresh_token", "refresh_token" : refreshToken}
        authorization = self.getAuthorizationHeader()
        attempts = 0
        while True:
            attempts = attempts + 1
            if attempts > 5:
                logging.error("Number of max attempts reached. Failed to refresh the authorization token.")
                break            
            print("Refreshing the authorization token. Attempt number: %d" % attempts)
            response = requests.post(url=AppConfig().get("uri_token"), data=post_data, headers={ "Authorization" : authorization })
            if response.status_code == 200:
                print("Authorization token obtained from fitbit.com")
                break
        return self.storeToken(response, database)

    def getAuthorizationHeader(self, token = None):
        # When there is no token, use the client and the client secret as authorization
        if token == None:
            authorization = base64.encodestring(('%s:%s' % (AppConfig().get("client_id"), AppConfig().get("client_secret"))).encode()).decode().replace('\n', '')
            authorization = "Basic %s" % authorization
        else:
            authorization = "%s %s" % (token.type, token.accessToken)
        return authorization