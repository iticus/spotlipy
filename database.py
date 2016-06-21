'''
Created on Jun 21, 2016

@author: ionut
'''

import psycopg2

import settings

_dbconn = psycopg2.connect(settings.DSN)


def insert_song(channel, artist, title, moment):
    cursor = _dbconn.cursor()
    query = "INSERT into songs(channel, artist, title, moment) VALUES(%s, %s, %s, %s)"
    cursor.execute(query, (channel, artist, title, moment))
    rows = cursor.fetchall()
    return len(rows) > 0


def get_songs():
    pass