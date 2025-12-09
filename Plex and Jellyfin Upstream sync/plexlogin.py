import os, json

try:
    from plexapi.server import PlexServer
except:
    os.system('pip install plexapi')
    from plexapi.server import PlexServer

try:
    from requests import get
except:
    os.system('pip install requests')
    from requests import get

import requests

# Get the value of the device tracker from Home Assistant.
# These are the API URL and the Token for authentification.
urlHA = 'http://homeassistant.local:8123/api/states/sensor.speedtest_cli_upload'
headersHA = {
    'Authorization': 'Bearer ---',
    'content-type': 'application/json'
}

# Get the real tracker state value out of the JSON data inside a string.
VarHA = get(urlHA, headers=headersHA)
DataHA = json.loads(VarHA.text)
StateHA = DataHA["state"]

urlJellyfin = 'https://a.b.de/System/Configuration'
headersJellyfin = {
    'Authorization': 'MediaBrowser Token="---"',
    'content-type': 'application/json'
}

VarJellyfin = get(urlJellyfin, headers=headersJellyfin)
DataJellyfin = '{"RemoteClientBitrateLimit": '+ str(((int(float(StateHA)))-10)*1000000) + '}'

r1 = requests.post(urlJellyfin, data=DataJellyfin, headers=headersJellyfin)

urlPlex = 'https://a.b.de'
tokenPlex = '---'

plex = PlexServer(urlPlex, tokenPlex)

plex.settings.get("wanTotalMaxUploadRate").set((int(float(StateHA))-10)*1000)
plex.settings.save()
