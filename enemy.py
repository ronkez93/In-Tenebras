#enemy class
import player

class enemy:

    MapSize=15

    def __init__(self, x, y, playerx, playery):
        self.tileX = x
        self.tileY = y
        self.playerTarget = player.player(playerx, playery)
        self.move1 = False

    def updatePlayerPos(self, playerx, playery):
        self.playerTarget.position(playerx,playery)
        self.move1 = True
