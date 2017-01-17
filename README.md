# Tournament Results

This project implements a Python module that uses the PostgreSQL database to keep track of players and matches in a game tournament.
Database schemas are defined to store the game matches between players. The Python module is used to rank the players and pair them up in matches in a tournament.

## Local Setup

To run the application locally, you need to enter the psql interactive terminal first and type `\i tournament.sql` in order to import the SQL commands
from the script. Then, go ahead and run `python tournament_test.py` to execute the unit tests. Finally, the outcome should be presented to you.
