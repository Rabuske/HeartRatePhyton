import webbrowser
from AppConfig      import AppConfig
import urllib.parse as urlparse
import requests
import base64
import json
import sqlite3

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

# Request authorization code
authorization_code = input("Authorization Code: ")

# Post request for the token
post_data = { "code" : authorization_code, "grant_type" : "authorization_code", "client_id" : AppConfig().get("client_id"), "redirect_uri" : AppConfig().get("uri_redirect")}
authorization = base64.encodestring(('%s:%s' % (AppConfig().get("client_id"), AppConfig().get("client_secret"))).encode()).decode().replace('\n', '')
authorization = "Basic %s" % authorization

response = requests.post(url=AppConfig().get("uri_token"), data=post_data, headers={ "Authorization" : authorization })
        