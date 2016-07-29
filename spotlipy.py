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
    uri = None
    
    logger.info('searching for %s by %s' % (song['title'], song['artist']))
    try:
        spotify_song = spotify_api.search_song(song)
    except Exception as e:
        logger.error('cannot search for spotify song: %s' % e)
        continue
        
    if spotify_song:
        status = 1
        uri = spotify_song['uri']
        logger.info('found %s (%s by %s)' % (uri, song['title'], song['artist']))

    result = database.update_song(song['id'], status, uri)
    if result:
        logger.info('updated song %s by %s with %s' % (song['title'], song['artist'], uri))

    time.sleep(3)


logger.info('performing tracks insert into spotify playlist')
found_songs = database.get_found_songs()
songs_by_playlist = {}
for song in found_songs:
    if not song['spotify_playlist'] in songs_by_playlist:
        songs_by_playlist[song['spotify_playlist']] = {'track_ids': [], 'song_ids': []}
    songs_by_playlist[song['spotify_playlist']]['track_ids'].append(song['spotify_uri'])
    songs_by_playlist[song['spotify_playlist']]['song_ids'].append(song['id'])


for playlist_url, values in songs_by_playlist.items():
    while values['track_ids']:
        tracks_ids = values['track_ids'][:100]
        song_ids = values['song_ids'][:100]
        del values['track_ids'][:100]
        del values['song_ids'][:100]
        logging.info('inserting %d tracks into %s' % (len(tracks_ids, playlist_url)))
        try:
            spotify_api.add_tracks(playlist_url, tracks_ids)
        except Exception as e:
            logging.error('cannot add tracks to playlist: %s' % e)
            continue
        
        logging.info('marking db entries as processed (3)')
        for i, song_id in enumerate(song_ids):
            database.update_song(song_id, 3, tracks_ids[i])
    
logger.info('finished')