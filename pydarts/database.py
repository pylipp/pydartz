import os.path
import time
from collections import Counter
from abc import ABCMeta

from tinydb import TinyDB, where
from lxml import etree


class LogEntryBase(object):
    """Abstract base class for all classes that are supposed to support
    logging.

    It holds a member `_log_entry` of type `lxml.etree._Element`. Its tag is
    derived from the lowercase class name. If a `parent` argument (an instance
    of a class that implements an `append` method, such as a list or this
    class) is passed, the `log_entry` is appended, s.t. the hierarchy of the
    `session` classes is reflected in the XML log.
    The initialization time of each instance is stored as timestamp for later
    reference.
    Any additional kwargs are passed to `lxml.etree.Element` where they are
    interpreted as XML attributes.
    """

    __metaclass__ = ABCMeta

    DT_FORMAT = "%Y%m%d-%H%M%S"

    def __init__(self, parent=None, test_data=None, **kwargs):
        tag = self.__class__.__name__.lower()
        self._log_entry = etree.Element(tag,
                timestamp=time.strftime(self.DT_FORMAT), **kwargs)
        if parent is not None:
            parent.append(self._log_entry)

        self._test_data = test_data

    def append(self, child_log_entry):
        self._log_entry.append(child_log_entry)


class PlayerEntry(object):
    """A container to facilitate evaluation of player statistics.

    It stores the player's total throws, points (visit per visit for e.g.
    histogram evaluation), finishes and darters.
    Some basic update and query methods are implemented.
    """

    def __init__(self, name=None, player_stats=None):
        self._name = name
        self._throws = 0
        self._points = []
        self._finishes = Counter()
        self._darters = Counter()

        if player_stats:
            self._throws = player_stats["throws"]
            self._points = player_stats["points"]
            self._finishes = player_stats["finishes"]
            self._darters = player_stats["darters"]

    def update(self, throws=0, points=0, darter=None):
        self._throws += throws
        self._points.append(points)

        # only called if current player won. Points of last leg are passed
        if darter is not None:
            self._finishes[points] += 1
            self._darters[darter] += 1

    def update_from_log(self, log_element):
        """Convenience method to update from a `lxml.etree._Element` visit."""
        self.update(
                points=int(log_element.get("points")),
                throws=int(log_element.get("throws"))
                )

    def to_dict(self):
        """Returns a dict representation of the PlayerEntry data."""
        return {
                self._name: dict(
                    throws=self._throws,
                    points=self._points,
                    finishes=self._finishes,
                    darters=self._darters
                    )
                }

    def average(self):
        if self._throws != 0:
            return self.total_points() / self._throws
        return -1

    def total_points(self):
        return sum(self._points)

    @property
    def throws(self):
        return self._throws


def analyze_sessions(sessions):
    """Analyze a `lxml.etree._Element` sessions object.

    First all player names occurring are collected and a dict of PlayerEntrys
    is built.
    It is iterated over every session played so far. For every visit, the
    corresponding PlayerEntry is updated. The data of the last visit of a leg
    is used to update the winner's finishes and darters.
    """
    player_names = set()
    for session in sessions:
        for name in session.get("players").split(','):
            player_names.add(name)

    players = {name: PlayerEntry(name) for name in player_names}

    for session in sessions:
        for leg in session:
            winner_name = leg[-1].get("player")
            winner = players[winner_name]
            winner_old_throws = winner.throws

            for visit in leg[:-1]:
                name = visit.get("player")
                player_entry = players[name]
                player_entry.update_from_log(visit)

            final_throws = int(leg[-1].get("throws"))
            final_points = int(leg[-1].get("points"))
            # X-darter per player
            visit_throws = final_throws + winner.throws - winner_old_throws
            winner.update(points=final_points, throws=final_throws, darter=visit_throws)

    return players


def add(field, value):
    """Operation to increment `field` of a `tinydb.Element` by `value`. The
    field is created if it does not exist."""
    def transform(element):
        if field in element:
            element[field] += value
        else:
            element[field] = value

    return transform


class Stats(TinyDB):
    """Keep track of player and session statistics.
    Pass a list of player names at initialization. New player entries are
    created if they don't exist in the database yet.
    An optional filepath can be passed which is convenient for testing. By
    default, the file `data/stats.json` is used.
    This class is an extension of `tinydb.TinyDB`."""

    def __init__(self, player_names=[], filepath=None):
        self._filepath = filepath
        if self._filepath is None:
            dirname = os.path.dirname(os.path.abspath(__file__))
            self._filepath = os.path.join(dirname, "..", "data", "stats.json")
        super().__init__(self._filepath)

        for name in player_names:
            if not self.table("players").get(where("name") == name):
                self.table("players").insert({"name": name})

    def update(self, player=None):
        """Update information about player performance. Should be called after
        a player's visit."""
        if player is not None:
            stats = {
                    "throws": 3 - player.darts,
                    "points": player.visit_sum()
                    }
            if player.victorious():
                stats["finish_{:03}".format(stats["points"])] = 1

            for k, v in stats.items():
                self.table("players").update(
                        add(k, v), where("name") == player.name)
