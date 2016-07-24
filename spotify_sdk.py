'''
Created on Jun 28, 2016

@author: ionut
'''

import logging
import spotify
import time

import settings

MAX_LOGIN_TRIES = 100 

logger = logging.getLogger('sdk')
_session = spotify.Session()
_session.login(settings.SPOTIFY_USR, settings.SPOTIFY_PWD)

i = 0
while True:
    i += 1
    if i >= MAX_LOGIN_TRIES:
        logger.error('cannot login to spotify service')
        break
    
    _session.process_events()
    time.sleep(0.1)
    if _session.connection.state == spotify.ConnectionState.LOGGED_IN:
        logger.info('logged into spotify service after %d tries' % i)
        break


def search_song(song):
    search = _session.search(query='artist:"%s" title:"%s"' % (song['artist'], song['title'])) 
    result = search.load()
    
    if not result.tracks:
        return None
    
    track = result.tracks[0]
    track.load()
    return track
 

def add_tracks(playlist_url, tracks):
    playlist = _session.get_playlist(playlist_url)
    playlist.load()
    _session.add_tracks(tracks)
