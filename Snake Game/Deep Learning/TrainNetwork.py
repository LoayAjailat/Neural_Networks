############################### IMPORT PACKAGES ###############################
import numpy as np
import math

#################################### CLASS ####################################
class NeuralNetwork():
	# def __init__(self):

	def DotProduct(self, vector1, vector2):
		product = 0
		for i in range(2):
			product += vector1[i]*vector2[i]
		return product

	def ComputeAngle(self, product, magnitude1, magnitude2):
		angle = math.acos(product/(magnitude1 * magnitude2))/math.pi
		return angle

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

	def run(self):
		angle = self.angle_with_apple([[260,250], [250,250]], [300,270])

#################################### MAIN ####################################
if __name__ == "__main__":
	nn = NeuralNetwork()
	nn.run()


