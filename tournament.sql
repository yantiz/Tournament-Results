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

CREATE TABLE players (id SERIAL PRIMARY KEY, name TEXT);

CREATE TABLE matches (winner INTEGER REFERENCES players (id), loser INTEGER REFERENCES players (id));

CREATE VIEW num_wins AS SELECT id, count(winner) AS wins FROM players LEFT JOIN matches ON id = winner GROUP BY id;

CREATE VIEW num_loses AS SELECT id, count(loser) AS loses FROM players LEFT JOIN matches ON id = loser GROUP BY id;
