'''
Created on Jun 28, 2016

@author: ionut
'''

import logging
import spotipy.util

from settings import SPOTIFY

logger = logging.getLogger('sdk')
token = spotipy.util.prompt_for_user_token(SPOTIFY['username'], SPOTIFY['api_scopes'], client_id=SPOTIFY['client_id'],
    client_secret=SPOTIFY['client_secret'], redirect_uri=SPOTIFY['redirect_url'])

_sp = None
if token:
    _sp = spotipy.Spotify(auth=token)
else:
    raise Exception('cannot login into spotify using the web API')


def search_song(song):
    song['artist'] = song['artist'].replace('/', ' ') #search improvement ("/" is usually not found)    
    results = _sp.search(q='artist:"%s" title:"%s"' % (song['artist'], song['title']), type='track') 
    
    if not results['tracks']['items']:
        return None
    
    track = results['tracks']['items'][0]
    return track
 

def add_tracks(playlist_url, tracks):
    _sp.user_playlist_add_tracks(SPOTIFY['username'], playlist_url, tracks)


def clear_playlist(playlist_url, tracks):
    _sp.user_playlist_remove_all_occurrences_of_tracks(
        SPOTIFY['username'], playlist_url, tracks)