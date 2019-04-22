import pygame
import math

import player
import battleship

class BattleScene:
    def __init__(self):
        self.BOARD_SIZE = 10
        self.SCREEN_RESOLUTION = (900, 640)
        self.p1, self.p2 = None, None
        self.originobject = self.objectclassiy()
        self.drawnobject = []

    def objectclassiy(self):
        ret = {}
        ret.update({'battleship': {}})
        ret.update({'board': None})
        ret.update({'explosion': None})
        ret.update({'cross': None})
        return ret

    def loadresource(self):
        try:
            self.originobject['board'] = pygame.image.load("board.png")
            self.originobject['explosion'] = pygame.image.load("explosion.png")
            self.originobject['cross'] = pygame.image.load("cross.png")
            self.originobject['battleship'].update(
                {'carrier': battleship.Battleship('carrier', "carrier.png")})
            self.originobject['battleship'].update(
                {'battleship': battleship.Battleship('battleship', "battleship.png")})
            self.originobject['battleship'].update(
                {'cruiser': battleship.Battleship('cruiser', "cruiser.png")})
            self.originobject['battleship'].update(
                {'submarine': battleship.Battleship('submarine', "submarine.png")})
            self.originobject['battleship'].update(
                {'destroyer': battleship.Battleship('destroyer', "destroyer.png")})
        except:
            return -1
        return 0

    def initgame(self, p1name, p2name):
        self.p1 = player.Player(p1name)
        self.p2 = player.Player(p2name)

        pygame.init()
        pygame.display.set_caption(str(
                                    self.p1.getname() +
                                    " VS " +
                                    self.p2.getname()
                                    ))
        pygame.display.set_mode(self.SCREEN_RESOLUTION)

        err = self.loadresource()

        if err == -1:
            print("Error loading resource")
            return False
        


        return True

    def startbattle(self, p1name, p2name):
        running = self.initgame(p1name, p2name)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                


                pygame.display.update()

if __name__ == "__main__":
    bs = BattleScene()
    bs.startbattle("tj", "receh")