import numpy as Np

def determinant(matrix):
        """
        :param data: [v1, ... ,vtaille]
        :param taille: 2, 3 :
        :return: integer D  * 100
        """
        # taille de la matrice carre' 2x2 or 3x3
        taille = len(matrix)

        if taille == 4:
            taille = 2
        else:
            taille = 3
        matrice = Np.array(matrix).reshape(taille, taille)
        determinant = Np.linalg.det(matrice)

        return determinant

def determinantMultiplier(matrix):
    """multiplication du determinant par 100"""
    return determinant(matrix) * 100