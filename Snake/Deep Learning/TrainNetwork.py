############################### IMPORT PACKAGES ###############################
import numpy as np
import math
from Snake import *
from tqdm import tqdm
import csv
import datetime as dt
import os.path
from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
#################################### CLASS ####################################
class GenerateTrainingData():
	def __init__(self):
		self.oGame = Snake()
		# Flags
		self.isNextRight 	= False #1
		self.isNextLeft 	= False #-1
		self.isNextFront 	= False #0
		# Coordinates
		self.rightStep  = [10,0]
		self.leftStep   = [-10,0]
		self.upStep 	= [0,-10]
		self.downStep   = [0,10]
		self.goRight    = [0,0,1]
		self.goFront	= [0,1,0]
		self.goLeft		= [1,0,0]

		date_stamp = dt.datetime.now().strftime("%Y%m%d")
		file_count = 1
		path = "./Training Data/"
		filename = f"{path}TrainingData_{date_stamp}"
		while os.path.isfile(f"{filename}_{file_count}.csv"):
			file_count += 1
		self.filename = f"{filename}_{file_count}.csv"
		
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
		vector_apple_normalised = vector_apple/magnitude_apple
		vector_snake_normalised = vector_snake/magnitude_snake
		
		# product = self.DotProduct(vector_apple, vector_snake)
		# angle   = self.ComputeAngle(product, magnitude_apple, magnitude_snake)
		angle = math.atan2(
		vector_apple_normalised[1] * vector_snake_normalised[0] - vector_apple_normalised[
			0] * vector_snake_normalised[1],
		vector_apple_normalised[1] * vector_snake_normalised[1] + vector_apple_normalised[
			0] * vector_snake_normalised[0]) / math.pi
		return angle, vector_apple_normalised, vector_snake_normalised

	def DistanceToApple(self, snake_pos, apple_pos):
		return np.linalg.norm(np.array(apple_pos) - np.array(snake_pos[0]))

	def GetVectors(self, snake_pos):
		vector_direction = np.array(snake_pos[0]) - np.array(snake_pos[1]) # Subtracts first block pos from the 2nd block to find direction its moving in
		# Vectors will always be either [10,0] for right direction, [-10,0] for left direction and [0,10] for continuing straight as the block pos are only 
		# 10 pixels apart
		vector_left = np.array([vector_direction[1], -vector_direction[0]]) # This formula goes left in whichever orientation the snake head is in
		vector_right = np.array([-vector_direction[1], vector_direction[0]]) # This formula goes right in whichever orientation the snake head is in
		return vector_direction, vector_right, vector_left

	def SetDirection(self, direction):
		if direction == 'R':
			self.isNextRight 	= True 
			self.isNextLeft  	= False
			self.isNextFront 	= False
		elif direction == 'L':
			self.isNextRight 	= False 
			self.isNextLeft  	= True
			self.isNextFront	= False
		elif direction == 'F':
			self.isNextRight 	= False 
			self.isNextLeft  	= False
			self.isNextFront 	= True

	def GenerateRandomDirection(self, angle, snake_pos):
		if angle > 0:
			self.SetDirection('R')
		elif angle < 0:
			self.SetDirection('L')
		else:
			self.SetDirection('F')
		return self.FindDirection(angle, snake_pos)
		
	# Finds the next calculated direction
	def FindDirection(self, angle, snake_pos):
		vector_direction, vector_right, vector_left = self.GetVectors(snake_pos)

		# If angle is > 0 then the apple is on the right side of the snake.
		# If angle is < 0 then the apple is on the left side of the snake.
		# If angle == 0 then the apple is in the same direction.
		next_direction = vector_direction
		if self.isNextRight:
			next_direction = vector_right
		elif self.isNextLeft:
			next_direction = vector_left
		else:
			next_direction = vector_direction
		
		button = self.GenerateNextButton(next_direction)
		return button
	
	def GenerateNextButton(self, direction):
		button = 0		
		if direction.tolist() == self.rightStep:
			button = 1
		elif direction.tolist() == self.leftStep:
			button = 0
		elif direction.tolist() == self.downStep:
			button = 3
		else:
			button = 2
			
		return button

	def isNextBlocked(self, snake_pos, direction):
		nextPos = snake_pos[0] + direction
		isBlocked = 0
		if self.oGame.Collision_Boundary(nextPos) or self.oGame.Collision_Self(nextPos.tolist(), snake_pos):
			isBlocked = 1
		return isBlocked

	def GetBlockedPath(self, snake_pos):
		vector_direction, vector_right, vector_left = self.GetVectors(snake_pos)

		isRightBlocked = self.isNextBlocked(snake_pos, vector_right)
		isLeftBlocked  = self.isNextBlocked(snake_pos, vector_left)
		isFrontBlocked = self.isNextBlocked(snake_pos, vector_direction)
		return isLeftBlocked, isFrontBlocked, isRightBlocked

	def GenerateOutput(self, inputs, training_data):
		isLeftBlocked  = inputs[0]
		isFrontBlocked = inputs[1]
		isRightBlocked = inputs[2]
		button 		   = inputs[3]
		angle 		   = inputs[4]
		snake_pos	   = inputs[5]

		output = self.goFront

		if self.isNextLeft:
			if isLeftBlocked:
				if isFrontBlocked and not isRightBlocked:
					output = self.goRight
					button = self.FindDirection(angle, snake_pos)
				elif not isFrontBlocked and isRightBlocked:
					output = self.goFront
					button = self.FindDirection(angle, snake_pos)
				elif not isFrontBlocked and not isRightBlocked:
					output = self.goRight
					button = self.FindDirection(angle, snake_pos)
			else:
				output = self.goLeft

		elif self.isNextFront:
			if isFrontBlocked:
				if isLeftBlocked and not isRightBlocked:
					button = self.FindDirection(angle, snake_pos)
					output = self.goRight
				elif not isLeftBlocked and isRightBlocked:
					button = self.FindDirection(angle, snake_pos)
					output = self.goLeft
				elif not isLeftBlocked and not isRightBlocked:
					button = self.FindDirection(angle, snake_pos)
					output = self.goRight
			else:
				output = self.goFront

		elif self.isNextRight:
			if isRightBlocked:
				if isFrontBlocked and not isLeftBlocked:
					button = self.FindDirection(angle, snake_pos)
					output = self.goLeft
				elif not isFrontBlocked and isLeftBlocked:
					button = self.FindDirection(angle, snake_pos)
					output = self.goFront
				elif not isFrontBlocked and not isLeftBlocked:
					button = self.FindDirection(angle, snake_pos)
					output = self.goLeft
			else:
				output = self.goRight

		# training_data.append(output)
		training_data = output

		return training_data, button

	def GenerateData(self):
		self.WriteCSV("", "", headers = True)
		training_data_x = []
		training_data_y = []
		training_games = 1000
		steps_per_game = 2500

		for _ in tqdm(range(training_games)):
			self.oGame.ResetGame()
			snake_pos = self.oGame.snake_pos
			apple_pos = self.oGame.apple_pos
			# distance = self.DistanceToApple(snake_pos, apple_pos)

			for _ in range(steps_per_game):
				angle, normVector_apple, normVector_snake = self.angle_with_apple(snake_pos, apple_pos)
				isLeftBlocked, isFrontBlocked, isRightBlocked = self.GetBlockedPath(snake_pos)
				button = self.GenerateRandomDirection(angle, snake_pos)
				training_data_y, button = self.GenerateOutput([isLeftBlocked, isFrontBlocked, isRightBlocked, button, angle, snake_pos], training_data_y)

				if isFrontBlocked and isRightBlocked and isLeftBlocked:
					break
				
				training_data_x = [isLeftBlocked, isFrontBlocked, isRightBlocked, normVector_apple[0], normVector_apple[1], normVector_snake[0], normVector_snake[1]]
				self.WriteCSV(training_data_x, training_data_y)
				snake_pos, apple_pos, crashed = self.oGame.TrainGame(button)
				if crashed:
					break

		return training_data_x, training_data_y
	
	def WriteCSV(self, x, y, headers = False):
		with open(self.filename, 'a', newline = '') as csvfile:
			writer = csv.writer(csvfile, delimiter=',')
			# Write the headers to the first row
			if headers:
				writer.writerow(["isLeftBlocked", "isFrontBlocked", "isRightBlocked", "Apple_x", "Apple_y", "Snake_x", "Snake_y", "Left", "Front", "Right"])
			else:
				writer.writerow([x[0], x[1], x[2], x[3], x[4], x[5], x[6], y[0], y[1], y[2]])

