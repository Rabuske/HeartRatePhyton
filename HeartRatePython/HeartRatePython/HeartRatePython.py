import webbrowser
import urllib.parse as urlparse
from urllib.parse import urlencode

# Overly complicated code to corretly generate the Fitbit URL 

# OAuth 2 authorization URL and parameters
url = 'https://www.fitbit.com/oauth2/authorize'
parameters = { 'client_id' : '227L8L', 'response_type' : 'code', 'scope' : 'heartrate', 'redirect_uri' : 'localhost:8080'}

# Break URL in parts
url_parts = list(urlparse.urlparse(url))

# Parse the parameters list and update the URL parts 
query = dict(urlparse.parse_qsl(url_parts[4]))
query.update(parameters)
url_parts[4] = urlencode(query)

# Generate the final URL 
final_url = urlparse.urlunparse(url_parts)

# Open browser to get the code
webbrowser.open(final_url,new=2)
