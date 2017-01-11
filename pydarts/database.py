from collections import Counter


class PlayerEntry(object):

    def __init__(self, name=None, player_stats=None):
        self._name = name
        self._throws = 0
        self._points = 0
        self._finishes = Counter()

        if player_stats:
            self._throws = player_stats["throws"]
            self._points = player_stats["points"]
            self._finishes = player_stats["finishes"]

    def update(self, throws, points, finished=False):
        self._throws += throws
        self._points += points
        if finished:
            self._finishes[throws] += 1

    def to_dict(self):
        return {
                self._name: dict(
                    throws=self._throws,
                    points=self._points,
                    finishes=self._finishes
                    )
                }

    def average(self):
        if self._throws != 0:
            return self._points / self._throws
        return 0
