import pygame
import utility

class RoomScene:
    def __init__(self):
        self.screen = None
        self.SCREEN_RESOLUTION = (640, 640)
        self.resource = {}
        
    
    def loadresource(self):
        try:
            self.resource.update({'background': (utility.Utility.loadimage('background.png'), (0, 0))})
        except:
            return False
        return True
    
    def drawscreen(self):
        for item in self.resource:
            self.screen.blit(self.resource[item][0], self.resource[item][1])

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

                mousepos = pygame.mouse.get_pos()

                self.drawscreen()
                pygame.display.update()

    def run(self):
        ret = self.startscene()
        return ret