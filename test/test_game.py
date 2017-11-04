import unittest

from pydarts.game import Game
from pydarts.communication import TestingCommunicator


class GameTestCase(unittest.TestCase):
    def test_single_player_game(self):
        communicator = TestingCommunicator(
                1,          # nr of players
                501,        # start value
                "Herbert",  # name
                1,          # nr of legs to win
                59, 59, 59, # visit data...
                58, "60d",
                1, 2, 3,
                "150d",
                50,
                )
        game = Game()
        game.run(communicator)

        self.assertTrue(game._sessions[0]._players[0].victorious())


if __name__ == "__main__":
    unittest.main()
