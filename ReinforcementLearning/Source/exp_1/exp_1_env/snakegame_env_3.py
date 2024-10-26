import gymnasium as gym
from gymnasium import spaces

import random
import numpy as np
import pygame

from typing import Optional
from collections import deque

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

SNAKE_LEN_GOAL = 30

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
		self.screen: Optional[pygame.Surface] = None
		self.render_mode = "human"
		self.apple_color = (0,0,255)
		self.apple_size = 10
		self.apple_thickness = 3
		self.clock = None
		self.action_space = spaces.Discrete(4)		
		self.observation_space = spaces.Box(low=-500, high=500, shape=(5+SNAKE_LEN_GOAL,), dtype=np.int64)

	def step(self, action):
		self.previous_actions.append(action)

		#cv2.imshow(<window name>, <image to show>)
		#cv2.imshow('a',self.img)
		#cv2.waitkey(<miliseconds>)
		# waits for miliseconds, passing 0 will make it wait for any key to be pressed.
		# necessary after imshow so python kernel doesn't explode
		#cv2.waitKey(1)
		
		#Creates a np array that's 500 by 500 by 3
		#this np array represents an image
		#self.img = np.zeros((500,500,3),dtype='uint8')
		
		# draw an apple onto the image
		#cv2.rectangle(<image on which to draw rectangle>, <start point>, <end point>, <color>, <thickness>)
		#self.apple_start_point = (self.apple_position[0], self.apple_position[1])
		#self.apple_size = 10
		#self.apple_end_point = (self.apple_position[0] + self.apple_size, self.apple_position[1] + self.apple_size)
		#self.apple_color = (0,0,255)
		#self.apple_thickness = 3
		#cv2.rectangle(self.img, self.apple_start_point, self.apple_end_point, self.apple_color, self.apple_thickness)
		
		# Display the snake onto the image
		#cv2.rectangle(<image on which to draw rectangle>, <start point>, <end point>, <color>, <thickness>)
		#remember the snake "parts" are stored in the snake_position var in an array, which is why we for loop through and create a rectangle for each part
		#self.snake_part_size = 10
		#self.snake_color = (0,255,0)
		#self.snake_thickness = 3
		#for position in self.snake_position:
			#start_position = (position[0], position[1])
			#end_position = (position[0] + self.snake_part_size, position[1] + self.snake_part_size)
			#cv2.rectangle(self.img, start_position, end_position, self.snake_color, self.snake_thickness)
		
		# Takes step after fixed time
		#t_end = time.time() + 0.2
		#t_end = time.time() + 0.05
		#k = -1
		#while time.time() < t_end:
			#if k == -1:
				#k = cv2.waitKey(125)
				#k = cv2.waitKey(1)
			#else:
				#continue				
		
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
			
		apple_reward = 0

		# Increase Snake length on eating apple
		if self.snake_head == self.apple_position:
			self.apple_position, self.score = collision_with_apple(self.apple_position, self.score)
			self.snake_position.insert(0,list(self.snake_head))
			apple_reward = 10000

		else:
			#if did not eat an apple...
			#add the latest position of the head to the snake parts list
			self.snake_position.insert(0,list(self.snake_head))
			#remove the last part of the snake, which is now outdated and unecessary
			#if no arg is passed to pop() then the default is used, -1, which is the index of the last item
			self.snake_position.pop()
			#the resulting pattern is that you just add the updated position of the head to the parts list, and now the old parts are the "updated" position of the subsequent parts, except for the last part which is now outdated
			#the position of the head at the previous time step is now the updated position of the part that follows the previous head, and so on, making the last position garbage data
		
		# On collision kill the snake and print the score
		if collision_with_boundaries(self.snake_head) == 1 or collision_with_self(self.snake_position) == 1:
			#font = cv2.FONT_HERSHEY_SIMPLEX
			#self.img = np.zeros((500,500,3),dtype='uint8')
			#cv2.putText(self.img,'Your Score is {}'.format(self.score),(140,250), font, 1,(255,255,255),2,cv2.LINE_AA)
			#cv2.imshow('a',self.img)
			self.terminated = True

		euclidean_dist_to_apple = np.linalg.norm(np.array(self.snake_head) - np.array(self.apple_position))
		self.total_reward = ((250 - euclidean_dist_to_apple) + apple_reward) / 100

		self.reward = self.total_reward - self.prev_reward
		self.prev_reward = self.total_reward

		if self.terminated:
			self.reward = -10

		#head_x, head_y, apple_delta_x, apple_delta_y, snake_length, previous_moves
		head_x = self.snake_head[0]
		head_y = self.snake_head[1]
		apple_delta_x = self.apple_position[0] - head_x
		apple_delta_y = self.apple_position[1] - head_y
		snake_length = len(self.snake_position)
		
		self.observation = [head_x, head_y, apple_delta_x, apple_delta_y, snake_length] + list(self.previous_actions)
		self.observation = np.array(self.observation)

		self.info = {}
		self.truncated = False
		if self.render_mode == "human":
			self.render()
		return self.observation, self.reward, self.terminated, self.truncated, self.info
	
	def reset(self, seed=None, options=None):
		self.terminated = False

		#self.img = np.zeros((500, 500, 3), dtype='uint8')
		# Initial Snake and Apple position
		self.snake_position = [[250, 250], [240, 250], [230, 250]]
		self.apple_position = [random.randrange(1,50)*10,random.randrange(1,50)*10]
		self.score = 0
		self.reward = 0
		self.prev_button_direction = 1
		self.button_direction = 1
		self.snake_head = [250,250]
		
		self.prev_reward = 0

		#head_x, head_y, apple_delta_x, apple_delta_y, snake_length, previous_moves
		head_x = self.snake_head[0]
		head_y = self.snake_head[1]
		apple_delta_x = self.apple_position[0] - head_x
		apple_delta_y = self.apple_position[1] - head_y
		snake_length = len(self.snake_position)
		self.previous_actions = deque(maxlen=SNAKE_LEN_GOAL)
		
		for _ in range(SNAKE_LEN_GOAL):
			self.previous_actions.append(-1)
		
		self.observation = [head_x, head_y, apple_delta_x, apple_delta_y, snake_length] + list(self.previous_actions)
		self.observation = np.array(self.observation)
	
		self.info = {}
		if self.render_mode == "human":
			self.render()
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

		for position in self.snake_position:

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