import pygame
import utility
import copy

class Battleship:
    DEG0, DEG90, DEG180, DEG270 = 0, 90, 180, 270
    SHIP_TYPE = ["carrier", "battleship", "cruiser", "submarine", "destroyer"]
    def __init__(self, name, imgfilename, angle=DEG0):
        self.name = name
        self.angle = 90
        self.visible = False
        self.image = utility.Utility.loadimage(imgfilename)
        self.size = self.setsize()

    def transformbattleshipangle(self, angle):
        tmp = (self.angle + angle) % 360
        self.image = pygame.transform.rotate(self.image, -self.angle)
        self.image = pygame.transform.rotate(self.image, tmp)
        self.angle = tmp
        return self
    
    def getcopy(self):
        return copy.deepcopy(self)
    
    def getimage(self):
        return copy.deepcopy(self.image)

    def setsize(self):
        if self.name == "carrier":
            return 5
        elif self.name == "battleship":
            return 4
        elif self.name == "cruiser":
            return 3
        elif self.name == "submarine":
            return 3
        elif self.name == "destroyer":
            return 2
        else:
            return -1
    


