'''
Created on Jun 20, 2016

@author: ionut
'''

import logging

import database
import radiosearch
import settings
import spotify

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
    status = 0
    spotify_song = spotify.search_song(song)
    if spotify_song:
        status = 1
    else:
        status = 2
    
    result = database.update_song(song['id'], status, spotify_song)
    if result:
        logger.info('updated song %s by %s with %s' % (song['title'], song['artist'], spotify_song))
    
    #TODO: implement remaining logic
    
logger.info('finished')