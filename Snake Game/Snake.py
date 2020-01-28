############################### IMPORT PACKAGES ###############################
import pygame
import random
import time 

###############################################################################
pygame.init()

#################################### CLASS ####################################
class Snake():
	def __init__(self):
		self.screen_width  = 640
		self.screen_height = 480
		self.window_colour = (200, 200, 200)
		self.screen_Main   = pygame.display.set_mode((self.screen_width, self.screen_height))
		pygame.display.set_caption("Snake")
		self.clock = pygame.time.Clock()
		self.red   = (255, 0, 0)
		self.white = (255, 255, 255)
		self.black = (0, 0, 0)
		self.blue  = (61, 112, 240)
		self.snake_head = [250, 250]
		self.snake_pos  = [[250,250], [240,250], [230,250]] #Starting length of the snake is 3 units where each unit is a 10×10 block
		self.apple_position = [random.randrange(1, self.screen_width/10)*10, random.randrange(10, self.screen_height/10)*10] #Random location
		self.quitGame = False
		self.crashed = False
		self.prevButton = 1
		self.left  = 0
		self.right = 1
		self.up    = 2
		self.down  = 3
		self.score = 0
		
	def DrawApple(self, location):
		w = 10
		h = 10
		x = location[0]
		y = location[1]
		rect = pygame.Rect(x, y, w, h)
		pygame.draw.rect(self.screen_Main, self.red , rect)
	
	def DrawSnake(self, location):
		w = 10
		h = 10
		for pos in location:
			x = pos[0]
			y = pos[1]
			rect = pygame.Rect(x, y, w, h)
			pygame.draw.rect(self.screen_Main, self.blue, rect)

	def BoundaryCollision(self):
		if self.snake_head[0] >= self.screen_width or self.snake_head[0] < 0 or self.snake_head[1] >= self.screen_height or self.snake_head[1] < 0:
			return True
		else:
			return False

	def SelfCollision(self):
		snake_head = self.snake_pos[0]
		if snake_head in self.snake_pos[1:]:
			return True
		else:
			return False

	def AppleCollision(self):
		self.apple_position = [random.randrange(1, self.screen_width/10)*10, random.randrange(10, self.screen_height/10)*10]
		self.score += 1

	def UpdateDirection(self, event, prevDirection):
		currentDirection = prevDirection
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT and prevDirection != self.right:
				currentDirection = self.left
			elif event.key == pygame.K_RIGHT and prevDirection != self.left:
				currentDirection = self.right
			elif event.key == pygame.K_UP and prevDirection != self.down:
				currentDirection = self.up
			elif event.key == pygame.K_DOWN and prevDirection != self.up:
				currentDirection = self.down
		return currentDirection

	def MoveSnake(self, direction):
		if direction == self.right:
			self.snake_head[0] += 10
		elif direction == self.left:
			self.snake_head[0] -= 10
		elif direction == self.down:
			self.snake_head[1] += 10
		elif direction == self.up:
			self.snake_head[1] -= 10
		
		if self.snake_head == self.apple_position:
			self.AppleCollision()
			self.IncreaseSize()
		else:
			self.UpdatePosition()

	def IncreaseSize(self):
		self.snake_pos.insert(0, list(self.snake_head))

	def UpdatePosition(self):
		self.snake_pos.insert(0, list(self.snake_head))
		self.snake_pos.pop()
		
	def UpdateDisplay(self):
		pygame.display.update()

	def DisplayScore(self, display_text):
		largeText = pygame.font.Font('freesansbold.ttf',35)
		TextSurf = largeText.render(display_text, True, self.black)
		TextRect = TextSurf.get_rect()
		TextRect.center = (int(self.screen_width/2), int(self.screen_height/2))
		self.screen_Main.blit(TextSurf, TextRect)
		pygame.display.update()
		# time.sleep(2)

	def RunGame(self):
		prevDirection = 1
		currentDirection = 1

		while not self.quitGame:
			while not self.crashed:
				# PyGame event interaction
				for event in pygame.event.get():
					# Quits program
					if event.type == pygame.QUIT:
						self.crashed = True
						self.quitGame = True
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_ESCAPE:
							self.crashed = True
							self.quitGame = True
					currentDirection = self.UpdateDirection(event, prevDirection)
				if not self.quitGame:
					self.screen_Main.fill(self.window_colour)
					self.DrawApple(self.apple_position)
					self.DrawSnake(self.snake_pos)
					self.MoveSnake(currentDirection)
					# self.UpdatePosition()
					self.UpdateDisplay()
					prevDirection = currentDirection
					isCollision = self.BoundaryCollision()
					if isCollision:
						self.crashed = True
					self.clock.tick(16)
			# PyGame event interaction
			for event in pygame.event.get():
				# Quits program
				if event.type == pygame.QUIT:
					self.quitGame = True
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						self.quitGame = True
			if self.quitGame:
				pygame.display.quit()
				pygame.quit()
			else:
				display_text = 'Your Score is: ' + str(self.score)
				self.DisplayScore(display_text)

#################################### MAIN ####################################
if __name__ == "__main__":
	game = Snake()
	game.RunGame()

