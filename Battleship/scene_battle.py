import pygame
import math

import player
import board
import battleship
import utility
import control

import pickle

class BattleScene:

    def __init__(self, board, ctl, sock, q, player):
        self.board = board
        self.is_attackboard = False
        self.SCREEN_RESOLUTION = (900, 640)
        self.screen = None
        self.ctl = ctl
        self.p1, self.p2 = None, None
        self.originobject = self.objectclassify()
        self.occupied = []
        self.drawnbattleship = []
        self.attackboard = []
        self.attackboard_hit = []
        self.defboard = []
        self.defboard_hit = []


        # socket to server
        self.sock = sock

        # queue for listener
        self.q = q

        # player detail
        self.player = player

        # hardcoded, males bikin class
        pygame.font.init()
        self.myboard_button_rect = pygame.Rect(650, 10, 240, 40)
        self.myboard_button_surface = pygame.font.Font(None, 48).render('My Board', True, pygame.Color('black'))

        self.enemyboard_button_rect = pygame.Rect(650, 60, 240, 40)
        self.enemyboard_button_surface = pygame.font.Font(None, 48).render('Attack Board', True, pygame.Color('black'))

        self.boxcolor = pygame.Color('black')
        self.buttonfill = pygame.Surface((self.myboard_button_rect.width, self.myboard_button_rect.height))
        self.buttonfill.fill((220, 220, 220))

    # init container of image or object
    def objectclassify(self):
        ret = {}
        ret.update({'battleship': {}})
        ret.update({'board': None})
        ret.update({'explosion': None})
        ret.update({'cross': None})
        ret.update({'green_cross': None})
        return ret

    # load resource before the start of game
    def loadresource(self):
        try:
            self.originobject.update({'board':  utility.Utility.loadimage("board.png")})
            # self.originobject['explosion'] = pygame.image.load("explosion.png")
            self.originobject.update({'cross': utility.Utility.loadimage("cross.png")})
            self.originobject.update({'green_cross': utility.Utility.loadimage("green_cross.png")})
            for model in battleship.Battleship.SHIP_TYPE:
                self.originobject['battleship'].update(
                    {model: battleship.Battleship(model, str(model+".png"))})
        except:
            return -1
        return 0

    # event when mouse hover
    def mousehover(self, boardpos):
        if self.ctl.mousestatus == self.ctl.NO_ACTION:
            pass
        # case when player is placing battleship
        elif self.ctl.mousestatus == self.ctl.IS_PLACINGSHIP and not self.illegalplacement(
                                                boardpos,
                                                self.originobject['battleship'][self.ctl.selectedbattleship].angle,
                                                self.originobject['battleship'][self.ctl.selectedbattleship].size
                                            ):
            # draw hovering image of battleship
            self.drawbattleshipshadow(boardpos, self.ctl.getpixelcoordinate(self.board, boardpos))

    # check if battleship is out of board
    def battleshipoutofboard(self, boardpos):
        tmp = self.originobject['battleship'][self.ctl.selectedbattleship]
        if tmp.angle in [tmp.DEG0, tmp.DEG180] and boardpos[1] - tmp.size < 0:
            return True
        if tmp.angle in [tmp.DEG90, tmp.DEG270] and ord(boardpos[0]) - ord('A') + 1 - tmp.size < 0:
            return True
        return False

    # check if the placement of battleship in the way of other battleship
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

    def illegalattack(self, boardcoor):
        if not boardcoor:
            return False
        print("boardcoor is", boardcoor)
        alpha = int(40 + 56*(ord(boardcoor[0])-65))
        number = int(40 + 56*(1-boardcoor[1]))
        hit_coor = (alpha, number)
        print("hit_coor is", hit_coor)
        if hit_coor in self.attackboard or hit_coor in self.attackboard_hit:
            return True
        return False

    # draw the image of battleship shadow
    def drawbattleshipshadow(self, boardpos, pixelpos):
        if pixelpos != None and not self.battleshipoutofboard(boardpos):
            tmp = self.originobject['battleship'][self.ctl.selectedbattleship]
            x = pixelpos[0] - tmp.size * self.board.SQUARE_WIDTH 
            y = pixelpos[1] - self.board.SQUARE_WIDTH
            if tmp.angle in [tmp.DEG0, tmp.DEG180]:
                x += (tmp.size - 1) * self.board.SQUARE_WIDTH
                y -= (tmp.size - 1) * self.board.SQUARE_WIDTH

            self.screen.blit(self.originobject['battleship'][self.ctl.selectedbattleship].image , (x, y))

    # save occupied tiles
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

    # draw items placed on board
    def drawboarditems(self):
        pygame.draw.rect(self.screen, self.boxcolor, self.myboard_button_rect, 8)
        pygame.draw.rect(self.screen, self.boxcolor, self.enemyboard_button_rect, 8)

        self.screen.blit(self.buttonfill, (self.myboard_button_rect.x, self.myboard_button_rect.y))
        self.screen.blit(self.buttonfill, (self.enemyboard_button_rect.x, self.enemyboard_button_rect.y))

        self.screen.blit(self.myboard_button_surface, (self.myboard_button_rect.x + 8, self.myboard_button_rect.y + 8))
        self.screen.blit(self.enemyboard_button_surface, (self.enemyboard_button_rect.x + 8, self.enemyboard_button_rect.y + 8))

        if not self.is_attackboard:
            for battleship_img, pos in self.drawnbattleship:
                self.screen.blit(battleship_img, pos)
            for attacked in self.defboard:
                self.screen.blit(self.originobject['cross'], attacked)
        else:
            for attacking in self.attackboard:
                self.screen.blit(self.originobject['cross'], attacking)
            for attacking in self.attackboard_hit:
                self.screen.blit(self.originobject['green_cross'], attacking)

    def placebattleship(self, mousepos):
        tm = self.ctl.getboardcoordinate(self.board, mousepos)
        tmp = self.ctl.getpixelcoordinate(self.board, tm)
        bs = self.originobject['battleship'][self.ctl.selectedbattleship]
        if not (self.illegalplacement(tm, bs.angle, bs.size) or self.battleshipoutofboard(tm)):
            originpos = [0, 0]
            if bs.angle in [bs.DEG0, bs.DEG180]:
                originpos[0] = tmp[0] - self.board.SQUARE_WIDTH
                originpos[1] = tmp[1] - self.board.SQUARE_WIDTH * bs.size
            if bs.angle in [bs.DEG90, bs.DEG270]:
                originpos[0] = tmp[0] - self.board.SQUARE_WIDTH * bs.size
                originpos[1] = tmp[1] - self.board.SQUARE_WIDTH
            
            self.occupytile(tm, bs.angle, bs.size)
            self.drawnbattleship.append((bs.image.copy(), tuple(originpos)))
            return 1
        return 0

    def isplacementfinished(self, idxship):
        if idxship == 1:
            # debug: is_attackphase; Production: is_waitingopponent
            return None, self.ctl.IS_ATTACKPHASE
        if idxship == 0:
            return battleship.Battleship.SHIP_TYPE[0], self.ctl.IS_PLACINGSHIP
        elif idxship <= 1:
            return battleship.Battleship.SHIP_TYPE[1], self.ctl.IS_PLACINGSHIP
        elif idxship <= 2:
            return battleship.Battleship.SHIP_TYPE[2], self.ctl.IS_PLACINGSHIP
        elif idxship <= 3:
            return battleship.Battleship.SHIP_TYPE[3], self.ctl.IS_PLACINGSHIP
        elif idxship <= 5:
            return battleship.Battleship.SHIP_TYPE[4], self.ctl.IS_PLACINGSHIP

    # initialization of game
    def initgame(self, p1name, p2name):
        self.p1 = player.Player(p1name)
        self.p2 = player.Player(p2name)
        self.ctl.mousestatus = self.ctl.IS_PLACINGSHIP

        pygame.init()
        title = "[" +self.player.name + "] in Battle => x[" + self.p1.getname() + " vs. " + self.p2.getname() + "]x"
        # pygame.display.set_caption(str(
        #                             self.p1.getname() +
        #                             " VS " +
        #                             self.p2.getname()
        #                             ))
        pygame.display.set_caption(title)
        self.screen = pygame.display.set_mode(self.SCREEN_RESOLUTION)

        err = self.loadresource()

        if err == -1:
            print("Error loading resource")
            return False
        
        self.screen.blit(self.originobject['board'], (0, 0))

        return True

    # start the battle scene
    def startbattle(self, p1name, p2name):
        # ncarrier, nbattleship, ncruiser, nsubmarine, ndestroyer = 1, 2, 1, 2, 4
        idxship = 0
        self.ctl.selectedbattleship = battleship.Battleship.SHIP_TYPE[0]
        self.ctl.mousestatus = self.ctl.IS_PLACINGSHIP
        running = self.initgame(p1name, p2name)
        waiting_turn = True
        opponent_is_ready = False
        can_hit = False
        mousepos = None
        while running:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.originobject['board'], (0, 0))
            self.drawboarditems()
            for event in pygame.event.get():
                if not self.q.empty():
                    msg = self.q.get().split()
                    print(msg)
                    if msg[0] == "WAIT":
                        waiting_turn = True
                        can_hit = False
                        print("I have to wait")
                    if msg[0] == "TURN":
                        waiting_turn = False
                        can_hit = True
                        print("Its my turn")
                    if msg[0] == "ATTD":
                        self.is_attackboard = False
                        attack_coor = (int(msg[1]), int(msg[2]))
                        print("i am attacked", attack_coor)
                        self.defboard.append(attack_coor)
                    if msg[0] == "HIT":
                        attack_coor = (int(msg[1]), int(msg[2]))
                        print("i successfully hit", attack_coor)
                        self.attackboard_hit.append(attack_coor)
                    if msg[0] == "MISS":
                        attack_coor = (int(msg[1]), int(msg[2]))
                        print("i missed a shot at", attack_coor)
                        self.attackboard.append(attack_coor)
                    if msg[0] == "ORDY":
                        opponent_is_ready = True
                        print("Opponent is now ready")
                        # return 6
                    if msg[0] == "WIN":
                        print("You win!")
                        self.clearboard()
                        return 6
                    if msg[0] == "LOSE":
                        print("You lose!")
                        self.clearboard()
                        self.sock.send(b"ILOSE")
                        return 6
                    # if msg[0] == "END":
                    #     return 6
                if event.type == pygame.QUIT:
                    running = False
                    return 0

                mousepos = pygame.mouse.get_pos()

                # case player in 'attack' phase
                if self.ctl.mousestatus == self.ctl.IS_ATTACKPHASE and event.type == pygame.MOUSEBUTTONUP:
                    if self.myboard_button_rect.collidepoint(mousepos):
                        self.is_attackboard = False
                    if self.enemyboard_button_rect.collidepoint(mousepos):
                        self.is_attackboard = True
                    
                    if self.is_attackboard:
                        if not self.illegalattack(self.ctl.getboardcoordinate(self.board, mousepos)):
                            tmp = self.ctl.getboardcoordinate(self.board, mousepos)
                            if tmp == None or waiting_turn or not opponent_is_ready:
                                continue
                            tmp = list(tmp)
                            tmp[0] = chr(ord(tmp[0])-1)
                            tmp[1] -= 1
                            tmp = self.ctl.getpixelcoordinate(self.board, tuple(tmp))
                            print("i attacked", tmp)
                            if can_hit:
                                can_hit = False
                                self.sock.send("ATT {} {}".format(*tmp).encode())
                            # self.attackboard.append(tuple(tmp)) # add cross to coordinate in attack board
                            # self.defboard.append(tuple(tmp)) # add cross to coordinate in my board

                # case player in 'placing battleship' phase
                if self.ctl.mousestatus == self.ctl.IS_PLACINGSHIP:
                    if event.type == pygame.MOUSEBUTTONUP:
                        idxship += self.placebattleship(mousepos)
                        
                    if event.type == pygame.KEYUP:
                        tmp = self.originobject['battleship'][self.ctl.selectedbattleship]
                        if event.key == pygame.K_LEFT:
                            tmp.transformbattleshipangle(tmp.DEG270)
                        elif event.key == pygame.K_RIGHT:
                            tmp.transformbattleshipangle(tmp.DEG90)
                        self.originobject['battleship'][self.ctl.selectedbattleship] = tmp

                    # case to change the battleship in placing phase
                    self.ctl.selectedbattleship, self.ctl.mousestatus = self.isplacementfinished(idxship)
                    if not self.ctl.selectedbattleship:
                        self.sock.send(b"OCUP " + pickle.dumps(self.occupied))

                    self.mousehover(self.ctl.getboardcoordinate(self.board, mousepos))

                pygame.display.update()

    def clearboard(self):
        self.attackboard = []
        self.attackboard_hit = []
        self.defboard = []
        self.defboard_hit = []
        self.occupied = []
        self.drawnbattleship = []
        self.is_attackboard = False

    def run(self):
        self.ctl = control.Control()
        self.board = board.Board(10)
        p1 = ''
        p2 = ''
        bsid = ''
        as_player = ''
        msg = self.sock.recv(1024).decode().split()
        if msg[0] == "BATL":
            p1 = msg[1]
            p2 = msg[2]
            bsid = msg[3]
            as_player = msg[4]


        # register to session
        self.sock.send("BTLS {}".format(bsid).encode())
        if self.sock.recv(1024).decode() == "GOAWAY":
            return 6

        ret = self.startbattle(p1, p2)
        return ret