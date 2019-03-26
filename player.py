# player class
import node
import enemy
import Map
import numpy as np
import csv
import math


class Player:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.fede = 5
        self.stamina = 5
        self.map = Map.Map()
        self.roomID = self.map.allNode[self.x][self.y].roomID()
        self.pathfindingGraph = self.map.getAllNode()       # grafo pathfinding giocatore
        # with open('grafo.txt') as csv_file:
          #  csv_reader = csv.reader(csv_file, delimiter=',')
           # for row in csv_reader:
            #    for i in range(1,8):
             #       if row[i]!=-1:
              #          self.pathfindingGraph[row[0],15][np.floor_divide(row[0],15)].addNeighbour(self.pathfindingGraph[row[i]%15][np.floor_divide(row[i],15)])



    def position(self, x, y):
        self.x = x
        self.y = y

    def distanceTo(self, x, y):
        dist=math.sqrt(abs(x - self.x)**2 + abs(y - self.y)**2)
        print (dist)
        return int(dist)

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

