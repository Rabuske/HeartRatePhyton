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
        webbrowser.open(final_uri,new=2)
        
    def getToken(self, database):
        if self.token == None:
            self.token = database.readToken()            
        if self.token == None:
            self.token = self.requestNewToken(database)
        elif self.token.isExpired():
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
        response = requests.post(url=AppConfig().get("uri_token"), data=post_data, headers={ "Authorization" : authorization })
        # 4) Save the new token in the database
        return self.storeToken(response, database)

    def storeToken(self, response, database):
        token = Token.createFromDDIC(response.json())
        database.storeToken(token)
        return token

    def refreshToken(self, refreshToken, database):
        post_data = { "grant_type" : "refresh_token", "refresh_token" : refreshToken}
        authorization = self.getAuthorizationHeader()
        response = requests.post(url=AppConfig().get("uri_token"), data=post_data, headers={ "Authorization" : authorization })
        return self.storeToken(response, database)

    def getAuthorizationHeader(self, token = None):
        # When there is no token, use the client and the client secret as authorization
        if token == None:
            authorization = base64.encodestring(('%s:%s' % (AppConfig().get("client_id"), AppConfig().get("client_secret"))).encode()).decode().replace('\n', '')
            authorization = "Basic %s" % authorization
        else:
            authorization = "%s %s" % (token.type, token.accessToken)
        return authorization