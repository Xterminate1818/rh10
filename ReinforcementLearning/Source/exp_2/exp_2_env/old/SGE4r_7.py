import gymnasium as gym
from gymnasium import spaces

import random
import numpy as np
import pygame

from typing import Optional
from collections import deque

from pathlib import Path

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

#region <GLOBAL - DEBUG>
	#STEP
#_SHOW_OBSERVATIONS_END_OF_STEP = False #show individual observations each time step?
_SHOW_REWARDS_END_OF_STEP = False #show individual rewards each time step?

	#EPISODE
_SHOW_EPISODE_START_END_MSG = False #show why the episode ended
_SHOW_AVG_REWARDS_END_OF_EPISODE = False #show average individual rewards by the end of the episode?

	#TRAINING
_SHOW_COUNTERS_END_OF_TRAINING = True #show counters (avg apples per episode, how many times terminated due to collision w self, etc.) at the end of training
#endregion

#region <GLOBAL - Settings>
#It is desired for the snake to be x units long.
SNAKE_LEN_GOAL = 30
#A single snake part has 2 parameters, x and y, so...
SNAKE_LEN_POS_DATA = SNAKE_LEN_GOAL * 2
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
	def __init__(self, run_name: Optional[str] = "Evaluation", render_mode: Optional[str] = "human"):
		super(SnakeGameEnv, self).__init__()
	   
		#region <INIT - DEBUG>
		if _SHOW_COUNTERS_END_OF_TRAINING:
			self.dbg_episodes_counter = 0 #calling Reset adds 1 to this counter...
			self.dbg_terminated_counter = 0 #when an episode ends, this counter increments by 1...
			self.dbg_terminated_max_apples = 0 #increments by 1 if the snake obtains ALL apples
			self.dbg_terminated_coll_self = 0 #increments by 1 if the snake collides w self
			self.dbg_terminated_coll_bound = 0 #increments by 1 if the snake collides w bound
			self.dbg_terminated_time_out = 0 #increments by 1 if the snake times out
		#endregion

		#region <INIT - System>
		self.maxStepsPerEpisode = 16000
		#endregion

		#region <INIT - Reward Values>
		self.rewValue_for_grabbing_apple = 50
		self.rewValue_for_reaching_max_apples = 1500
		self.rewValue_for_delta_distance_to_apple = 2
		self.rewValue_for_colliding_w_self = -2
		self.timeCoefficient_for_colliding_w_self = 1
		self.rewValue_for_colliding_w_bound = -2
		self.timeCoefficient_for_colliding_w_bound = 1
		self.rewValue_for_timing_out = -3
		self.timeCoefficient_for_timing_out = 1
		#endregion

		#region <INIT - Render Related>
		self.render_mode = render_mode
		self.run_name = run_name
		self.screen: Optional[pygame.Surface] = None
		self.clock = None
		#endregion

		self.action_space = spaces.Discrete(4)		
		self.observation_space = spaces.Box(low=-500, high=500, shape=(7 + SNAKE_LEN_POS_DATA,), dtype=np.int64)
	
	#----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
	
	#STEP
	def step(self, action):
		self.timesteps += 1
		term_reason = 0

		#region <STEP - Reward Buffers>
		#buffers for possible rewards this step, actual values set in env init
		#run-time rewards
		reward_for_grabbing_apple = 0
		reward_for_delta_distance_to_apple = 0

		#terminal rewards
		reward_for_reaching_max_apples = 0
		reward_for_colliding_w_self = 0
		reward_for_colliding_w_bound = 0
		reward_for_timing_out = 0
		#endregion
		
		#Move the snake's head based on the action taken
		if action == 0:
			self.snake_head[0] -= 10 #left
			vel_x = -10
			vel_y = 0
		elif action == 1:
			self.snake_head[0] += 10 #right
			vel_x = 10
			vel_y = 0
		elif action == 2:
			self.snake_head[1] += 10 #up
			vel_x = 0
			vel_y = 10
		elif action == 3:
			self.snake_head[1] -= 10 #down	
			vel_x = 0
			vel_y = -10

		#distance-based scaling to reward run-time distance-based progress
		#First we determine how far is the snake from the apple
		#We invert it, since we want to reward well for being close and reward harshly for being far
		Euclid_Dist_to_Apple = np.linalg.norm(np.array(self.snake_head) - np.array(self.apple_position))
		Inverted_Euclid_Dist_to_Apple = -1 * Euclid_Dist_to_Apple

		#The distance range is 500 to 0, with 500 being super far and 0 being right on target, 250 would be the midpoint...
		#The reward range is -2 to 2, with -2 being awarded when distance is 500 and 2 being awarded when being right on target, the midpoint would be 0...
		oldMax = 0
		oldMin = -500
		newMax = self.rewValue_for_delta_distance_to_apple
		newMin = -1 * self.rewValue_for_delta_distance_to_apple
		oldRange = (oldMax - oldMin)
		newRange = (newMax - newMin)
		adjusted_reward_for_delta_distance_to_apple = (((Inverted_Euclid_Dist_to_Apple - oldMin) * newRange) / oldRange) + newMin
		 
		reward_for_delta_distance_to_apple = adjusted_reward_for_delta_distance_to_apple
		if _SHOW_AVG_REWARDS_END_OF_EPISODE:
			self.dbg_reward_for_delta_distance_to_apple += reward_for_delta_distance_to_apple

		#The issue with the "adjusted reward for delta distance to apple" is that it establishes a "green" zone and a "red" zone in the mind of the agent
			#As a result of these zones, the agent does learn to get as close as possible to the apple, but it will avoid actually touching it
			#We solve this by caching the reward that was obtained when in the green zone...
			#With these parmeters, the green zone is anything in the range 0 to 250
			#So we just have to ensure that the termination conditions have a punishment that is strong enough to defeat going in circles for a long time, but it must not slash the reward for grabbing the apples...

		#Process what happens if the snake's head hits an apple as a result of the action taken
		if self.snake_head == self.apple_position:
			self.apple_position = collision_with_apple(self.apple_position) #move the apple somewhere random (this is for next frame)	
			self.apple_count += 1
			self.snake_body_actual_length += 1
			reward_for_grabbing_apple = self.rewValue_for_grabbing_apple		#fill the apple reward buffer
			if _SHOW_AVG_REWARDS_END_OF_EPISODE:
				self.dbg_reward_for_grabbing_apple += reward_for_grabbing_apple
			#print(f"got an apple, the value of the reward for this is:{reward_for_grabbing_apple}")
			self.snake_body.insert(0,list(self.snake_head)) 				#Attach the apple that was eaten to the snake (this increases the length of the snake)
		else: #Process what happens if the snake's head does NOT hit an apple as a result of the action taken
			self.snake_body.insert(0,list(self.snake_head))					#Attach the empty space that was moved into to the snake
			self.snake_body.pop()											#remove the last body part in the list
																			#this sequence results in the actual movement of the snake		

		#region <STEP - Reward Processing - Terminal>
		#Check if the max snake length has been reached
		if self.apple_count >= SNAKE_LEN_GOAL and self.terminated == False:
			term_reason = 1

			reward_for_reaching_max_apples = self.rewValue_for_reaching_max_apples
			self.terminated = True

			if _SHOW_COUNTERS_END_OF_TRAINING:
				self.dbg_terminated_counter += 1
				self.dbg_terminated_max_apples += 1

		#Check if collided with self and process the result of having done so
		if collision_with_self(self.snake_body) == 1 and self.terminated == False:
			term_reason = 2		
			
			#clear run-time rewards...
			#reward_for_grabbing_apple = 0
			#reward_for_delta_distance_to_apple = 0

			reward_for_colliding_w_self = self.rewValue_for_colliding_w_self + (-1 * self.timeCoefficient_for_colliding_w_self * self.timesteps)
			self.terminated = True

			if _SHOW_COUNTERS_END_OF_TRAINING:
				self.dbg_terminated_counter += 1
				self.dbg_terminated_coll_self += 1

		#Check if collided with the map boundary and process the result of having done so
		if collision_with_boundaries(self.snake_head) == 1 and self.terminated == False:
			term_reason = 3

			#clear run-time rewards...
			#reward_for_grabbing_apple = 0
			#reward_for_delta_distance_to_apple = 0

			reward_for_colliding_w_bound = self.rewValue_for_colliding_w_bound + (-1 * self.timeCoefficient_for_colliding_w_bound * self.timesteps)
			self.terminated = True	

			if _SHOW_COUNTERS_END_OF_TRAINING:
				self.dbg_terminated_counter += 1	
				self.dbg_terminated_coll_bound += 1		

		#check if the max timesteps has been reached
		if self.timesteps > self.maxStepsPerEpisode and self.terminated == False:
			term_reason = 4

			reward_for_timing_out = self.rewValue_for_timing_out + (-1 * self.timeCoefficient_for_timing_out * self.timesteps)
			self.terminated = True

			if _SHOW_COUNTERS_END_OF_TRAINING:
				self.dbg_terminated_counter += 1
				self.dbg_terminated_time_out += 1
		#endregion

		#region <STEP - Reward Summation>		
		reward_for_this_step = reward_for_grabbing_apple + reward_for_delta_distance_to_apple + reward_for_reaching_max_apples + reward_for_colliding_w_bound + reward_for_colliding_w_self + reward_for_timing_out
		reward_for_this_step = round(reward_for_this_step, 5)
		self.reward = reward_for_this_step
		if _SHOW_AVG_REWARDS_END_OF_EPISODE:
			self.dbg_reward += self.reward	
		#endregion

		#region <STEP - Observation>
		#Where is the apple located, exactly?
		#0
		apple_pos_x = self.apple_position[0] #gets updated when the agent hits an apple
		#1
		apple_pos_y = self.apple_position[1]

		#2 - 61
		#where am I?
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

		#62
		#how many body components do I have?
		#WARNING: This is only updated when an apple is eaten...minimum should always be 3...
		#self.snake_body_actual_length = 3

		#63
		#What is the snake position relative to the apple position?
		#This parameter essentially points direction.
		# (-) in x means apple is left of snake, (+) in x means apple is to the right of snake
		rel_delta_x_to_apple = self.apple_position[0] - self.snake_head[0]
		#64
		# (-) in y means apple is below of snake, (+) in y means apple is above the snake
		rel_delta_y_to_apple = self.apple_position[1] - self.snake_head[1]		

		#65
		#What is my velocity?
		#This parameter tells the snake in which direction is it currently going.
		#WARNING: This is updated at run-time in step
		#vel_x = 0
		#66
		#vel_y = 0	
		#endregion
		
		self.observation = [apple_pos_x, apple_pos_y] + list(snake_body_components_buffer) + [self.snake_body_actual_length, rel_delta_x_to_apple, rel_delta_y_to_apple, vel_x, vel_y]
		self.observation = np.array(self.observation)

		self.info = {}
		self.truncated = False
		if self.render_mode == "human":
			self.render()
		
		#region <GLOBAL - DEBUG>
			#STEP
		if _SHOW_REWARDS_END_OF_STEP:
			print(f"	reward_for_grabbing_apple: {reward_for_grabbing_apple}")
			print(f"	reward_for_delta_distance_to_apple: {reward_for_delta_distance_to_apple}")
			print(f"	reward_for_reaching_max_apples: {reward_for_reaching_max_apples}")
			print(f"	reward_for_colliding_w_bound: {reward_for_colliding_w_bound}")
			print(f"	reward_for_colliding_w_self: {reward_for_colliding_w_self}")
			print(f"	reward_for_timing_out: {reward_for_timing_out}")
			print(f"	reward_for_this_step: {reward_for_this_step}\n")

			#EPISODE
		if self.terminated:
			if _SHOW_AVG_REWARDS_END_OF_EPISODE:
				print(f"	avg_reward_for_grabbing_apple: {(self.dbg_reward_for_grabbing_apple / self.timesteps)}")
				print(f"	avg_reward_for_delta_distance_to_apple: {(self.dbg_reward_for_delta_distance_to_apple / self.timesteps)}")
				print(f"	avg_reward_per_step: {(self.dbg_reward / self.timesteps)}")
			if _SHOW_EPISODE_START_END_MSG:
				if term_reason == 1:					
					print(f"END (Reached Max Apples)\n")
				elif term_reason == 2:
					print(f"END (Collided w Self)\n")
				elif term_reason == 3:
					print(f"END (Collided w Boundary)\n")
				elif term_reason == 4:
					print(f"END (Timed Out)\n")
		#endregion

		#print(f"action: {action}")
		#print(f"obs: {self.observation}, rew: {self.reward}, term: {self.terminated}")
		return self.observation, self.reward, self.terminated, self.truncated, self.info
	
	#----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

	#RESET
	def reset(self, seed=None, options=None):
		if _SHOW_EPISODE_START_END_MSG:
			print(f"START (Reset)")

		#region <RESET - Debug>
		if _SHOW_AVG_REWARDS_END_OF_EPISODE:
			self.dbg_reward_for_grabbing_apple = 0
			self.dbg_reward_for_delta_distance_to_apple = 0
			self.dbg_reward = 0

		if _SHOW_COUNTERS_END_OF_TRAINING:
			self.dbg_episodes_counter += 1		
		#endregion

		#region <RESET - System>
		self.terminated = False
		self.reward = 0
		self.apple_count = 0 #used to calculate reward for catching an apple...
		self.timesteps = 0 #limit is 8000
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

		#region <RESET - Reward>
		#See "distance-based scaling to reward run-time distance-based progress" in step for details about how this parameter is used...
		self.green_zone_reward = 0
		#endregion

		#region <RESET - Observation>
		#Where is the apple located, exactly?
		#0
		apple_pos_x = self.apple_position[0] #gets updated when the agent hits an apple
		#1
		apple_pos_y = self.apple_position[1]

		#2 - 61
		#where am I?
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

		#62
		#how many body components do I have?
		#on init/reset, it's 3 body parts
		self.snake_body_actual_length = 3

		#63
		#What is the apple position relative to the snake position?
		#This parameter essentially points direction to the apple.
		# (-) in x means apple is left of snake, (+) in x means apple is to the right of snake
		rel_delta_x_to_apple = self.apple_position[0] - self.snake_head[0]
		#64
		# (-) in y means apple is below of snake, (+) in y means apple is above the snake
		rel_delta_y_to_apple = self.apple_position[1] - self.snake_head[1]

		#65
		#What is my velocity?
		#This parameter tells the snake in which direction is it currently going.
		#on init/reset it would be zero...
		vel_x = 0
		#66
		vel_y = 0
		#endregion

		self.observation = [apple_pos_x, apple_pos_y] + list(snake_body_components_buffer) + [self.snake_body_actual_length, rel_delta_x_to_apple, rel_delta_y_to_apple, vel_x, vel_y]
		self.observation = np.array(self.observation)
	
		self.info = {}
		if self.render_mode == "human":
			self.render()
		return self.observation, self.info	
		
	#----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

	#Call this from trainer script to check whether the epoch-based debug info should be shown...
	def DEBUG_CHECK(self): 
		return _SHOW_COUNTERS_END_OF_TRAINING
	
	def DEBUG_OUTPUT(self):
		print(f"episodes: {self.dbg_episodes_counter}")
		print(f"terminations: {self.dbg_terminated_counter}")
		print(f"term max apples: {self.dbg_terminated_max_apples}")
		print(f"term coll w self: {self.dbg_terminated_coll_self}")
		print(f"term coll w bound: {self.dbg_terminated_coll_bound}")
		print(f"term time out: {self.dbg_terminated_time_out}")

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
		_APPLE_COLOR = (255, 0, 0)
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
			_FILE_NAME = Path(__file__).stem #we fetch the name of this script and remove the .py
			_RUN_NAME = self.run_name
			_DISPLAY_NAME = f"{_FILE_NAME} {_RUN_NAME}"
			pygame.display.set_caption(_DISPLAY_NAME)
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
		elif mode == "rgb_array":
			return np.transpose(
				np.array(pygame.surfarray.pixels3d(self.surf)), axes=(1, 0, 2)
			)
		#endregion