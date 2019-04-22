import pygame
import utility
import copy

class Battleship:
    DEG0, DEG90, DEG180, DEG270 = 0, 90, 180, 270
    
    def __init__(self, name, imgfilename, angle=DEG0):
        self.name = name
        self.angle = angle
        self.visible = False
        self.image = utility.Utility.loadimage(imgfilename)
        self.size = self.setsize()

    def setangle(self, angle):
        self.angle = angle
    
    def rotateleft(self):
        self.angle -= self.DEG90
    
    def rotateright(self):
        self.angle += self.DEG90
    
    def getcopy(self):
        return copy.deepcopy(self)

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
    


