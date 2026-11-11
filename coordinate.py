class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def getX(self):
        """
        Cette méthode retourne la valeur de x de l'objet.
        :return: Valeur de x de l'objet.
        """
        return self.x

    def getY(self):
        """
        Cette méthode retourne la valeur de y de l'objet.
        :return: Retourne la valeur de y de l'objet.
        """
        return self.y

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    def clamp_x(self, min_x, max_x):
        """
        Cette méthode va vérifier si x est entre min_x et max_x et si non, on lui affecte la valeur min_x ou max_x.
        :param min_x: Valeur minimale de x.
        :param max_x: Valeur maximale de x.
        """
        if self.x < min_x:
            self.x =  min_x
        elif self.x > max_x:
            self.x = max_x

    def move(self, dx=0, dy=0):
        """
        Cette méthode va ajouter dx à la position x de l'objet et dy à la position y de l'objet.
        Si aucune valeur n'est entrée pour une position elle ajoutera 0.
        :param dx: La valeur à ajouter à la position x de l'objet.
        :param dy: La valeur à ajouter à la position y de l'objet.
        """
        self.x += dx
        self.y += dy

    def get_tuple(self):
        """
        Retourne un tuple contenant les valeurs de x et de y de l'objet.
        :return: Retourne un tuple contenant les valeurs de x et de y de l'objet.
        """
        return (self.x, self.y)
