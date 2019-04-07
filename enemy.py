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
        self.maxMovement = 3
        self.remainingMovement = self.maxMovement
        self.turnToSpawn = self.portalSpawn
        spawnX = np.random.random_integers(self.MapSize-1)
        spawnY = np.random.random_integers(self.MapSize-1)
        while self.nodes[spawnY][spawnX].roomID == 12:
            spawnX = np.random.random_integers(self.MapSize-1)
            spawnY = np.random.random_integers(self.MapSize-1)
        print("portale in")
        print(spawnX)
        print(spawnY)
        self.nodes[spawnY][spawnX].setPortal(True)
        self.spawnManifestazione()
        self.spawnManifestazione()
        self.maxEvent = True
        self.turnToSpawnMan = self.turniSpawnManifestazione

    # aggiorna la posizione del giocatore sulla base delle coordinate date DA GESTIRE MANIFESTAZIONI E CHIUSURA PORTALI
    def updatePlayerPos(self, playerx, playery):
        self.playerTarget.y=playery
        self.playerTarget.x=playerx
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
        print("target")
        print(self.playerTarget.x)
        print(self.playerTarget.y)
        source = self.nodes[self.tileY][self.tileX]
        target = self.nodes[y][x]
        dist = [[0 for j in range(15)] for i in range(15)]
        prev = [[node.Node() for j in range(15)] for i in range(15)]
        unvisited = []
        for n in range(len(self.nodes)): #righe
            for m in range(len(self.nodes[0])): #colonne
                if self.nodes[n][m] != source:
                    dist[n][m] = float('inf')
                    prev[n][m] = None
                unvisited.append(self.nodes[n][m])
        while len(unvisited) > 0:
            u = None
            for n in unvisited:
                if u is None or dist[n.y][n.x] < dist[u.y][u.x]:
                    u = n
            if u.x == target.x and u.y == target.y:
                break
            unvisited.remove(u)
            for n in u.neighbours:
                alt = dist[u.y][u.x] + self.map.costToEnter(u.x, u.y, n.x, n.y)
                if alt < dist[n.y][n.x]:
                    dist[n.y][n.x] = alt
                    prev[n.y][n.x] = self.nodes[u.y][u.x]
        #print(prev)
        if prev[target.x][target.y] is None:
            return
        cpath = []
        curr = target
        while curr is not None:
            cpath.append(curr)
            curr = prev[curr.y][curr.x]
        cpath.reverse()
        for n in cpath:
            print("percorso:")
            print(n.x)
            print(n.y)
        self.currentpath = cpath

    # chiede se la cella alle coordinate passate e anche la cella di un portale
    def onPortal(self, x, y):
        return self.nodes[y][x].portal

    # funzione per distruggere un portale nella casella di coordinate passate
    def destroyPortal(self, x, y):
        self.nodes[y][x].setPortal(False)
        for n in range(len(self.nodes)):
            for m in range(len(self.nodes[0])):
                if self.nodes[n][m].portal and n != y and m !=x:
                    self.nodes[n][m].neighbours.remove(self.nodes[y][x])
                    self.nodes[y][x].neighbours.remove(self.nodes[n][m])
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
            if self.currentpath is not None:
                if len(self.currentpath) is not None:  # se non sono sul giocatore il nemico si muove finche puo
                    self.remainingMovement -= self.map.costToEnter(self.tileX, self.tileY, self.currentpath[1].x,
                                                                   self.currentpath[1].y)
                    self.tileX = self.currentpath[1].x
                    self.tileY = self.currentpath[1].y
                    self.currentpath.pop(0)
                    if len(self.currentpath) == 1:  # se dopo essersi mosso sono arrivato al giocatore cancello il percorso
                        player.fede-=1
                        self.currentpath = None
                        self.remainingMovement=0
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
                                if not self.nodes[spawnY][
                                    spawnX].portal and not self.nodes[spawnY][spawnX].manifestazione:  # se le coordinate non hanno gia un portale, controllo se non ce n'e un altro nella stanza
                                    stanza = self.nodes[spawnY][spawnX].roomID
                                    spawned = True
                                    for n in range(len(self.nodes)):
                                        for m in range(len(self.nodes[0])):
                                            if self.nodes[n][m].portal and self.nodes[n][m].roomID == stanza:
                                             spawned = False
                                    if spawned:  # dopo che trovo delle coordinate valide aggiorno i vicini creando collegamenti con gli altri portali
                                        self.nodes[spawnY][spawnX].setPortal(True)
                                        for n in range(len(self.nodes)):
                                            for m in range(len(self.nodes[0])):
                                                if self.nodes[n][m].portal:  # controllo di non aggiungere un collegamento tra nodo a se stesso
                                                    if m != spawnX or n != spawnY:
                                                        self.nodes[n][m].addNeighbour(self.nodes[spawnY][spawnX])
                                                        self.nodes[spawnY][spawnX].addNeighbour(self.nodes[n][m])
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
            for n in range(len(self.nodes)):
                for m in range(len(self.nodes[0])):
                    if self.nodes[n][m].manifestazione:
                        if self.nodes[n][m].roomID==self.nodes[spawnY][spawnX].roomID:
                            spawn=False
                    if self.playerTarget.distanceTo(spawnX,spawnY)<7:
                        spawn = False
                    if self.nodes[spawnX][spawnY].portal:
                        spawn=False
        self.nodes[spawnY][spawnX].manifestazione=True
        print("manifestazione in")
        print(spawnX)
        print(spawnY)

    def getNodes(self):
        return self.nodes

    def risolviManifestazione(self, x, y):
        self.nodes[y][x].manifestazione=False
        self.maxEvent = False
        self.turnToSpawnMan = self.turniSpawnManifestazione

    def countportal(self):
        count=0
        for n in range(len(self.nodes)):
            for m in range(len(self.nodes[0])):
                if self.nodes[n][m].portal:
                    count +=1
        print("portali aperti:")
        print(count)
        return count
