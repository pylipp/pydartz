from .database import LogEntryBase, save_session


class Session(LogEntryBase):
    """Representation of a darts session.
    Initialized with a list of players and the number of
    legs to play.

    For testing, a deque of deques containing the players' visits can be
    passed. See the tests for an example.
    """

    def __init__(self, players, nr_legs=1, test_legs=None, log_parent=None):
        super().__init__(log_parent, test_data=test_legs,
                players=','.join([p.name for p in players]))

        self._players = players
        self._nr_legs = nr_legs

    def _player_won_enough_legs(self):
        largest_nr_of_victories = max((p.nr_won_legs for p in self._players))
        return self._nr_legs <= largest_nr_of_victories

    def run(self):
        """Play until a player has won the predefined number of legs. Print the
        score if not in test mode.
        """
        test_run = self._test_data is not None
        Leg.start_player_index = 0

        while not self._player_won_enough_legs():
            visits = None if self._test_data is None else self._test_data.popleft()

            for p in self._players:
                p.reset()

            leg = Leg(self._players, log_parent=self, test_visits=visits)
            leg.run()

            save_session()

            if not test_run:
                for p in self._players:
                    print("    {}: {:2d}".format(p.name, p.nr_won_legs))
                print(80 * "=")


class Leg(LogEntryBase):
    """Representation of a darts leg. Players start alternatingly which is
    established by the static variable `start_player_index` that is incremented
    every time a Leg instance is created.

    For testing, one can pass a deque for the `test_visits` argument. The
    leftmost element will be popped at every visit and (unpacked) serve as
    input for `testing_args` of `Player.play`. See the tests for an example.
    """

    start_player_index = 0

    def __init__(self, players, test_visits=None, log_parent=None):

        super().__init__(log_parent, test_visits)

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

            visit = [] if self._test_data is None else self._test_data.popleft()

            current_player.play(*visit, log_entry=self._log_entry)

            if current_player.victorious():
                current_player.just_won_leg()
                break

            self._current_player_index += 1
            self._current_player_index %= self._nr_players
