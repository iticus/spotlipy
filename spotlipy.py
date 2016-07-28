'''
Created on Jun 20, 2016

@author: ionut
'''

import logging
import spotify_api
import time

import database
import radiosearch
import settings

logger = logging.getLogger('spotlipy')
logger.info('starting spotlipy application')

month = settings.MONTH
date = settings.DATE
logger.info('performing radio search')
for station in settings.STATIONS:
    continue
    logger.info('searching songs on station %d, month: %d, date: %d' % (
        station, month, date))
    songs = radiosearch.find_songs(station, month, date)
    for song in songs:
        result = database.insert_song(song)
        if result:
            logger.info('inserted song %s by %s' % (song['title'], song['artist']))


logger.info('performing spotify song search')
unprocessed_songs = database.get_unprocessed_songs()
for song in unprocessed_songs:
    status = 2
    url = None
    
    logger.info('searching for %s by %s' % (song['title'], song['artist']))
    try:
        spotify_song = spotify_api.search_song(song)
    except Exception as e:
        logger.error('cannot search for spotify song: %s' % e)
        continue
        
    if spotify_song:
        status = 1
        url = spotify_song.link.url
        logger.info('found %s (%s by %s)' % (url, song['title'], song['artist']))

    result = database.update_song(song['id'], status, url)
    if result:
        logger.info('updated song %s by %s with %s' % (song['title'], song['artist'], url))

    time.sleep(3)


logger.info('performing tracks insert into spotify playlist')
found_songs = database.get_found_songs()

songs_by_playlist = {}
for song in found_songs:
    songs_by_playlist.setdefault(song['spotify_playlist'], []).append(song['spotify_url'])


for playlist_url, values in songs_by_playlist.items():
    
    while values:
        tracks = values[:100]
        values[:100] = []
        try:
            spotify_api.add_tracks(playlist_url, tracks)
        except Exception as e:
            logging.error('cannot add tracks to playlist: %s' % e)
            continue
    
    #TODO: update songs
    
        
    
    
    #TODO: implement remaining logic
    
logger.info('finished')