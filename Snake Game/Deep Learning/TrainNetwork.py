############################### IMPORT PACKAGES ###############################
import numpy as np
import math

#################################### CLASS ####################################
class NeuralNetwork():
	# def __init__(self):

	# Calculate the dot product of 2 vectors
	def DotProduct(self, vector1, vector2):
		product = 0
		for i in range(2):
			product += vector1[i]*vector2[i]
		return product

	# Calculates the angle between 2 magnitude vectors in radians
	def ComputeAngle(self, product, magnitude1, magnitude2):
		angle = math.acos(product/(magnitude1 * magnitude2))/math.pi
		return angle

	# Find the directional angle between the snake's head and the apple
	def angle_with_apple(self, snake_pos, apple_pos):
		vector_apple = np.array(apple_pos) - np.array(snake_pos[0]) # They need to be converted to np.array() so it can subtract, otherwise it fails
		vector_snake = np.array(snake_pos[0]) - np.array(snake_pos[1])

		magnitude_apple = np.linalg.norm(vector_apple)
		magnitude_snake = np.linalg.norm(vector_snake)
		if magnitude_apple == 0:
			magnitude_apple = 10
		if magnitude_snake == 0:
			magnitude_snake = 10
		
		product = self.DotProduct(vector_apple, vector_snake)
		angle   = self.ComputeAngle(product, magnitude_apple, magnitude_snake)
		print(angle)
		return angle

	def FindDirection(self, angle, snake_pos):
		# If angle is > 0 then the apple is on the right side of the snake.
		# If angle is < 0 then the apple is on the left side of the snake.
		# If angle == 0 then the apple is in the same direction.
		if angle > 0:
			direction = 1 # Go right
		elif angle < 0:
			direction = -1 # Go left
		else:
			direction = 0 # Continue in same direction

		vector_direction = np.array(snake_pos[0]) - np.array(snake_pos[1]) # Subtracts first block pos from the 2nd block to find direction its moving in
		# Vectors will always be either [10,0] for right direction, [-10,0] for left direction and [0,10] for continuing straight as the block pos are only 
		# 10 pixels apart
		vector_left = np.array([vector_direction[1], -vector_direction[0]]) ####### I THINK THESE ARE REVERSED FOR LEFT AND RIGHT
		vector_right = np.array([-vector_direction[1], vector_direction[0]])

		#### IMPLEMENT YOUR OWN VERSION OF THIS PLEASE

	def run(self):
		angle = self.angle_with_apple([[260,250], [250,250]], [300,270])

#################################### MAIN ####################################
if __name__ == "__main__":
	nn = NeuralNetwork()
	nn.run()


