from coordinate import Coordinate


class Entity:

    def __init__(self, x, y, hp, speed):
        self.hp = hp
        self.speed = speed
        self.coordinate = Coordinate(x, y)
        self.image = None

    def is_alive(self):
        """
        Cette méthode va nous retourner un booléen pour vérifier que notre objet est toujours vivant (hp > 0).
        :return: True si il est encore en vie et False sinon.
        """
        return self.hp > 0

    def get_coordinate(self):
        """
        Cette méthode va nous retouner les coordonées de l'objet sous la forme d'une instance de la classe Coordinate.
        :return: Retourne les coordonnées sous une instance de la classe Coordinate.
        """
        return self.coordinate

    def get_x(self):
        """
        Cette méthode va nous retourner la valeur de x de l'objet.
        :return: Retourne la valeur de x de l'objet.
        """
        return self.coordinate.getX()

    def get_y(self):
        """
        Cette méthode va nous retourner la valeur de y de l'objet.
        :return: Retourne la valeur de y de l'objet.
        """
        return self.coordinate.getY()

    def get_hp(self):
        """
        Cette méthode va nous retourner la valeur de la vie de l'objet.
        :return: Retourne la valeur de la vie de l'objet.
        """
        return self.hp

    def set_hp(self, hp):
        """
        Cette méthode va nous permettre de modifier la vie de l'objet.
        :param hp: Vie avec laquelle on veut modifier la vie de l'objet.
        """
        self.hp = hp

    def draw(self, screen):
        """
        Cette méthode va dessiner l'image choisie aux coordonnées de l'objet.
        :param screen: Surface de jeu.
        """
        screen.blit(self.image, self.coordinate.get_tuple())

    def take_damage(self, damage):
        """
        Cette méthode va retirer la valeur de damage de la vie de l'objet.
        :param damage: Les dégats qu'on veut affliger à l'objet.
        """
        self.hp -= damage
