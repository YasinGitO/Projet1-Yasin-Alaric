import random

import pygame

from arme import creer_arme
from ennemy import Ennemy, EnnemiTank
from player import Player
from powerup import PowerUp


class Game:
    def __init__(self):
        self.players = []
        self.ennemies = []
        self.powerups = []
        self.spawn_delay = 2000      # délai de départ entre 2 apparitions d'ennemis (ms)
        self.spawn_delay_min = 400   # délai minimum, quel que soit le score (ms)
        self.spawn_delay_step = 25   # millisecondes gagnées par point de score
        self.last_spawn = 0
        self.tank_chance = 0.25      # 25% de chance d'avoir un tank
        self.powerup_chance = 0.2    # 20% de chance qu'un ennemi mort laisse un power-up
        self.level = 1
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.running = True
        self.game_over = False
        self.font = pygame.font.Font(None, 80)
        self.hud_font = pygame.font.Font(None, 30)
        self.background = pygame.image.load('image/background.png')
        self.level_music = {1: "sounds/background.wav"}

    def get_screen_size(self):
        return self.screen.get_size()

    def set_background(self, background):
        self.background = pygame.image.load(background)

    def handle_collisions(self, player):
        """
        Vérifie les collisions entre les balles du joueur et les ennemis.
        Si une balle touche un ennemi : la balle disparait et l'ennemi perd des PV (take_damage).
        Si l'ennemi n'a plus de vie, il est retiré du jeu.
        """
        for bullet in player.weapon.shooted_bullets[:]:
            for ennemi in self.ennemies:
                if ennemi.is_hit_by(bullet):
                    ennemi.take_damage(bullet.damage)
                    player.weapon.shooted_bullets.remove(bullet)
                    break
        for ennemi in self.ennemies[:]:
            if not ennemi.is_alive():
                self.ennemies.remove(ennemi)
                player.add_score(ennemi.get_points())
                self.drop_powerup(ennemi)

    def spawn_ennemy(self):
        """
        Fait apparaitre un ennemi en haut de l'écran, à une position x aléatoire.
        Avec une chance de tank_chance, c'est un tank.
        """
        x = random.randint(0, self.get_screen_size()[0] - 64)
        if random.random() < self.tank_chance:
            ennemi = EnnemiTank(x, 0, self)
        else:
            ennemi = Ennemy(x, 0, 1, 3, 1, self)
        if random.random() < 0.5:
            ennemi.speed = -ennemi.speed
        self.ennemies.append(ennemi)

    def get_spawn_delay(self):
        """
        Plus le score est élevé, plus le délai entre 2 ennemis est court (jusqu'à spawn_delay_min).
        """
        score = sum(player.get_score() for player in self.players)
        return max(self.spawn_delay_min, self.spawn_delay - score * self.spawn_delay_step)

    def update_spawn(self):
        """
        Fait apparaitre un nouvel ennemi toutes les get_spawn_delay() millisecondes.
        """
        now = pygame.time.get_ticks()
        if now - self.last_spawn >= self.get_spawn_delay():
            self.last_spawn = now
            self.spawn_ennemy()

    def drop_powerup(self, ennemi):
        """
        Un ennemi qui meurt laisse parfois un power-up (arme au hasard) à l'endroit où il est mort.
        """
        if random.random() < self.powerup_chance:
            nom = random.choice(["Mitraillette", "Canon"])
            self.powerups.append(PowerUp(ennemi.get_x(), ennemi.get_y(), nom))

    def handle_powerups(self, player):
        """
        Fait tomber les power-ups. Si le joueur en touche un, il change d'arme.
        """
        for powerup in self.powerups[:]:
            powerup.update()
            if powerup.get_rect().colliderect(player.get_rect()):
                player.change_weapon(creer_arme(powerup.weapon_name))
                self.powerups.remove(powerup)
            elif powerup.is_out_of_screen(self.get_screen_size()[1]):
                self.powerups.remove(powerup)

    def handle_player_collisions(self, player):
        """
        Vérifie les collisions entre le joueur et les ennemis.
        Si un ennemi touche le joueur : le joueur perd les dégâts de l'ennemi et l'ennemi disparait.
        Si un ennemi arrive à la hauteur du joueur ou si le joueur n'a plus de vie : game over.
        """
        for ennemi in self.ennemies[:]:
            if ennemi.get_rect().colliderect(player.get_rect()):
                player.take_damage(ennemi.get_damage())
                self.ennemies.remove(ennemi)
            elif ennemi.get_y() + ennemi.image.get_height() >= player.get_y():
                self.game_over = True
        if not player.is_alive():
            self.game_over = True

    def draw_hud(self, player):
        arme = player.weapon.type
        if player.weapon.ammo is not None:
            arme += f" ({player.weapon.ammo})"
        texte = f"Score: {player.get_score()}   PV: {player.get_hp()}   Arme: {arme}"
        self.screen.blit(self.hud_font.render(texte, True, (255, 255, 255)), (10, 10))

    def draw_game_over(self):
        texte = self.font.render("GAME OVER", True, (255, 255, 255))
        x = (self.get_screen_size()[0] - texte.get_width()) // 2
        y = (self.get_screen_size()[1] - texte.get_height()) // 2
        self.screen.blit(texte, (x, y))



def main():
    game = Game()
    joueur = Player(game, "Alaric")
    game.players.append(joueur)
    game.spawn_ennemy()
    clock = pygame.time.Clock()
    while game.running:
        # RGB = Red, Green, Blue
        game.screen.fill((0, 0, 0))
        # Background Image
        game.screen.blit(game.background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False

        if not game.game_over:
            joueur.handle_input()
            joueur.update()

            game.update_spawn()
            for ennemi in game.ennemies:
                ennemi.update()
            game.handle_collisions(joueur)
            game.handle_powerups(joueur)
            game.handle_player_collisions(joueur)

        joueur.draw(game.screen)
        for ennemi in game.ennemies:
            ennemi.draw(game.screen)
        for powerup in game.powerups:
            powerup.draw(game.screen)
        game.draw_hud(joueur)

        if game.game_over:
            game.draw_game_over()
        pygame.display.flip()

        clock.tick(60)



if __name__ == "__main__":
    main()


# gérer victoire/défaite
# niveaux
