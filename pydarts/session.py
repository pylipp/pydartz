import os.path
from collections import deque, Counter

from lxml import etree
import yaml

from .database import LogEntryBase


# load the finishes table
dirname = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(dirname, "..", "data", "finishes.yml")) as file:
    finishes = yaml.load(file)


class Player(object):
    """Representation of a player.
    Holds long-term, per-game and per-visit information. Provides routines to
    perform a classic 501.
    Each player has a unique name and index that are passed at initialization.
    It is also required to pass a start value to initialize the player's
    remaining score."""

    def __init__(self, name, index, start_value):
        self._name = name
        self._index = index
        self._score_left = start_value
        self._throws = 0
        self._darts = 3
        self._visit = []

    def begin(self):
        """Reset actions at the beginning of a player's turn."""
        if self._visit:
            self._visit = []
        self._darts = 3

    def victorious(self):
        return self._score_left == 0

    def substract(self, score, is_total=True):
        """Substract `score` from the player's `score_left`. If `is_total` is
        true or if the score is obviously the last one of a player's turn, the
        number of remaining darts is set to zero.
        Note that score has to be valid since this method does not do any
        checks on its own."""
        self._score_left -= score
        #TODO this logic should be moved to _process_score
        if is_total or score + sum(self._visit) == 180:
            self._throws += self._darts
            self._darts = 0
        else:
            self._throws += 1
            self._darts -= 1
        self._visit.append(score)

    def score_valid(self, score):
        """Check whether `score` is valid, i.e. the current visit must not
        exceed 180, the player must not be busted and the score has to be
        legitimatly thrown (e.g. one cannot score 130 with two remaining darts.)

        Raises a ValueError if the score is invalid.
        """
        difference = self._score_left - score

        if score + sum(self._visit) > 180 or \
                score > 60 * self._darts or \
                difference < 0 or difference == 1:
            raise ValueError

        return True

    def print_info(self):
        """Print information on player's left score and darts and, optionally,
        finishing options."""
        print("{p.name} has {p.score_left} and {0} left.".format(
            ["one dart", "two darts", "three darts"][self._darts - 1], p=self))
        if self._score_left in finishes:
            print("Finish options: ")
            for finish in finishes[self._score_left]:
                print("\t" + " ".join(finish))

    @property
    def score_left(self):
        return self._score_left

    @property
    def darts(self):
        return self._darts

    @property
    def name(self):
        return self._name

    @property
    def throws(self):
        return self._throws

    def visit_sum(self):
        return sum(self._visit)

    def play(self, *testing_args, log_entry=None):
        """Read score input given by the user while checking for errors.
        Player information is printed before each throw. If _process_score()
        does not raise any errors, the input score is substracted from the
        player's remaining score.
        The procedure is repeated if the player has darts remaining and has not
        yet won.
        If the `log_entry` argument is passed, the current visit is logged.

        Passing up to three string values to `testing_args` is useful for
        testing and will make the method non-interactive."""

        self.begin()

        testing_args = deque(testing_args)
        interactive = len(testing_args) == 0

        while self._darts and not self.victorious():
            if interactive:
                self.print_info()
                input_ = input("{}'s score: ".format(self._name)).strip()
            else:
                input_ = testing_args.popleft()
            try:
                score, is_total = self._process_score(input_)
                self.substract(score, is_total)
            except ValueError as e:
                if interactive:
                    print(e)
                else:
                    raise
        if log_entry is not None:
            etree.SubElement(log_entry, "visit",
                    attrib=dict(
                        player=self._name,
                        points=str(self.visit_sum()),
                        throws=str(3 - self._darts)
                        ))

    def _process_score(self, score):
        """Parse the passed score. Valid options are:
        - x (an integer between 0 and 180)
        - xd (an integer between 0 and 180, with the character 'd' appended,
          indicating that the player's turn is over ('done'))
        - d (equivalent to '0d')
        - b (the character 'b', indicating that the player busted. The player's
          score will be reset in substract())
        A ValueError is thrown if an invalid score is passed. This can be
        caused by a score that exceeds the remaining score allowed in the
        current visit or by a typo."""
        try:
            if score.endswith("d"):
                if len(score) == 1:
                    score = 0
                else:
                    score = int(score[:-1])
                is_total = True
            elif score.lower() == "b":
                # player busted, undo whatever he scored so far in his turn
                # all three darts are taken into account for the average, see
                # http://www.dartsnutz.net/forum/archive/index.php/thread-18910.html
                score = -self.visit_sum()
                is_total = True
            else:
                score = int(score)
                is_total = False

            if self.score_valid(score):
                return score, is_total
        except (ValueError):
            # custom message
            raise ValueError("Invalid input: {}".format(score))


class Session(LogEntryBase):
    """Representation of a darts session.
    Initialized with a list of player names, the start value, and the number of
    legs to play.
    """

    def __init__(self, player_names, start_value, nr_legs=1, log_parent=None):
        super().__init__(log_parent)

        self._player_names = player_names
        self._start_value = start_value
        self._nr_legs = nr_legs

    def run(self):
        """Play the predefined number of legs. Keep track of the total session
        score using a counter.
        """
        counter = Counter()
        for i in range(self._nr_legs):
            leg = Leg(self._player_names, self._start_value, log_parent=self)
            leg.run()
            counter[leg.current_player_name()] += 1

            for name in self._player_names:
                print("    {}: {:2d}".format(name, counter.get(name, 0)))
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

    def __init__(self, player_names, start_value=501, test_visits=None,
            log_parent=None):

        super().__init__(log_parent)

        self._players = []
        for i, name in enumerate(player_names):
            self._players.append(Player(name, i, start_value))

        self._nr_players = len(self._players)

        self._current_player_index = Leg.start_player_index % self._nr_players
        Leg.start_player_index += 1

        self._test_visits = test_visits

    def run(self):
        """Main game loop. Players are taking turns and playing until a player
        wins. If this is repeatedly run, the players' start value is not
        automatically reset.
        """
        while True:
            current_player = self._players[self._current_player_index]

            visit = []
            if self._test_visits is not None:
                visit = self._test_visits.popleft()

            current_player.play(*visit, log_entry=self._log_entry)

            if current_player.victorious():
                break

            self._current_player_index += 1
            self._current_player_index %= self._nr_players

    def current_player_name(self):
        return self._players[self._current_player_index].name
