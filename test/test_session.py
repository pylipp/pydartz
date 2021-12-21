# pylint: disable=protected-access
import unittest
from unittest import mock
from datetime import datetime

from pydartz.session import Leg, Session
from pydartz.player import Player
from pydartz.communication import TestingCommunicator


def _180_single_player_communicator():
    return TestingCommunicator(
                "180d",
                60, 60, 57,
                60, 60, 24
                )


class LegTestCase(unittest.TestCase):
    def test_single_player_9_darter(self):
        communicator = _180_single_player_communicator()
        mike = Player("Mike", communicator=communicator)
        leg = Leg([mike])
        leg.run()
        self.assertEqual(leg._current_player_index, 0)
        self.assertTrue(mike.victorious())

    def test_two_player_101(self):
        # pylint: disable=bad-whitespace
        communicator = TestingCommunicator(
                # Hans   Fritz
                "60d",   19, 17, 3,
                19, "b", 12, 50,
                )
        hans = Player("Hans", 101, communicator=communicator)
        fritz = Player("Fritz", 101, communicator=communicator)
        # static variable is increased by previous tests...
        # in reality, the Session handles this
        Leg.start_player_index = 0
        leg = Leg([hans, fritz])
        leg.run()

        self.assertEqual(leg._current_player_index, 1)
        self.assertTrue(fritz.victorious())
        self.assertEqual(hans.score_left, 41)

    def test_logging_without_parent(self):
        leg = Leg(["Peter"])
        # might fail around midnight...
        self.assertEqual(
                datetime.strptime(leg._log_entry.get("timestamp"),
                    Leg.DT_FORMAT).day, datetime.today().day)

    def test_logging_with_parent(self):
        log_parent = []
        Leg(["Mike"], log_parent=log_parent)
        log_entry = log_parent[0]
        self.assertEqual(log_entry.tag, "leg")
        self.assertEqual(len(log_entry), 0)

    def test_single_player_9_darter_logging(self):
        communicator = _180_single_player_communicator()
        players = [Player("Mike", communicator=communicator)]
        log_parent = []
        leg = Leg(players, log_parent=log_parent)
        leg.run()

        visits_log_entry = log_parent[0]
        self.assertEqual(len(visits_log_entry), 3)
        self.assertEqual(visits_log_entry[0].get("throws"), "3")
        self.assertEqual(visits_log_entry[2].get("points"), "144")
        # assert average etc

    def test_single_player_invalid_visit(self):
        with mock.patch.object(TestingCommunicator, 'print_error') as \
                print_error_patch:
            communicator = TestingCommunicator(
                    "180d",
                    60, 60, 57,
                    60, 60, 60,  # <-- this is invalid
                    24
                    )
            player = Player("Mike", communicator=communicator)
            leg = Leg([player])
            leg.run()
        self.assertEqual(print_error_patch.call_count, 1)
        self.assertTrue(player.victorious())


class SessionTestCase(unittest.TestCase):
    def test_single_player_9_darter_session(self):
        communicator = _180_single_player_communicator()
        players = [Player("Peter", communicator=communicator)]
        session = Session(players, 1, communicator=communicator)
        session.run()

        self.assertEqual(len(session._log_entry[0]), 3)
        self.assertEqual(len(session._log_entry), 1)

    def test_two_player_session(self):
        # pylint: disable=bad-whitespace
        communicator = TestingCommunicator(
                # Adam     Eve
                "60d",      20, 11, 20,
                "40",
                            "60d",
                20, 11, 20, 40,
                "60d",      20, 11, 20,
                "40",
                )
        adam = Player("Adam", 100, communicator=communicator)
        eve = Player("Eve", 100, communicator=communicator)
        session = Session([adam, eve], 2, communicator=communicator)
        session.run()

        self.assertTrue(adam.victorious())
        self.assertEqual(eve.score_left, 49)


if __name__ == '__main__':
    unittest.main()
