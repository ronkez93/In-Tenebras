# enemy class
import player
import node
import Map
import numpy as np
import math


class Enemy:

    def __init__(self):  # inizializzazione: posizione nemico, posizione giocatore, spawn 2 eventi e portale
        self.MapSize = 15
        self.portalSpawn = 4
        self.turniSpawnManifestazione = 4
        global turniSpawnManifestazione
        self.map = Map.Map()
        self.nodes = self.map.getAllNode()
        self.playerTarget = player.Player()
        self.playerTarget.x=7
        self.playerTarget.y=14
        self.tileX = np.random.random_integers(self.MapSize-1)
        self.tileY = np.random.random_integers(self.MapSize-1)

        print(self.tileX)
        print(self.tileY)
        while self.playerTarget.distanceTo(self.tileX, self.tileY) < 7:
            print(self.playerTarget.distanceTo(self.tileX, self.tileY))
            print(self.tileX)
            print(self.tileY)
            self.tileX = np.random.random_integers(self.MapSize-1)
            self.tileY = np.random.random_integers(self.MapSize-1)
        self.move1 = False
        self.GeneratePathfindingGraph()
        self.currentpath = []
        self.maxMovement = 2
        self.remainingMovement = self.maxMovement
        self.turnToSpawn = self.portalSpawn
        spawnX = np.random.random_integers(self.MapSize-1)
        spawnY = np.random.random_integers(self.MapSize-1)
        while self.nodes[spawnX][spawnY].roomID == 12:
            spawnX = np.random.random_integers(self.MapSize-1)
            spawnY = np.random.random_integers(self.MapSize-1)
        self.nodes[spawnX][spawnY].setPortal(True)
        self.spawnManifestazione()
        self.spawnManifestazione()
        self.maxEvent = True
        self.turnToSpawnMan = self.turniSpawnManifestazione

    # aggiorna la posizione del giocatore sulla base delle coordinate date DA GESTIRE MANIFESTAZIONI E CHIUSURA PORTALI
    def updatePlayerPos(self, playerx, playery):
        self.playerTarget.position(playerx, playery)
        self.move1 = True

    # crea una struttura basandosi sui nodi vicini
    def GeneratePathfindingGraph(self):
        # Now that all the nodes exist, calculate their neighbours
        for x in range(self.MapSize):
            for y in range(self.MapSize):
                if x > 0:
                    self.nodes[x][y].addNeighbour(self.nodes[x - 1][y])
                    if y > 0:
                        self.nodes[x][y].addNeighbour(self.nodes[x - 1][y - 1])
                    if y < self.MapSize - 1:
                        self.nodes[x][y].addNeighbour(self.nodes[x - 1][y + 1])
                if x < self.MapSize - 1:
                    self.nodes[x][y].addNeighbour(self.nodes[x + 1][y])
                    if y > 0:
                        self.nodes[x][y].addNeighbour(self.nodes[x + 1][y - 1])
                    if y < self.MapSize - 1:
                        self.nodes[x][y].addNeighbour(self.nodes[x + 1][y + 1])
                if y > 0:
                    self.nodes[x][y].addNeighbour(self.nodes[x][y - 1])
                if y < self.MapSize - 1:
                    self.nodes[x][y].addNeighbour(self.nodes[x][y + 1])

    # cambia lo stato del nemico cosi che puo muoversi
    def setMove(self):
        self.move1 = True

    # crea un lista di nodi currentpath contenente tutte le celle per arrivare alla posizione passata
    def generatepathto(self, x, y):
        source = self.nodes[self.tileY][self.tileX]
        target = self.nodes[y][x]
        dist = {node: float('inf') for node in self.nodes}
        prev = {node: None for node in self.nodes}
        dist[source]=0
        vertices=self.nodes.copy()
        unvisited = []
        for n in range(len(self.nodes)):
            for m in range(len(self.nodes[0])):
                unvisited.append(self.nodes[n][m])
        while len(unvisited) > 0:
            u = None
            for n in unvisited:
                if u is None or dist[n] < dist[u]:
                    u = n
            if u == target:
                break
            unvisited.remove(u)
            for n in u.neighbours:
                alt = dist[u.y][u.x] + self.map.costToEnter(u.x, u.y, n.x, n.y)
                if alt < dist[n.y][n.x]:
                    dist[n.y][n.x] = alt
                    prev[self.nodes[n.y][n.x]] = u
        print(prev)
        if prev[target] is None:
            return
        cpath = []
        curr = target
        while curr is not None:
            cpath.append(curr)
            curr = prev[curr]
        cpath.reverse()
        self.currentpath = cpath

    # chiede se la cella alle coordinate passate e anche la cella di un portale
    def onPortal(self, x, y):
        return self.nodes[y][x].portal

    # funzione per distruggere un portale nella casella di coordinate passate
    def destroyPortal(self, x, y):
        self.nodes[x][y].setPortal(False)
        for n in range(len(self.nodes)):
            for m in range(len(self.nodes[0])):
                if self.nodes[n][m].portal and n != x and m !=y:
                    self.nodes[n][m].neighbours.remove(self.nodes[x][y])
                    self.nodes[x][y].neighbours.remove(self.nodes[n][m])
        #for n in self.nodes:
        #    if n.getx != x and n.gety != y and n.getPortal:
        #        self.nodes[n.getx][n.gety].neighbours.remove(self.nodes[x][y])
        #        self.nodes[x][y].neighbours.remove(self.nodes[n.getx][n.gety])

    # cambia il mannimo numero di movimenti a disposizione del nemico sulla base dei bpm del giocatore
    def setMaxMovement(self, MM):
        self.maxMovement = MM

    # turno del nemico
    def update(self):
        self.generatepathto(self.playerTarget.x, self.playerTarget.y)
        while self.move1:  # finche tocca al nemico creo il percorso fino al giocatore
            print("generato percorso lungo:")
            print(len(self.currentpath))
            if len(self.currentpath) is not None:  # se non sono sul giocatore il nemico si muove finche puo
                self.remainingMovement -= self.map.costToEnter(self.tileX, self.tileY, self.currentpath[1].x,
                                                               self.currentpath[1].y)
                self.tileX = self.currentpath[1].x
                self.tileY = self.currentpath[1].y
                self.currentpath.pop(0)
                if len(self.currentpath) == 1:  # se dopo essersi mosso sono arrivato al giocatore cancello il percorso
                    self.currentpath = None
                if self.remainingMovement <= 0:  # se ho finito i movimenti a disposizione resetto le variabili di movimento e vedo se devo spawnare un portale
                    self.move1 = False
                    self.remainingMovement = self.maxMovement
                    self.turnToSpawn -= 1
                    if self.turnToSpawn == 0:  # se e il momento di spawnare un portale
                        self.turnToSpawn = self.portalSpawn
                        spawned = False
                        while not spawned:  # finche non viene spawnato genero coordinate e verifico che non siano in una stanza con gia un portale
                            spawnX = np.random.random_integers(self.MapSize-1)
                            spawnY = np.random.random_integers(self.MapSize-1)
                            if not self.nodes[spawnX][
                                spawnY].getPortal():  # se le coordinate non hanno gia un portale, controllo se non ce n'e un altro nella stanza
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
                if self.tileX == self.playerTarget.getX() and self.tileY == self.playerTarget.getY():  # se ho raggiunto il giocatore, il nemico non si muove piu e si teletrasporta ad almeno sei caselle di distanza. il ciocatore perde fede
                    self.remainingMovement = 0
                    distance = False
                    while not distance:
                        newX = np.random.random_integers(self.MapSize-1)
                        newY = np.random.random_integers(self.MapSize-1)
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
        return self.tileY + self.tileX * self.MapSize

    def spawnManifestazione(self):
        spawn = False
        spawnX = -1
        spawnY = -1
        while not spawn:
            spawn = True
            spawnX = np.random.random_integers(self.MapSize-1)
            spawnY = np.random.random_integers(self.MapSize-1)
            print("dimensioni")
            print(len(self.nodes))
            print(len(self.nodes[0]))
            for n in range(len(self.nodes)):
                for m in range(len(self.nodes[0])):
                    if self.nodes[n][m].manifestazione:
                        if self.nodes[n][m].roomID==self.nodes[spawnX][spawnY].roomID:
                            spawn=False
                    if self.playerTarget.distanceTo(spawnX,spawnY)<7:
                        spawn = False
                    if self.nodes[spawnX][spawnY].portal:
                        spawn=False
        self.nodes[spawnX][spawnY].manifestazione=True

    def getNodes(self):
        return self.nodes

    def risolviManifestazione(self, x, y):
        self.nodes[x][y].manifestazione=False
        self.maxEvent = False
        self.turnToSpawnMan = self.turniSpawnManifestazione

