'''
Created on Jun 20, 2016

@author: ionut
'''

import radiosearch

songs = radiosearch.find_songs(8, 6, 12)
for song in songs:
    print(song)