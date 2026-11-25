import random

import pygame

from arme import creer_arme
from ennemy import Ennemy, EnnemiTank
from powerup import PowerUp

# --- Configuration & Équilibrage ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

SPAWN_DELAY_INITIAL = 2000   # délai de départ entre 2 apparitions d'ennemis (ms)
SPAWN_DELAY_MIN = 400        # délai minimum, quel que soit le score (ms)
SPAWN_DELAY_STEP = 25        # millisecondes gagnées par point de score

TANK_CHANCE = 0.25           # 25% de chance d'avoir un tank
POWERUP_CHANCE = 0.2         # 20% de chance qu'un ennemi mort laisse un power-up

DEFAULT_BACKGROUND = 'image/background.png'
LEVEL_MUSIC = {1: "sounds/background.wav"}


class Game:
    def __init__(self):
        # État de la partie
        self.players = []
        self.ennemies = []
        self.powerups = []
        self.level = 1
        self.last_spawn = 0
        self.running = True
        self.game_over = False

        # Initialisation graphique / moteur
        self._init_pygame()

    def _init_pygame(self):
        """Initialise la fenêtre, les polices et les ressources de base."""
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.font = pygame.font.Font(None, 80)
        self.hud_font = pygame.font.Font(None, 30)
        self.background = pygame.image.load(DEFAULT_BACKGROUND)

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
        Avec une chance de TANK_CHANCE, c'est un tank.
        """
        x = random.randint(0, self.get_screen_size()[0] - 64)
        if random.random() < TANK_CHANCE:
            ennemi = EnnemiTank(x, 0, self)
        else:
            ennemi = Ennemy(x, 0, 1, 3, 1, self)
        if random.random() < 0.5:
            ennemi.speed = -ennemi.speed
        self.ennemies.append(ennemi)

    def get_spawn_delay(self):
        """
        Plus le score est élevé, plus le délai entre 2 ennemis est court (jusqu'à SPAWN_DELAY_MIN).
        """
        score = sum(player.get_score() for player in self.players)
        return max(SPAWN_DELAY_MIN, SPAWN_DELAY_INITIAL - score * SPAWN_DELAY_STEP)

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
        if random.random() < POWERUP_CHANCE:
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

