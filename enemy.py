# enemy class
from .player import Player
from .node import Node
from .Map import Map
import numpy as np
import math


class Enemy:
    MapSize = 15
    portalSpawn = 4
    turniSpawnManifestazione = 4

    def __init__(self, playerx,
                 playery):  # inizializzazione: posizione nemico, posizione giocatore, spawn 2 eventi e portale
        global MapSize
        global portalSpawn
        global turniSpawnManifestazione
        self.map = Map()
        self.nodes = self.map.getAllNode()
        self.playerTarget = Player(playerx, playery)
        self.tileX = np.random.random_integers(MapSize)
        self.tileY = np.random.random_integers(MapSize)
        while self.playerTarget.distanceTo(self.tileX, self.tileY) < 7:
            self.tileX = np.random.random_integers(MapSize)
            self.tileY = np.random.random_integers(MapSize)
        self.move1 = False
        self.GeneratePathfindingGraph()
        self.currentpath = []
        self.maxMovement = 2
        self.remainingMovement = self.maxMovement
        self.turnToSpawn = portalSpawn
        spawnX = np.random.random_integers(MapSize)
        spawnY = np.random.random_integers(MapSize)
        while self.nodes[spawnX][spawnY].getRoom() == 12:
            spawnX = np.random.random_integers(MapSize)
            spawnY = np.random.random_integers(MapSize)
        self.nodes[spawnX][spawnY].setPortal(True)
        self.spawnManifestazione()
        self.spawnManifestazione()
        self.maxEvent = True
        self.turnToSpawnMan = turniSpawnManifestazione

    # aggiorna la posizione del giocatore sulla base delle coordinate date DA GESTIRE MANIFESTAZIONI E CHIUSURA PORTALI
    def updatePlayerPos(self, playerx, playery):
        self.playerTarget.position(playerx, playery)
        self.move1 = True

    # crea una struttura basandosi sui nodi vicini
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

    # cambia lo stato del nemico così che può muoversi
    def setMove(self):
        self.move1 = True

    # crea un lista di nodi currentpath contenente tutte le celle per arrivare alla posizione passata
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

    # chiede se la cella alle coordinate passate è anche la cella di un portale
    def onPortal(self, x, y):
        return self.nodes[x][y].getPortal()

    # funzione per distruggere un portale nella casella di coordinate passate
    def destroyPortal(self, x, y):
        self.nodes[x][y].setPortal(False)
        for n in self.nodes:
            if n.getx != x and n.gety != y and n.getPortal:
                self.nodes[n.getx][n.gety].neighbours.remove(self.nodes[x][y])
                self.nodes[x][y].neighbours.remove(self.nodes[n.getx][n.gety])

    # cambia il mannimo numero di movimenti a disposizione del nemico sulla base dei bpm del giocatore
    def setMaxMovement(self, MM):
        self.maxMovement = MM

    # turno del nemico
    def update(self):
        while self.move1:  # finchè tocca al nemico creo il percorso fino al giocatore
            self.generatepathto(self.playerTarget.getX(), self.playerTarget.getY())
            if self.currentpath is not None:  # se non sono sul giocatore il nemico si muove finchè può
                self.remainingMovement -= self.map.costToEnter(self.tileX, self.tileY, self.currentpath[1].getx(),
                                                               self.currentpath[1].gety())
                self.tileX = self.currentpath[1].getx()
                self.tileY = self.currentpath[1].gety()
                self.currentpath.pop(0)
                if len(self.currentpath) == 1:  # se dopo essersi mosso sono arrivato al giocatore cancello il percorso
                    self.currentpath = None
                if self.remainingMovement <= 0:  # se ho finito i movimenti a disposizione resetto le variabili di movimento e vedo se devo spawnare un portale
                    self.move1 = False
                    self.remainingMovement = self.maxMovement
                    self.turnToSpawn -= 1
                    if self.turnToSpawn == 0:  # se è il momento di spawnare un portale
                        self.turnToSpawn = self.portalSpawn
                        spawned = False
                        while not spawned:  # finchè non viene spawnato genero coordinate e verifico che non siano in una stanza con già un portale
                            spawnX = np.random.random_integers(self.MapSize)
                            spawnY = np.random.random_integers(self.MapSize)
                            if not self.nodes[spawnX][
                                spawnY].getPortal():  # se le coordinate non hanno già un portale, controllo se non ce n'è un altro nella stanza
                                stanza = self.nodes[spawnX][spawnY].getRoom()
                                spawned = True
                                for n in self.nodes:
                                    if n.getRoom() == stanza:
                                        spawned = False
                                if spawned:  # dopo che trovo delle coordinate valide aggiorno i vicini creando collegamenti con gli altri portali
                                    self.nodes[spawnX][spawnY].setPortal(True)
                                    for n in self.nodes:
                                        if n.getPortal():  # controllo di non aggiungere un collegamento tra nodo a se stesso
                                            if n.getx() != spawnX or n.gety() != spawnY:
                                                self.nodes[n.getx()][n.gety()].addNeighbour(self.nodes[spawnX][spawnY])
                                                self.nodes[spawnX][spawnY].addNeighbour(self.nodes[n.getx()][n.gety()])
                    if not self.maxEvent:  #
                        self.turnToSpawnMan -= 1
                        if self.turnToSpawnMan == 0:
                            self.spawnManifestazione()
                            self.maxEvent = True
                if self.tileX == self.playerTarget.getX() and self.tileY == self.playerTarget.getY():  # se ho raggiunto il giocatore, il nemico non si muove più e si teletrasporta ad almeno sei caselle di distanza. il ciocatore perde fede
                    self.remainingMovement = 0
                    distance = False
                    while not distance:
                        newX = np.random.random_integers(self.MapSize)
                        newY = np.random.random_integers(self.MapSize)
                        if np.abs(self.tileX - newX) >= 6 or np.abs(self.tileY - newY):
                            distance = True
                            self.tileX = newX
                            self.tileY = newY
                            self.playerTarget.decrementaFede()

    def getX(self):
        return self.tileX

    def getY(self):
        return self.tileY

    def getPos(self):
        return self.tileY * self.MapSize + self.tileX

    def spawnManifestazione(self):
        spawn = False
        spawnX = -1
        spawnY = -1
        while not spawn:
            spawn = True
            spawnX = np.random.random_integers(MapSize)
            spawnY = np.random.random_integers(MapSize)
            for n in self.nodes:
                if n.getRoom() == self.nodes[spawnX][spawnY] or self.nodes[spawnX][spawnY].getRoom() == \
                        self.nodes[self.playerTarget.getX()][self.playerTarget.getY()].getRoom():
                    spawn = False
        self.nodes[spawnX][spawnY].setManifestazione(True)

    def getNodes(self):
        return self.nodes

    def risolviManifestazione(self, x, y):
        self.nodes[x][y].setManifestazione(False)
        self.maxEvent = False
        self.turnToSpawnMan = self.turniSpawnManifestazione
