import numpy as np

apple_position = [120, 90]
snake_head_on_activity_start = [140, 240]
rewValue = 0

#on INIT, we set the rew scale based on spawn positions
delta_distance_on_activity = np.linalg.norm(np.array(snake_head_on_activity_start) - np.array(apple_position))
prev_delta_pos = delta_distance_on_activity

oldMax = 0
oldMin = delta_distance_on_activity
newMax = 2
newMin = 0
oldRange = (oldMax - oldMin)
newRange = (newMax - newMin)

#the snake moves...
new_snake_pos = [130, 240] #m1

#we check if the snake was closer or farther than the previous step, and give reward based on that...
new_delta_pos = np.linalg.norm(np.array(new_snake_pos) - np.array(apple_position))
if new_delta_pos < prev_delta_pos:
    print("the snake got closer...")
    rewValue = (((new_delta_pos - oldMin) * newRange) / oldRange) + newMin
else:
    print("the snake got farther...")
    rewValue = 0
prev_delta_pos = new_delta_pos
print(f"newValue: {rewValue}")

#snake moves again
new_snake_pos = [130, 230] #m2

#we check if the snake was closer or farther than the previous step, and give reward based on that...
new_delta_pos = np.linalg.norm(np.array(new_snake_pos) - np.array(apple_position))
if new_delta_pos < prev_delta_pos:
    print("the snake got closer...")
    rewValue = (((new_delta_pos - oldMin) * newRange) / oldRange) + newMin
else:
    print("the snake got farther...")
    rewValue = 0
prev_delta_pos = new_delta_pos
print(f"newValue: {rewValue}")

#snake moves again
new_snake_pos = [120, 230] #m3

#we check if the snake was closer or farther than the previous step, and give reward based on that...
new_delta_pos = np.linalg.norm(np.array(new_snake_pos) - np.array(apple_position))
if new_delta_pos < prev_delta_pos:
    print("the snake got closer...")
    rewValue = (((new_delta_pos - oldMin) * newRange) / oldRange) + newMin
else:
    print("the snake got farther...")
    rewValue = 0
prev_delta_pos = new_delta_pos
print(f"newValue: {rewValue}")

#snake moves again
new_snake_pos = [120, 240] #m4

#we check if the snake was closer or farther than the previous step, and give reward based on that...
new_delta_pos = np.linalg.norm(np.array(new_snake_pos) - np.array(apple_position))
if new_delta_pos < prev_delta_pos:
    print("the snake got closer...")
    rewValue = (((new_delta_pos - oldMin) * newRange) / oldRange) + newMin
else:
    print("the snake got farther...")
    rewValue = 0
prev_delta_pos = new_delta_pos
print(f"newValue: {rewValue}")

#snake moves again
new_snake_pos = [130, 240] #m5

#we check if the snake was closer or farther than the previous step, and give reward based on that...
new_delta_pos = np.linalg.norm(np.array(new_snake_pos) - np.array(apple_position))
if new_delta_pos < prev_delta_pos:
    print("the snake got closer...")
    rewValue = (((new_delta_pos - oldMin) * newRange) / oldRange) + newMin
else:
    print("the snake got farther...")
    rewValue = 0
prev_delta_pos = new_delta_pos
print(f"newValue: {rewValue}")

#snake moves again
new_snake_pos = [140, 240] #m6

#we check if the snake was closer or farther than the previous step, and give reward based on that...
new_delta_pos = np.linalg.norm(np.array(new_snake_pos) - np.array(apple_position))
if new_delta_pos < prev_delta_pos:
    print("the snake got closer...")
    rewValue = (((new_delta_pos - oldMin) * newRange) / oldRange) + newMin
else:
    print("the snake got farther...")
    rewValue = 0
prev_delta_pos = new_delta_pos
print(f"newValue: {rewValue}")
