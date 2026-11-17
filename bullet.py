import pygame

from coordinate import Coordinate

class Bullet:

     def __init__(self, x, y, weapon_damage=1):
         self.image = pygame.image.load('image/bullet.png')
         self.coordinate = Coordinate(x, y)
         self.speed = -50
         self.default_damage = 1
         # dégâts totaux = dégâts de la balle * dégâts de l'arme
         self.damage = self.default_damage * weapon_damage

     def update(self):
         self.coordinate.move(dy=self.speed)

     def draw(self, screen):
         screen.blit(self.image, self.coordinate.get_tuple())

     def get_rect(self):
         # le rectangle couvre aussi le chemin parcouru pendant cette frame (la balle va vite)
         x, y = self.coordinate.get_tuple()
         return pygame.Rect(x, y, self.image.get_width(), self.image.get_height() + abs(self.speed))

     def is_out_of_screen(self):
         return self.coordinate.getY() +self.image.get_height() < 0