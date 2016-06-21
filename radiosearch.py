'''
Created on Jun 21, 2016

@author: ionut
'''

import bs4
import requests
import time

import settings


data = {
    'artist': '',
    'title': '',
    #'channel': channel,
    #'month': month,
    #'date': date,
    'shour': '',
    'sampm': '',
    'stz': '',
    'ehour': '',
    'eampm': '', 
    #'page': ''
}


def get_songs_from_html(html):
    songs = []
    s = bs4.BeautifulSoup(html, 'html.parser')
    result_table = None
    for table in s.find_all('table'):
        if 'Search results' in table.text:
            result_table = table
            break
    
    if not result_table:
        return []
    
    for row in result_table.find_all('tr'):
        cells = row.find_all('td')
        if not len(cells) > 4:
            continue #empty row
        
        if cells[0].text == 'Channel' and cells[1].text == 'Artist' and cells[2].text == 'Title':
            continue #header row
         
        song = {
            'channel': cells[0].text, 
            'artist': cells[1].text,
            'title': cells[2].text,
            'date': cells[3].text,
            'time': cells[4].text,
        }
        songs.append(song)
    
    return songs


def find_songs(channel, month, date):
    songs = []
    data['channel'] = channel
    data['month'] = month
    data['date'] = date
    
    page = 1
    while True:
        r = requests.get(settings.SEARCH_URL, params=data)
        result = get_songs_from_html(r.content)
        if not result:
            break
        
        songs.extend(result)
        data['page'] = page
        page += 1
        time.sleep(1)

    return songs
    