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

#region <GLOBAL - Settings>
#It is desired for the snake to be x units long.
SNAKE_LEN_GOAL = 30
#A single snake part has 2 parameters, x and y, so...
SNAKE_LEN_POS_DATA = SNAKE_LEN_GOAL * 2
#How many times can the snake change directions per apple catch before being penalized?
MAX_DIR_CHANGES_PER_APPLE = 5
#endregion

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
		self.rewValue_for_grabbing_apple = 5
		self.rewValue_for_colliding_w_self = -10
		self.rewValue_for_colliding_w_bound = -10
		#endregion

		#region <INIT - Render Related>
		self.render_mode = "human"
		self.screen: Optional[pygame.Surface] = None
		self.clock = None
		#endregion

		self.action_space = spaces.Discrete(4)		
		self.observation_space = spaces.Box(low=-500, high=500, shape=(4 + SNAKE_LEN_POS_DATA,), dtype=np.int64)
	
	#----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
	
	#STEP
	def step(self, action):
		
		#buffers for possible rewards, set in env init
		reward_for_grabbing_apple = 0
		reward_for_colliding_w_self = 0
		reward_for_colliding_w_bound = 0
		
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
			self.apple_count += 1
			reward_for_grabbing_apple = self.rewValue_for_grabbing_apple * self.apple_count 						#fill the apple reward buffer
			print(f"got an apple, the value of the reward for this is:{self.rewValue_for_grabbing_apple}")
			self.snake_body.insert(0,list(self.snake_head)) 				#Attach the apple that was eaten to the snake (this increases the length of the snake)
		else: #Process what happens if the snake's head does NOT hit an apple as a result of the action taken
			self.snake_body.insert(0,list(self.snake_head))					#Attach the empty space that was moved into to the snake
			self.snake_body.pop()											#remove the last body part in the list
																			#this sequence results in the actual movement of the snake
		
		#Check if collided with self and process the result of having done so
		if collision_with_self(self.snake_body) == 1:
			reward_for_colliding_w_self = self.rewValue_for_colliding_w_self	
			self.terminated = True

		#Check if collided with the map boundary and process the result of having done so
		if collision_with_boundaries(self.snake_head) == 1:
			reward_for_colliding_w_bound = self.rewValue_for_colliding_w_bound
			self.terminated = True		

		#region <STEP - Reward>		
		reward_for_this_step = reward_for_grabbing_apple + reward_for_colliding_w_bound + reward_for_colliding_w_self
		self.reward = reward_for_this_step
	
		#what happens if the episode is terminated...?
		#if self.terminated:
			#pass
		#endregion

		#region <STEP - Observation>
		#Where is the apple located, exactly?
		#0
		apple_pos_x = self.apple_position[0] #gets updated when the agent hits an apple
		#1
		apple_pos_y = self.apple_position[1]

		#2
		#What is the snake position relative to the apple position?
		#This parameter essentially points direction.
		# (-) in x means apple is left of snake, (+) in x means apple is to the right of snake
		rel_delta_x_to_apple = self.apple_position[0] - self.snake_head[0]
		#3
		# (-) in y means apple is below of snake, (+) in y means apple is above the snake
		rel_delta_y_to_apple = self.apple_position[1] - self.snake_head[1]		

		#4 - 63
		#this doesn't need to be 'self' since it's being constructed from the snake body buffer and then appended to the observation
		snake_body_components_buffer = deque(maxlen=SNAKE_LEN_POS_DATA)
		for _ in range(SNAKE_LEN_POS_DATA):
			snake_body_components_buffer.append(-1)

		j = 0
		for i in range(len(self.snake_body)):
			snake_body_components_buffer[j] = self.snake_body[i][0]
			j += 1
			snake_body_components_buffer[j] = self.snake_body[i][1]
			j += 1
		#endregion
		
		self.observation = [apple_pos_x, apple_pos_y, rel_delta_x_to_apple, rel_delta_y_to_apple] + list(snake_body_components_buffer)
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
		#how many apples were obtained in one episode?
		self.apple_count = 0 #used to calculate reward...
		#endregion

		#region <RESET - Actors>
		self.apple_position = [random.randrange(10, 490, 10), random.randrange(10, 490, 10)]

		#construct snake...
		snake_head_x = random.randrange(120, 370, 10)
		snake_head_y = random.randrange(120, 370, 10)

		#snake part 1 and 2
		_SNAKE_SIZE = 10 #WARNING: This is a local variable, it should be consistent with the one found in render
		snake_part_1_x = 0 #buffers...
		snake_part_1_y = 0
		snake_part_2_x = 0
		snake_part_2_y = 0
				
		snake_part_dir_sel = random.randrange(0,3) #0: left, #1: right, 2: up, 3: down
		if snake_part_dir_sel == 0: #part 1, left
			snake_part_1_x = snake_head_x - _SNAKE_SIZE
			snake_part_1_y = snake_head_y

			snake_part_dir_sel = random.randrange(0,2) #0: left, #1: up, #2: down
			if snake_part_dir_sel == 0: #part 2, left
				snake_part_2_x = snake_part_1_x - _SNAKE_SIZE
				snake_part_2_y = snake_part_1_y
			elif snake_part_dir_sel == 1: #part 2, up
				snake_part_2_x = snake_part_1_x
				snake_part_2_y = snake_part_1_y + _SNAKE_SIZE
			elif snake_part_dir_sel == 2: #part 2, down
				snake_part_2_x = snake_part_1_x
				snake_part_2_y = snake_part_1_y - _SNAKE_SIZE

		elif snake_part_dir_sel == 1: #part 1, right
			snake_part_1_x = snake_head_x + _SNAKE_SIZE
			snake_part_1_y = snake_head_y

			snake_part_dir_sel = random.randrange(0,2) #0: right, #1: up, #2: down
			if snake_part_dir_sel == 0: #part 2, right
				snake_part_2_x = snake_part_1_x + _SNAKE_SIZE
				snake_part_2_y = snake_part_1_y
			elif snake_part_dir_sel == 1: #part 2, up
				snake_part_2_x = snake_part_1_x
				snake_part_2_y = snake_part_1_y + _SNAKE_SIZE
			elif snake_part_dir_sel == 2: #part 2, down
				snake_part_2_x = snake_part_1_x
				snake_part_2_y = snake_part_1_y - _SNAKE_SIZE

		elif snake_part_dir_sel == 2: #part 1, up
			snake_part_1_x = snake_head_x
			snake_part_1_y = snake_head_y + _SNAKE_SIZE

			snake_part_dir_sel = random.randrange(0,2) #0: left, #1: right, #2: up
			if snake_part_dir_sel == 0: #part 2, left
				snake_part_2_x = snake_part_1_x - _SNAKE_SIZE
				snake_part_2_y = snake_part_1_y
			elif snake_part_dir_sel == 1: #part 2, right
				snake_part_2_x = snake_part_1_x + _SNAKE_SIZE
				snake_part_2_y = snake_part_1_y
			elif snake_part_dir_sel == 2: #part 2, up
				snake_part_2_x = snake_part_1_x
				snake_part_2_y = snake_part_1_y + _SNAKE_SIZE

		elif snake_part_dir_sel == 3: #part 1, down
			snake_part_1_x = snake_head_x
			snake_part_1_y = snake_head_y - _SNAKE_SIZE

			snake_part_dir_sel = random.randrange(0,2) #0: left, #1: right, #2: down
			if snake_part_dir_sel == 0: #part 2, left
				snake_part_2_x = snake_part_1_x - _SNAKE_SIZE
				snake_part_2_y = snake_part_1_y
			elif snake_part_dir_sel == 1: #part 2, right
				snake_part_2_x = snake_part_1_x + _SNAKE_SIZE
				snake_part_2_y = snake_part_1_y
			elif snake_part_dir_sel == 2: #part 2, up
				snake_part_2_x = snake_part_1_x
				snake_part_2_y = snake_part_1_y - _SNAKE_SIZE

		self.snake_body = [[snake_head_x, snake_head_y], [snake_part_1_x, snake_part_1_y], [snake_part_2_x, snake_part_2_y]]
		self.snake_head = [snake_head_x, snake_head_y]
		#endregion		

		#region <RESET - Observation>
		#Where is the apple located, exactly?
		#0
		apple_pos_x = self.apple_position[0]
		#1
		apple_pos_y = self.apple_position[1]

		#2
		#What is the snake position relative to the apple position?
		#This parameter essentially points direction.
		# (-) in x means apple is left of snake, (+) in x means apple is to the right of snake
		rel_delta_x_to_apple = self.apple_position[0] - self.snake_head[0]
		#3
		# (-) in y means apple is below of snake, (+) in y means apple is above the snake
		rel_delta_y_to_apple = self.apple_position[1] - self.snake_head[1]		

		#4 - 63
		#this doesn't need to be 'self' since it's being constructed from the snake body buffer and then appended to the observation
		snake_body_components_buffer = deque(maxlen=SNAKE_LEN_POS_DATA)
		for _ in range(SNAKE_LEN_POS_DATA):
			snake_body_components_buffer.append(-1)

		j = 0
		for i in range(len(self.snake_body)):
			snake_body_components_buffer[j] = self.snake_body[i][0]
			j += 1
			snake_body_components_buffer[j] = self.snake_body[i][1]
			j += 1
		#endregion

		self.observation = [apple_pos_x, apple_pos_y, rel_delta_x_to_apple, rel_delta_y_to_apple] + list(snake_body_components_buffer)
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