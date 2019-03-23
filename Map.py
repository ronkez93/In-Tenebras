import node
import numpy as np


class Map:

    def __init__(self):
        self.allNode = np.array([[node.Node() for j in range(15)] for i in range(15)], np.dtype(node.Node()))
        self.matrix = np.array([[1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4],
                               [1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4],
                               [2, 2, 2, 2, 2, 3, 3, 5, 5, 4, 4, 4, 4, 4, 4],
                               [2, 2, 2, 2, 2, 3, 3, 5, 5, 4, 4, 4, 4, 4, 4],
                               [2, 2, 2, 2, 2, 6, 6, 5, 5, 4, 4, 4, 4, 4, 4],
                               [2, 2, 2, 2, 2, 6, 6, 5, 5, 4, 4, 4, 4, 4, 4],
                               [7, 7, 7, 7, 7, 6, 6, 8, 8, 8, 8, 9, 9, 9, 9],
                               [7, 7, 7, 7, 7, 6, 6, 8, 8, 8, 8, 9, 9, 9, 9],
                               [7, 7, 7, 7, 7, 6, 6, 8, 8, 8, 8, 10, 10, 10, 10],
                               [7, 7, 7, 7, 7, 6, 6, 8, 8, 8, 8, 10, 10, 10, 10],
                               [11, 11, 11, 11, 11, 12, 12, 12, 12, 8, 8, 10, 10, 10, 10],
                               [11, 11, 11, 11, 11, 12, 12, 12, 12, 13, 13, 10, 10, 10, 10],
                               [14, 14, 15, 15, 15, 12, 12, 12, 12, 13, 13, 16, 16, 16, 16],
                               [14, 14, 15, 15, 15, 12, 12, 12, 12, 13, 13, 16, 16, 16, 16],
                               [14, 14, 15, 15, 15, 12, 12, 12, 12, 13, 13, 16, 16, 16, 16]])
        for i in range(15):  # righe
            for j in range(15):  # colonne
                self.allNode[i][j].setxyID(i, j, self.matrix[i][j])
                # = Node(i,j,self.matrix[i,j])

    def getAllNode(self):
        return self.allNode

    def costToEnter(self, x1, y1, x2, y2):
        if x1 != x2 and y1 != y2:
            return 1.001
        else:
            return 1.000
