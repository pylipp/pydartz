"""
Module containing top game logic and routine.
"""

from .session import Session
from .player import Player
from .database import sessions_log


class Game(object):

    def __init__(self):
        self._sessions = []

    def run(self, communicator):
        nr_players = communicator.get_input("Nr of players: ", type_=int, min_=1)

        names = []
        for i in range(nr_players):
            name = communicator.get_input("Name of player {}: ".format(i+1),
                    min_=1)
            names.append(name)

        start_value = communicator.get_input("Start value: ", type_=int, min_=2)

        nr_legs = communicator.get_input("Nr of legs: ", type_=int, min_=1)

        players = []
        for name in names:
            players.append(Player(name, start_value, communicator=communicator))

        session = Session(players, nr_legs, log_parent=sessions_log,
                communicator=communicator)
        session.run()
