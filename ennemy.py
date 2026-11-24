import pygame

from entity import Entity

class Ennemy(Entity):
    def __init__(self, x, y, hp=1, speed=3, damage=1, game=None, points=1):
        super().__init__(x, y, hp, speed)
        self.damage = damage
        self.points = points  # points gagnés par le joueur quand l'ennemi est tué
        self.image = pygame.image.load('image/enemy.png')
        self.game = game

    def update(self):
        min_x = 0
        max_x = self.game.get_screen_size()[0] - self.image.get_width()
        self.coordinate.move(dx=self.speed)
        if self.coordinate.getX() > max_x:
            self.coordinate.clamp_x(min_x, max_x)
            self.speed = -self.speed
            self.coordinate.setY(self.coordinate.getY() + 75)
        if self.coordinate.getX() < 0:
            self.coordinate.clamp_x(min_x, max_x)
            self.speed = abs(self.speed)
            self.coordinate.setY(self.coordinate.getY() + 75)


    def draw(self, screen):
        screen.blit(self.image, self.coordinate.get_tuple())

    def is_out_of_screen(self):
        return self.coordinate.getX() + self.image.get_width() < 0
    def get_damage(self):
        return self.damage
    def get_points(self):
        return self.points
    def get_speed(self):
        return self.speed
    def get_hp(self):
        return self.hp
    def get_rect(self):
        x, y = self.coordinate.get_tuple()
        return pygame.Rect(x, y, self.image.get_width(), self.image.get_height())

    def is_hit_by(self, bullet):
        """
        Retourne True si la balle touche cet ennemi.
        """
        return self.get_rect().colliderect(bullet.get_rect())

    def touch_ennemy(self, player):
        if player.get_player_width_y() > self.image.get_height():
            player.take_damage(self.damage)



class EnnemiTank(Ennemy):
    """
    Nouveau type de monstre : plus lent, plus gros en points de vie (3 balles pour le tuer)
    mais il fait plus de dégâts.
    """
    def __init__(self, x, y, game=None):
        super().__init__(x, y, hp=3, speed=2, damage=2, game=game, points=2)
        self.image = pygame.image.load('image/ufo.png')
        self.image = pygame.transform.scale(self.image, (64, 64))


# certains ennemis auront plus de vie que d'autres et apporteront plus de points lors de son kill
# variables
# enemyImg = []  TODO : trouver des nouvelles images pour les ennemis
# enemyX = []
# enemyY = []
# enemyX_change = []
# enemyY_change = []
# num_of_enemies = 6
# points de vie ex. vie 1 = 1 balle pour tuer, 2 vie = 2 balle pour tuer etc
# points qu'il apporte point de vie * 10
# dégats qu'il apporte'
# boss de jeux