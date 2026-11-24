import pygame
from pygame import mixer
from bullet import Bullet

# Les différentes armes du jeu : nom -> dégâts, délai entre 2 tirs (en ms), couleur du power-up,
# munitions (None = infini : après ses munitions, l'arme est remplacée par le Pistolet)
ARMES = {
    "Pistolet": {"damage": 1, "cooldown": 400, "color": (255, 255, 255), "ammo": None},
    "Mitraillette": {"damage": 1, "cooldown": 150, "color": (255, 200, 0), "ammo": 40},
    "Canon": {"damage": 3, "cooldown": 800, "color": (255, 70, 70), "ammo": 10},
}


def creer_arme(nom):
    """
    Crée une arme à partir de son nom (voir le dictionnaire ARMES).
    """
    infos = ARMES[nom]
    return Arme(nom, infos["damage"], infos["cooldown"], ammo=infos["ammo"])


class Arme:

    def __init__(self, type, damage=1, cooldown=100000000000, zone=1, ammo=None):
        self.type = type
        self.damage = damage
        self.zone = zone
        self.image = None
        self.last_shot = 0
        self.cooldown = cooldown
        self.ammo = ammo  # None = munitions infinies
        self.shooted_bullets = []
        self.bulletSound = mixer.Sound("sounds/laser.wav")


    def is_empty(self):
        return self.ammo is not None and self.ammo <= 0

    def shoot(self, center_x, start_y):
        """
        Tire une balle centrée sur center_x. Retourne True si une balle est partie.
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot < self.cooldown or self.is_empty():
            return False

        self.last_shot = current_time
        bullet = Bullet(0, start_y, self.damage)
        bullet.coordinate.setX(center_x - bullet.image.get_width() // 2)
        self.shooted_bullets.append(bullet)
        if self.ammo is not None:
            self.ammo -= 1
        self.bulletSound.play()
        return True

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