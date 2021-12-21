from .database import LogEntryBase
from .communication import INFO_LEG


class Session(LogEntryBase):
    """Representation of a darts session.
    Initialized with a list of players and the number of legs to win.
    """

    def __init__(self, players, nr_legs=1, log_parent=None, communicator=None):
        super().__init__(log_parent,
                players=','.join([p.name for p in players]))

        self._players = players
        self._nr_legs = nr_legs
        self._communicator = communicator

    def _player_won_enough_legs(self):
        largest_nr_of_victories = max((p.nr_won_legs for p in self._players))
        return self._nr_legs <= largest_nr_of_victories

    def run(self):
        """Play until a player has won the predefined number of legs."""
        Leg.start_player_index = 0

        for p in self._players:
            p._nr_won_legs = 0

        while not self._player_won_enough_legs():
            leg = Leg(self._players, log_parent=self)
            leg.run()

            self.save()

            self._communicator.print_info(INFO_LEG, players=self._players)


class Leg(LogEntryBase):
    """Representation of a darts leg. Players start alternatingly which is
    established by the static variable `start_player_index` that is incremented
    every time a Leg instance is created.
    """

    start_player_index = 0

    def __init__(self, players, log_parent=None):
        super().__init__(log_parent)

        self._players = players
        self._nr_players = len(self._players)

        self._current_player_index = Leg.start_player_index % self._nr_players
        Leg.start_player_index += 1

    def run(self):
        """Players are taking turns and playing until a player wins."""
        for p in self._players:
            p.reset()

        while True:
            current_player = self._players[self._current_player_index]

            visit = Visit(current_player, log_parent=self)
            visit.run()

            if current_player.victorious():
                current_player.just_won_leg()
                break

            self._current_player_index += 1
            self._current_player_index %= self._nr_players


class Visit(LogEntryBase):
    """Representation of a player's visit. Only used to log visit information to
    the parent leg log.
    """

    def __init__(self, player, log_parent=None):
        super().__init__(log_parent, player=player.name)
        self._player = player

    def run(self):
        """The player plays one visit. The log entry is updated."""
        self._player.play()
        self._log_entry.attrib.update(
            dict(
                points=str(self._player.visit_sum()),
                throws=str(3 - self._player.darts)))
