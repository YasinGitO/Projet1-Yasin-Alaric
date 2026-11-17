import os
import unittest

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

from bullet import Bullet
from ennemy import Ennemy, EnnemiTank
from game import Game
from player import Player


class CollisionTest(unittest.TestCase):

    def setUp(self):
        self.game = Game()
        self.joueur = Player(self.game, "Test")

    def test_bullet_damages_and_kills_ennemy(self):
        ennemi = Ennemy(100, 100, hp=1, game=self.game)
        self.game.ennemies.append(ennemi)
        self.joueur.weapon.shooted_bullets.append(Bullet(110, 110))
        self.game.handle_collisions(self.joueur)
        self.assertEqual(ennemi.get_hp(), 0)
        self.assertEqual(self.game.ennemies, [])
        self.assertEqual(self.joueur.weapon.shooted_bullets, [])

    def test_tank_survives_one_bullet(self):
        tank = EnnemiTank(100, 100, game=self.game)
        self.game.ennemies.append(tank)
        self.joueur.weapon.shooted_bullets.append(Bullet(110, 110))
        self.game.handle_collisions(self.joueur)
        self.assertEqual(tank.get_hp(), 2)
        self.assertEqual(len(self.game.ennemies), 1)

    def test_bullet_miss(self):
        ennemi = Ennemy(100, 100, hp=1, game=self.game)
        self.game.ennemies.append(ennemi)
        self.joueur.weapon.shooted_bullets.append(Bullet(500, 500))
        self.game.handle_collisions(self.joueur)
        self.assertEqual(ennemi.get_hp(), 1)
        self.assertEqual(len(self.joueur.weapon.shooted_bullets), 1)

    def test_ennemy_touching_player_hurts_and_game_over(self):
        tank = EnnemiTank(self.joueur.get_x(), self.joueur.get_y(), game=self.game)
        self.game.ennemies.append(tank)
        self.game.handle_player_collisions(self.joueur)
        self.assertEqual(self.joueur.get_hp(), 1)
        self.assertFalse(self.game.game_over)
        self.game.ennemies.append(Ennemy(self.joueur.get_x(), self.joueur.get_y(), hp=1, damage=1, game=self.game))
        self.game.handle_player_collisions(self.joueur)
        self.assertEqual(self.joueur.get_hp(), 0)
        self.assertTrue(self.game.game_over)

    def test_ennemy_reaching_bottom_is_game_over(self):
        self.game.ennemies.append(Ennemy(0, 450, hp=1, game=self.game))
        self.game.handle_player_collisions(self.joueur)
        self.assertTrue(self.game.game_over)

    def test_weapon_damage_is_used(self):
        self.joueur.weapon.damage = 3
        self.joueur.weapon.cooldown = 0
        self.joueur.weapon.shoot(0, 0)
        self.assertEqual(self.joueur.weapon.shooted_bullets[0].damage, 3)


if __name__ == "__main__":
    unittest.main()
