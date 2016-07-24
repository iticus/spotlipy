'''
Created on Jun 21, 2016

@author: ionut
'''

import datetime
import logging
import psycopg2
from psycopg2.extras import DictCursor

import settings

logger = logging.getLogger('database')
_dbconn = psycopg2.connect(settings.DSN)


def insert_song(song):
    cursor = _dbconn.cursor(cursor_factory=DictCursor)
    query = "INSERT into songs(channel, artist, title, played, found) VALUES(%s, %s, %s, %s, %s) RETURNING id"
    try:
        cursor.execute(query, (song['channel'], song['artist'], song['title'], song['played'], datetime.datetime.now()))
        _dbconn.commit()
    except psycopg2.IntegrityError:
        logger.warning('could not insert song %s as it is already present' % song['title'])
        _dbconn.rollback()
        return False
        
    except Exception as e:
        logger.error('could not insert song %s: %s' % (song['title'], e))
        _dbconn.rollback()
        return False
        
    rows = cursor.fetchall()
    cursor.close()
    return len(rows) > 0


def get_unprocessed_songs():
    cursor = _dbconn.cursor(cursor_factory=DictCursor)
    query = "SELECT id, channel, artist, title, spotify_id FROM songs WHERE status=0"
    try:
        cursor.execute(query)
    except Exception as e:
        logger.error('could not retrieve unprocessed songs: %s' % e)
        return []
    
    rows = cursor.fetchall()
    cursor.close()
    return rows


def get_found_songs():
    cursor = _dbconn.cursor(cursor_factory=DictCursor)
    query = """SELECT id, channel, artist, title, spotify_id 
    FROM songs INNER JOIN playlists on songs.channel = playlists.channel
    WHERE songs.status=1"""
    try:
        cursor.execute(query)
    except Exception as e:
        logger.error('could not retrieve found songs: %s' % e)
        return []
    
    rows = cursor.fetchall()
    cursor.close()
    return rows


def update_song(song_id, status, spotify_id=None):
    cursor = _dbconn.cursor(cursor_factory=DictCursor)
    query = "UPDATE songs SET status=%s, spotify_id=%s WHERE id=%s RETURNING id"
    try:
        cursor.execute(query, (status, spotify_id, song_id))
        _dbconn.commit()
    except Exception as e:
        logger.error('could not update song %s: %s' % (song_id, e))
        _dbconn.rollback()
        return False
        
    rows = cursor.fetchall()
    cursor.close()
    return len(rows) > 0    
