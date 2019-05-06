import pygame
import utility

class LoginScene:
    def __init__(self):
        self.screen = None
        self.SCREEN_RESOLUTION = (640, 640)
        self.resource = {}
        self.username = ''
        self.password = ''
        self.username_rect = pygame.rect.Rect(100, 100, 350, 80)
        self.password_rect = pygame.rect.Rect(100, 200, 350, 80)
        self.login_rect = pygame.rect.Rect(40, 480, 260, 60)
        self.quit_rect = pygame.rect.Rect(40, 550, 260, 60)
        self.boxcolor = pygame.Color('black')
    
    def loadresource(self):
        try:
            self.resource.update({'background': (utility.Utility.loadimage('background.png'), (0, 0))})
            self.resource.update({'logo': (utility.Utility.loadimage('logo.png'), (0, 0))})
            # self.resource.update({'loginbutton': (utility.Utility.loadimage('loginbutton.png'), (40, 480))})
            # self.resource.update({'quitbutton': (utility.Utility.loadimage('quitbutton.png'), (40, 550))})
        except:
            return False
        return True
    
    def drawscreen(self):
        for item in self.resource:
            self.screen.blit(self.resource[item][0], self.resource[item][1])
        pygame.draw.rect(self.screen, self.boxcolor, self.username_rect, 2)
        pygame.draw.rect(self.screen, self.boxcolor, self.password_rect, 2)
        pygame.draw.rect(self.screen, self.boxcolor, self.login_rect, 2)
        pygame.draw.rect(self.screen, self.boxcolor, self.quit_rect, 2)
        username_surface = pygame.font.Font(None, 64).render(self.username, True, pygame.Color('yellow'))
        password_surface = pygame.font.Font(None, 64).render(self.username, True, pygame.Color('yellow'))
        login_surface = pygame.font.Font(None, 64).render('LOGIN', True, pygame.Color('yellow'))
        quit_surface = pygame.font.Font(None, 64).render('QUIT', True, pygame.Color('yellow'))
        self.screen.blit(username_surface, (self.username_rect.x + 8, self.username_rect.y + 8))
        self.screen.blit(password_surface, (self.password_rect.x + 8, self.password_rect.y + 8))
        self.screen.blit(login_surface, (self.login_rect.x + 8, self.login_rect.y + 8))
        self.screen.blit(quit_surface, (self.quit_rect.x + 8, self.quit_rect.y + 8))

    def startscene(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.SCREEN_RESOLUTION)
        running = self.loadresource()
        mousepos = None
        while running:
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return 0

                self.drawscreen()

                mousepos = pygame.mouse.get_pos()

                if event.type == pygame.MOUSEBUTTONUP:
                    if self.username_rect.collidepoint(mousepos):
                        pass
                    elif self.password_rect.collidepoint(mousepos):
                        pass
                    elif self.login_rect.collidepoint(mousepos):
                        return 4
                    elif self.quit_rect.collidepoint(mousepos):
                        return 0


                pygame.display.update()

    def run(self):
        ret = self.startscene()
        return ret