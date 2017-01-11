import os.path
import yaml


dirname = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(dirname, "..", "data", "finishes.yml")) as file:
    finishes = yaml.load(file)


class Player(object):

    def __init__(self, name, index, start_value):
        self._name = name
        self._index = index
        self._stats = None
        self._score_left = start_value
        self._darts = 3
        self._visit = []

    def begin(self):
        if self._visit:
            self._visit = []
        self._darts = 3

    def victorious(self):
        return self._score_left == 0

    def substract(self, score, is_total=True):
        self._score_left -= score
        if is_total or score + sum(self._visit) == 180:
            self._darts = 0
        else:
            self._visit.append(score)
            self._darts -= 1

    def score_valid(self, score):
        # visit score must not exceed 180
        if score + sum(self._visit) > 180:
            return False
        # remaining score must not be negative or one
        difference = self._score_left - score
        return difference == 0 or difference > 1

    def print_info(self):
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


    def read_input(self):
        while True:
            input_ = input("{}'s score: ".format(self._name)).strip()
            try:
                if input_.endswith("d"):
                    score = int(input_[:-1])
                    is_total = True
                else:
                    score = int(input_)
                    is_total = False
                # validate the input
                if self.score_valid(score):
                    return score, is_total
                else:
                    print("Invalid score: {}".format(score))
            except (ValueError):
                print("Invalid input: {}".format(input_))


class Session(object):

    def __init__(self, player_names, start_value):
        self._players = []
        for i, name in enumerate(player_names):
            self._players.append(Player(name, i, start_value))
        self._current_player_index = 0
        self._nr_players = len(self._players)

    def run(self):
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
