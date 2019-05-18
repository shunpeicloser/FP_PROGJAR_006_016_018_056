import pygame
import utility

class LoginScene:
    def __init__(self, sock, challenge_sock):
        self.screen = None
        self.SCREEN_RESOLUTION = (640, 640)
        self.resource = {}
        self.username = ''
        self.password = ''
        self.username_rect = pygame.rect.Rect(150, 250, 350, 80)
        self.password_rect = pygame.rect.Rect(150, 350, 350, 80)
        self.login_rect = pygame.rect.Rect(40, 480, 260, 60)
        self.quit_rect = pygame.rect.Rect(40, 550, 260, 60)
        self.register_rect = pygame.rect.Rect(320, 550, 260, 60)
        self.boxcolor = pygame.Color('black')

        # socket to server
        self.sock = sock
        self.challenge_sock = challenge_sock
    
    def loadresource(self):
        try:
            self.resource.update({'background': (utility.Utility.loadimage('background.png'), (0, 0))})
            self.resource.update({'logo': (utility.Utility.loadimage('logo.png'), (300, 120))})
            # self.resource.update({'loginbutton': (utility.Utility.loadimage('loginbutton.png'), (40, 480))})
            # self.resource.update({'quitbutton': (utility.Utility.loadimage('quitbutton.png'), (40, 550))})
        except:
            return False
        return True
    
    def drawscreen(self):
        for item in self.resource:
            self.screen.blit(self.resource[item][0], self.resource[item][1])

        pygame.draw.rect(self.screen, self.boxcolor, self.username_rect, 8)
        pygame.draw.rect(self.screen, self.boxcolor, self.password_rect, 8)
        pygame.draw.rect(self.screen, self.boxcolor, self.login_rect, 8)
        pygame.draw.rect(self.screen, self.boxcolor, self.quit_rect, 8)
        pygame.draw.rect(self.screen, self.boxcolor, self.register_rect, 8)

        username_surface = pygame.font.Font(None, 64).render(self.username, True, pygame.Color('black'))
        password_surface = pygame.font.Font(None, 64).render(self.password, True, pygame.Color('black'))
        login_surface = pygame.font.Font(None, 64).render('LOGIN', True, pygame.Color('white'))
        quit_surface = pygame.font.Font(None, 64).render('QUIT', True, pygame.Color('white'))
        register_surface = pygame.font.Font(None, 64).render('REGISTER', True, pygame.Color('white'))
        
        username_fill = pygame.Surface((350, 80))
        password_fill = pygame.Surface((350, 80))
        login_fill = pygame.Surface((260, 60))
        quit_fill = pygame.Surface((260, 60))
        register_fill = pygame.Surface((260, 60))

        username_fill.fill((255, 255, 255))
        password_fill.fill((255, 255, 255))
        login_fill.fill((0, 0, 0))
        quit_fill.fill((0, 0, 0))
        register_fill.fill((0, 0, 0))
        
        self.screen.blit(username_fill, (self.username_rect.x, self.username_rect.y))
        self.screen.blit(password_fill, (self.password_rect.x, self.password_rect.y))
        self.screen.blit(login_fill, (self.login_rect.x, self.login_rect.y))
        self.screen.blit(quit_fill, (self.quit_rect.x, self.quit_rect.y))
        self.screen.blit(register_fill, (self.register_rect.x, self.register_rect.y))

        self.screen.blit(username_surface, (self.username_rect.x + 8, self.username_rect.y + 8))
        self.screen.blit(password_surface, (self.password_rect.x + 8, self.password_rect.y + 8))
        self.screen.blit(login_surface, (self.login_rect.x + 8, self.login_rect.y + 8))
        self.screen.blit(quit_surface, (self.quit_rect.x + 8, self.quit_rect.y + 8))
        self.screen.blit(register_surface, (self.register_rect.x + 8, self.register_rect.y + 8))

    def startscene(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.SCREEN_RESOLUTION)
        running = self.loadresource()
        mousepos = None
        is_username, is_password = False, False
        while running:
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return 0

                mousepos = pygame.mouse.get_pos()

                if event.type == pygame.MOUSEBUTTONUP:
                    if self.username_rect.collidepoint(mousepos):
                        is_username = True
                        is_password = False
                    elif self.password_rect.collidepoint(mousepos):
                        is_username = False
                        is_password = True
                    else:
                        is_username, is_password = False, False

                    if self.register_rect.collidepoint(mousepos):
                        return 2
                    elif self.login_rect.collidepoint(mousepos):
                        print(self.username, self.password)
                        # attempt to login
                        self.sock.send("LUSR {}".format(self.username).encode())
                        resp = self.sock.recv(1024).decode().split()[0]
                        # get response code
                        if resp != "201":
                            print("invalid login bos")
                            self.username = ""
                            self.password = ""
                            continue

                        # continue with password
                        self.sock.send("LPAS {}".format(self.password).encode())
                        resp = self.sock.recv(1024).decode().split()[0]
                        if resp != "290":
                            print("invalid login bos")
                            self.username = ""
                            self.password = ""
                            continue

                        # initiating challenge socket
                        self.challenge_sock.connect(("127.0.0.1", 9001))
                        self.challenge_sock.send("CSCK {}".format(self.username).encode())
                        resp = self.challenge_sock.recv(1024)
                        print(resp.decode())


                        print("login success. to the lobby we go!")
                        return 6
                    elif self.quit_rect.collidepoint(mousepos):
                        return 0

                if is_username:
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_BACKSPACE:
                            self.username = self.username[:-1]
                            # self.username.pop()
                        else:
                            self.username += chr(event.key)
                elif is_password:
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_BACKSPACE:
                            self.password = self.password[:-1]
                            # self.password.pop()
                        else:
                            self.password += chr(event.key)
                self.drawscreen()
                pygame.display.update()

    def run(self):
        ret = self.startscene()
        return ret