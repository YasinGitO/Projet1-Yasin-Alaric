import pygame.image
import coordinate

class Player:

    def __init__(self, game, name):
        self.game = game
        self.image = pygame.image.load('image/player.png')
        self.coordinate = coordinate.Coordinate(370, 480)
        self.life = 3
        self.name = name

    def __str__(self):
        return f"Player {self.name} at {self.coordinate} with {self.life} lives"

    def __repr__(self):
        return f"Player {self.name} at {self.coordinate} with {self.life} lives"

    def __eq__(self, other):
        return self.name == other.name

    def move_left(self):
        self.coordinate.move(- 5)

    def move_right(self):
        self.coordinate.move(5)

    def setImage(self, image):
        self.image = pygame.image.load(image)

    def draw(self, screen):
        screen.blit(self.image, (self.coordinate.getX(), self.coordinate.getY()))



# playerImg = pygame.image.load('image/player.png')
# playerX = 370
# playerY = 480
# playerX_change = 0
# changer de png quand on a une arme différente
# arme par défaut (qui pourra changer)
# 3 vies
