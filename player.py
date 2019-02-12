# player class
from .node import Node
from .enemy import Enemy
import numpy as np
import csv


class Player:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.fede = 5
        self.stamina = 5
        self.pathfindingGraph = np.array([[Node() for j in range(15)] for i in range(15)])


    def position(self, x, y):
        self.x = x
        self.y = y

    def distanceTo(self, x, y):
        return int(np.sqrt((x - self.x) ^ 2 + (y - self.y) ^ 2))

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    def decrementaFede(self):
        self.fede -= 1

    def decrementaStamina(self):
        self.stamina -=1

