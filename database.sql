--songs
CREATE TABLE songs(
	id bigserial PRIMARY KEY,
    channel text,
    artist text,
    title text,
    played timestamp without time zone,
    found timestamp without time zone
);

CREATE INDEX ON songs(channel);
CREATE INDEX ON songs(artist);
CREATE INDEX ON songs(played);