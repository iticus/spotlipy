'''
Created on Jun 20, 2016

@author: ionut
'''

import logging
logging.basicConfig(level=logging.DEBUG, 
    format='[%(asctime)s] - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("spotify.search").setLevel(logging.WARNING)
logging.getLogger("spotify.session").setLevel(logging.WARNING)

#Database connection - Postgres / Amazon RDS
DSN = "dbname='spotlipy' user='postgres' host='127.0.0.1' password='password'"

#dogstarradio search URL
SEARCH_URL = 'http://www.dogstarradio.com/search_playlist.php'

#for stations numbers and names see stations.txt
STATIONS = [
    34, 44
]

MONTH = 7
DATE = 22

#Spotify settings
SPOTIFY = {
    'username': 'username',
    'client_id': 'client_id',
    'client_secret': 'client_secret',
    'redirect_url': 'redirect_url',
    'api_scopes': 'playlist-read-private playlist-modify-public playlist-modify-private' 
}
