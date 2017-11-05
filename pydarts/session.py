from .database import LogEntryBase, save_session, log_visit


class Session(LogEntryBase):
    """Representation of a darts session.
    Initialized with a list of players and the number of legs to win.
    """

    def __init__(self, players, nr_legs=1, log_parent=None, communicator=None):
        super(Session, self).__init__(log_parent,
                players=','.join([p.name for p in players]))

        self._players = players
        self._nr_legs = nr_legs
        self._communicator = communicator

    def _player_won_enough_legs(self):
        largest_nr_of_victories = max((p.nr_won_legs for p in self._players))
        return self._nr_legs <= largest_nr_of_victories

    def run(self):
        """Play until a player has won the predefined number of legs. Print the
        score if not in test mode.
        """
        Leg.start_player_index = 0

        while not self._player_won_enough_legs():
            for p in self._players:
                p.reset()

            leg = Leg(self._players, log_parent=self)
            leg.run()

            save_session()

            for p in self._players:
                self._communicator.print_output(
                        "    {}: {:2d}".format(p.name, p.nr_won_legs))
            self._communicator.print_output(80 * "=")


class Leg(LogEntryBase):
    """Representation of a darts leg. Players start alternatingly which is
    established by the static variable `start_player_index` that is incremented
    every time a Leg instance is created.
    """

    start_player_index = 0

    def __init__(self, players, log_parent=None):
        super(Leg, self).__init__(log_parent)

        self._players = players
        self._nr_players = len(self._players)

        self._current_player_index = Leg.start_player_index % self._nr_players
        Leg.start_player_index += 1

    def run(self):
        """Main game loop. Players are taking turns and playing until a player
        wins. If this is repeatedly run, the players' start value is not
        automatically reset.
        """
        while True:
            current_player = self._players[self._current_player_index]

            current_player.play()

            log_visit(current_player, self._log_entry)

            if current_player.victorious():
                current_player.just_won_leg()
                break

            self._current_player_index += 1
            self._current_player_index %= self._nr_players
