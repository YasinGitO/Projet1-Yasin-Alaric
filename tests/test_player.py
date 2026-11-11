import unittest

from player import Player

class PlayerTest(unittest.TestCase):

    def test_player_str(self):
        joueur = Player(1,2)
        self.assertEqual(str(joueur), "Player 1")