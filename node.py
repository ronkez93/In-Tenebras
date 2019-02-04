#node class
import numpy as np

class Node:

    def __init__(self, x, y, roomID):
        self.x=x
        self.y=y
        self.roomID=roomID
        self.neighbours = []
        self.portal = False

    def getID(self):
        return self.x+self.y*15

    def addNeighbour(self,n):
        self.neighbours.append(n)


