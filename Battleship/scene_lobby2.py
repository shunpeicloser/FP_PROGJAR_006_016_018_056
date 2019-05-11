import pygame
import utility
import player

class LobbyScene:
	def __init__(self):
		self.screen = None
		self.SCREEN_RESOLUTION = (640, 640)
		self.resource = {}
		self.lobby = []
		for j in range(10):
			temp = player.Player("progjar"+str(j))
			if ((j%2) == 0):
				temp.goPlay()
			self.lobby.append(temp)
		self.quit_rect = pygame.rect.Rect(40, 550, 150, 60)
		self.boxcolor = pygame.Color('black')

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
		quit_surface = pygame.font.Font(None, 64).render('QUIT', True, pygame.Color('white'))
		quit_fill = pygame.Surface((150, 60))
		quit_fill.fill((0, 0, 0))
		
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

		for i in range(len(self.lobby)):
			list_user = self.lobby[i]
			if(list_user.is_ingame() != True):
				num_id.append(pygame.font.Font(None, 45).render(str(z+1), True, pygame.Color('white')))
				player_name.append(pygame.font.Font(None, 45).render(str(list_user.getname()), True, pygame.Color('white')))
				self.screen.blit(num_id[z], (70,basey))
				self.screen.blit(player_name[z], (250,basey))

				list_user.createRect(pygame.rect.Rect(65, basey, 490, 30))
				list_user.creteFill(pygame.Surface((490, 30)))
				if ((z%2) == 0):
					list_user.getFill().set_alpha(60)
				else:
					list_user.getFill().set_alpha(0)
				list_user.getFill().fill((0, 0, 0))
				self.screen.blit(list_user.getFill(), (list_user.getRect().x, list_user.getRect().y))

				basey = basey + 30
				z = z + 1

		self.screen.blit(quit_fill, (self.quit_rect.x, self.quit_rect.y))
		self.screen.blit(quit_surface, (self.quit_rect.x + 8, self.quit_rect.y + 8))

	def startScene(self):
		pygame.init()
		self.screen = pygame.display.set_mode(self.SCREEN_RESOLUTION)
		running = self.loadResource()
		mousepos = None
		while running:
			self.screen.fill((0, 0, 0))
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
					return 0

				mousepos = pygame.mouse.get_pos()
				if event.type == pygame.MOUSEBUTTONUP:
					if self.quit_rect.collidepoint(mousepos):
						return 0
					for i in range(len(self.lobby)):
						if(self.lobby[i].is_ingame() != True):
							if self.lobby[i].getRect().collidepoint(mousepos):
								print(self.lobby[i].getname())
								# return 0 #return nomor room bisa deh
				self.drawScreen()
				pygame.display.update()

	def run(self):
		ret = self.startScene()
		return ret
