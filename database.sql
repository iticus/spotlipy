--Postgres database structure for spotlipy

--songs
CREATE TABLE songs(
	id bigserial PRIMARY KEY,
    channel text NOT NULL,
    artist text NOT NULL,
    title text NOT NULL,
    played timestamp without time zone NOT NULL,
    found timestamp without time zone NOT NULL,
    status smallint NOT NULL DEFAULT 0,
    spotify_id text DEFAULT NULL,
    UNIQUE (channel, artist, title)
);
CREATE INDEX ON songs(channel);
CREATE INDEX ON songs(artist);
CREATE INDEX ON songs(played);
CREATE INDEX ON songs(status);
--status: 0 unprocessed, 1 - found on Spotify, 2 - not found on Spotify


--playlists
CREATE TABLE playlists(
	id bigserial PRIMARY KEY,
    channel text NOT NULL,
    spotify_playlist text NOT NULL,
    added timestamp without time zone NOT NULL
);
CREATE INDEX ON playlists(channel);
CREATE INDEX ON playlists(spotify_playlist);