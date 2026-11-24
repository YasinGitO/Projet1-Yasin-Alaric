import pygame.image
import coordinate
from arme import creer_arme
from entity import Entity


class Player(Entity):

    def __init__(self, game, name):
        super().__init__(x=370, y=480, hp=3, speed=5)
        self.image = pygame.image.load('image/Main Ship - Base - Full health.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))

        self.game = game
        self.name = name
        self.score = 0
        self.weapon = creer_arme("Pistolet")
        self.direction_x = 0


    def __str__(self):
        return f"Player {self.name} at {self.coordinate} with {self.hp} lives and score {self.score}"

    def __repr__(self):
        return f"Player {self.name} at {self.coordinate} with {self.hp} lives and score {self.score}"

    def __eq__(self, other):
        if not isinstance(other, Player):
            return False
        return self.name == other.name and self.coordinate == other.coordinate and self.hp == other.hp

    def set_image(self, image):
        """
        Cette méthode va changer l'image du joueur.
        :param image: L'image avec laquelle on veut changer l'image du joueur.
        """
        self.image = pygame.image.load(image)

    def draw(self, screen):
        """
        Cette méthode va afficher l'image du joueur et de l'arme sur la fenêtre de jeu aux coordonées du joueur.
        :param screen: Surface de jeu.
        """
        super().draw(screen)
        self.weapon.draw(screen)

    def get_player_width(self):
        """
        Cette méthode retourne la largeur de l'image du joueur (taille sur l'axe x).
        :return: Largeur de l'image du joueur.
        """
        return self.image.get_width()

    def get_screen_width_x(self):
        """
        Cette méthode retourne la taille de l'écran sur l'axe x.
        :return: taille de l'axe x de la fenêtre de jeu.
        """
        return self.game.get_screen_size()[0]

    def get_rect(self):
        """
        Cette méthode retourne le rectangle occupé par le joueur (pour les collisions).
        :return: pygame.Rect du joueur.
        """
        x, y = self.coordinate.get_tuple()
        return pygame.Rect(x, y, self.image.get_width(), self.image.get_height())

    def get_player_width_y(self):
        return self.image.get_height()

    def update(self):
        """
        Cette méthode permet de déplacer le jouer sur l'axe x selon la direction et la vitesse du joueur
        grace a coordinate.move() et permet de vérifier si on est dans les limites de la fenêtre de jeu
        grace a coordinate.clamp_x().
        """
        min_x = 0
        max_x = self.get_screen_width_x() - self.get_player_width()
        self.coordinate.move(dx=self.direction_x)
        self.coordinate.clamp_x(min_x, max_x)
        self.weapon.update()

    def str_score(self) -> str:
        """
        Cette méthode va retourner le score du joueur en str.
        :return: Le score du joueur en string.
        """
        return f"Score: {self.score}"

    def get_score(self)  -> int :
        """
        Cette méthode va retourner le score du joueur.
        :return: Score du joueur en int.
        """
        return self.score

    def add_score(self, score):
        self.score += score

    def change_weapon(self, nouvelle_arme):
        """
        Cette méthode remplace l'arme du joueur. Les balles déjà tirées continuent leur chemin.
        :param nouvelle_arme: La nouvelle arme (instance de Arme).
        """
        nouvelle_arme.shooted_bullets = self.weapon.shooted_bullets
        self.weapon = nouvelle_arme

    def shoot(self):
        """
        Cette méthode va utiliser l'arme du joueur pour tirer un projectile depuis le milieu du vaisseau.
        Quand l'arme n'a plus de munitions, on revient au Pistolet.
        """
        centre_x = self.get_x() + self.get_player_width() // 2
        self.weapon.shoot(centre_x, self.get_y())
        if self.weapon.is_empty():
            self.change_weapon(creer_arme("Pistolet"))

    def handle_input(self):
        """
        Cette méthode va gerer les déplacements du joueur an ajoutant ou soustrayant la vitesse à la direction.
        Elle va aussi gerer le tir de l'arme.
        A chaque itération la direction va être remise à 0.
        """
        keys = pygame.key.get_pressed()
        self.direction_x = 0

        if keys[pygame.K_LEFT]:
            self.direction_x = -self.speed
        if keys[pygame.K_RIGHT]:
            self.direction_x = self.speed
        if keys[pygame.K_SPACE]:
            self.shoot()

# playerImg = pygame.image.load('image/player.png')
# playerX = 370
# playerY = 480
# playerX_change = 0
# changer de png quand on a une arme différente
# arme par défaut (qui pourra changer)
# 3 vies
