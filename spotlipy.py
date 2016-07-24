'''
Created on Jun 20, 2016

@author: ionut
'''

import logging
import spotify_sdk
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
    spotify_song = spotify_sdk.search_song(song)
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
for song in found_songs:
    status = 3
    spotify_sdk.add_tracks(playlist_url, tracks)
        
    
    
    #TODO: implement remaining logic
    
logger.info('finished')