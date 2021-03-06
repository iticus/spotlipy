'''
Created on Jun 20, 2016

@author: ionut
'''

import argparse
import logging
import spotify_api
import time

import database
import radiosearch
import settings

logger = logging.getLogger('spotlipy')
logger.info('starting spotlipy application')


def radio_search():
    month = settings.MONTH
    date = settings.DATE
    logger.info('performing radio search')
    for station in settings.STATIONS:
        logger.info('searching songs on station %s, month: %s, date: %s' % (
            station, month, date))
        songs = radiosearch.find_songs(station, month, date)
        for song in songs:
            result = database.insert_song(song)
            if result:
                logger.info('inserted song %s by %s' % (song['title'], song['artist']))


def spotify_search():
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
            time.sleep(3)
            continue
            
        if spotify_song:
            status = 1
            uri = spotify_song['uri']
            logger.info('found %s (%s by %s)' % (uri, song['title'], song['artist']))
    
        result = database.update_song(song['id'], status, uri)
        if result:
            logger.info('updated song %s by %s with %s' % (song['title'], song['artist'], uri))
    
        time.sleep(3)


def spotify_insert():
    logger.info('performing tracks insert into spotify playlist')
    found_songs = database.get_found_songs()
    songs_by_playlist = {}
    existing_tracks = {}
    for song in found_songs:
        playlist = song['spotify_playlist'] 
        if not playlist in songs_by_playlist:
            songs_by_playlist[playlist] = {'track_ids': [], 'song_ids': []}
            existing_tracks[playlist] = spotify_api.get_tracks(playlist)
            time.sleep(3)
        
        if song['spotify_uri'] in existing_tracks[playlist]:
            logger.warning('skipping already existing track: %s' % song['spotify_uri'])
            database.update_song(song['id'], 3, song['spotify_uri'])
            continue
        
        songs_by_playlist[song['spotify_playlist']]['track_ids'].append(song['spotify_uri'])
        songs_by_playlist[song['spotify_playlist']]['song_ids'].append(song['id'])
    
    
    for playlist_url, values in songs_by_playlist.items():
        while values['track_ids']:
            tracks_ids = values['track_ids'][:100]
            song_ids = values['song_ids'][:100]
            del values['track_ids'][:100]
            del values['song_ids'][:100]
            logging.info('inserting %d tracks into %s' % (len(tracks_ids), playlist_url))
            try:
                time.sleep(3)
                spotify_api.add_tracks(playlist_url, tracks_ids)
            except Exception as e:
                logging.error('cannot add tracks to playlist: %s' % e)
                continue
            
            logging.info('marking db entries as processed (3)')
            for i, song_id in enumerate(song_ids):
                database.update_song(song_id, 3, tracks_ids[i])

parser = argparse.ArgumentParser(description='spotlipy: search radio tracks and insert them into spotify')
parser.add_argument('-a','--action', choices=['radio_search', 'spotify_search', 'spotify_insert', 'all'], required=False, 
    help='action to be performed')
args = vars(parser.parse_args())

if args['action'] == 'radio_search':
    radio_search()
elif args['action'] == 'spotify_search':
    spotify_search()
elif args['action'] == 'spotify_insert':
    spotify_insert()
elif args['action'] in [None, 'all']:
    radio_search()
    spotify_search()
    spotify_insert()
 
logger.info('finished')