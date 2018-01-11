-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;

\c tournament;

CREATE TABLE players (
    player_id serial PRIMARY KEY,
    full_name text,
    num_matches integer,
    num_wins integer
);

CREATE TABLE matches (
    match_id serial,
    round integer,
    winner_id integer REFERENCES players(player_id),
    lower_id integer REFERENCES players(player_id)
);