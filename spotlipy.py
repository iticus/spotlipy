'''
Created on Jun 20, 2016

@author: ionut
'''

import logging

import radiosearch
import settings

logging.info('starting spotlipy application')

month = settings.MONTH
date = settings.DATE
for station in settings.STATIONS:
    logging.info('searching songs on station %d, month: %d, date: %d' % (
        station, month, date))
    songs = radiosearch.find_songs(station, month, date)
    #TODO: save songs in DB
    
    
logging.info('finished')