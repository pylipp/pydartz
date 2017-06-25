"""
Module containing top game logic and routine.
"""

from .session import Session, Player
from .communication import get_input
from .database import sessions_log


class Game(object):

    def __init__(self):
        self._sessions = []

    def run(self):
        nr_players = get_input("Nr of players: ", type_=int, min_=1)

        names = []
        for i in range(nr_players):
            name = get_input("Name of player {}: ".format(i+1), min_=1)
            names.append(name)

        start_value = get_input("Start value: ", type_=int, min_=2)

        nr_legs = get_input("Nr of legs: ", type_=int, min_=1)

        players = []
        for i, name in enumerate(names):
            players.append(Player(name, i, start_value))

        session = Session(names, start_value, nr_legs, log_parent=sessions_log)
        session.run()
