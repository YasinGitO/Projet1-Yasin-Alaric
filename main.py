import pygame
from game import Game
from player import Player

FPS = 60

def main():
    game = Game()
    joueur = Player(game, "Alaric")
    game.players.append(joueur)
    game.spawn_ennemy()
    clock = pygame.time.Clock()
    while game.running:
        game.screen.fill((0, 0, 0))
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

        clock.tick(FPS)


if __name__ == "__main__":
    main()