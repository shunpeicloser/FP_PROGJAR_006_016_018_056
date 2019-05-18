import pygame
import utility

class HighscoreScene:
	def __init__(self, sock):
		self.screen = None
		self.SCREEN_RESOLUTION = (640, 640)
		self.resource = {}
		# self.username = []
		# self.points
		self.username = ['agu','sat','ceh','yar','tam','adi','tej','jee','pl9','pl10']
		self.points = ['10','9','8','7','6','5','4','3','2','1']
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
		
		# Quit Button
		quit_surface = pygame.font.Font(None, 64).render('QUIT', True, pygame.Color('white'))
		quit_fill = pygame.Surface((150, 60))
		quit_fill.fill((0, 0, 0))
		self.screen.blit(quit_fill, (self.quit_rect.x, self.quit_rect.y))
		self.screen.blit(quit_surface, (self.quit_rect.x + 8, self.quit_rect.y + 8))
		ranking = []
		user = []
		poin = []
		basey = 150 # Y starting coordinate for highscore list

		# Header
		hs_text = pygame.font.Font(None, 64).render('HIGHSCORES', True, pygame.Color('white'))
		self.screen.blit(hs_text, (170,30))

		# Thead
		rank_text = pygame.font.Font(None, 48).render('RANK', True, pygame.Color('white'))
		self.screen.blit(rank_text, (80,100))
		username_text = pygame.font.Font(None, 48).render('USERNAME', True, pygame.Color('white'))
		self.screen.blit(username_text, (260,100))
		score_text = pygame.font.Font(None, 48).render('SCORE', True, pygame.Color('white'))
		self.screen.blit(score_text, (500,100))


		# Highscore List
		for i in range(len(self.username)):
			ranking.append(pygame.font.Font(None, 45).render(str(i+1), True, pygame.Color('white')))
			user.append(pygame.font.Font(None, 45).render(self.username[i], True, pygame.Color('white')))
			poin.append(pygame.font.Font(None, 45).render(self.points[i], True, pygame.Color('white')))

			self.screen.blit(ranking[i], (80,basey))
			self.screen.blit(user[i], (260,basey))
			self.screen.blit(poin[i], (500,basey))
			basey = basey + 30

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
				self.drawScreen()
				pygame.display.update()

	def run(self):
		ret = self.startScene()
		return ret
