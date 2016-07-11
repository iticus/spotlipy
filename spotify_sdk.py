'''
Created on Jun 28, 2016

@author: ionut
'''

import spotify
import time

import settings

MAX_LOGIN_TRIES = 100 

_session = spotify.Session()
_session.login(settings.SPOTIFY_USR, settings.SPOTIFY_PWD)


i = 0
while True:
    i += 1
    if i >= MAX_LOGIN_TRIES:
        break
    
    _session.process_events()
    time.sleep(0.1)
    if _session.connection.state == spotify.ConnectionState.LOGGED_IN:
        break


def search_song(song):
    search = _session.search(query='artist:"%s" title:"%s"' % (song['artist'], song['title'])) 
    result = search.load()
    
    if not result.tracks:
        return None
    
    track = result.tracks[0]
    track.load()
    return track
 

def add_tracks(spotify_playlist, tracks):
    
    pass
    #TODO: implement function
    #_session.playlist_container.insert(0, playlist)
