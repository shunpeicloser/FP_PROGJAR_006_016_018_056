import pygame
import utility
import room

class LobbyScene:
	def __init__(self):
		self.screen = None
		self.SCREEN_RESOLUTION = (640, 640)
		self.resource = {}
		self.lobby = []
		for i in range(10):
			temp = room.Room()
			temp.createRoom(i)
			temp.setName("progjar"+str(i))
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
		
		room_id = []
		room_name = []
		room_player = []
		basey = 150
		hs_text = pygame.font.Font(None, 64).render('LOBBY', True, pygame.Color('white'))
		self.screen.blit(hs_text, (240,30))

		num_text = pygame.font.Font(None, 48).render('No', True, pygame.Color('white'))
		self.screen.blit(num_text, (70,100))
		roomname_text = pygame.font.Font(None, 48).render('Room Name', True, pygame.Color('white'))
		self.screen.blit(roomname_text, (250,100))
		players_text = pygame.font.Font(None, 48).render('Players', True, pygame.Color('white'))
		self.screen.blit(players_text, (490,100))

		for i in range(len(self.lobby)):
			my_room = self.lobby[i]
			room_id.append(pygame.font.Font(None, 45).render(str((my_room.getId()+1)), True, pygame.Color('white')))
			room_name.append(pygame.font.Font(None, 45).render(my_room.getName(), True, pygame.Color('white')))
			room_player.append(pygame.font.Font(None, 45).render(str(my_room.getNumPlayer()), True, pygame.Color('white')))

			self.screen.blit(room_id[i], (70,basey))
			self.screen.blit(room_name[i], (250,basey))
			self.screen.blit(room_player[i], (490,basey))

			my_room.createRect(pygame.rect.Rect(65, basey, 490, 30))
			my_room.creteFill(pygame.Surface((490, 30)))
			if ((i%2) == 0):
				my_room.getFill().set_alpha(60)
			else:
				my_room.getFill().set_alpha(0)
			my_room.getFill().fill((0, 0, 0))
			self.screen.blit(my_room.getFill(), (my_room.getRect().x, my_room.getRect().y))

			basey = basey + 30

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
						if self.lobby[i].getRect().collidepoint(mousepos):
							print(self.lobby[i].getId())
							return 0 #return nomor room bisa deh
				self.drawScreen()
				pygame.display.update()

	def run(self):
		ret = self.startScene()
		return ret
