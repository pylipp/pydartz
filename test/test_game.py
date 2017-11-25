# pylint: disable=protected-access
import unittest

from pydarts.game import Game
from pydarts.communication import TestingCommunicator
from pydarts.database import analyze_sessions


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
        game = Game(communicator)
        game.run()

        self.assertTrue(game._sessions[0]._players[0].victorious())

    def test_single_player_two_sessions_game(self):
        communicator = TestingCommunicator(
            1,
            16,
            "Anton",
            2,
            16,
            8, 8,
            "a",  # invalid input
            "y",
            4, 4, 8,
            16,
            " ",  # invalid input
            "Q",
        )
        log = []
        game = Game(communicator, sessions_log=log)
        game.run()

        player_info = analyze_sessions(log)["Anton"].to_dict()["Anton"]
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
        log = []
        game = Game(communicator, sessions_log=log)
        game.run()

        player_info = analyze_sessions(log)["Anton"].to_dict()["Anton"]
        self.assertEqual(player_info["throws"], 6)
        self.assertListEqual(player_info["points"], [16, 16, 32])
        self.assertEqual(player_info["darters"][2], 3)


if __name__ == "__main__":
    unittest.main()
