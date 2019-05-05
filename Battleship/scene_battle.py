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
        self.occupied = []
        self.drawnbattleship = []

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
            for model in battleship.Battleship.SHIP_TYPE:
                self.originobject['battleship'].update(
                    {model: battleship.Battleship(model, str(model+".png"))})
        except:
            return -1
        return 0

    def mousehover(self, boardpos):
        if self.ctl.mousestatus == self.ctl.NO_ACTION:
            pass
        elif self.ctl.mousestatus == self.ctl.IS_PLACINGSHIP and not self.illegalplacement(
                                                boardpos,
                                                self.originobject['battleship'][self.ctl.selectedbattleship].angle,
                                                self.originobject['battleship'][self.ctl.selectedbattleship].size
                                            ):
            self.drawbattleshipshadow(boardpos, self.ctl.getpixelcoordinate(self.board, boardpos))

    def battleshipoutofboard(self, boardpos):
        tmp = self.originobject['battleship'][self.ctl.selectedbattleship]
        if tmp.angle in [tmp.DEG0, tmp.DEG180] and boardpos[1] - tmp.size < 0:
            return True
        if tmp.angle in [tmp.DEG90, tmp.DEG270] and ord(boardpos[0]) - ord('A') + 1 - tmp.size < 0:
            return True
        return False

    def illegalplacement(self, coor, angle, size):
        if coor == None:
            return True

        deltax, deltay = 0, 0
        if angle == battleship.Battleship.DEG0 or angle == battleship.Battleship.DEG180:
            deltax, deltay = 0, -1
        elif angle == battleship.Battleship.DEG90 or angle == battleship.Battleship.DEG270:
            deltax, deltay = -1, 0
        
        defendant = []

        for i in range(0, size):
            defendant.append(str(chr(ord(coor[0]) + i * deltax) + chr(ord('0') + coor[1] + i * deltay)))
        for d in defendant:
            if d in self.occupied:
                return True
        
        return False

    def drawbattleshipshadow(self, boardpos, pixelpos):
        if pixelpos != None and not self.battleshipoutofboard(boardpos):
            tmp = self.originobject['battleship'][self.ctl.selectedbattleship]
            x = pixelpos[0] - tmp.size * self.board.SQUARE_WIDTH 
            y = pixelpos[1] - self.board.SQUARE_WIDTH
            if tmp.angle in [tmp.DEG0, tmp.DEG180]:
                x += (tmp.size - 1) * self.board.SQUARE_WIDTH
                y -= (tmp.size - 1) * self.board.SQUARE_WIDTH

            self.screen.blit(self.originobject['battleship'][self.ctl.selectedbattleship].image , (x, y))

    def occupytile(self, coor, angle, size):
        tmp = [0, 0]
        deltax, deltay = 0, 0
        if angle == battleship.Battleship.DEG0 or angle == battleship.Battleship.DEG180:
            deltax, deltay = 0, -1
        elif angle == battleship.Battleship.DEG90 or angle == battleship.Battleship.DEG270:
            deltax, deltay = -1, 0
        for i in range(0, size):
            tmp[0] = chr((ord(coor[0]) + i * deltax))
            tmp[1] = chr(ord('0') + coor[1] + i * deltay)
            self.occupied.append(str(tmp[0] + tmp[1]))
        
        return

    def drawboarditems(self):
        for battleship_img, pos in self.drawnbattleship:
            self.screen.blit(battleship_img, pos)

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
        
        self.screen.blit(self.originobject['board'], (0, 0))

        return True

    def startbattle(self, p1name, p2name):
        ncarrier, nbattleship, ncruiser, nsubmarine, ndestroyer = 1, 2, 1, 2, 4
        idxship = 0
        self.ctl.selectedbattleship = battleship.Battleship.SHIP_TYPE[0]
        running = self.initgame(p1name, p2name)
        mousepos = None
        while running:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.originobject['board'], (0, 0))
            self.drawboarditems()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

                mousepos = pygame.mouse.get_pos()

                if self.ctl.mousestatus == self.ctl.IS_PLACINGSHIP:
                    if event.type == pygame.MOUSEBUTTONUP:
                        tm = self.ctl.getboardcoordinate(self.board, mousepos)
                        tmp = self.ctl.getpixelcoordinate(self.board, tm)
                        bs = self.originobject['battleship'][self.ctl.selectedbattleship]
                        if not self.illegalplacement(tm, bs.angle, bs.size):
                            originpos = [0, 0]
                            if bs.angle in [bs.DEG0, bs.DEG180]:
                                originpos[0] = tmp[0] - self.board.SQUARE_WIDTH
                                originpos[1] = tmp[1] - self.board.SQUARE_WIDTH * bs.size
                            if bs.angle in [bs.DEG90, bs.DEG270]:
                                originpos[0] = tmp[0] - self.board.SQUARE_WIDTH * bs.size
                                originpos[1] = tmp[1] - self.board.SQUARE_WIDTH
                            
                            self.occupytile(tm, bs.angle, bs.size)
                            self.drawnbattleship.append((bs.image.copy(), tuple(originpos)))
                            idxship += 1

                    if event.type == pygame.KEYUP:
                        tmp = self.originobject['battleship'][self.ctl.selectedbattleship]
                        if event.key == pygame.K_LEFT:
                            tmp.transformbattleshipangle(tmp.DEG270)
                        elif event.key == pygame.K_RIGHT:
                            tmp.transformbattleshipangle(tmp.DEG90)
                        self.originobject['battleship'][self.ctl.selectedbattleship] = tmp

                    if idxship == 1:
                        self.ctl.selectedbattleship = battleship.Battleship.SHIP_TYPE[1]
                    elif idxship == 3:
                        self.ctl.selectedbattleship = battleship.Battleship.SHIP_TYPE[2]
                    elif idxship == 4:
                        self.ctl.selectedbattleship = battleship.Battleship.SHIP_TYPE[3]
                    elif idxship == 6:
                        self.ctl.selectedbattleship = battleship.Battleship.SHIP_TYPE[4]
                    elif idxship == 10:
                        self.ctl.mousestatus = self.ctl.IS_WAITFOROPPONENT

                    self.mousehover(self.ctl.getboardcoordinate(self.board, mousepos))

                pygame.display.update()

if __name__ == "__main__":
    board = board.Board(10)
    ctl = control.Control()
    bs = BattleScene(board, ctl)

    # DEBUG
    ctl.mousestatus = ctl.IS_PLACINGSHIP

    bs.startbattle("tj", "receh")