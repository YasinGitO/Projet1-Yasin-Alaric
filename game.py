import pygame


class Game:
    def __init__(self):
        self.players = []
        self.level = 1
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.running = True
        self.background = pygame.image.load('image/background.png')
        self.level_music = {1: "sounds/background.wav"}

    def get_screen_size(self):
        return self.screen.get_size()

    def set_background(self, background):
        self.background = pygame.image.load(background)


# gérer victoire/défaite
# niveaux
