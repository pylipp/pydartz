import os
import unittest
from collections import Counter
from tinydb import where
from pydarts.database import PlayerEntry, Stats
from pydarts.session import Player


class PlayerEntryTestCase(unittest.TestCase):
    def test_default_init(self):
        entry = PlayerEntry()
        self.assertEqual(0, entry._throws)
        self.assertEqual(0, entry._points)
        self.assertEqual(0, len(entry._finishes))

    def test_init_with_stats(self):
        player_stats = dict(throws=123, points=4567, finishes=Counter({20: 89}))
        entry = PlayerEntry(player_stats=player_stats)
        self.assertEqual(123, entry._throws)
        self.assertEqual(4567, entry._points)
        self.assertEqual(89, entry._finishes[20])

    def test_update(self):
        entry = PlayerEntry()
        entry.update(9, 501, True)
        self.assertEqual(9, entry._throws)
        self.assertEqual(501, entry._points)
        self.assertEqual(1, entry._finishes[9])

    def test_to_dict(self):
        player_stats = dict(throws=123, points=4567, finishes=Counter({20: 89}))
        entry = PlayerEntry("Michael", player_stats)
        self.assertDictEqual(player_stats, entry.to_dict()["Michael"])

    def test_average(self):
        entry = PlayerEntry()
        entry.update(10, 420)
        self.assertEqual(42, entry.average())


class StatsTestCase(unittest.TestCase):
    def setUp(self):
        dirname = os.path.dirname(os.path.abspath(__file__))
        self.filepath = os.path.join(dirname, "test_db.json")

    def test_duplicate_player_names(self):
        player_names = ["Michael", "Phil", "Gary", "Phil"]
        stats = Stats(player_names, self.filepath)
        self.assertEqual(3, len(stats.table("players")))
        stats.close()

    def test_update(self):
        stats = Stats(["Max"], self.filepath)
        player = Player("Max", 0, 301)
        # first visit
        player.substract(180, True)
        stats.update(player=player)
        player_element = stats.table("players").get(where("name") == "Max")
        self.assertEqual(player_element["throws"], 3)
        self.assertEqual(player_element["points"], 180)
        # second visit
        player.begin()
        player.substract(57, False)
        player.substract(64, True)
        stats.update(player=player)
        player_element = stats.table("players").get(where("name") == "Max")
        self.assertEqual(player_element["throws"], 6)
        self.assertEqual(player_element["points"], 301)
        self.assertEqual(player_element["finish_121"], 1)
        stats.close()

    def tearDown(self):
        os.remove(self.filepath)


if __name__ == '__main__':
    unittest.main()
