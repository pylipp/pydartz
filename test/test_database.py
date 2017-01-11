import unittest
from collections import Counter
from pydarts.database import PlayerEntry


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


if __name__ == '__main__':
    unittest.main()