class NeuralNetwork():
	# def __init__(self):
	# 	from keras.models import Sequential
	# 	from keras.layers import Dense
	# 	from keras.models import model_from_json
		
	def ExtractData(self, filename):
		training_data_x = []
		training_data_y = []
		count = 0
		with open(filename) as csv_file:
			print("INFO: Extracting data...")
			csv_reader = csv.reader(csv_file, delimiter=',')
			for row in csv_reader:
				if count == 0:
					count += 1
					continue
				else:
					training_data_x.append([int(row[0]),int(row[1]),int(row[2]),\
						float(row[3]), float(row[4]),\
							int(float(row[5])),int(float(row[6]))])
					training_data_y.append([int(row[7]), int(row[8]), int(row[9])] )
					# training_data_y.append([int(float(row[7][1])), int(float(row[7][4])), int(float(row[7][7]))] )
		print("INFO: Data extracted.")
		return training_data_x, training_data_y
	
	def CreateModel(self, data):
		print("INFO: Creating model...")
		training_data_x, training_data_y = self.ExtractData(data)
		model = Sequential()
		model.add(Dense(units=9,input_dim=7))

		model.add(Dense(units=15, activation='relu'))
		model.add(Dense(output_dim=3,  activation = 'softmax'))

		model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
		model.fit((np.array(training_data_x).reshape(-1,7)),( np.array(training_data_y).reshape(-1,3)), batch_size = 256,epochs= 3)

		model.save_weights('model.h5')
		model_json = model.to_json()
		with open('./Model/model.json', 'w') as json_file:
			json_file.write(model_json)
			print("INFO: Model created.")
		return model

	def PlayAutonomous(self, model, weights):
		json_file = open(model, 'r')
		loaded_json_model = json_file.read()
		model = model_from_json(loaded_json_model)
		model.load_weights(weights)
		o_GenData = GenerateTrainingData()
		o_Game = Snake()
		
		training_data_y = []
		# oGame.ResetGame()
		snake_pos = o_Game.snake_pos
		apple_pos = o_Game.apple_pos
		# distance = self.DistanceToApple(snake_pos, apple_pos)

		for step in range(200000):
			angle, normVector_apple, normVector_snake = o_GenData.angle_with_apple(snake_pos, apple_pos)
			isLeftBlocked, isFrontBlocked, isRightBlocked = o_GenData.GetBlockedPath(snake_pos)
			# button = o_GenData.GenerateRandomDirection(angle, snake_pos)
			# training_data_y, button = o_GenData.GenerateOutput([isLeftBlocked, isFrontBlocked, isRightBlocked, button, angle, snake_pos], training_data_y)

			predicted_direction = np.argmax(np.array(model.predict(np.array([isLeftBlocked, isFrontBlocked,\
					isRightBlocked, normVector_apple[0], normVector_apple[1], normVector_snake[0], normVector_snake[1]])\
						.reshape(-1, 7))))

			new_direction = np.array(snake_pos[0]) - np.array(snake_pos[1])
			if predicted_direction == 0: #Left
				new_direction = np.array([new_direction[1], -new_direction[0]])
			elif predicted_direction == 1: # Continue
				new_direction = np.array(snake_pos[0]) - np.array(snake_pos[1])
			elif predicted_direction == 2: # Right
				new_direction = np.array([-new_direction[1], new_direction[0]])
			button = o_GenData.GenerateNextButton(new_direction)

			isBlocked = o_GenData.isNextBlocked(snake_pos,new_direction)
			if isBlocked:
				break
			
			snake_pos, apple_pos, _ = o_Game.TrainGame(button)
			print(step)

#################################### MAIN ####################################
if __name__ == "__main__":
	# model = GenerateTrainingData()
	# model.GenerateData()
	model = NeuralNetwork()
	# model.CreateModel("./Training Data/TrainingData_20200207_5.csv")
	model.PlayAutonomous('./Model/model.json', './Model/model.h5')