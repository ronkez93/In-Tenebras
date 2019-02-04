# enemy class
from .player import Player
from .node import Node
from .Map import Map
import numpy as np
import math


class Enemy:
    MapSize = 15
    portalSpawn = 4

    def __init__(self, playerx, playery):
        global MapSize
        self.map = Map()
        self.nodes = self.map.getAllNode()
        self.playerTarget = Player(playerx, playery)
        self.tileX = np.random.random_integer(MapSize)
        self.tileY = np.random.random_integer(MapSize)
        while self.playerTarget.distanceTo(self.tileX, self.tileY) < 7:
            self.tileX = np.random.random_integer(MapSize)
            self.tileY = np.random.random_integer(MapSize)
        self.move1 = False
        self.GeneratePathfindingGraph()
        self.currentpath = []
        self.remainingMovement = 4

    def updatePlayerPos(self, playerx, playery):
        self.playerTarget.position(playerx, playery)
        self.move1 = True

    def GeneratePathfindingGraph(self):
        # Now that all the nodes exist, calculate their neighbours
        for x in range(MapSize):
            for y in range(MapSize):
                if x > 0:
                    self.nodes[x][y].addNeighbour(self.nodes[x - 1][y])
                    if y > 0:
                        self.nodes[x][y].addNeighbour(self.nodes[x - 1][y - 1])
                    if y < MapSize - 1:
                        self.nodes[x][y].addNeighbour(self.nodes[x - 1][y + 1])
                if x < MapSize - 1:
                    self.nodes[x][y].addNeighbour(self.nodes[x + 1][y])
                    if y > 0:
                        self.nodes[x][y].addNeighbour(self.nodes[x + 1][y - 1])
                    if y < MapSize - 1:
                        self.nodes[x][y].addNeighbour(self.nodes[x + 1][y + 1])
                if y > 0:
                    self.nodes[x][y].addNeighbour(self.nodes[x][y - 1])
                if y < MapSize - 1:
                    self.nodes[x][y].addNeighbour(self.nodes[x][y + 1])

    def setMove(self):
        self.move1 = True

    def generatepathto(self, x, y):
        source = self.nodes[self.tileX][self.tileY]
        target = self.nodes[x][y]
        nodes = set(self.nodes)
        dist = {source: 0}
        prev = {source: None}
        unvisited = []
        for node in nodes:
            if node != source:
                dist[node] = math.inf
                prev[node] = None
            unvisited.append(node)
        while len(unvisited) > 0:
            u = None
            for n in unvisited:
                if u is None or dist[n] < dist[u]:
                    u = n
            if u == target:
                break
            unvisited.remove(u)
            for n in u.getNeighbour():
                alt = dist[u] + self.map.costToEnter(u.getx, u.gety, n.getx, n.gety)
                if alt < dist[n]:
                    dist[n] = alt
                    prev[n] = u
        if prev[target] is None:
            return
        cpath = []
        curr = target
        while curr is not None:
            cpath.append(curr)
            curr = prev[curr]
        cpath.reverse()
        self.currentpath = cpath

    def onPortal(self,x,y):
        return self.nodes[x][y].getPortal()

    def destroyPortal(self,x,y):
        self.nodes[x][y].setPortal(False)
        for n in self.nodes:
            if n.getx != x and n.gety != y and n.getPortal:
                self.nodes[n.getx][n.gety].neighbours.remove(self.nodes[x][y])
                self.nodes[x][y].neighbours.remove(self.nodes[n.getx][n.gety])