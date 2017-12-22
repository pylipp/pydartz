"""
Module containing top game logic and routine.
"""

from .session import Session
from .player import Player
from .communication import (INPUT_NR_PLAYERS, INPUT_NR_LEGS, INPUT_PLAYER_NAME,
                            INPUT_START_VALUE, INPUT_ANOTHER_SESSION
                            )


class Game(object):

    def __init__(self, communicator, sessions_log=None):
        self._communicator = communicator
        self._sessions_log = sessions_log
        self._current_session = None

    def run(self):
        """Repeatly creates and runs sessions. Stops if the player decides to
        quit.
        """

        while True:
            if self._current_session is None:
                self._init_session()
            else:
                if not self._query_another_session():  # quit
                    return

            self._current_session.run()

    def _init_session(self):
        """Initializes a new session by querying required input (number of
        players, start value, player names, number of legs to win).
        """

        nr_players = self._communicator.get_input(INPUT_NR_PLAYERS)

        start_value = self._communicator.get_input(INPUT_START_VALUE)

        players = []
        for i in range(nr_players):
            name = self._communicator.get_input(INPUT_PLAYER_NAME, i + 1)
            players.append(
                    Player(name, start_value, communicator=self._communicator))

        nr_legs = self._communicator.get_input(INPUT_NR_LEGS)

        self._current_session = Session(players, nr_legs,
                                        log_parent=self._sessions_log,
                                        communicator=self._communicator)

    def _query_another_session(self):
        """Query the user about how to proceed. Three replies are possible:
        - n (no): play again but ask for new session parameters
        - y (yes): play again, using the previous session's parameters
        - q (quit): quit the game

        :return: False if user requested to quit
        """

        continuing = True
        reply = self._communicator.get_input(INPUT_ANOTHER_SESSION)

        if reply == 'n':
            # query parameters for new session
            self._init_session()
        elif reply == 'y':
            # copy previous session's parameters
            self._current_session = Session(self._current_session._players,
                                            self._current_session._nr_legs,
                                            log_parent=self._sessions_log,
                                            communicator=self._communicator)
        else:
            continuing = False

        return continuing
