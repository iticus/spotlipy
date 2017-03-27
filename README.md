# spotlipy
Python application to populate Spotify playlists with songs from radio stations

## Installation

### Dependencies

 - sudo aptitude update
 - sudo aptitude install postgresql-9.3 postgresql-server-dev-9.3 
 - sudo pip3 install psycopg2
 - sudo pip3 install spotipy 

Copy project files on your computer or use `git clone https://github.com/iticus/spotlipy.git`

### Database

 - login as postgres user: `sudo -iu postgres bash`
 - use the builtin client: `psql` and enter the following:
   `create database spotlipy;`
   `alter role postgres with password 'NEW_PWD';`
   paste contents of `database.sql`
 - exit

### Settings

 - `cp settings_default.py settings.py`
 - `nano settings` and edit relevant entries
  - database password
  - stations list (see `stations.txt` for valid values)
  - broadcast month and date
  - spotify credentials (register your app and get them from the Spotify developer page)


## Run
Run `python3 spotlipy.py` or make a cron entry for example. On first run you need to authorize the request (just open the given URL in your browser, login and paste back the URL received).


## Notes

The callback URL should be changed to something you own preferably.
