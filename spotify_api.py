'''
Created on Jun 28, 2016

@author: ionut
'''

import logging
import spotipy.util
import time

from settings import SPOTIFY

logger = logging.getLogger('api')
_sp = None


def _login():
    global _sp
    token = spotipy.util.prompt_for_user_token(SPOTIFY['username'], SPOTIFY['api_scopes'], client_id=SPOTIFY['client_id'],
        client_secret=SPOTIFY['client_secret'], redirect_uri=SPOTIFY['redirect_url'])
    
    if token:
        _sp = spotipy.Spotify(auth=token)
    else:
        raise Exception('cannot login into spotify using the web API')


def search_song(song):
    song['artist'] = song['artist'].replace('/', ' ') #search improvement ("/" is usually not found)
    
    try:
        results = _sp.search(q='artist:"%s" title:"%s"' % (song['artist'], song['title']), type='track')
    except Exception as e:
        logging.warning('cannot search for song; trying to relogin: %s' % e)
        time.sleep(3)
        _login()
        time.sleep(3)
        results = _sp.search(q='artist:"%s" title:"%s"' % (song['artist'], song['title']), type='track')
    
    if not results['tracks']['items']:
        return None
    
    track = results['tracks']['items'][0]
    return track
 

def get_tracks(playlist_url):
    
    tracks = []
    try:
        results = _sp.user_playlist(SPOTIFY['username'], playlist_url, fields="tracks,next")
    except Exception as e:
        logging.warning('cannot search retrieve playlist tracks; trying to relogin: %s' % e)
        time.sleep(3)
        _login()
        time.sleep(3)
        results = _sp.user_playlist(SPOTIFY['username'], playlist_url, fields="tracks,next")
    
    tracks.extend(results['tracks']['items'])
    if results['tracks']['next']:
        results = results['tracks']
        i = 0
        while True:
            time.sleep(3)
            if i > 10:
                logger.warning('too many retries reached')
                break
            try:
                results = _sp.next(results)
                if not results:
                    break
                tracks.extend(results['items'])
            except Exception as e:
                logging.warning('cannot search retrieve playlist tracks; trying to relogin: %s' % e)
                _login()
                i += 1
                continue
         
    response = {}
    for track in tracks:
        response[track['track']['uri']] = track['track']

    return response


def add_tracks(playlist_url, tracks):
    try:
        _sp.user_playlist_add_tracks(SPOTIFY['username'], playlist_url, tracks)
    except Exception as e:
        logging.warning('cannot add tracks to playlist; trying to relogin: %s' % e)
        time.sleep(3)
        _login()
        time.sleep(3)
        _sp.user_playlist_add_tracks(SPOTIFY['username'], playlist_url, tracks)


def clear_playlist(playlist_url, tracks):
    _sp.user_playlist_remove_all_occurrences_of_tracks(
        SPOTIFY['username'], playlist_url, tracks)
    

_login()

