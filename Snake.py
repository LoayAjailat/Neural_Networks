"""
Snake Game

[brief summary] The code runs a modern recreation of the retro game Snake.
				The purpose of the software is two-fold:
					1. Create a fun & visual game using the pygame library
					2. Train a neural network to learn to play the game autonomously
				
[author]        Loay Ajailat
"""
################################# IMPORT PACKAGES #################################
import pygame
import random
import time 

###################################### CLASS ######################################
class Snake():
	def __init__(self):
		# Initialise pygame
		if pygame.get_init:
			pygame.init()
		
		# Screen Configs 
		self.screen_width  = 500
		self.screen_height = 500
		self.window_colour = (200, 200, 200)
		self.screen_Main   = pygame.display.set_mode((self.screen_width, self.screen_height))
		pygame.display.set_caption("Snake")
		self.clock = pygame.time.Clock() # Game's framerate - speed
		
		# Colours
		self.red   = (255, 0, 0)
		self.white = (255, 255, 255)
		self.black = (0, 0, 0)
		self.blue  = (61, 112, 240)
		
		# Snake and apple coordinates
		centre_x = int(self.screen_width/2)
		x = [centre_x, centre_x - 10, centre_x - 20]
		y = int(self.screen_height/2)
		self.snake_head = [x[0], y]
		self.snake_pos  = [[x[0], y], [x[1], y], [x[2], y]] #Len of the snake is 3 units (each unit is a 10×10 block)
		self.apple_pos = [random.randrange(1, int(self.screen_width/10))*10, random.randrange(10, int(self.screen_height/10))*10]
		
		# Directions
		self.prevButton = 1
		self.left  = 0
		self.right = 1
		self.up    = 2
		self.down  = 3
		self.score = 0
		
		# States
		self.quitGame  = False
		self.crashed   = False
		self.resetGame = False
		
	# Draws the apple on screen
	def DrawApple(self, location):
		w = 10
		h = 10
		x = location[0]
		y = location[1]
		rect = pygame.Rect(x, y, w, h)
		pygame.draw.rect(self.screen_Main, self.red , rect)
	
	# Draws the snake by drawing each block in its size
	def DrawSnake(self, location):
		w = 10
		h = 10
		for pos in location: # Draw each block
			x = pos[0]
			y = pos[1]
			rect = pygame.Rect(x, y, w, h)
			pygame.draw.rect(self.screen_Main, self.blue, rect)

	# Checks if the snake head collided with any of the boundaries
	def Collision_Boundary(self, snake_head):
		if snake_head[0] >= self.screen_width or snake_head[0] < 0 or snake_head[1] >= self.screen_height or snake_head[1] < 0:
			return True
		else:
			return False

	# Checks if the snake head collided with its own body 
	def Collision_Self(self, snake_head, snake_pos):
		if snake_head in snake_pos[1:]:
			return True
		else:
			return False

	# Assigns the apple a random position on screen on collision and increases the score
	def Collision_Apple(self):
		self.apple_pos = [random.randrange(1, self.screen_width/10)*10, random.randrange(10, self.screen_height/10)*10]
		self.score += 1

	# Updates the direction the snake needs to take
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

	# Changes the snake head's direction
	def MoveSnake(self, direction):
		if direction == self.right:
			self.snake_head[0] += 10
		elif direction == self.left:
			self.snake_head[0] -= 10
		elif direction == self.down:
			self.snake_head[1] += 10
		elif direction == self.up:
			self.snake_head[1] -= 10
		
		if self.snake_head == self.apple_pos:
			self.Collision_Apple()
			self.IncreaseSize()
		else:
			self.UpdatePosition()

	# Increase the size of the snake 
	def IncreaseSize(self):
		self.snake_pos.insert(0, list(self.snake_head))

	# Update the position of the snake
	def UpdatePosition(self):
		# Add the new head to the pos list then remove the tail
		self.snake_pos.insert(0, list(self.snake_head))
		self.snake_pos.pop()
		
	# Updates the pygame display
	def UpdateDisplay(self):
		pygame.display.set_caption(f"Score: {self.score}")
		pygame.display.update()

	# Displays the final score on screen
	def DisplayScore(self, display_text):
		largeText = pygame.font.Font('freesansbold.ttf', 24)
		TextSurf = largeText.render(display_text, True, self.black)
		TextRect = TextSurf.get_rect()
		TextRect.center = (int(self.screen_width/2), int(self.screen_height/2))
		self.screen_Main.blit(TextSurf, TextRect)
		pygame.display.update()

	# Sets flag that snake has crashed
	def SetCrashed(self):
		self.crashed = True

	# Set flag to quit game
	def QuitGame(self):
		self.quitGame = True
	
	# Resets the game
	def ResetGame(self):
		self.quitGame = False
		self.crashed  = False
		centre_x = int(self.screen_width/2)
		x = [centre_x, centre_x - 10, centre_x - 20]
		y = int(self.screen_height/2)
		self.snake_head = [x[0], y]
		self.snake_pos  = [[x[0], y], [x[1], y], [x[2], y]] #Len of the snake is 3 units (each unit is a 10×10 block)
		self.apple_pos = [random.randrange(1, int(self.screen_width/10))*10, random.randrange(10, int(self.screen_height/10))*10]
		self.score = 0
		self.resetGame = True

	# Plays the game
	def PlayGame(self, direction = 1):
		prevDirection = 1
		currentDirection = direction

		try:
			while not self.quitGame:
				while not self.crashed:
					# PyGame event interaction
					for event in pygame.event.get():
						# Quits program
						if event.type == pygame.QUIT:
							self.SetCrashed()
							self.QuitGame()
						if event.type == pygame.KEYDOWN:
							if event.key == pygame.K_ESCAPE:
								self.SetCrashed()
								self.QuitGame()
						currentDirection = self.UpdateDirection(event, prevDirection)
					if not self.quitGame:
						self.screen_Main.fill(self.window_colour)
						self.DrawApple(self.apple_pos)
						self.DrawSnake(self.snake_pos)
						self.MoveSnake(currentDirection)
						# self.UpdatePosition()
						self.UpdateDisplay()
						prevDirection = currentDirection
						if self.Collision_Boundary(self.snake_head) or self.Collision_Self(self.snake_head, self.snake_pos):
							display_text = 'Your Score is: ' + str(self.score)
							self.DisplayScore(display_text)
							self.SetCrashed()
						self.clock.tick(16) # Sets the framerate to 16
				
				# PyGame event interaction
				for event in pygame.event.get():
					# Quits program
					if event.type == pygame.QUIT:
						self.QuitGame()
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_ESCAPE:
							self.QuitGame()
						if event.key == pygame.K_SPACE:
							self.ResetGame()

				if self.quitGame:
					pygame.display.quit()
					pygame.quit()
				elif self.resetGame:
					currentDirection = direction
				else:
					display_text = 'Your Score is: ' + str(self.score)
					self.DisplayScore(display_text)
		except Exception as e:
			print(f"Error: {e}")
			text = "Error running game. Please restart."
			self.DisplayScore(text)

	# Train game
	def TrainGame(self, direction = 1):
		while not self.crashed:
			crashed = False
			self.screen_Main.fill(self.window_colour)
			self.DrawApple(self.apple_pos)
			self.DrawSnake(self.snake_pos)
			self.MoveSnake(direction)
			# self.UpdatePosition()
			self.UpdateDisplay()
			self.clock.tick(128) # 64
			if self.Collision_Boundary(self.snake_head) or self.Collision_Self(self.snake_head, self.snake_pos):
				crashed = True
			return self.snake_pos, self.apple_pos, crashed

#################################### MAIN ####################################
if __name__ == "__main__":
	game = Snake()
	game.PlayGame()

