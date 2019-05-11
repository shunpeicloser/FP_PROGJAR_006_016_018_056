class Lobby:
    def __init__(self):
        self.id = None
        self.name = None
        self.player = []
        self.my_rect = None
        self.my_fill = None
    
    def createLobby(self,id):
        self.id = id;

    def setName(self,name):
        self.name = name;

    def joinLobby(self,username):
    	self.player.append(username)

    def createRect(self,my_rect):
    	self.my_rect = my_rect

    def creteFill(self,my_fill):
    	self.my_fill = my_fill

    def getFill(self):
    	return self.my_fill

    def getRect(self):
    	return self.my_rect

    def getId(self):
    	return self.id

    def getName(self):
    	return self.name

    def getNumPlayer(self):
    	return len(self.player)