# enemy class
from .player import Player
from .node import Node
from .Map import Map
import numpy as np


class Enemy:
    MapSize = 15
    portalSpawn = 4

    def __init__(self, playerx, playery):
        global MapSize
        self.nodes = [[Node() for j in range(MapSize)] for i in range(MapSize)]
        self.nodes = Map.getAllNode()
        self.p = Player(playerx, playery)
        self.tileX = np.random.random_integer(MapSize)
        self.tileY = np.random.random_integer(MapSize)
        while self.p.distanceTo(self.tileX, self.tileY) < 7:
            self.tileX = np.random.random_integer(MapSize)
            self.tileY = np.random.random_integer(MapSize)
        self.move1 = False

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


