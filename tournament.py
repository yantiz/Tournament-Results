#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    cur = db.cursor()
    cur.execute("TRUNCATE matches;")
    db.commit()
    db.close()

def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    cur = db.cursor()
    cur.execute("TRUNCATE players CASCADE;")
    db.commit()
    db.close()

def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    cur = db.cursor()
    cur.execute("SELECT count(*) FROM players;")
    num_players = cur.fetchone()[0]
    db.close()
    return num_players


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    cur = db.cursor()
    cur.execute("INSERT INTO players (name) VALUES (%s)", (name,))
    db.commit()
    db.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    cur = db.cursor()
    cur.execute("""
            SELECT players.id, name, wins, wins + loses AS matches
            FROM players 
                JOIN num_wins ON players.id = num_wins.id
                JOIN num_loses ON num_wins.id = num_loses.id;
            """)
    standings = cur.fetchall()
    db.close()
    return standings 


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    cur = db.cursor()
    cur.execute("INSERT INTO matches VALUES (%s, %s)", (winner, loser))
    db.commit()
    db.close()
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    pairs = []
    db = connect()
    cur = db.cursor()
    cur.execute("""
            SELECT players.id, name, wins
            FROM players LEFT JOIN num_wins ON players.id = num_wins.id
            ORDER BY wins;
            """)
    records = cur.fetchall()
    for i in xrange(0, len(records), 2):
        pair = (records[i][0], records[i][1], records[i+1][0], records[i+1][1])
        pairs.append(pair)
    db.close()
    return pairs
