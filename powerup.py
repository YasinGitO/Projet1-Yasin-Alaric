import pygame

from arme import ARMES
from coordinate import Coordinate


class PowerUp:
    """
    Bonus qui tombe quand un ennemi meurt. Si le joueur le touche, il change d'arme.
    """

    def __init__(self, x, y, weapon_name):
        self.weapon_name = weapon_name
        self.coordinate = Coordinate(x, y)
        self.speed = 3
        # image simple dessinée par code : un cercle de la couleur de l'arme avec sa première lettre
        self.image = pygame.Surface((32, 32), pygame.SRCALPHA)
        pygame.draw.circle(self.image, ARMES[weapon_name]["color"], (16, 16), 16)
        lettre = pygame.font.Font(None, 28).render(weapon_name[0], True, (0, 0, 0))
        self.image.blit(lettre, ((32 - lettre.get_width()) // 2, (32 - lettre.get_height()) // 2))

    def update(self):
        self.coordinate.move(dy=self.speed)

    def draw(self, screen):
        screen.blit(self.image, self.coordinate.get_tuple())

    def get_rect(self):
        x, y = self.coordinate.get_tuple()
        return pygame.Rect(x, y, self.image.get_width(), self.image.get_height())

    def is_out_of_screen(self, screen_height):
        return self.coordinate.getY() > screen_height
