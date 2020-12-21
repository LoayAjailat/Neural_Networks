# Modern Snake Game
This project is intended to build a game using the Pygame library that can be played by the user or played autonomously by the system.

## Instructions
### Play as user
To play Snake as a user, please run the Snake.py software. 
Use the arrow keys to move the snake around the screen.

Keys:
    UP Arrow    - Upwards direction
    
    LEFT Arrow  - Left direction
    
    RIGHT Arrow - Right direction
    
    DOWN Arrow  - Downwards direction
    
    SPACE       - Resets game
    
    ESC         - Exits game

### Autonomous playing
The project already contains a trained model that can run the game autonomously.

To play snake autonomously, please enter the DeepLearning directory in your terminal and run TrainNetwork.py

NOTE: To kill an autonomous play, use CTRL-C in the terminal. Terminating within the GUI is a feature in progress.
      Recent bug discovered that causes the GUI to crash if screen is pressed. Fix is in progress.

### Training model
To create a new training model. Uncomment the training option in the main section in TrainNetwork.py and run.

### Extra
To increase/decrease the speed at which the game is run, change the value set in 'self.clock.tick(128)'. Higher values speed up the game while lower values slow down the game.

## Future work
1. Add a Main menu
2. Allow pausing game by opening main menu
3. Menu should incorporate the following options:
    - Start game
        - As user
        - Autonomous
    - Train neural network model
        - Specify csv file directory
    - Leaderboards
    - Settings
        - Change framerate (speed of snake)
        - Change colour of snake, apple, and background
4. Allow interrupting the training process
    
## Requirements
numpy
math
tqdm
csv
datetime
tensorflow
keras

