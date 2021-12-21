# pylint: disable=protected-access
import unittest
from unittest import mock
from collections import Counter

from xml.etree import ElementTree as etree

from pydartz.database import PlayerEntry, analyze_sessions, LogEntryBase
from pydartz.session import Session, Visit
from pydartz.player import Player
from pydartz.communication import TestingCommunicator


class PlayerEntryTestCase(unittest.TestCase):
    def test_default_init(self):
        entry = PlayerEntry()
        self.assertEqual(0, entry._throws)
        self.assertListEqual([], entry._points)
        self.assertEqual(0, len(entry._finishes))

    def test_init_with_stats(self):
        player_stats = dict(throws=123, points=4567, finishes=Counter({20:
            89}), darters=Counter())
        entry = PlayerEntry(player_stats=player_stats)
        self.assertEqual(123, entry._throws)
        self.assertEqual(4567, entry._points)
        self.assertEqual(89, entry._finishes[20])
        self.assertEqual(0, len(entry._darters))

    def test_update(self):
        entry = PlayerEntry()
        entry.update(9, 501)
        self.assertEqual(9, entry._throws)
        self.assertEqual(501, entry._points[0])
        self.assertEqual(0, len(entry._finishes))
        self.assertEqual(501, entry.total_points())

    def test_to_dict(self):
        player_stats = dict(throws=123, points=4567, finishes=Counter({20: 89}),
                darters=Counter({9: 2}))
        entry = PlayerEntry("Michael", player_stats)
        self.assertDictEqual(player_stats, entry.to_dict()["Michael"])

    def test_average(self):
        entry = PlayerEntry()
        entry.update(10, 420)
        self.assertEqual(42, entry.average())


class LogEntryBaseTestCase(unittest.TestCase):
    def test_save(self):
        parent = LogEntryBase()
        parent.save = mock.MagicMock()
        log_entry_base = LogEntryBase(parent=parent)
        log_entry_base.save()
        self.assertEqual(parent.save.call_count, 1)


class AnalysisTestCase(unittest.TestCase):
    def test_analyse_sessions(self):
        sessions = etree.Element("sessions")
        communicator = TestingCommunicator(
                "180d",
                60, 60, 57,
                60, 60, 24
                )
        session = Session([Player("Peter", communicator=communicator)], 1,
                log_parent=sessions, communicator=communicator)
        session.run()

        player_entry = analyze_sessions(sessions)["Peter"]

        self.assertEqual(player_entry.total_points(), 501)
        self.assertAlmostEqual(player_entry.average(), 501/9)
        self.assertEqual(player_entry.throws, 9)
        self.assertEqual(player_entry._finishes[144], 1)
        self.assertEqual(player_entry._darters[9], 1)


class PlayerLoggingTestCase(unittest.TestCase):
    def setUp(self):
        self.player = Player("Raymond")

    def test_single_visit_logging(self):
        log_entry = etree.Element("leg")
        self.player._communicator = TestingCommunicator("60", "50", "40")
        visit = Visit(self.player, log_parent=log_entry)
        visit.run()
        self.assertEqual(len(log_entry), 1)
        visit_log_entry = log_entry[0]
        self.assertEqual(visit_log_entry.get("player"), self.player.name)
        self.assertEqual(visit_log_entry.get("points"), "150")
        self.assertEqual(visit_log_entry.get("throws"), "3")

if __name__ == '__main__':
    unittest.main()
