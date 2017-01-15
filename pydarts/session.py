import os.path
import yaml


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
        self._stats = None
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
        None that score has to be valid since this method does not do any
        checks on its own."""
        self._score_left -= score
        if is_total or score + sum(self._visit) == 180:
            self._throws += self._darts
            self._darts = 0
        else:
            self._throws += 1
            self._darts -= 1
        self._visit.append(score)

    def score_valid(self, score):
        """Check whether `score` is valid, i.e. the current visit must not
        exceed 180 and the player must not be busted."""
        if score + sum(self._visit) > 180:
            return False
        difference = self._score_left - score
        return difference == 0 or difference > 1

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

    def read_input(self):
        """Read score input given by the user while checking for errors.
        To declare a score as total, append a 'd' (for 'done') to the score."""
        while True:
            input_ = input("{}'s score: ".format(self._name)).strip()
            try:
                if input_.endswith("d"):
                    if len(input_) == 1:
                        score = 0
                    else:
                        score = int(input_[:-1])
                    is_total = True
                elif input_.lower() == "b":
                    # player busted, undo whatever he scored so far in his turn
                    # all three darts are taken into account for the average, see
                    # http://www.dartsnutz.net/forum/archive/index.php/thread-18910.html
                    score = -self.visit_sum()
                    is_total = True
                else:
                    score = int(input_)
                    is_total = False

                if self.score_valid(score):
                    return score, is_total
                else:
                    print("Invalid score: {}".format(score))
            except (ValueError):
                print("Invalid input: {}".format(input_))


class Session(object):
    """Representation of a darts session.
    Initialized with a list of player names and the start value."""

    def __init__(self, player_names, start_value):
        self._players = []
        for i, name in enumerate(player_names):
            self._players.append(Player(name, i, start_value))
        self._current_player_index = 0
        self._nr_players = len(self._players)

    def run(self):
        """Main game loop. Players are taking turns and playing until a player
        wins."""
        while True:
            current_player = self._players[self._current_player_index]
            current_player.begin()

            while current_player.darts and not current_player.victorious():
                current_player.print_info()
                score, is_total = current_player.read_input()
                current_player.substract(score, is_total)

            if current_player.victorious():
                print("{} has won!".format(current_player.name))
                break

            self._current_player_index += 1
            self._current_player_index %= self._nr_players
