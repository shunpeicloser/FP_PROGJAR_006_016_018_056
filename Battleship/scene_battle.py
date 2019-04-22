import pygame
import math

import player
import board
import battleship
import utility
import control

class BattleScene:
    def __init__(self, board, ctl):
        self.board = board
        self.SCREEN_RESOLUTION = (900, 640)
        self.screen = None
        self.ctl = ctl
        self.p1, self.p2 = None, None
        self.originobject = self.objectclassify()
        self.drawnobject = []

    def objectclassify(self):
        ret = {}
        ret.update({'battleship': {}})
        ret.update({'board': None})
        ret.update({'explosion': None})
        ret.update({'cross': None})
        return ret

    def loadresource(self):
        try:
            self.originobject.update({'board':  utility.Utility.loadimage("board.png")})
            # self.originobject['explosion'] = pygame.image.load("explosion.png")
            self.originobject.update({'cross': utility.Utility.loadimage("cross.png")})
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
        self.screen = pygame.display.set_mode(self.SCREEN_RESOLUTION)

        err = self.loadresource()

        if err == -1:
            print("Error loading resource")
            return False
        
        # initial resource to be drawn
        self.drawnobject.append(self.originobject['board'])
        for item in self.drawnobject:
            self.screen.blit(item, (0, 0))

        return True

    def startbattle(self, p1name, p2name):
        running = self.initgame(p1name, p2name)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                
                if event.type == pygame.MOUSEBUTTONUP:
                    tmp = self.ctl.getboardcoordinate(self.board, pygame.mouse.get_pos())
                    print(tmp)
                    print(self.ctl.getpixelcoordinate(self.board, tmp))


                pygame.display.update()

if __name__ == "__main__":
    board = board.Board(10)
    ctl = control.Control()
    bs = BattleScene(board, ctl)
    bs.startbattle("tj", "receh")