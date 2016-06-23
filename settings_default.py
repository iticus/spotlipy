'''
Created on Jun 20, 2016

@author: ionut
'''

import logging
logging.basicConfig(level=logging.DEBUG, 
    format='[%(asctime)s] - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

#Database connection - Postgres / Amazon RDS
DSN = "dbname='spotlipy' user='postgres' host='127.0.0.1' password='password'"

#dogstarradio search URL
SEARCH_URL = 'http://www.dogstarradio.com/search_xm_playlist.php'

#for stations numbers and names see stations.txt
STATIONS = [
    4, 5, 6
]

MONTH = 6
DATE = 15