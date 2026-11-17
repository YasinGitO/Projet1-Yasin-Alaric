import pygame
from pygame import mixer
from bullet import Bullet

class Arme:

    def __init__(self, type, damage=1, cooldown=100000000000, zone=1):
        self.type = type
        self.damage = damage
        self.zone = zone
        self.image = None
        self.last_shot = 0
        self.cooldown = cooldown
        self.shooted_bullets = []
        self.bulletSound = mixer.Sound("sounds/laser.wav")


    def shoot(self, start_x, start_y):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot < self.cooldown:
            return

        self.last_shot = current_time
        self.shooted_bullets.append(Bullet(start_x, start_y, self.damage))
        self.bulletSound.play()

    def update(self):
        for bullet in self.shooted_bullets[:]:
            bullet.update()
            if bullet.is_out_of_screen():
                self.shooted_bullets.remove(bullet)

    def draw(self, screen):
        for bullet in self.shooted_bullets:
            bullet.draw(screen)


#   changer type de munitions
#   tirer sur l'arme pour l'avoir
#   arme a dégat de zone
#   arme a cadence * 2
#   arme de mêlée (dégats * 10)
#   pistolet a dégats * 3
#   png arme
#   bullet