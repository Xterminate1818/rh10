import gymnasium as gym
from gymnasium import spaces

import random
import numpy as np
import pygame

from typing import Optional
from collections import deque

import time
import cv2

def collision_with_apple(apple_position, score):
	apple_position = [random.randrange(1,50)*10,random.randrange(1,50)*10]
	score += 1
	return apple_position, score

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
#A single snake part has 2 parameters, x and y, so...
SNAKE_LEN_POS_DATA = SNAKE_LEN_GOAL * 2

WINDOW_W = 500
WINDOW_H = 500
FPS = 50  # Frames per second
SCALE = 30.0  # affects how fast-paced the game is, forces should be adjusted as well

class SnakeGameEnv(gym.Env):

	metadata = {
		"render_modes": [
			"human",
			"rgb_array",
			"state_pixels",
		],
		"render_fps": FPS,
	}

	def __init__(self, render_mode: Optional[str] = None):
		super(SnakeGameEnv, self).__init__()

		#<Apple Init>
		self.apple_color = (0,0,255)
		self.apple_size = 10
		self.apple_thickness = 3
		self.collision_w_self = 0
		#</Apple Init>

		self.screen: Optional[pygame.Surface] = None
		self.render_mode = "human"
		self.clock = None
		self.action_space = spaces.Discrete(4)
		#The obs_space SHAPE would be the amount of parameters plus the necessary "slots" to accomodate the maximum possible snake parts data (x and y param)		
		self.observation_space = spaces.Box(low=-500, high=500, shape=(11 + SNAKE_LEN_POS_DATA,), dtype=np.int64)

	def step(self, action):	
		self.episode_length += 1

		collided_w_self = 0 #obs space flag
		collided_w_boundary = 0 #obs space flag

		# Change the head position based on the action direction
		# update the position of the head based on the action that was taken
		if action == 1:
			self.snake_head[0] += 10
		elif action == 0:
			self.snake_head[0] -= 10
		elif action == 2:
			self.snake_head[1] += 10
		elif action == 3:
			self.snake_head[1] -= 10
		
		#Did I change direction from the previous episode?
		if action != self.prev_action and action != -1:
			self.dir_change_count += 1		
			
		reward_for_grabbing_apple = 0
		reward_for_colliding_w_self = 0 #-500
		reward_for_colliding_w_bound = 0 #-500
		reward_for_changing_dir_more_than_5_times = 0 #-10 * dir_change_count (if > 4)
		reward_for_being_too_far_from_apple = 0

		# Increase Snake length on eating apple
		if self.snake_head == self.apple_position:
			self.apple_position, self.score = collision_with_apple(self.apple_position, self.score)
			self.apple_count += 1
			self.dir_change_count = 0
			self.snake_body.insert(0,list(self.snake_head))
			reward_for_grabbing_apple = 10000

		else:
			#if did not eat an apple...
			#add the latest position of the head to the snake parts list
			self.snake_body.insert(0,list(self.snake_head))
			#remove the last part of the snake, which is now outdated and unecessary
			#if no arg is passed to pop() then the default is used, -1, which is the index of the last item
			self.snake_body.pop()
			#the resulting pattern is that you just add the updated position of the head to the parts list, and now the old parts are the "updated" position of the subsequent parts, except for the last part which is now outdated
			#the position of the head at the previous time step is now the updated position of the part that follows the previous head, and so on, making the last position garbage data
		
		if collision_with_boundaries(self.snake_head) == 1:
			collided_w_boundary = 1
			reward_for_colliding_w_bound = -500 * self.episode_length
			self.terminated = True

		if collision_with_self(self.snake_body) == 1:
			collided_w_self = 1
			self.collision_w_self += 1
			reward_for_colliding_w_self = -500 * self.collision_w_self
			self.terminated = True

		#did I change direction too many times between apple captures?
		if self.dir_change_count > 5:
			reward_for_changing_dir_more_than_5_times = self.dir_change_count * -10

		#am I too far from the apple?
		euclidean_dist_to_apple = np.linalg.norm(np.array(self.snake_head) - np.array(self.apple_position))
		reward_for_being_too_far_from_apple = -1 * euclidean_dist_to_apple

		reward_for_this_step = reward_for_grabbing_apple + reward_for_colliding_w_bound + reward_for_colliding_w_self + reward_for_changing_dir_more_than_5_times + reward_for_being_too_far_from_apple
		self.reward = reward_for_this_step		

		if self.terminated:
			self.reward = reward_for_this_step
		
		#Where is the apple located?
		apple_pos_x = self.apple_position[0]
		apple_pos_y = self.apple_position[1]

		#What is my position relative to the apple position?
		#This parameter essentially points direction.
		# (-) in x means apple is to my left, (+) in x means apple is to my right
		rel_delta_x_to_apple = self.apple_position[0] - self.snake_head[0]
		# (-) in y means apple is below me, (+) in y means apple is above me
		rel_delta_y_to_apple = self.apple_position[1] - self.snake_head[1]

		#what is my "true" length?
		snake_length = len(self.snake_body)
		
		#where exactly are the components of my body?
		snake_body_components_buffer = deque(maxlen=SNAKE_LEN_POS_DATA)
		for _ in range(SNAKE_LEN_POS_DATA):
			snake_body_components_buffer.append(-1)

		j = 0
		for i in range(len(self.snake_body)):
			snake_body_components_buffer[j] = self.snake_body[i][0]
			j += 1
			snake_body_components_buffer[j] = self.snake_body[i][1]
			j += 1
		
		#what is the maximum length I can be?
		max_snake_length = len(snake_body_components_buffer)

		#going from apple to apple, what was the most amount of times that I changed my direction?
		self.prev_action = action #this can be values 0 to 4, initialized as -1

		self.observation = [apple_pos_x, apple_pos_y, rel_delta_x_to_apple, rel_delta_y_to_apple] + list(snake_body_components_buffer) + [snake_length, max_snake_length, collided_w_self, collided_w_boundary, self.apple_count, self.prev_action, self.dir_change_count]
		self.observation = np.array(self.observation)

		self.info = {}
		self.truncated = False
		if self.render_mode == "human":
			self.render()
		return self.observation, self.reward, self.terminated, self.truncated, self.info
	
	def reset(self, seed=None, options=None):
		self.score = 0
		self.reward = 0		
		self.prev_reward = 0

		#<System Reset>
		self.terminated = False
		self.episode_length = 0
		#</System Reset>

		#<Apple Reset>
		self.apple_position = [random.randrange(1,500), random.randrange(1,500)]
		#</Apple Reset>

		#<Snake Reset>
		self.snake_body = [[250, 250], [240, 250], [230, 250]]
		self.snake_head = self.snake_body[0]
		#</Snake Reset>		

		#<Observation Space>
		#Where is the apple located, exactly?
		apple_pos_x = self.apple_position[0]
		apple_pos_y = self.apple_position[1]

		#What is the snake position relative to the apple position?
		#This parameter essentially points direction.
		# (-) in x means apple is left of snake, (+) in x means apple is to the right of snake
		rel_delta_x_to_apple = self.apple_position[0] - self.snake_head[0]
		# (-) in y means apple is below of snake, (+) in y means apple is above the snake
		rel_delta_y_to_apple = self.apple_position[1] - self.snake_head[1]

		#what is my "true" length?
		snake_length = len(self.snake_body)
		
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
		
		#what is the maximum length I can be?
		max_snake_length = len(snake_body_components_buffer)

		#did I collide with myself last time?
		collided_w_self = 0

		#did I collide with the boundary last time?
		collided_w_boundary = 0

		#how many apples did I get last time?
		self.apple_count = 0

		#going from apple to apple, what was the most amount of times that I changed my direction?
		self.prev_action = -1 #this can be values 0 to 4, initialized as -1
		self.dir_change_count = 0 #first one is free, same when u grab an apple

		self.observation = [apple_pos_x, apple_pos_y, rel_delta_x_to_apple, rel_delta_y_to_apple] + list(snake_body_components_buffer) + [snake_length, max_snake_length, collided_w_self, collided_w_boundary, self.apple_count, self.prev_action, self.dir_change_count]
		self.observation = np.array(self.observation)
		#</Observation Space>
	
		#<Info>
		self.info = {}
		#</Info>

		#<Rendering>
		if self.render_mode == "human":
			self.render()
		#</Rendering>

		return self.observation, self.info
	
	def render(self):
		if self.render_mode is None:
			assert self.spec is not None
			gym.logger.warn(
				"You are calling render method without specifying any render mode. "
				"You can specify the render_mode at initialization, "
				f'e.g. gym.make("{self.spec.id}", render_mode="rgb_array")'
			)
			return
		else:
			return self._render(self.render_mode)
		
	def _render(self, mode: str):
		assert mode in self.metadata["render_modes"]

		pygame.font.init()
		if self.screen is None and mode == "human":		
			pygame.init()
			pygame.display.init()
			self.screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
		if self.clock is None:		
			self.clock = pygame.time.Clock()

		#if "t" not in self.__dict__:
			#return  # reset() not called yet

		## Actual rendering stuff
		#We create a surface which is the background of the game
		self.surf = pygame.Surface((WINDOW_W, WINDOW_H))	
		#pygame.transform.scale(self.surf, (SCALE, SCALE))
		#we color the background as black
		self.color_black = (0, 0, 0)	
		self.surf.fill(self.color_black)	
		#print(f"screen width: {self.screen.get_rect().w}, screen height: {self.screen.get_rect().h}")
		#print(f"surf width: {self.surf.get_rect().w}, surf height: {self.surf.get_rect().h}")
		# we draw the apple onto the surface
		#pygame.draw.rect(<surface to draw on>, <color>, <rectangle to draw>, <thickness>)
		#print(f"apple position, start point: {self.apple_position[0]},{self.apple_position[1]}")
		#print(f"apple position, end point: {self.apple_position[0] + self.apple_size},{self.apple_position[1] + self.apple_size}")
		pygame.draw.rect(
			self.surf, 
			self.apple_color,
			#pygame.rect(<top-left x pos>, <top-left y pos>, <width>, <height>)
			pygame.Rect(
					self.apple_position[0], 
			   		self.apple_position[1], 
					self.apple_size, 
					self.apple_size
			),
			self.apple_thickness
		)		

		# Now we draw the snake
		self.snake_part_size = 10
		self.snake_color = (0,255,0)
		self.snake_thickness = 3

		for position in self.snake_body:

			pygame.draw.rect(
				self.surf, 
				self.snake_color,
				pygame.Rect(
					position[0], 
					position[1], 
					self.snake_part_size, 
					self.snake_part_size),
				self.snake_thickness
			)		

		# if game ended, end it
		#if collision_with_boundaries(self.snake_head) == 1 or collision_with_self(self.snake_position) == 1:
			#font = cv2.FONT_HERSHEY_SIMPLEX
			#self.img = np.zeros((500,500,3),dtype='uint8')
			#cv2.putText(self.img,'Your Score is {}'.format(self.score),(140,250), font, 1,(255,255,255),2,cv2.LINE_AA)
			#cv2.imshow('a',self.img)
		if mode == "human":		
			pygame.event.pump()
			# We need to ensure that human-rendering occurs at the predefined framerate.
			# The following line will automatically add a delay to keep the framerate stable.
			self.clock.tick(self.metadata["render_fps"])
			assert self.screen is not None
			self.screen.fill(0)
			self.screen.blit(self.surf, (0, 0))
			# The following line copies our drawings from `canvas` to the visible window
			#self.screen.blit(self.surf, self.surf.get_rect())
			pygame.display.update()
			#pygame.display.flip()

			
		else:  # rgb_array
			return np.transpose(
				np.array(pygame.surfarray.pixels3d(self.surf)), axes=(1, 0, 2)
			)