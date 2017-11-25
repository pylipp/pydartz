"""
Module containing top game logic and routine.
"""

from .session import Session
from .player import Player
from .database import sessions_log


class Game(object):

    def __init__(self, communicator):
        self._sessions = []
        self._communicator = communicator

    def run(self):
        """Creates a session and runs it."""

        session = self._init_session()
        session.run()
        self._sessions.append(session)

    def _init_session(self):
        """Initializes a new session by querying required input (number of
        players, start value, player names, number of legs to win).
        """

        nr_players = self._communicator.get_input("Nr of players: ", type_=int,
                min_=1)

        start_value = self._communicator.get_input("Start value: ", type_=int,
                min_=2)

        players = []
        for i in range(nr_players):
            name = self._communicator.get_input(
                    "Name of player {}: ".format(i+1), min_=1)
            players.append(
                    Player(name, start_value, communicator=self._communicator))

        nr_legs = self._communicator.get_input("Nr of legs: ", type_=int, min_=1)

        return Session(players, nr_legs, log_parent=sessions_log,
                communicator=self._communicator)
