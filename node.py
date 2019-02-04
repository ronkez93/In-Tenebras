#node class
import numpy as np

class Node:

    def __init__(self, x=-1, y=-1, roomID=-1):
        self.x=x
        self.y=y
        self.roomID=roomID
        self.neighbours = []
        self.portal = False

    def getID(self):
        return self.x+self.y*15

    def addNeighbour(self,n):
        self.neighbours.append(n)

    def setxyID(self,x,y,ID):
        self.x=x
        self.y=y
        self.roomID=ID

    def getNeighbour(self):
        return self.neighbours

    def getx(self):
        return self.x

    def gety(self):
        return self.y



