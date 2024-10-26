import gymnasium as gym
from gymnasium import spaces

import random
import numpy as np
import pygame

from typing import Optional
from collections import deque

def collision_with_apple(apple_position):
	apple_position = [random.randrange(1,50)*10,random.randrange(1,50)*10]
	return apple_position

def collision_with_boundaries(snake_head):
	if snake_head[0]>=500 or snake_head[0]<0 or snake_head[1]>=500 or snake_head[1]<0 :
		return 1
	else:
		return 0

def collision_with_self(snake_position):
	snake_head = snake_position[0]
	if snake_head in snake_position[1:]:
		return 1
	else:
		return 0

#It is desired for the snake to be x units long.
SNAKE_LEN_GOAL = 30

class SnakeGameEnv(gym.Env):

	#region <SnakeGameEnv - metadata>
	metadata = {
		"render_modes": [
			"human",
			"rgb_array",
			"state_pixels",
		],
		"render_fps": 50,
	}
	#endregion

	#INIT
	def __init__(self, render_mode: Optional[str] = None):
		super(SnakeGameEnv, self).__init__()

		#region <INIT - Reward Values>
		self.rewValue_AppleReward = 10000
		#endregion

		#region <INIT - Render Related>
		self.render_mode = "human"
		self.screen: Optional[pygame.Surface] = None
		self.clock = None
		#endregion

		self.action_space = spaces.Discrete(4)		
		self.observation_space = spaces.Box(low=-500, high=500, shape=(5+SNAKE_LEN_GOAL,), dtype=np.int64)
	
	#----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
	
	#STEP
	def step(self, action):
		#buffers for possible rewards
		apple_reward = 0
		dist_based_reward = 0
		
		#Move the snake's head based on the action taken
		if action == 0:
			self.snake_head[0] -= 10 #left
		elif action == 1:
			self.snake_head[0] += 10 #right
		elif action == 2:
			self.snake_head[1] += 10 #up
		elif action == 3:
			self.snake_head[1] -= 10 #down			

		#Process what happens if the snake's head hits an apple as a result of the action taken
		if self.snake_head == self.apple_position:
			self.apple_position = collision_with_apple(self.apple_position) #move the apple somewhere random (this is for next frame)
			apple_reward = self.rewValue_AppleReward 						#fill the apple reward buffer
			print(f"got an apple, the value of the reward for this is:{self.rewValue_AppleReward}")
			self.snake_body.insert(0,list(self.snake_head)) 				#Attach the apple that was eaten to the snake (this increases the length of the snake)
		else: #Process what happens if the snake's head does NOT hit an apple as a result of the action taken
			self.snake_body.insert(0,list(self.snake_head))					#Attach the empty space that was moved into to the snake
			self.snake_body.pop()											#remove the last body part in the list
																			#this sequence results in the actual movement of the snake
		
		#Check if collided with self and process the result of having done so
		if collision_with_self(self.snake_body) == 1:			
			self.terminated = True

		#Check if collided with the map boundary and process the result of having done so
		if collision_with_boundaries(self.snake_head) == 1:
			self.terminated = True		

		#produce a reward based on the distance from the snake head to the apple position
		euclidean_dist_to_apple = np.linalg.norm(np.array(self.snake_head) - np.array(self.apple_position))
		dist_based_reward = 250 - euclidean_dist_to_apple

		#add up all the possible rewards (and in this case scale it down by 100)
		self.total_reward = (apple_reward + dist_based_reward) / 100

		#correct the reward (since it's being stored in a self buffer, we need to update it so it only reflects the reward for this step, this could just be reset each step instead...)
		self.reward = self.total_reward - self.prev_reward
		self.prev_reward = self.total_reward

		#what happens if the episode is terminated...?
		if self.terminated:
			self.reward = -10 #idk why this is -10, seems arbitrary

		#region <STEP - Observation>
		#0
		head_x = self.snake_head[0]
		#1
		head_y = self.snake_head[1]

		#2
		apple_delta_x = self.apple_position[0] - head_x
		#3
		apple_delta_y = self.apple_position[1] - head_y

		#4
		snake_length = len(self.snake_body)
		
		#5 - 34
		#Add the latest action to the list of actions
		self.previous_actions.append(action)
		#endregion
		
		self.observation = [head_x, head_y, apple_delta_x, apple_delta_y, snake_length] + list(self.previous_actions)
		self.observation = np.array(self.observation)

		self.info = {}
		self.truncated = False
		if self.render_mode == "human":
			self.render()
		return self.observation, self.reward, self.terminated, self.truncated, self.info
	
	#----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

	#RESET
	def reset(self, seed=None, options=None):

		#region <RESET - System>
		self.terminated = False
		self.reward = 0		
		self.prev_reward = 0
		#endregion

		#region <RESET - Actors>
		self.apple_position = [random.randrange(1,500), random.randrange(1,500)]
		self.snake_body = [[250, 250], [240, 250], [230, 250]]
		self.snake_head = [250, 250]
		#endregion		

		#region <RESET - Observation>
		#0
		head_x = self.snake_head[0]
		#1
		head_y = self.snake_head[1]

		#2
		apple_delta_x = self.apple_position[0] - head_x
		#3
		apple_delta_y = self.apple_position[1] - head_y

		#4
		snake_length = len(self.snake_body)

		#5 - 34
		self.previous_actions = deque(maxlen=SNAKE_LEN_GOAL)		
		for _ in range(SNAKE_LEN_GOAL):
			self.previous_actions.append(-1)		
		#endregion

		self.observation = [head_x, head_y, apple_delta_x, apple_delta_y, snake_length] + list(self.previous_actions)
		self.observation = np.array(self.observation)
	
		self.info = {}
		if self.render_mode == "human":
			self.render()
		return self.observation, self.info	
	
	#----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
	
	#RENDER
	def render(self):
		if self.render_mode is None:
			assert self.spec is not None
			gym.logger.warn(
				"You are calling render method without specifying any render mode."
				"You can specify the render_mode at initialization,"
				f'e.g. gym.make("{self.spec.id}", render_mode="rgb_array")'
			)
			return
		else:
			return self._render(self.render_mode)
		
	def _render(self, mode: str):
		assert mode in self.metadata["render_modes"]

		#region <RENDER - Settings>
		_WINDOW_W = 500
		_WINDOW_H = 500
		_BGND_COLOR = (0, 0, 0) #Black
		_APPLE_COLOR = (0, 0, 255)
		_APPLE_SIZE = 10
		_APPLE_THICKNESS = 3
		_SNAKE_COLOR = (0, 255, 0)
		_SNAKE_SIZE = 10
		_SNAKE_THICKNESS = 3
		#endregion

		#region <RENDER - Init>
		pygame.font.init()
		if self.screen is None and mode == "human":		
			pygame.init()
			pygame.display.init()
			self.screen = pygame.display.set_mode((_WINDOW_W, _WINDOW_H))
		if self.clock is None:		
			self.clock = pygame.time.Clock()
		#endregion		

		#region <RENDER - Draw>
		#We create a surface which represents the background of the game
		self.surf = pygame.Surface((_WINDOW_W, _WINDOW_W))

		#we color the background black
		self.surf.fill(_BGND_COLOR)

		#we draw the apple onto the surface (background)
		#pygame.draw.rect(<surface to draw on>, <color>, <rectangle to draw>, <thickness>)
		pygame.draw.rect(
			self.surf, 
			_APPLE_COLOR,
			#pygame.rect(<top-left x pos>, <top-left y pos>, <width>, <height>)
			pygame.Rect(
					self.apple_position[0], 
			   		self.apple_position[1], 
					_APPLE_SIZE, 
					_APPLE_SIZE
			),
			_APPLE_THICKNESS
		)		

		#we draw each of the parts that represent the snake onto the background
		for position in self.snake_body:
			pygame.draw.rect(
				self.surf, 
				_SNAKE_COLOR,
				pygame.Rect(
					position[0], 
					position[1], 
					_SNAKE_SIZE, 
					_SNAKE_SIZE
				),
				_SNAKE_THICKNESS
			)		
		#endregion

		#region <RENDER - End>
		#Note: I don't really know what the stuff below is about...I think it might be pygame stuff
		if mode == "human":		
			pygame.event.pump()
			# We need to ensure that human-rendering occurs at the predefined framerate.
			# The following line will automatically add a delay to keep the framerate stable.
			self.clock.tick(self.metadata["render_fps"]) #the fps setting in the "metadata" enum
			assert self.screen is not None
			self.screen.fill(0)
			self.screen.blit(self.surf, (0, 0))
			# The following line copies our drawings from `canvas` to the visible window
			#self.screen.blit(self.surf, self.surf.get_rect())
			pygame.display.update()		
		else:  # rgb_array
			return np.transpose(
				np.array(pygame.surfarray.pixels3d(self.surf)), axes=(1, 0, 2)
			)
		#endregion