#node class


class node:

    def __init__(self, x, y):
        self.x=x
        self.y=y
        self.neighbours = []
        self.portal = False

    def getID(self):
        return self.x+self.y*15
