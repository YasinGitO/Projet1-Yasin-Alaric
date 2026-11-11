from entity import Entity


class Ennemy(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 1, 3)
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