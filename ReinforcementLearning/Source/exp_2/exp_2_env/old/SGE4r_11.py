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
	def __init__(self, dbg_report_dir = "", render_run_str: Optional[str] = "Evaluation", render_mode: Optional[str] = "human"):
		super(SnakeGameEnv, self).__init__()
	   
		#region <INIT - DEBUG>
		#WARNING: If evaluating the model this variable should be False
		self.dbg_enable = True
		self.report_dir = dbg_report_dir 		#Where should the end of training report be placed?

		#time-tracking
		self.DBG_timesteps_counter = 0 			#Used to determine which timestep we are in, 0 to 10,000, should match _TIMESTEPS_PER_CHECKPOINT, updated on step start
		self.DBG_checkpoint_counter = 0 		#Used to determine which checkpoint we are in, 1 to _TOTAL_CHECKPOINTS, updated on reset if DBG_timesteps_counter is > 10,000

		#During a checkpoint
		self.DBG_checkpoint_high_score = 0				#Used to keep track of what the high score is THIS checkpoint, updates if the highscore is beat during an episode
		self.DBG_checkpoint_preamble_done = False	#Have we written the checkpoint preamble already (runs on start of new Checkpoint), resets in reset function when a checkpoint flip happens
		#exported to TensorBoard via info buffer at end of step
		self.DBG_performance_points = 0				#Used to quickly identify top performer checkpoints. Adds to the score whenever a HS is reached.

		#End of Training
		self.DBG_best_performance_points = 0
		self.DBG_best_pp_timesteps = 0
		self.DBG_best_pp_checkpoint = 0			

		#Buffer where all logs are stored until the training session ends, printed on env.close()
		self.DBG_TRAINING_REPORT = [
			"----- TRAINING REPORT -----",
			"----- ----- ----- ----- ----- ----- ----- ----- ----- -----",
			"----- ----- ----- ----- ----- ----- ----- ----- ----- -----"
		]

		self.DBG_episode_count = 0 							#Updated when an episode terminates
		self.DBG_terminated_due_to_collision_w_self = 0 	#Updated when a snake collides w self
		self.DBG_terminated_due_to_collision_w_bound = 0 	#Updated when a snake collides w bound
		self.DBG_terminated_due_to_time_out = 0 			#Updated when a snake hits the episode time limit
		#endregion

		#region <INIT - System>
		self.snake_len_goal = 30
		self.snake_len_pos_data = self.snake_len_goal * 2
		self.maxStepsPerEpisode = 16000
		#endregion

		#region <INIT - Reward Values>
		self.rewValue_for_grabbing_apple = 50
		self.rewValue_for_reaching_max_apples = 500
		self.scaleCoefficient_for_delta_distance_to_apple = 0.001
		self.rewValue_for_colliding_w_self = -2
		self.timeCoefficient_for_colliding_w_self = 0.05
		self.rewValue_for_colliding_w_bound = -2
		self.timeCoefficient_for_colliding_w_bound = 0.05
		self.rewValue_for_timing_out = -4
		self.timeCoefficient_for_timing_out = 0.05
		#endregion

		#region <INIT - Render Related>
		self.render_mode = render_mode
		self.run_name = render_run_str
		self.screen: Optional[pygame.Surface] = None
		self.clock = None
		#endregion

		self.action_space = spaces.Discrete(4)		
		self.observation_space = spaces.Box(low=-500, high=500, shape=(7 + self.snake_len_pos_data,), dtype=np.int64)
	
	#----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
	
	#STEP
	def step(self, action):
		
		#region <STEP - DEBUG>
		self.DBG_timesteps_counter += 1
		#endregion

		self.ep_timesteps += 1

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

		#distance-based reward
		Euclid_Dist_to_Apple = np.linalg.norm(np.array(self.snake_head) - np.array(self.apple_position))
		Inverted_Euclid_Dist_to_Apple = -1 * Euclid_Dist_to_Apple
		 
		reward_for_delta_distance_to_apple = Inverted_Euclid_Dist_to_Apple * self.scaleCoefficient_for_delta_distance_to_apple

		#Process what happens if the snake's head hits an apple as a result of the action taken
		if self.snake_head == self.apple_position:
			self.apple_position = collision_with_apple(self.apple_position) #move the apple somewhere random (this is for next frame)	

			self.apple_count += 1
			self.snake_body_actual_length += 1

			reward_for_grabbing_apple = self.rewValue_for_grabbing_apple		#fill the apple reward buffer

			self.snake_body.insert(0,list(self.snake_head)) 				#Attach the apple that was eaten to the snake (this increases the length of the snake)

			#region	<STEP - DEBUG>
			# Episode to Episode Info
			if self.dbg_enable:
				if self.apple_count > self.DBG_checkpoint_high_score:
					self.DBG_checkpoint_high_score = self.apple_count
					self.DBG_performance_points += self.apple_count
					self.DBG_TRAINING_REPORT.append(f"({self.DBG_checkpoint_counter}, {self.DBG_timesteps_counter}, {(self.DBG_checkpoint_counter * 10000) + self.DBG_timesteps_counter}) - NEW Episode HS: {self.DBG_checkpoint_high_score}")
				elif self.apple_count == self.DBG_checkpoint_high_score:				
					self.DBG_performance_points += self.apple_count						
					self.DBG_TRAINING_REPORT.append(f"({self.DBG_checkpoint_counter}, {self.DBG_timesteps_counter}, {(self.DBG_checkpoint_counter * 10000) + self.DBG_timesteps_counter}) - - - - - Repeat Episode HS: {self.DBG_checkpoint_high_score}")	

				# End of Training Info
				if self.DBG_performance_points > self.DBG_best_performance_points:
					self.DBG_best_performance_points = self.DBG_performance_points
					self.DBG_best_pp_timesteps = self.DBG_timesteps_counter
					self.DBG_best_pp_checkpoint = self.DBG_checkpoint_counter
			#endregion

		else: #Process what happens if the snake's head does NOT hit an apple as a result of the action taken
			self.snake_body.insert(0,list(self.snake_head))					#Attach the empty space that was moved into to the snake
			self.snake_body.pop()											#remove the last body part in the list
																			#this sequence results in the actual movement of the snake		

		#region <STEP - Reward Processing - Terminal>
		#Check if the max snake length has been reached
		if self.apple_count >= self.snake_len_pos_data and self.terminated == False:
			reward_for_reaching_max_apples = self.rewValue_for_reaching_max_apples
			self.terminated = True

		#Check if collided with self and process the result of having done so
		if collision_with_self(self.snake_body) == 1 and self.terminated == False:	
			#Total amount of times the agent terminated due to collision w self during the training session is displayed at the very end of training...			
			self.DBG_terminated_due_to_collision_w_self += 1

			reward_for_colliding_w_self = self.rewValue_for_colliding_w_self + (-1 * self.timeCoefficient_for_colliding_w_self * self.ep_timesteps)
			self.terminated = True

		#Check if collided with the map boundary and process the result of having done so
		if collision_with_boundaries(self.snake_head) == 1 and self.terminated == False:
			#Total amount of times the agent terminated due to collision w boundary during the training session is displayed at the very end of training...
			self.DBG_terminated_due_to_collision_w_bound += 1

			reward_for_colliding_w_bound = self.rewValue_for_colliding_w_bound + (-1 * self.timeCoefficient_for_colliding_w_bound * self.ep_timesteps)
			self.terminated = True

		#check if the max timesteps has been reached
		if self.ep_timesteps > self.maxStepsPerEpisode and self.terminated == False:
			#Total amount of times the agent terminated due to time out during the training session is displayed at the very end of training...
			self.DBG_terminated_due_to_time_out += 1

			reward_for_timing_out = self.rewValue_for_timing_out + (-1 * self.timeCoefficient_for_timing_out * self.ep_timesteps)
			self.terminated = True
		#endregion

		#region <STEP - Reward Summation>		
		reward_for_this_step = reward_for_grabbing_apple + reward_for_delta_distance_to_apple + reward_for_reaching_max_apples + reward_for_colliding_w_bound + reward_for_colliding_w_self + reward_for_timing_out
		#reward_for_this_step = round(reward_for_this_step, 5)
		self.reward = reward_for_this_step
		#endregion

		if self.terminated:
			self.DBG_episode_count += 1	

		#region <STEP - Construct Observation>
		#Where is the apple located, exactly?
		#0
		apple_pos_x = self.apple_position[0] #gets updated when the agent hits an apple
		#1
		apple_pos_y = self.apple_position[1]

		#2 - 61
		#where am I?
		#this doesn't need to be 'self' since it's being constructed from the snake body buffer and then appended to the observation
		snake_body_components_buffer = deque(maxlen=self.snake_len_pos_data)
		for _ in range(self.snake_len_pos_data):
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

		self.observation = [apple_pos_x, apple_pos_y] + list(snake_body_components_buffer) + [self.snake_body_actual_length, rel_delta_x_to_apple, rel_delta_y_to_apple, vel_x, vel_y]
		self.observation = np.array(self.observation)
		#endregion
		
		#region <STEP - Construct Info>
		self.info = {
			"performance_points" : self.DBG_performance_points
		}
		#endregion

		self.truncated = False

		if self.render_mode == "human":
			self.render()

		return self.observation, self.reward, self.terminated, self.truncated, self.info
	
	#----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

	#RESET
	def reset(self, seed=None, options=None):

		#region <RESET - DEBUG>
		#This should only run on checkpoint start
		if self.dbg_enable:
			if not self.DBG_checkpoint_preamble_done:
				self.DBG_TRAINING_REPORT.append(f"CHECKPOINT: {self.DBG_checkpoint_counter}")
				self.DBG_checkpoint_preamble_done = True

			#This causes checkpoint end
			if self.DBG_timesteps_counter >= 10000:
				self.DBG_timesteps_counter -= 10000
				self.DBG_checkpoint_counter += 1	

				self.DBG_checkpoint_high_score = 0 #New checkpoint so we reset the current highscore	
				self.DBG_TRAINING_REPORT.append(f"Performance Points: {self.DBG_performance_points}")
				self.DBG_performance_points = 0	

				#we reset this flag since new checkpoint is about to begin
				self.DBG_checkpoint_preamble_done = False
				
				self.DBG_TRAINING_REPORT.append(f"----- ----- ----- ----- ----- ----- ----- ----- ----- -----")	
		#endregion

		#region <RESET - System>
		self.terminated = False
		self.reward = 0
		self.apple_count = 0 #used to calculate reward for catching an apple...
		self.ep_timesteps = 0 #limit is 8000
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

		#region <RESET - Construct Observation>
		#Where is the apple located, exactly?
		#0
		apple_pos_x = self.apple_position[0] #gets updated when the agent hits an apple
		#1
		apple_pos_y = self.apple_position[1]

		#2 - 61
		#where am I?
		#this doesn't need to be 'self' since it's being constructed from the snake body buffer and then appended to the observation
		snake_body_components_buffer = deque(maxlen=self.snake_len_pos_data)
		for _ in range(self.snake_len_pos_data):
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

		self.observation = [apple_pos_x, apple_pos_y] + list(snake_body_components_buffer) + [self.snake_body_actual_length, rel_delta_x_to_apple, rel_delta_y_to_apple, vel_x, vel_y]
		self.observation = np.array(self.observation)
		#endregion

		#region <RESET - Construct Info>
		self.info = {
			"performance_points" : self.DBG_performance_points
		}
		#endregion
		
		if self.render_mode == "human":
			self.render()

		return self.observation, self.info	
		
	#----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

	#CLOSE
	def close(self):
		if self.dbg_enable:
			self.DEBUG_PRINT_END_OF_TRAINING_DATA()
			self.DEBUG_REPORT_END_OF_TRAINING_DATA()

		return super().close()
	
	def DEBUG_PRINT_END_OF_TRAINING_DATA(self):
		for x in range(len(self.DBG_TRAINING_REPORT)):
			print(self.DBG_TRAINING_REPORT[x])

		print("----- ----- ----- ----- ----- ----- ----- ----- ----- -----")
		print("----- ----- ----- ----- ----- ----- ----- ----- ----- -----")

		print(f"Best Performance Points ({self.DBG_best_pp_checkpoint}, {self.DBG_best_pp_timesteps}, {(self.DBG_best_pp_checkpoint * 10000) + self.DBG_best_pp_timesteps}): {self.DBG_best_performance_points}")
	
		print("----- ----- ----- ----- ----- ----- ----- ----- ----- -----")
		print("----- ----- ----- ----- ----- ----- ----- ----- ----- -----")

		print(f"Total Episodes: {self.DBG_episode_count}")	

		calculate_percent_col_w_self = (self.DBG_terminated_due_to_collision_w_self / self.DBG_episode_count)	 * 100	
		percent_term_col_w_self = round(calculate_percent_col_w_self, 2)
		print(f"Terminated due to Collision w Self: {self.DBG_terminated_due_to_collision_w_self}, {percent_term_col_w_self}%")	

		calculate_percent_col_w_bound = (self.DBG_terminated_due_to_collision_w_bound / self.DBG_episode_count)	 * 100	
		percent_term_col_w_bound = round(calculate_percent_col_w_bound, 2)
		print(f"Terminated due to Collision w Boundary: {self.DBG_terminated_due_to_collision_w_bound}, {percent_term_col_w_bound}%")

	def DEBUG_REPORT_END_OF_TRAINING_DATA(self):
		if not self.report_dir == None:
			try:
				file = open(self.report_dir, 'a')

				for x in range(len(self.DBG_TRAINING_REPORT)):
					str_to_write = self.DBG_TRAINING_REPORT[x] + "\n"
					file.write(str_to_write)

				file.write("----- ----- ----- ----- ----- ----- ----- ----- ----- -----\n")
				file.write("----- ----- ----- ----- ----- ----- ----- ----- ----- -----\n")

				file.write(f"Best Performance Points ({self.DBG_best_pp_checkpoint}, {self.DBG_best_pp_timesteps}, {(self.DBG_best_pp_checkpoint * 10000) + self.DBG_best_pp_timesteps}): {self.DBG_best_performance_points}\n")

				file.write("----- ----- ----- ----- ----- ----- ----- ----- ----- -----\n")
				file.write("----- ----- ----- ----- ----- ----- ----- ----- ----- -----\n")

				file.write(f"Total Episodes: {self.DBG_episode_count}\n")	

				calculate_percent_col_w_self = (self.DBG_terminated_due_to_collision_w_self / self.DBG_episode_count)	 * 100	
				percent_term_col_w_self = round(calculate_percent_col_w_self, 2)
				file.write(f"Terminated due to Collision w Self: {self.DBG_terminated_due_to_collision_w_self}, {percent_term_col_w_self}%\n")	

				calculate_percent_col_w_bound = (self.DBG_terminated_due_to_collision_w_bound / self.DBG_episode_count)	 * 100	
				percent_term_col_w_bound = round(calculate_percent_col_w_bound, 2)
				file.write(f"Terminated due to Collision w Boundary: {self.DBG_terminated_due_to_collision_w_bound}, {percent_term_col_w_bound}%\n")	

				file.close()				
			except IOError:
				print(f"I/O error: {IOError} when trying to save EOT report to a file.")		

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