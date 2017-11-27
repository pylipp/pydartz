"""
Module containing top game logic and routine.
"""

from .session import Session
from .player import Player


class Game(object):

    def __init__(self, communicator, sessions_log=None):
        self._sessions = []
        self._communicator = communicator
        self._sessions_log = sessions_log

    def run(self):
        """Repeatly creates and runs sessions. Stops if the player decides to
        quit.
        """

        session = None
        while True:
            if session is None:
                session = self._init_session()
            else:
                # non-first run
                reply = self._communicator.get_input(
                    "Again (y/n/q)? ", choices="ynq").lower()

                if reply == 'n':
                    # query parameters for new session
                    session = self._init_session()
                elif reply == 'y':
                    # copy previous session's parameters
                    session = Session(session._players, session._nr_legs,
                                      log_parent=self._sessions_log,
                                      communicator=self._communicator)
                else:  # quit
                    return

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

        return Session(players, nr_legs, log_parent=self._sessions_log,
                communicator=self._communicator)
