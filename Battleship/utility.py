import pygame

class Utility:
    @staticmethod
    def loadimage(filename):
        return pygame.image.load(str("image/"+filename))