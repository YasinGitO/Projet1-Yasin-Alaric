import pygame

from ennemy import Ennemy
from player import Player


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



def main():
    game = Game()
    joueur = Player(game, "Alaric")
    game.players.append(joueur)
    ennemi = Ennemy(0, 100, 1, 3, 1, game)
    clock = pygame.time.Clock()
    while game.running:
        # RGB = Red, Green, Blue
        game.screen.fill((0, 0, 0))
        # Background Image
        game.screen.blit(game.background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False

        joueur.handle_input()
        joueur.update()
        joueur.draw(game.screen)


        ennemi.update()
        ennemi.draw(game.screen)
        pygame.display.flip()

        clock.tick(60)



if __name__ == "__main__":
    main()


# gérer victoire/défaite
# niveaux
