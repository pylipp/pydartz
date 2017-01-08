class Player(object):

    def __init__(self, name, index, start_value):
        self._name = name
        self._index = index
        self._stats = None
        self._score_left = start_value
        self._darts = 3

    def begin(self):
        self._darts = 3

    def victorious(self):
        return self._score_left == 0

    def substract(self, score, is_total=True):
        self._score_left -= score
        if is_total:
            self._darts = 0
        else:
            self._darts -= 1

    @property
    def score_left(self):
        return self._score_left

    @property
    def darts(self):
        return self._darts

    @property
    def name(self):
        return self._name


def read_input(player):
    while True:
        input_ = input("{}'s score: ".format(player.name)).strip()
        try:
            if input_.endswith("f"):
                score = int(input_[:-1])
                option = show_finish_options
                return score, option
            else:
                score = int(input_)
                return score, None
        except (ValueError):
            pass


def show_finish_options(score_left):
    pass


class Session(object):

    def __init__(self, player_names, start_value):
        self._players = []
        for i, name in enumerate(player_names):
            self._players.append(Player(name, i, start_value))
        self._current_player_index = 0

    def run(self):
        while True:
            current_player = self._players[self._current_player_index]
            current_player.begin()
            print("{cp.name} has {cp.score_left} left.".format(cp=current_player))

            while current_player.darts and not current_player.victorious():
                score, option = read_input(current_player)
                current_player.substract(score, option is None)
                if callable(option):
                    option(current_player.score_left)

            if current_player.victorious():
                print("{} has won!".format(current_player.name))
                break
