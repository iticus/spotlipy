# spotlipy
Python application to populate Spotify playlists with songs from radio stations

##Installation

sudo aptitude update
sudo aptitude install postgresql-9.3 postgresql-server-dev-9.3 
sudo pip3 install psycopg2
sudo pip3 install beautifulsoup4

sudo -iu postgres bash
psql
create database spotlipy;
alter role postgres with password 'NEW_PWD';


sudo apt-get install libspotify-dev

