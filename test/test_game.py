# pylint: disable=protected-access
import unittest

from pydartz.game import Game
from pydartz.communication import TestingCommunicator
from pydartz.database import analyze_sessions


def run_game(communicator):
    log = []
    game = Game(communicator, sessions_log=log)
    game.run()
    return analyze_sessions(log)


class GameTestCase(unittest.TestCase):
    def test_single_player_game(self):
        communicator = TestingCommunicator(
                1,           # nr of players
                501,        # start value
                "Herbert",  # name
                1,          # nr of legs to win
                59, 59, 59, # visit data...
                58, "60d",
                1, 2, 3,
                "150d",
                50,
                "q",
                )
        infos = run_game(communicator)
        player_info = infos["Herbert"].to_dict()["Herbert"]
        self.assertListEqual(player_info["points"], [177, 118, 6, 150, 50])

    def test_single_player_two_sessions_game(self):
        communicator = TestingCommunicator(
            1,
            16,
            "Anton",
            2,
            16,
            8, 8,
            "y",
            4, 4, 8,
            16,
            "q",
        )
        infos = run_game(communicator)
        player_info = infos["Anton"].to_dict()["Anton"]
        self.assertEqual(player_info["throws"], 7)
        self.assertListEqual(player_info["points"], [16 for _ in range(4)])

    def test_two_various_sessions_game(self):
        communicator = TestingCommunicator(
            1,
            16,
            "Anton",
            2,
            8, 8,
            8, 8,
            "n",
            2,
            32,
            "Anton", "Herbert",
            1,
            16, 16,
            "q",
        )
        infos = run_game(communicator)
        player_info = infos["Anton"].to_dict()["Anton"]
        self.assertEqual(player_info["throws"], 6)
        self.assertListEqual(player_info["points"], [16, 16, 32])
        self.assertEqual(player_info["darters"][2], 3)


if __name__ == "__main__":
    unittest.main()
