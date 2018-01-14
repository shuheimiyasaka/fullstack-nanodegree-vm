#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    # Open a cursor to perform database operations
    cur = conn.cursor()
    # Execute a command: this creates a new table
    cur.execute("DELETE FROM matches;")

    cur.execute("UPDATE players "+
                "SET num_wins = 0, num_matches = 0;")
    # Make the changes to the database persistent
    conn.commit()
    # Close communication with the database
    cur.close()
    conn.close()

def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    # Open a cursor to perform database operations
    cur = conn.cursor()
    # Execute a command: this creates a new table
    cur.execute("DELETE FROM players;")
    # Make the changes to the database persistent
    conn.commit()
    # Close communication with the database
    cur.close()
    conn.close()

def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    # Open a cursor to perform database operations
    cur = conn.cursor()
    # Execute a command: this creates a new table
    cur.execute("SELECT count(*) as count FROM players;")
    res = cur.fetchone()[0]
    
    # Make the changes to the database persistent
    conn.commit()
    # Close communication with the database
    cur.close()
    conn.close()

    return res


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    """Returns the number of players currently registered."""
    conn = connect()
    # Open a cursor to perform database operations
    cur = conn.cursor()
    # Execute a command: this creates a new table
    cur.execute("INSERT INTO players (full_name) "+
                "VALUES (%s);", (bleach.clean(name),))
    # Make the changes to the database persistent
    conn.commit()
    # Close communication with the database
    cur.close()
    conn.close()

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
    conn = connect()
    # Open a cursor to perform database operations
    cur = conn.cursor()
    # Execute a command: this creates a new table
    cur.execute("SELECT player_id, full_name, num_wins, num_matches "+
        "FROM players "+
        "order by num_wins desc, full_name;")
    res = cur.fetchall()
    
    # Make the changes to the database persistent
    conn.commit()
    # Close communication with the database
    cur.close()
    conn.close()

    return res


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    # Open a cursor to perform database operations
    cur = conn.cursor()
    # Execute a command: this creates a new table
    cur.execute("INSERT INTO matches (winner_id, loser_id) "+
                "VALUES (%s, %s);", 
                (bleach.clean(str(winner)), bleach.clean(str(loser))))
    
    cur.execute("UPDATE players "+
                "SET num_matches = num_matches + 1 " + 
                "WHERE player_id = %s or " +
                "      player_id = %s;", 
                (bleach.clean(str(winner)), bleach.clean(str(loser))))

    cur.execute("UPDATE players "+
                "SET num_wins = num_wins + 1 " +
                "WHERE player_id = %s;", (bleach.clean(str(winner)),))

    # Make the changes to the database persistent
    conn.commit()
    # Close communication with the database
    cur.close()
    conn.close()


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
    pair_list = playerStandings()
    pair_one = [player[:2] for player in pair_list[::2]]
    pair_two = [player[:2] for player in pair_list[1::2]]
    swiss_pairings = zip(pair_one, pair_two)
    swiss_pairings = [(pairs[0][0], pairs[0][1], pairs[1][0], pairs[1][1]) 
        for pairs in swiss_pairings]
    return swiss_pairings


