import unittest

from pydarts.session import Player


class PlayerEntryTestCase(unittest.TestCase):
    def setUp(self):
        self.player = Player("Raymond", 0, 501)

    def test_not_victorious(self):
        self.assertFalse(self.player.victorious())

    def test_scores_valid(self):
        self.assertTrue(self.player.score_valid(180))
        self.player._visit.append(60)
        self.assertFalse(self.player.score_valid(121))
        # hack low remaining score
        self.player._score_left = 40
        self.assertTrue(self.player.score_valid(20))
        # busted
        self.assertFalse(self.player.score_valid(39))
        self.assertFalse(self.player.score_valid(42))
        # finish
        self.assertTrue(self.player.score_valid(40))

    def test_substract(self):
        # first visit
        self.player.substract(180, True)
        self.assertEqual(self.player.score_left, 321)
        self.assertEqual(self.player.throws, 3)
        self.assertEqual(self.player.darts, 0)
        self.assertEqual(self.player.visit_sum(), 180)
        # second visit
        self.player.begin()
        self.assertEqual(self.player.visit_sum(), 0)
        self.assertEqual(self.player.darts, 3)
        self.player.substract(60, False)
        self.assertEqual(self.player.throws, 4)
        self.assertEqual(self.player.darts, 2)
        self.player.substract(60, False)
        self.player.substract(60, False)
        self.assertEqual(self.player.throws, 6)
        self.assertEqual(self.player.darts, 0)
        self.assertEqual(self.player.visit_sum(), 180)
        self.assertEqual(self.player.score_left, 141)
        # third visit, busting for testing reasons
        self.player.begin()
        self.player.substract(0, True)
        self.assertEqual(self.player.throws, 9)
        self.assertEqual(self.player.score_left, 141)
        # fourth visit, busts again
        self.player.begin()
        self.player.substract(60, False)
        self.assertEqual(self.player.score_left, 81)
        self.player.substract(-60, True)
        self.assertEqual(self.player.throws, 12)
        self.assertEqual(self.player.score_left, 141)
        # fifth visit, finishes
        self.player.begin()
        self.player.substract(141, True)
        self.assertEqual(self.player.throws, 15)
        self.assertTrue(self.player.victorious())


if __name__ == '__main__':
    unittest.main()
