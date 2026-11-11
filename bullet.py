import pygame

from coordinate import Coordinate

class Bullet:

     def __init__(self, x, y):
         self.image = pygame.image.load('image/bullet.png')
         self.coordinate = Coordinate(x, y)
         self.speed = -50
         self.default_damage = 1
         self.damage = self.default_damage

     def update(self):
         self.coordinate.move(dy=self.speed)

     def draw(self, screen):
         screen.blit(self.image, self.coordinate.get_tuple())

     def is_out_of_screen(self):
         return self.coordinate.getY() +self.image.get_height() < 0