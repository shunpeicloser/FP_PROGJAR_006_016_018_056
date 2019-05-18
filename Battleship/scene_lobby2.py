import pygame
import utility
import player
import pickle

class LobbyScene:
    def __init__(self, sock, q):
        self.screen = None
        self.SCREEN_RESOLUTION = (640, 640)
        self.resource = {}
        self.lobby = []
        self.quit_rect = pygame.rect.Rect(40, 550, 150, 60)
        self.refresh_rect = pygame.rect.Rect(210, 550, 230, 60)
        self.hi_scores_rect = pygame.rect.Rect(450, 550, 180, 60)
        self.boxcolor = pygame.Color('black')

        # socket to server
        self.sock = sock

        # msg queue
        self.q = q

    def loadResource(self):
        try:
            self.resource.update({'background': (utility.Utility.loadimage('background.png'), (0, 0))})
            # self.resource.update({'logo': (utility.Utility.loadimage('logo.png'), (300, 120))})
            # self.resource.update({'loginbutton': (utility.Utility.loadimage('loginbutton.png'), (40, 480))})
            # self.resource.update({'quitbutton': (utility.Utility.loadimage('quitbutton.png'), (40, 550))})
        except:
            return False
        return True

    def drawScreen(self):
        for item in self.resource:
            self.screen.blit(self.resource[item][0], self.resource[item][1])
        pygame.draw.rect(self.screen, self.boxcolor, self.quit_rect, 8)
        pygame.draw.rect(self.screen, self.boxcolor, self.refresh_rect, 8)
        pygame.draw.rect(self.screen, self.boxcolor, self.hi_scores_rect, 8)
        quit_surface = pygame.font.Font(None, 64).render('QUIT', True, pygame.Color('white'))
        refresh_surface = pygame.font.Font(None, 64).render('REFRESH', True, pygame.Color('white'))
        hi_scores_surface = pygame.font.Font(None, 45).render('HI-SCORES', True, pygame.Color('white'))
        quit_fill = pygame.Surface((150, 60))
        refresh_fill = pygame.Surface((230, 60))
        hi_scores_fill = pygame.Surface((180, 60))
        quit_fill.fill((0, 0, 0))
        refresh_fill.fill((0, 0, 0))
        hi_scores_fill.fill((0, 0, 0))

        num_id = []
        player_name = []
        basey = 150
        z = 0
        hs_text = pygame.font.Font(None, 64).render('LOBBY', True, pygame.Color('white'))
        self.screen.blit(hs_text, (240,30))

        num_text = pygame.font.Font(None, 48).render('No', True, pygame.Color('white'))
        self.screen.blit(num_text, (70,100))
        roomname_text = pygame.font.Font(None, 48).render('Player Name', True, pygame.Color('white'))
        self.screen.blit(roomname_text, (250,100))

        for player in self.lobby:
            num_id.append(pygame.font.Font(None, 45).render(str(z+1), True, pygame.Color('white')))
            player_name.append(pygame.font.Font(None, 45).render(str(player.getname()), True, pygame.Color('white')))
            self.screen.blit(num_id[z], (70,basey))
            self.screen.blit(player_name[z], (250,basey))

            player.createRect(pygame.rect.Rect(65, basey, 490, 30))
            player.creteFill(pygame.Surface((490, 30)))
            if z%2:
                player.getFill().set_alpha(60)
            else:
                player.getFill().set_alpha(0)
            player.getFill().fill((0, 0, 0))
            self.screen.blit(player.getFill(), (player.getRect().x, player.getRect().y))

            basey = basey + 30
            z = z + 1

        self.screen.blit(quit_fill, (self.quit_rect.x, self.quit_rect.y))
        self.screen.blit(quit_surface, (self.quit_rect.x + 8, self.quit_rect.y + 8))
        self.screen.blit(refresh_fill, (self.refresh_rect.x, self.refresh_rect.y))
        self.screen.blit(refresh_surface, (self.refresh_rect.x + 8, self.refresh_rect.y + 8))
        self.screen.blit(hi_scores_fill, (self.hi_scores_rect.x, self.hi_scores_rect.y))
        self.screen.blit(hi_scores_surface, (self.hi_scores_rect.x + 8, self.hi_scores_rect.y + 8))

    def getPlayers(self):
        # send request players listing
        self.sock.send(b"PLST")
        self.lobby = self.sock.recv(1024)
        self.lobby = pickle.loads(self.lobby)

    def startScene(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.SCREEN_RESOLUTION)
        running = self.loadResource()
        mousepos = None
        self.getPlayers()
        while running:
            if not self.q.empty():
                command, opponent = self.q.get().split()
                if command == "INVD":
                    print("You are challenged by", opponent)
                    # self.sock.send(b"OK")
                    # print("Sending answer to", opponent)

                    # wait for ok from server
                    while self.q.empty():
                        pass
                    resp = self.q.get().split()[0]
                    if resp == "293":
                        print("Battle Started vs", opponent)
                        return 4

            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return 0

                mousepos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.quit_rect.collidepoint(mousepos):
                        return 0
                    if self.hi_scores_rect.collidepoint(mousepos):
                        # refresh event here
                        print("go to highscores")
                        return 5
                    if self.refresh_rect.collidepoint(mousepos):
                        # refresh event here
                        print("refreshed")
                        self.getPlayers()
                        continue
                    for player in self.lobby:
                            if player.getRect().collidepoint(mousepos):
                                print("i clicked", player.getname())
                                self.sock.send("INVT {}".format(player.getname()).encode())
                                resp = self.sock.recv(1024).decode().split()[0]
                                if resp == "293":
                                    print("Battle Started vs", player.getname())
                                    return 4
                                else:
                                    continue
                self.drawScreen()
                pygame.display.update()

    def run(self):
        ret = self.startScene()
        return ret
