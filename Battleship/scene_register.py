import pygame
import utility

class RegisterScene:
    def __init__(self):
        self.screen = None
        self.SCREEN_RESOLUTION = (640, 640)
        self.resource = {}
        self.username = ''
        self.password = ''
        self.username_rect = pygame.rect.Rect(150, 100, 350, 80)
        self.password_rect = pygame.rect.Rect(150, 200, 350, 80)
        self.confirm_rect = pygame.rect.Rect(300, 300, 260, 60)
        self.back_rect = pygame.rect.Rect(20, 300, 260, 60)
        self.boxcolor = pygame.Color('black')
    
    def loadresource(self):
        try:
            self.resource.update({'background': (utility.Utility.loadimage('background.png'), (0, 0))})
        except:
            return False
        return True
    
    def drawscreen(self):
        for item in self.resource:
            self.screen.blit(self.resource[item][0], self.resource[item][1])

        pygame.draw.rect(self.screen, self.boxcolor, self.username_rect, 8)
        pygame.draw.rect(self.screen, self.boxcolor, self.password_rect, 8)
        pygame.draw.rect(self.screen, self.boxcolor, self.confirm_rect, 8)
        pygame.draw.rect(self.screen, self.boxcolor, self.back_rect, 8)

        username_surface = pygame.font.Font(None, 64).render(self.username, True, pygame.Color('black'))
        password_surface = pygame.font.Font(None, 64).render(self.password, True, pygame.Color('black'))
        confirm_surface = pygame.font.Font(None, 64).render('CONFIRM', True, pygame.Color('white'))
        back_surface = pygame.font.Font(None, 64).render('BACK', True, pygame.Color('white'))
        
        username_fill = pygame.Surface((self.username_rect.width, self.username_rect.height))
        password_fill = pygame.Surface((self.password_rect.width, self.password_rect.height))
        confirm_fill = pygame.Surface((self.confirm_rect.width, self.confirm_rect.height))
        back_fill = pygame.Surface((self.back_rect.width, self.back_rect.height))

        username_fill.fill((255, 255, 255))
        password_fill.fill((255, 255, 255))
        confirm_fill.fill((0, 0, 0))
        back_fill.fill((0, 0, 0))
        
        self.screen.blit(username_fill, (self.username_rect.x, self.username_rect.y))
        self.screen.blit(password_fill, (self.password_rect.x, self.password_rect.y))
        self.screen.blit(confirm_fill, (self.confirm_rect.x, self.confirm_rect.y))
        self.screen.blit(back_fill, (self.back_rect.x, self.back_rect.y))

        self.screen.blit(username_surface, (self.username_rect.x + 8, self.username_rect.y + 8))
        self.screen.blit(password_surface, (self.password_rect.x + 8, self.password_rect.y + 8))
        self.screen.blit(confirm_surface, (self.confirm_rect.x + 8, self.confirm_rect.y + 8))
        self.screen.blit(back_surface, (self.back_rect.x + 8, self.back_rect.y + 8))

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

                    if self.confirm_rect.collidepoint(mousepos):
                        return 1
                    elif self.back_rect.collidepoint(mousepos):
                        return 1

                if is_username:
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_BACKSPACE:
                            self.username = self.username[:-1]
                        else:
                            self.username += chr(event.key)
                elif is_password:
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_BACKSPACE:
                            self.password = self.password[:-1]
                        else:
                            self.password += chr(event.key)
                self.drawscreen()
                pygame.display.update()

    def run(self):
        ret = self.startscene()
        return ret