class Player:
    def __init__(self, name):
        self.name = name
        self.ingame = False
        self.my_rect = None
        self.my_fill = None
    
    def getname(self):
        return self.name

    def is_ingame(self):
        return self.ingame

    def goPlay(self):
        self.ingame = True

    def createRect(self,my_rect):
        self.my_rect = my_rect

    def creteFill(self,my_fill):
        self.my_fill = my_fill

    def getFill(self):
        return self.my_fill

    def getRect(self):
        return self.my_rect