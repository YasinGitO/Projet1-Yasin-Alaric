import pygame

from ennemy import Ennemy, EnnemiTank
from player import Player


class Game:
    def __init__(self):
        self.players = []
        self.ennemies = []
        self.level = 1
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.running = True
        self.game_over = False
        self.font = pygame.font.Font(None, 80)
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
        self.ennemies = [e for e in self.ennemies if e.is_alive()]

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

    def draw_game_over(self):
        texte = self.font.render("GAME OVER", True, (255, 255, 255))
        x = (self.get_screen_size()[0] - texte.get_width()) // 2
        y = (self.get_screen_size()[1] - texte.get_height()) // 2
        self.screen.blit(texte, (x, y))



def main():
    game = Game()
    joueur = Player(game, "Alaric")
    game.players.append(joueur)
    game.ennemies.append(Ennemy(0, 100, 1, 3, 1, game))
    game.ennemies.append(EnnemiTank(300, 20, game))
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

            for ennemi in game.ennemies:
                ennemi.update()
            game.handle_collisions(joueur)
            game.handle_player_collisions(joueur)

        joueur.draw(game.screen)
        for ennemi in game.ennemies:
            ennemi.draw(game.screen)

        if game.game_over:
            game.draw_game_over()
        pygame.display.flip()

        clock.tick(60)



if __name__ == "__main__":
    main()


# gérer victoire/défaite
# niveaux
