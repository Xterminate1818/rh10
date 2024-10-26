# exp_2

The goal of this experiment is to solve the Snake Game environment. To do so, we start by building upon the codebase from [exp_1](Source/exp_1). As the solution is developed we update the observation function and the reward function between iterations of exp_2. The workflow consists of utilizing a variant of **SGE4r** and **exp_2** where SGE4r is the template for the environment (contains observation and reward functions) and exp_2 is the template for the training activity (save model, load model, etc.). SGE4r is modified, then deployed using exp_2, then the results are studied in order to make a new modification to SGE4r before being evaluated again using exp_2. The pattern continues, building upon itself from version to version, until a suitable result is obtained in the context of solving the Snake Game environment.

## Contents

- [Workflow](#workflow)
    - [Training a Model](#training-a-model-and-saving-it)
    - [Loading a Model](#loading-a-model-to-evaluate-it)
    - [Visualizing Model Performance using TensorBoard](#visualizing-model-performance-using-tensorboard)
    - [Visualizing a Model as a .gif File](#loading-a-model-to-evaluate-it-and-save-the-visualization-to-a-gif-file)
- [Results](#results)

## Workflow

**Note:** For organizational purposes, SGE4r (environment) scripts are in the [exp_2_env](Source/exp_2/exp_2_env) folder.

**Note:** The [exp_2_test.py](Source/exp_2/exp_2_test.py) script isn't really used for training a model, it is meant to be used to output debug messages that should be appearing during run-time from the SGE4r script, so it is a script meant for debugging/development of the environment rather than actual agent training activities.

### Training a model and saving it

I suggest utilizing system cmd terminals since you can open multiples of them and have each of them train a model, you'd be surprised how model performance can be very different going from one training session to another, even if using the same SGE4r environment and the same exp_2 training activity script. 

**WARNING:** Remember that when training this way with multiple terminals, they're different models from each other. In other words, they're separate agents - they're not sharing experience with each other.

The script used to launch a training session is [exp_2_save.py](Source/exp_2/exp_2_save.py)

- Open a CMD terminal, outside of VS Code
- utilizing the ```dir```/```cd``` commands, navigate to the workspace folder
    - i.e. type `cd Desktop/Development/SkillNexus/SentdexRLTutorials` and press enter
- activate the project VENV
    - i.e. type `C:/Users/Mauricio/Desktop/Development/SkillNexus/SentdexRLTutorials/VENV/sentdexrltutorials/Scripts/activate` and press enter
- run the training script
    - i.e. type `C:/Users/Mauricio/Desktop/Development/SkillNexus/SentdexRLTutorials/Source/exp_2/exp_2_save.py` and press enter

Remember that you should go into [exp_2_save.py](Source/exp_2/exp_2_save.py) and update the training details at the top of the script. By updating the training details you can save different agents and differentiate between them.

If you need to stop training click on the CMD terminal to restore focus to it and then press `ctrl + c` many times until the script is interrupted. You CAN continue to train at a later time, see the next section for instructions.

### Continue to train a model and save it after having had to pause training (warning: imperfect solution)

**WARNING - TODO:** The [exp_2_continue.py](Source/exp_2/exp_2_continue.py) script needs to be updated to ensure that the instructions in this section work.

**WARNING - TODO:** The instructions here are imperfect: Training will continue and complete but the logs used by tensorboard will be incoherent.

The script used to continue a training session is [exp_2_continue.py](Source/exp_2/exp_2_continue.py)

- Open a CMD terminal, outside of VS Code
- utilizing the ```dir```/```cd``` commands, navigate to the workspace folder
    - i.e. type `cd Desktop/Development/SkillNexus/SentdexRLTutorials` and press enter
- activate the project VENV
    - i.e. type `C:/Users/Mauricio/Desktop/Development/SkillNexus/SentdexRLTutorials/VENV/sentdexrltutorials/Scripts/activate` and press enter
- run the continue training script
    - i.e. type `C:/Users/Mauricio/Desktop/Development/SkillNexus/SentdexRLTutorials/Source/exp_2/exp_2_continue.py` and press enter

Remember that you should go into [exp_2_continue.py](Source/exp_2/exp_2_continue.py) and update the training details at the top of the script. By updating the training details you can have the agent pickup where it left off in the previous training session.

### Loading a model to evaluate it

For loading a model and evaluating it, i.e. to look at what an agent does, you don't necessarily need to use a cmd terminal that is external to VS Code.

The script used to launch an evaluation session is [exp_2_load.py](Source/exp_2/exp_2_load.py)

- Open a CMD terminal, outside of VS Code
- utilizing the ```dir```/```cd``` commands, navigate to the workspace folder
    - i.e. type `cd Desktop/Development/SkillNexus/SentdexRLTutorials` and press enter
- activate the project VENV
    - i.e. type `C:/Users/Mauricio/Desktop/Development/SkillNexus/SentdexRLTutorials/VENV/sentdexrltutorials/Scripts/activate` and press enter
- run the load checkpoint script
    - i.e. type `C:/Users/Mauricio/Desktop/Development/SkillNexus/SentdexRLTutorials/Source/exp_2/exp_2_load.py` and press enter

You should go into the [exp_2_load.py](Source/exp_2/exp_2_load.py) and update the loading details at the top of the script. The main parameter that needs updating is the time_str parameter since it points to the checkpoint that you wish to load. One thing to remember is that in order for you to know which checkpoint to load you should inspect *tensorboard* to find the checkpoint with the best average reward.

### Visualizing model performance using TensorBoard

- Open a CMD terminal, outside of VS Code
- utilizing the ```dir```/```cd``` commands, navigate to the workspace folder
    - i.e. type `cd Desktop/Development/SkillNexus/SentdexRLTutorials` and press enter
- activate the project VENV
    - i.e. type `C:/Users/Mauricio/Desktop/Development/SkillNexus/SentdexRLTutorials/VENV/sentdexrltutorials/Scripts/activate` and press enter
- utilizing the ```dir```/```cd``` commands, navigate to the appropriate data folder
    - i.e. type `cd Source/exp_2/exp_2_data` and press enter
- run TensorBoard
    - i.e. type `tensorboard --logdir=logs` and press enter

### Loading a model to evaluate it and save the visualization to a gif file

For loading. evaluating, and saving the visualization of a model to a gif file, i.e. to look at what an agent does and save it to a gif, you don't necessarily need to use a cmd terminal that is external to VS Code.

The script used to launch an evaluation session and record it to a gif is [exp_2_load_to_gif.py](Source/exp_2/exp_2_load_to_gif.py)

- Open a CMD terminal, outside of VS Code
- utilizing the ```dir```/```cd``` commands, navigate to the workspace folder
    - i.e. type `cd Desktop/Development/SkillNexus/SentdexRLTutorials` and press enter
- activate the project VENV
    - i.e. type `C:/Users/Mauricio/Desktop/Development/SkillNexus/SentdexRLTutorials/VENV/sentdexrltutorials/Scripts/activate` and press enter
- run the load checkpoint to save it to gif script
    - i.e. type `C:/Users/Mauricio/Desktop/Development/SkillNexus/SentdexRLTutorials/Source/exp_2/exp_2_load_to_gif.py` and press enter

You should go into the [exp_2_load_to_gif.py](Source/exp_2/exp_2_load_to_gif.py) and update the loading details at the top of the script. You can also edit the gif parameters that follwo. The main parameter that needs updating is the time_str parameter since it points to the checkpoint that you wish to load. One thing to remember is that in order for you to know which checkpoint to load you should inspect *tensorboard* to find the checkpoint with the best average reward. You can then modify the gif parameters so that you can properly label the agent that you just recorded.

## Results

<details>
<summary> <strong>SGE4r_3</strong> </summary>

**Date:** 01/07/24

<details>
<summary> <strong>Observation Function</strong> </summary>

| <div align="center"> 0 </div>  | <div align="center"> 1 </div> | <div align="center"> 2 </div> | <div align="center"> 3 </div> | <div align="center"> 4 - 63 </div> |
| ------------- |:-------------:| ------------- | ------------- | ------------- |
| apple_pos_x | apple_pos_y | rel_delta_x_to_apple | rel_delta_y_to_apple | snake_body_components_buffer |

rel_delta_to_apple **=** apple_position **-** snake_head

snake_body_components_buffer **=** { part1_x, part1_y, part2_x, part2_y, **...** , -1, -1 }

</details>

<details>
<summary> <strong>Reward Function</strong> </summary>

<details>
<summary> <strong>Code</strong> </summary>

```python
reward_for_grabbing_apple = 0
reward_for_delta_distance_to_apple = 0
reward_for_reaching_max_apples = 0
reward_for_colliding_w_self = 0
reward_for_colliding_w_bound = 0
reward_for_timing_out = 0

# Reward for grabbing apple
if snake_head == apple_position:
    apple_count += 1
    reward_for_grabbing_apple = 6 * apple_count

# Reward for being close/far to the apple
euclidean_dist_to_apple = np.linalg.norm(np.array(snake_head) - np.array(apple_position))
inv_dist = -1 * euclidean_dist_to_apple
oldMax = 0
oldMin = -500
newMax = 2
newMin = -2
oldRange = (oldMax - oldMin)
newRange = (newMax - newMin)
adjDistReward = (((inv_dist - oldMin) * newRange) / oldRange) + newMin
    
reward_for_delta_distance_to_apple = adjDistReward

# Reward for reaching max apples
if apple_count >= 30:
    reward_for_reaching_max_apples = 5000

# Reward for colliding w self
if collision_with_self(snake_body) == 1:
    reward_for_colliding_w_self = -20

# Reward for colliding w boundary
if collision_with_boundaries(snake_head) == 1:
    reward_for_colliding_w_bound = -15

# Reward for timing out
if timesteps > 8000:
    reward_for_timing_out = -1000

reward_for_this_step = reward_for_grabbing_apple + 
            reward_for_delta_distance_to_apple + 
            reward_for_reaching_max_apples + 
            reward_for_colliding_w_bound + 
            reward_for_colliding_w_self + 
            reward_for_timing_out
```

</details>

</details>

<details>
<summary> <strong>Discussion</strong> </summary>

### Observation

The agent knows where the apple is located, it also knows where each of its body parts are, and it also knows the relative distance between itself and the apple. Due to how the relative distance is calculated, when the value is (-) in the x component, the apple is to the left of the snake and when the value is (+) the apple is to the right of the snake. Similarly, when the value is (-) in the y component, the apple is below the snake and when the value is (+) the apple is above. The relative distance between the snake and the apple can therefore maybe be interpreted as a helper for having a sense of direction from the snake to where the apple is.

### Reward

The reward function consists of two run-time components and four terminal components. The first reward is granted for grabbing apples. In this iteration, there is a counter that keeps track of the apples that have been grabbed in this episode and it resets to 0 on termination. The reward at the end of the episode is 6 * the apple counter. This was done to incentivize grabbing apples consecutively, however I am unsure if keeping an apple counter and using it as part of the reward is allowed as a form of RL. The second reward is a formula where the euclidean distance from the snake to the apple is used to determine a reward using a distance to reward scale-mapping. This was done to incentivize getting closer to the apple and to punish getting farther. The scale is determined from the distance range of -500 to 0 being mapped to the reward scale of -2 to 2. This means if the snake is at the farthest point then the reward will be the most negative while if the snake is at the closest point the reward is the most positive. This reward mechanism does cause an issue where the snake discovers a "green zone" and runs in circles within this zone rather than pursue grabbing apples. Essentially the reward mechanism causes a circle with radius of 250 around the apple as the green zone, so the snake will be within this distance but avoid actually grabbing the apple because doing so causes the apple to move which could potentially force the snake into the red zone.

The termination rewards in this iteration are self explanatory but the values are entirely arbitrary. Reaching 30 apples grabbed, which is the goal, rewards 5000 at the end of the episode, which is probably way too much. Colliding with itself or with a boundary provides a reward of -20 and -15 respectively, which I think is more reasonable. And timing out, which the agent has 8000 timesteps, is -1000 which I think is reasonable-ish considering the agent can accumulate a whole bunch of rewards by grabbing the apples consecutively.

I am curious if the reward function is allowed to be somewhat dependent on sequencing like for example could I set a timelimit of 100 steps and if an apple is grabbed the timer restarts. Could I cache the positive reward for existing in the green zone and if termination is caused by colliding w self, I provide a negative reward that clears the accumulated reward that was obtained while going in circles.

With this observation and reward definitions, the agent looks like it wants to grab an apple but much prefers to just exist in the green zone since it can accumulate rewards semi-indefinitely (it hasn't gone in circles long enough to hit the episode length limit).

</details>

<p align="center">
    <img alt="episode length mean" src="Source/exp_2/exp_2_data/visuals/images/01_07_24_SGE4r_3_PPO_r1_ep_len_mean.png" width="20%">   
&nbsp; &nbsp; &nbsp; &nbsp;
    <img alt="episode reward mean" src="Source/exp_2/exp_2_data/visuals/images/01_07_24_SGE4r_3_PPO_r1_ep_rew_mean.png" width="20%">     
&nbsp; &nbsp; &nbsp; &nbsp;
    <img alt="evaluation of 30 episodes" src="Source/exp_2/exp_2_data/visuals/gifs/01_07_24_SGE4r_3_PPO_r1_320000.gif" width="15%">  
</p>

</details>

<details>
<summary> <strong>SGE4r_4</strong> </summary>

**Date:** 01/08/24

<details>
<summary> <strong>Observation Function</strong> </summary>

| <div align="center"> 0 </div>  | <div align="center"> 1 </div> | <div align="center"> 2 </div> | <div align="center"> 3 </div> | <div align="center"> 4 - 63 </div> |
| ------------- |:-------------:| ------------- | ------------- | ------------- |
| apple_pos_x | apple_pos_y | rel_delta_x_to_apple | rel_delta_y_to_apple | snake_body_components_buffer |

rel_delta_to_apple **=** apple_position **-** snake_head

snake_body_components_buffer **=** { part1_x, part1_y, part2_x, part2_y, **...** , -1, -1 }

</details>

<details>
<summary> <strong>Reward Function</strong> </summary>

<details>
<summary> <strong>Difference</strong> </summary>

{- reward_for_reaching_max_apples = 5000 -} \
{+ reward_for_reaching_max_apples = 360 +}

{- reward_for_colliding_w_self = -20 -} \
{+ reward_for_colliding_w_self = -2 + (-1 * 0.05 * timesteps) +}

{- reward_for_colliding_w_bound = -15 -} \
{+ reward_for_colliding_w_bound = -1 + (-1 * 0.05 * timesteps) +}

{- reward_for_timing_out = -1000 -} \
{+ reward_for_timing_out = -360 +}

</details>

<details>
<summary> <strong>Code</strong> </summary>

```python
reward_for_grabbing_apple = 0
reward_for_delta_distance_to_apple = 0
reward_for_reaching_max_apples = 0
reward_for_colliding_w_self = 0
reward_for_colliding_w_bound = 0
reward_for_timing_out = 0

# Reward for grabbing apple
if snake_head == apple_position:
    apple_count += 1
    reward_for_grabbing_apple = 6 * apple_count

# Reward for being close/far to the apple
euclidean_dist_to_apple = np.linalg.norm(np.array(snake_head) - np.array(apple_position))
inv_dist = -1 * euclidean_dist_to_apple
oldMax = 0
oldMin = -500
newMax = 2
newMin = -2
oldRange = (oldMax - oldMin)
newRange = (newMax - newMin)
adjDistReward = (((inv_dist - oldMin) * newRange) / oldRange) + newMin
    
reward_for_delta_distance_to_apple = adjDistReward

# Reward for reaching max apples
if apple_count >= 30:
    reward_for_reaching_max_apples = 360

# Reward for colliding w self
if collision_with_self(snake_body) == 1:
    reward_for_colliding_w_self = -2 + (-1 * 0.05 * timesteps)

# Reward for colliding w boundary
if collision_with_boundaries(snake_head) == 1:
    reward_for_colliding_w_bound = -1 + (-1 * 0.05 * timesteps)

# Reward for timing out
if timesteps > 8000:
    reward_for_timing_out = -360

reward_for_this_step = reward_for_grabbing_apple + 
            reward_for_delta_distance_to_apple + 
            reward_for_reaching_max_apples + 
            reward_for_colliding_w_bound + 
            reward_for_colliding_w_self + 
            reward_for_timing_out
```

</details>

</details>

<details>
<summary> <strong>Discussion</strong> </summary>

In the previous iteration it looks like the agent has at least some inclination to grab apples but the issue is it likes to go in circles very much. To try to fix this I changed the termination reward for colliding w self or colliding w boundary so that they're dependent on the amount of time that has passed. This way, if the agent has been going in circles a lot then although it has accumulated a lot of rewards from the green zone it also is allowing the punishment for colliding w self or colliding w boundary to accumulate, which means that once that does happen, the rewards it had accumulated while in the green zone will be wiped out. I also put in a coefficient to tune how much of an impact time has on the punishment. I also reduced the reward for reaching max apples and the punishment for timing out, but I think both of these parmeters do not yet matter since the agent has never triggered those cases.

Compared to the previous iteration, it looks like the agent is getting slightly closer to the apple before going in circles, and it also appears like the agent lives a bit longer before cashing in the reward from being in the green zone.

</details>

<p align="center">
    <img alt="episode length mean" src="Source/exp_2/exp_2_data/visuals/images/01_08_24_SGE4r_4_PPO_r1_ep_len_mean.png" width="20%">   
&nbsp; &nbsp; &nbsp; &nbsp;
    <img alt="episode reward mean" src="Source/exp_2/exp_2_data/visuals/images/01_08_24_SGE4r_4_PPO_r1_ep_rew_mean.png" width="20%">     
&nbsp; &nbsp; &nbsp; &nbsp;
    <img alt="evaluation of 30 episodes" src="Source/exp_2/exp_2_data/visuals/gifs/01_08_24_SGE4r_4_PPO_r1_360000.gif" width="15%">  
</p>

</details>

<details>
<summary> <strong>SGE4r_5</strong> </summary>

**Date:** 01/09/24

<details>
<summary> <strong>Observation Function</strong> </summary>

| <div align="center"> 0 </div>  | <div align="center"> 1 </div> | <div align="center"> 2 </div> | <div align="center"> 3 </div> | <div align="center"> 4 - 63 </div> |
| ------------- |:-------------:| ------------- | ------------- | ------------- |
| apple_pos_x | apple_pos_y | rel_delta_x_to_apple | rel_delta_y_to_apple | snake_body_components_buffer |

rel_delta_to_apple **=** apple_position **-** snake_head

snake_body_components_buffer **=** { part1_x, part1_y, part2_x, part2_y, **...** , -1, -1 }

</details>

<details>
<summary> <strong>Reward Function</strong> </summary>

<details>
<summary> <strong>Difference</strong> </summary>

{- inv_dist = -1 * euclidean_dist_to_apple -} \
{- oldMax = 0 -} \
{- oldMin = -500 -} \
{- newMax = 2 -} \
{- newMin = -2 -} \
{- oldRange = (oldMax - oldMin) -} \
{- newRange = (newMax - newMin) -} \
{- adjDistReward = (((inv_dist - oldMin) * newRange) / oldRange) + newMin -} \
{- reward_for_delta_distance_to_apple = adjDistReward -} \
{+ reward_for_delta_distance_to_apple = -1 * distance +}

</details>

<details>
<summary> <strong>Code</strong> </summary>

```python
reward_for_grabbing_apple = 0
reward_for_delta_distance_to_apple = 0
reward_for_reaching_max_apples = 0
reward_for_colliding_w_self = 0
reward_for_colliding_w_bound = 0
reward_for_timing_out = 0

# Reward for grabbing apple
if snake_head == apple_position:
    apple_count += 1
    reward_for_grabbing_apple = 6 * apple_count

# Reward for being close/far to the apple
distance = np.linalg.norm(np.array(snake_head) - np.array(apple_position))
reward_for_delta_distance_to_apple = -1 * distance

# Reward for reaching max apples
if apple_count >= 30:
    reward_for_reaching_max_apples = 360

# Reward for colliding w self
if collision_with_self(snake_body) == 1:
    reward_for_colliding_w_self = -2 + (-1 * 0.05 * timesteps)

# Reward for colliding w boundary
if collision_with_boundaries(snake_head) == 1:
    reward_for_colliding_w_bound = -1 + (-1 * 0.05 * timesteps)

# Reward for timing out
if timesteps > 8000:
    reward_for_timing_out = -360

reward_for_this_step = reward_for_grabbing_apple + 
            reward_for_delta_distance_to_apple + 
            reward_for_reaching_max_apples + 
            reward_for_colliding_w_bound + 
            reward_for_colliding_w_self + 
            reward_for_timing_out
```
</details>

</details>

<details>
<summary> <strong>Discussion</strong> </summary>

In the last iteration we could see that the behavior of getting into the green zone quickly and going in circles before eventually colliding w self is still present. To try to get rid of this, I changed the distance-based rewards so that it no longer uses the variable scaling. Instead, it simply uses -1 * euclidean distance as the parameter, which in theory would mean that the farther away the snake is from the apple, the worse the reward. And the only way to alleviate those negative rewards is to grab apples as quickly as possible. However looking at the resulting performance the agent simply reaches the conclusion to end itself as quickly as possible by moving in one direction.

</details>

<p align="center">
    <img alt="episode length mean" src="Source/exp_2/exp_2_data/visuals/images/01_09_24_SGE4r_5_PPO_r1_ep_len_mean.png" width="20%">   
&nbsp; &nbsp; &nbsp; &nbsp;
    <img alt="episode reward mean" src="Source/exp_2/exp_2_data/visuals/images/01_09_24_SGE4r_5_PPO_r1_ep_rew_mean.png" width="20%">     
&nbsp; &nbsp; &nbsp; &nbsp;
    <img alt="evaluation of 30 episodes" src="Source/exp_2/exp_2_data/visuals/gifs/01_09_24_SGE4r_5_PPO_r1_410000.gif" width="15%">  
</p>

</details>

<details>
<summary> <strong>SGE4r_6</strong> </summary>

**Date:** 01/10/24

<details>
<summary> <strong>Observation Function</strong> </summary>

| <div align="center"> 0 </div>  | <div align="center"> 1 </div> | <div align="center"> 2 - 62 </div> | <div align="center"> 63 </div> | <div align="center"> 64 </div> | <div align="center"> 65 </div> | <div align="center"> 66 </div> | <div align="center"> 67 </div> |
| ------------- |:-------------:| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
| apple_pos_x | apple_pos_y | snake_body_components_buffer | snake_body_actual_length | rel_delta_x_to_apple | rel_delta_y_to_apple | vel_x | vel_y |

snake_body_components_buffer **=** { part1_x, part1_y, part2_x, part2_y, **...** , -1, -1 }

rel_delta_to_apple **=** apple_position **-** snake_head

vel_x, vel_y    **=** -10, 0    `if` action **==** 0

vel_x, vel_y    **=** 10, 0     `if` action **==** 1

vel_x, vel_y    **=** 0, 10     `if` action **==** 2

vel_x, vel_y    **=** 0, -10    `if` action **==** 3

</details>

<details>
<summary> <strong>Reward Function</strong> </summary>

<details>
<summary> <strong>Difference</strong> </summary>

{- apple_count += 1 -} \
{- reward_for_grabbing_apple = 6 * apple_count -} \
{+ reward_for_grabbing_apple = 20 +}

{- reward_for_delta_distance_to_apple = -1 * distance -} \
{+ inv_dist = -1 * euclidean_dist_to_apple +} \
{+ oldMax = 0 +} \
{+ oldMin = -500 +} \
{+ newMax = 2 +} \
{+ newMin = -2 +} \
{+ oldRange = (oldMax - oldMin) +} \
{+ newRange = (newMax - newMin) +} \
{+ adjDistReward = (((inv_dist - oldMin) * newRange) / oldRange) + newMin +} \
{+ reward_for_delta_distance_to_apple = adjDistReward +}

{- if timesteps > 8000: -} \
{+ if timesteps > 16000: +}

</details>

<details>
<summary> <strong>Code</strong> </summary>

```python
reward_for_grabbing_apple = 0
reward_for_delta_distance_to_apple = 0
reward_for_reaching_max_apples = 0
reward_for_colliding_w_self = 0
reward_for_colliding_w_bound = 0
reward_for_timing_out = 0

# Reward for grabbing apple
if snake_head == apple_position:
    reward_for_grabbing_apple = 20

# Reward for being close/far to the apple
euclidean_dist_to_apple = np.linalg.norm(np.array(snake_head) - np.array(apple_position))
inv_dist = -1 * euclidean_dist_to_apple
oldMax = 0
oldMin = -500
newMax = 2
newMin = -2
oldRange = (oldMax - oldMin)
newRange = (newMax - newMin)
adjDistReward = (((inv_dist - oldMin) * newRange) / oldRange) + newMin
    
reward_for_delta_distance_to_apple = adjDistReward

# Reward for reaching max apples
if apple_count >= 30:
    reward_for_reaching_max_apples = 360

# Reward for colliding w self
if collision_with_self(snake_body) == 1:
    reward_for_colliding_w_self = -2 + (-1 * 1 * timesteps)

# Reward for colliding w boundary
if collision_with_boundaries(snake_head) == 1:
    reward_for_colliding_w_bound = -2 + (-1 * 1 * timesteps)

# Reward for timing out
if timesteps > 16000:
    reward_for_timing_out = -3 + (-1 * 1 * timesteps)

reward_for_this_step = reward_for_grabbing_apple + 
            reward_for_delta_distance_to_apple + 
            reward_for_reaching_max_apples + 
            reward_for_colliding_w_bound + 
            reward_for_colliding_w_self + 
            reward_for_timing_out
```

</details>

</details>

<details>
<summary> <strong>Discussion</strong> </summary>

In this iteration the distance-based green/red zone reward component is brought back. The reward for grabbing apples is set to a flat addition of 20 instead of the previously used sequentially incrementing reward. Looking at the behavior between this iteration and SGE4r_4, the behavior looks very similar. The difference can best be seen in the graphs since in SGE4r_4 the system didn't seem very stable compared to the current iteration. This stability seen in the graphs may be more desirable?

</details>

<p align="center">
    <img alt="episode length mean" src="Source/exp_2/exp_2_data/visuals/images/01_10_24_SGE4r_6_PPO_r2_ep_len_mean.png" width="20%">   
&nbsp; &nbsp; &nbsp; &nbsp;
    <img alt="episode reward mean" src="Source/exp_2/exp_2_data/visuals/images/01_10_24_SGE4r_6_PPO_r2_ep_rew_mean.png" width="20%">     
&nbsp; &nbsp; &nbsp; &nbsp;
    <img alt="evaluation of 30 episodes" src="Source/exp_2/exp_2_data/visuals/gifs/01_10_24_SGE4r_6_PPO_r2_440000.gif" width="15%">  
</p>

</details>

<details>
<summary> <strong>SGE4r_7</strong> </summary>

**Date:** 01/11/24

<details>
<summary> <strong>Observation Function</strong> </summary>

| <div align="center"> 0 </div>  | <div align="center"> 1 </div> | <div align="center"> 2 - 62 </div> | <div align="center"> 63 </div> | <div align="center"> 64 </div> | <div align="center"> 65 </div> | <div align="center"> 66 </div> | <div align="center"> 67 </div> |
| ------------- |:-------------:| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
| apple_pos_x | apple_pos_y | snake_body_components_buffer | snake_body_actual_length | rel_delta_x_to_apple | rel_delta_y_to_apple | vel_x | vel_y |

snake_body_components_buffer **=** { part1_x, part1_y, part2_x, part2_y, **...** , -1, -1 }

rel_delta_to_apple **=** apple_position **-** snake_head

vel_x, vel_y    **=** -10, 0    `if` action **==** 0

vel_x, vel_y    **=** 10, 0     `if` action **==** 1

vel_x, vel_y    **=** 0, 10     `if` action **==** 2

vel_x, vel_y    **=** 0, -10    `if` action **==** 3

</details>

<details>
<summary> <strong>Reward Function</strong> </summary>

<details>
<summary> <strong>Difference</strong> </summary>

{- reward_for_grabbing_apple = 20 -} \
{+ reward_for_grabbing_apple = 50 +}

{- reward_for_reaching_max_apples = 360 -} \
{+ reward_for_reaching_max_apples = 1500 +}

</details>

<details>
<summary> <strong>Code</strong> </summary>

```python
reward_for_grabbing_apple = 0
reward_for_delta_distance_to_apple = 0
reward_for_reaching_max_apples = 0
reward_for_colliding_w_self = 0
reward_for_colliding_w_bound = 0
reward_for_timing_out = 0

# Reward for grabbing apple
if snake_head == apple_position:
    reward_for_grabbing_apple = 50

# Reward for being close/far to the apple
euclidean_dist_to_apple = np.linalg.norm(np.array(snake_head) - np.array(apple_position))
inv_dist = -1 * euclidean_dist_to_apple
oldMax = 0
oldMin = -500
newMax = 2
newMin = -2
oldRange = (oldMax - oldMin)
newRange = (newMax - newMin)
adjDistReward = (((inv_dist - oldMin) * newRange) / oldRange) + newMin
    
reward_for_delta_distance_to_apple = adjDistReward

# Reward for reaching max apples
if apple_count >= 30:
    reward_for_reaching_max_apples = 1500

# Reward for colliding w self
if collision_with_self(snake_body) == 1:
    reward_for_colliding_w_self = -2 + (-1 * 1 * timesteps)

# Reward for colliding w boundary
if collision_with_boundaries(snake_head) == 1:
    reward_for_colliding_w_bound = -2 + (-1 * 1 * timesteps)

# Reward for timing out
if timesteps > 16000:
    reward_for_timing_out = -3 + (-1 * 1 * timesteps)

reward_for_this_step = reward_for_grabbing_apple + 
            reward_for_delta_distance_to_apple + 
            reward_for_reaching_max_apples + 
            reward_for_colliding_w_bound + 
            reward_for_colliding_w_self + 
            reward_for_timing_out
```

</details>

</details>

<details>
<summary> <strong>Discussion</strong> </summary>

I was trying to make grabbing apples more tasty for the agent so I increased the value slightly since it does look like it understands to get as close as possible to the apple but the reward for existing in the green zone is just too good compared to grabbing apples.

</details>

<p align="center">
    <img alt="episode length mean" src="Source/exp_2/exp_2_data/visuals/images/01_11_24_SGE4r_7_PPO_r2_ep_len_mean.png" width="20%">   
&nbsp; &nbsp; &nbsp; &nbsp;
    <img alt="episode reward mean" src="Source/exp_2/exp_2_data/visuals/images/01_11_24_SGE4r_7_PPO_r2_ep_rew_mean.png" width="20%">     
&nbsp; &nbsp; &nbsp; &nbsp;
    <img alt="evaluation of 30 episodes" src="Source/exp_2/exp_2_data/visuals/gifs/01_11_24_SGE4r_7_PPO_r2_500000.gif" width="15%">  
</p>

</details>

<details>
<summary> <strong>SGE4r_8</strong> </summary>

**Date:** 01/11/24

<details>
<summary> <strong>Observation Function</strong> </summary>

| <div align="center"> 0 </div>  | <div align="center"> 1 </div> | <div align="center"> 2 - 62 </div> | <div align="center"> 63 </div> | <div align="center"> 64 </div> | <div align="center"> 65 </div> | <div align="center"> 66 </div> | <div align="center"> 67 </div> |
| ------------- |:-------------:| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
| apple_pos_x | apple_pos_y | snake_body_components_buffer | snake_body_actual_length | rel_delta_x_to_apple | rel_delta_y_to_apple | vel_x | vel_y |

snake_body_components_buffer **=** { part1_x, part1_y, part2_x, part2_y, **...** , -1, -1 }

rel_delta_to_apple **=** apple_position **-** snake_head

vel_x, vel_y    **=** -10, 0    `if` action **==** 0

vel_x, vel_y    **=** 10, 0     `if` action **==** 1

vel_x, vel_y    **=** 0, 10     `if` action **==** 2

vel_x, vel_y    **=** 0, -10    `if` action **==** 3

</details>

<details>
<summary> <strong>Reward Function</strong> </summary>

<details>
<summary> <strong>Difference</strong> </summary>

{- newMin = -2 -} \
{+ newMin = 0 +}

</details>

<details>
<summary> <strong>Code</strong> </summary>

```python
reward_for_grabbing_apple = 0
reward_for_delta_distance_to_apple = 0
reward_for_reaching_max_apples = 0
reward_for_colliding_w_self = 0
reward_for_colliding_w_bound = 0
reward_for_timing_out = 0

# Reward for grabbing apple
if snake_head == apple_position:
    reward_for_grabbing_apple = 50

# Reward for being close/far to the apple
euclidean_dist_to_apple = np.linalg.norm(np.array(snake_head) - np.array(apple_position))
inv_dist = -1 * euclidean_dist_to_apple
oldMax = 0
oldMin = -500
newMax = 2
newMin = 0
oldRange = (oldMax - oldMin)
newRange = (newMax - newMin)
adjDistReward = (((inv_dist - oldMin) * newRange) / oldRange) + newMin
    
reward_for_delta_distance_to_apple = adjDistReward

# Reward for reaching max apples
if apple_count >= 30:
    reward_for_reaching_max_apples = 1500

# Reward for colliding w self
if collision_with_self(snake_body) == 1:
    reward_for_colliding_w_self = -2 + (-1 * 1 * timesteps)

# Reward for colliding w boundary
if collision_with_boundaries(snake_head) == 1:
    reward_for_colliding_w_bound = -2 + (-1 * 1 * timesteps)

# Reward for timing out
if timesteps > 16000:
    reward_for_timing_out = -3 + (-1 * 1 * timesteps)

reward_for_this_step = reward_for_grabbing_apple + 
            reward_for_delta_distance_to_apple + 
            reward_for_reaching_max_apples + 
            reward_for_colliding_w_bound + 
            reward_for_colliding_w_self + 
            reward_for_timing_out
```

</details>

</details>

<details>
<summary> <strong>Discussion</strong> </summary>

The only thing I changed here was make the reward for moving positive all the time with 0 at farthest distance from apple and 2 at closest distance. The idea was maybe this way the agent wouldn't mind grabbing apples since grabbing them no longer poses a threat to being forced into the red zone. But the behavior remains the same and the snake prefers to exist in the green zone.

</details>

<p align="center">
    <img alt="episode length mean" src="Source/exp_2/exp_2_data/visuals/images/01_11_24_SGE4r_8_PPO_r1_ep_len_mean.png" width="20%">   
&nbsp; &nbsp; &nbsp; &nbsp;
    <img alt="episode reward mean" src="Source/exp_2/exp_2_data/visuals/images/01_11_24_SGE4r_8_PPO_r1_ep_rew_mean.png" width="20%">     
&nbsp; &nbsp; &nbsp; &nbsp;
    <img alt="evaluation of 30 episodes" src="Source/exp_2/exp_2_data/visuals/gifs/01_11_24_SGE4r_8_PPO_r1_490000.gif" width="15%">  
</p>

</details>

<details>
<summary> <strong>SGE4r_9</strong> </summary>

**Date:** 01/12/24

<details>
<summary> <strong>Observation Function</strong> </summary>

| <div align="center"> 0 </div>  | <div align="center"> 1 </div> | <div align="center"> 2 - 62 </div> | <div align="center"> 63 </div> | <div align="center"> 64 </div> | <div align="center"> 65 </div> | <div align="center"> 66 </div> | <div align="center"> 67 </div> |
| ------------- |:-------------:| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
| apple_pos_x | apple_pos_y | snake_body_components_buffer | snake_body_actual_length | rel_delta_x_to_apple | rel_delta_y_to_apple | vel_x | vel_y |

snake_body_components_buffer **=** { part1_x, part1_y, part2_x, part2_y, **...** , -1, -1 }

rel_delta_to_apple **=** apple_position **-** snake_head

vel_x, vel_y    **=** -10, 0    `if` action **==** 0

vel_x, vel_y    **=** 10, 0     `if` action **==** 1

vel_x, vel_y    **=** 0, 10     `if` action **==** 2

vel_x, vel_y    **=** 0, -10    `if` action **==** 3

</details>

<details>
<summary> <strong>Reward Function</strong> </summary>

<details>
<summary> <strong>Difference</strong> </summary>

{- reward_for_grabbing_apple = 50 -} \
{+ reward_for_grabbing_apple = 6 +}

{- inv_dist = -1 * euclidean_dist_to_apple -} \
{- oldMax = 0 -} \
{- oldMin = -500 -} \
{- newMax = 2 -} \
{- newMin = -2 -} \
{- oldRange = (oldMax - oldMin) -} \
{- newRange = (newMax - newMin) -} \
{- adjDistReward = (((inv_dist - oldMin) * newRange) / oldRange) + newMin -} \
{- reward_for_delta_distance_to_apple = adjDistReward -}

{- reward_for_reaching_max_apples = 1500 -} \
{+ reward_for_reaching_max_apples = 360 +}

{- reward_for_colliding_w_self = -2 + (-1 * 1 * timesteps) -} \
{+ reward_for_colliding_w_self = -2 + (-1 * 0.05 * timesteps) +}

{- reward_for_colliding_w_bound = -2 + (-1 * 1 * timesteps) -} \
{+ reward_for_colliding_w_bound = -2 + (-1 * 0.05 * timesteps) +}

{- reward_for_timing_out = -3 * (-1 + 1 * timesteps) -} \
{+ reward_for_timing_out = -4 * (-1 + 0.05 * timesteps) +}

</details>

<details>
<summary> <strong>Code</strong> </summary>

```python
reward_for_grabbing_apple = 0
reward_for_delta_distance_to_apple = 0
reward_for_reaching_max_apples = 0
reward_for_colliding_w_self = 0
reward_for_colliding_w_bound = 0
reward_for_timing_out = 0

# Reward for grabbing apple
if snake_head == apple_position:
    reward_for_grabbing_apple = 6

# Reward for reaching max apples
if apple_count >= 30:
    reward_for_reaching_max_apples = 360

# Reward for colliding w self
if collision_with_self(snake_body) == 1:
    reward_for_colliding_w_self = -2 + (-1 * 0.05 * timesteps)

# Reward for colliding w boundary
if collision_with_boundaries(snake_head) == 1:
    reward_for_colliding_w_bound = -2 + (-1 * 0.05 * timesteps)

# Reward for timing out
if timesteps > 16000:
    reward_for_timing_out = -4 + (-1 * 0.05 * timesteps)

reward_for_this_step = reward_for_grabbing_apple + 
            reward_for_delta_distance_to_apple + 
            reward_for_reaching_max_apples + 
            reward_for_colliding_w_bound + 
            reward_for_colliding_w_self + 
            reward_for_timing_out
```

</details>

</details>

<details>
<summary> <strong>Discussion</strong> </summary>

Out of curiosity I decided to run the experiment having removed the distance-based reward entirely. I am expecting the snake to decide to collide w itself immediately since there is a negative reward associated with colliding w itself but it is dependent on time. So the longer it waits to collide w itself, the worse the punishment. I'm hoping that it can learn that it can avoid the penalty by just picking up apples and terminating upon reaching 30 of them. But that seems very unlikely. I think in the end, there needs to be some kind of incentive for the agent to move at all.

I ended up running this experiment 6 times, 3 ran for 1 million steps and 3 ran for 5 million steps.

Initially, in all runs, the agent minimizes the episode length by terminating as quickly as possible. This is likely due to the time-based punishment that is given on termination (collision w self or collision w boundary).

In runs 1, 2 and 3, after some time (around 400k to 800k) the agents start allowing for longer and longer episodes. Then, the reward starts to slowly approach 0 as the agents presumibly take their time to grab *some* apples before terminating. Below are some examples of the best performers out of the three runs.

In runs 4, 5, and 6, after some time (around 1 million to 1.5 million) the agents start allowing for much longer episodes than in the previous batch of runs and the reward is becoming more and more positive before the rewards becomes very negative. I suspect that the agent simply isn't learning fast enough that if it grabs a ton of apples it will terminate with no punishment at all. So the graphs basically say that yes, the agent is learning to grab apples, but it's all for nothing if the agent terminates due to colliding w itself or colliding w boundary since the punishment for terminating that way wipes out any progress made by grabbing the apples.

I think this can all be alleviated by either increasing the value of grabbing an apple or reducing the impact that time has on punishment even more. However, since we want the agent to learn that terminating due to collisions is bad, maybe the coefficient should actually be increased slightly along with increasing the value of the apples as well.

One thing I noticed is that for a while the agents will slowly learn to go for the apple as quick as possible and the average reward will be positive for a bit before the agent breaksdown. The best one in this version was r5 at 3.7 million steps, getting a high score of 4 apples in one episode, which thus far was unheard of.

So for now it looks like we might be able to solve the environment if we just tune the current existing parameters...

</details>

### Ran for 1 million steps

<p align="center">
    <img alt="episode length mean" src="Source/exp_2/exp_2_data/visuals/images/01_12_24_SGE4r_9_PPO_r2_ep_len_mean.png" width="20%">   
&nbsp; &nbsp; &nbsp; &nbsp;
    <img alt="episode reward mean" src="Source/exp_2/exp_2_data/visuals/images/01_12_24_SGE4r_9_PPO_r2_ep_rew_mean.png" width="20%">     
&nbsp; &nbsp; &nbsp; &nbsp;
    <img alt="evaluation of 30 episodes" src="Source/exp_2/exp_2_data/visuals/gifs/01_12_24_SGE4r_9_PPO_r2_640000_1.gif" width="15%">     
&nbsp; &nbsp; &nbsp; &nbsp;
    <img alt="evaluation of 30 episodes" src="Source/exp_2/exp_2_data/visuals/gifs/01_12_24_SGE4r_9_PPO_r2_760000_2.gif" width="15%">     
&nbsp; &nbsp; &nbsp; &nbsp;
    <img alt="evaluation of 30 episodes" src="Source/exp_2/exp_2_data/visuals/gifs/01_12_24_SGE4r_9_PPO_r2_960000_3.gif" width="15%">  
</p>

<p align="center">
    <img alt="episode length mean" src="Source/exp_2/exp_2_data/visuals/images/01_12_24_SGE4r_9_PPO_r3_ep_len_mean.png" width="20%">   
&nbsp; &nbsp; &nbsp; &nbsp;
    <img alt="episode reward mean" src="Source/exp_2/exp_2_data/visuals/images/01_12_24_SGE4r_9_PPO_r3_ep_rew_mean.png" width="20%">     
&nbsp; &nbsp; &nbsp; &nbsp;
    <img alt="evaluation of 30 episodes" src="Source/exp_2/exp_2_data/visuals/gifs/01_12_24_SGE4r_9_PPO_r3_810000_1.gif" width="15%">     
&nbsp; &nbsp; &nbsp; &nbsp;
    <img alt="evaluation of 30 episodes" src="Source/exp_2/exp_2_data/visuals/gifs/01_12_24_SGE4r_9_PPO_r3_910000_2.gif" width="15%">     
&nbsp; &nbsp; &nbsp; &nbsp;
    <img alt="evaluation of 30 episodes" src="Source/exp_2/exp_2_data/visuals/gifs/01_12_24_SGE4r_9_PPO_r3_1000000_3.gif" width="15%">  
</p>

### Ran for 5 million steps

<p align="center">
    <img alt="episode length mean" src="Source/exp_2/exp_2_data/visuals/images/01_12_24_SGE4r_9_PPO_r5_ep_len_mean.png" width="20%">   
&nbsp; &nbsp; &nbsp; &nbsp;
    <img alt="episode reward mean" src="Source/exp_2/exp_2_data/visuals/images/01_12_24_SGE4r_9_PPO_r5_ep_rew_mean.png" width="20%">     
&nbsp; &nbsp; &nbsp; &nbsp;
    <img alt="evaluation of 30 episodes" src="Source/exp_2/exp_2_data/visuals/gifs/01_12_24_SGE4r_9_PPO_r5_1100000_1.gif" width="15%">     
&nbsp; &nbsp; &nbsp; &nbsp;
    <img alt="evaluation of 30 episodes" src="Source/exp_2/exp_2_data/visuals/gifs/01_12_24_SGE4r_9_PPO_r5_2770000_2.gif" width="15%">     
&nbsp; &nbsp; &nbsp; &nbsp;
    <img alt="evaluation of 30 episodes" src="Source/exp_2/exp_2_data/visuals/gifs/01_12_24_SGE4r_9_PPO_r5_3720000_3.gif" width="15%">  
</p>

<p align="center">
    <img alt="episode length mean" src="Source/exp_2/exp_2_data/visuals/images/01_12_24_SGE4r_9_PPO_r6_ep_len_mean.png" width="20%">   
&nbsp; &nbsp; &nbsp; &nbsp;
    <img alt="episode reward mean" src="Source/exp_2/exp_2_data/visuals/images/01_12_24_SGE4r_9_PPO_r6_ep_rew_mean.png" width="20%">     
&nbsp; &nbsp; &nbsp; &nbsp;
    <img alt="evaluation of 30 episodes" src="Source/exp_2/exp_2_data/visuals/gifs/01_12_24_SGE4r_9_PPO_r6_1670000_1.gif" width="15%">     
&nbsp; &nbsp; &nbsp; &nbsp;
    <img alt="evaluation of 30 episodes" src="Source/exp_2/exp_2_data/visuals/gifs/01_12_24_SGE4r_9_PPO_r6_2100000_2.gif" width="15%">     
&nbsp; &nbsp; &nbsp; &nbsp;
    <img alt="evaluation of 30 episodes" src="Source/exp_2/exp_2_data/visuals/gifs/01_12_24_SGE4r_9_PPO_r6_3940000_3.gif" width="15%">  
</p>

</details>

<details>
<summary> <strong>SGE4r_10</strong> </summary>

**Date:** 01/13/24

<details>
<summary> <strong>Observation Function</strong> </summary>

| <div align="center"> 0 </div>  | <div align="center"> 1 </div> | <div align="center"> 2 - 62 </div> | <div align="center"> 63 </div> | <div align="center"> 64 </div> | <div align="center"> 65 </div> | <div align="center"> 66 </div> | <div align="center"> 67 </div> |
| ------------- |:-------------:| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
| apple_pos_x | apple_pos_y | snake_body_components_buffer | snake_body_actual_length | rel_delta_x_to_apple | rel_delta_y_to_apple | vel_x | vel_y |

snake_body_components_buffer **=** { part1_x, part1_y, part2_x, part2_y, **...** , -1, -1 }

rel_delta_to_apple **=** apple_position **-** snake_head

vel_x, vel_y    **=** -10, 0    `if` action **==** 0

vel_x, vel_y    **=** 10, 0     `if` action **==** 1

vel_x, vel_y    **=** 0, 10     `if` action **==** 2

vel_x, vel_y    **=** 0, -10    `if` action **==** 3

</details>

<details>
<summary> <strong>Reward Function</strong> </summary>

<details>
<summary> <strong>Difference</strong> </summary>

{- reward_for_grabbing_apple = 6 -} \
{+ reward_for_grabbing_apple = 20 +}

{- reward_for_reaching_max_apples = 360 -} \
{+ reward_for_reaching_max_apples = 500 +}

</details>

<details>
<summary> <strong>Code</strong> </summary>

```python
reward_for_grabbing_apple = 0
reward_for_delta_distance_to_apple = 0
reward_for_reaching_max_apples = 0
reward_for_colliding_w_self = 0
reward_for_colliding_w_bound = 0
reward_for_timing_out = 0

# Reward for grabbing apple
if snake_head == apple_position:
    reward_for_grabbing_apple = 20

# Reward for reaching max apples
if apple_count >= 30:
    reward_for_reaching_max_apples = 500

# Reward for colliding w self
if collision_with_self(snake_body) == 1:
    reward_for_colliding_w_self = -2 + (-1 * 0.05 * timesteps)

# Reward for colliding w boundary
if collision_with_boundaries(snake_head) == 1:
    reward_for_colliding_w_bound = -2 +* (-1 * 0.05 * timesteps)

# Reward for timing out
if timesteps > 16000:
    reward_for_timing_out = -4 + (-1 * 0.05 * timesteps)

reward_for_this_step = reward_for_grabbing_apple + 
            reward_for_delta_distance_to_apple + 
            reward_for_reaching_max_apples + 
            reward_for_colliding_w_bound + 
            reward_for_colliding_w_self + 
            reward_for_timing_out
```

</details>

</details>

<details>
<summary> <strong>Discussion</strong> </summary>

Similar to the performance of GEAR 9, as time progressed the reward started approaching 0 before breaking through into the positive rewards space. The amount of apples captured increased from 1 to 2 to 3 to 4, though 4 was rare. I wasn't able to capture the event though, so I think this version of the model might not have been as good as the best of GEAR 9.

I am suspecting that there needs to be a distance-based reward so that the agent will learn to grab apples more quickly in the timeline, we don't want to be running training for 5 million steps after all, ideally just 1 million, ideally 300,000.

</details>

<p align="center">
    <img alt="episode length mean" src="Source/exp_2/exp_2_data/visuals/images/01_13_24_SGE4r_10_PPO_r3_ep_len_mean.png" width="20%">   
&nbsp; &nbsp; &nbsp; &nbsp;
    <img alt="episode reward mean" src="Source/exp_2/exp_2_data/visuals/images/01_13_24_SGE4r_10_PPO_r3_ep_rew_mean.png" width="20%">     
&nbsp; &nbsp; &nbsp; &nbsp;
    <img alt="evaluation of 30 episodes" src="Source/exp_2/exp_2_data/visuals/images/01_13_24_SGE4r_10_PPO_r3_performance_points.png" width="20%">
</p>

<p align="center">
    <img alt="episode length mean" src="Source/exp_2/exp_2_data/visuals/gifs/01_13_24_SGE4r_10_PPO_r3_1880000_3.gif" width="15%">   
&nbsp; &nbsp; &nbsp; &nbsp;
    <img alt="episode reward mean" src="Source/exp_2/exp_2_data/visuals/gifs/01_13_24_SGE4r_10_PPO_r3_2300000_2.gif" width="15%">     
&nbsp; &nbsp; &nbsp; &nbsp;
    <img alt="evaluation of 30 episodes" src="Source/exp_2/exp_2_data/visuals/gifs/01_13_24_SGE4r_10_PPO_r3_2650000_1.gif" width="15%">
</p>

</details>

<details>
<summary> <strong>SGE4r_11</strong> </summary>

**Date:** 01/14/24

<details>
<summary> <strong>Observation Function</strong> </summary>

| <div align="center"> 0 </div>  | <div align="center"> 1 </div> | <div align="center"> 2 - 62 </div> | <div align="center"> 63 </div> | <div align="center"> 64 </div> | <div align="center"> 65 </div> | <div align="center"> 66 </div> | <div align="center"> 67 </div> |
| ------------- |:-------------:| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
| apple_pos_x | apple_pos_y | snake_body_components_buffer | snake_body_actual_length | rel_delta_x_to_apple | rel_delta_y_to_apple | vel_x | vel_y |

snake_body_components_buffer **=** { part1_x, part1_y, part2_x, part2_y, **...** , -1, -1 }

rel_delta_to_apple **=** apple_position **-** snake_head

vel_x, vel_y    **=** -10, 0    `if` action **==** 0

vel_x, vel_y    **=** 10, 0     `if` action **==** 1

vel_x, vel_y    **=** 0, 10     `if` action **==** 2

vel_x, vel_y    **=** 0, -10    `if` action **==** 3

</details>

<details>
<summary> <strong>Reward Function</strong> </summary>

<details>
<summary> <strong>Difference</strong> </summary>

{- reward_for_grabbing_apple = 20 -} \
{+ reward_for_grabbing_apple = 50 +}

{+ Euclid_Dist_to_Apple = np.linalg.norm(np.array(self.snake_head) - np.array(self.apple_position)) +} \
{+ Inverted_Euclid_Dist_to_Apple = -1 * Euclid_Dist_to_Apple +} \
{+ reward_for_delta_distance_to_apple = Inverted_Euclid_Dist_to_Apple * 0.001 +}

</details>

<details>
<summary> <strong>Code</strong> </summary>

```python
reward_for_grabbing_apple = 0
reward_for_delta_distance_to_apple = 0
reward_for_reaching_max_apples = 0
reward_for_colliding_w_self = 0
reward_for_colliding_w_bound = 0
reward_for_timing_out = 0

# Reward for grabbing apple
if snake_head == apple_position:
    reward_for_grabbing_apple = 50

# Distance-based reward
Euclid_Dist_to_Apple = np.linalg.norm(np.array(snake_head) - np.array(apple_position))
Inverted_Euclid_Dist_to_Apple = -1 * Euclid_Dist_to_Apple
reward_for_delta_distance_to_apple = Inverted_Euclid_Dist_to_Apple * 0.001

# Reward for reaching max apples
if apple_count >= 30:
    reward_for_reaching_max_apples = 500

# Reward for colliding w self
if collision_with_self(snake_body) == 1:
    reward_for_colliding_w_self = -2 + (-1 * 0.05 * timesteps)

# Reward for colliding w boundary
if collision_with_boundaries(snake_head) == 1:
    reward_for_colliding_w_bound = -2 + (-1 * 0.05 * timesteps)

# Reward for timing out
if timesteps > 15000:
    reward_for_timing_out = -4 + (-1 * 0.05 * timesteps)

reward_for_this_step = reward_for_grabbing_apple + 
            reward_for_delta_distance_to_apple + 
            reward_for_reaching_max_apples + 
            reward_for_colliding_w_bound + 
            reward_for_colliding_w_self + 
            reward_for_timing_out
```

</details>

</details>

<details>
<summary> <strong>Discussion</strong> </summary>

Adding the distance-based reward made the performance terrible, so much so that I can't even capture anything particularly useful for the results. Also I ran it with the wrong file name which messed up the beginning of the graphs.

I think the best course of action right now is to take the best parts of the best performers and run them again with the updated logging functionality to get better insight on what was happening throughout the training.

</details>

<p align="center">
    <img alt="episode length mean" src="Source/exp_2/exp_2_data/visuals/images/01_14_24_SGE4r_11_PPO_r3_ep_len_mean.png" width="20%">   
&nbsp; &nbsp; &nbsp; &nbsp;
    <img alt="episode reward mean" src="Source/exp_2/exp_2_data/visuals/images/01_14_24_SGE4r_11_PPO_r3_ep_rew_mean.png" width="20%">     
&nbsp; &nbsp; &nbsp; &nbsp;
    <img alt="evaluation of 30 episodes" src="Source/exp_2/exp_2_data/visuals/gifs/01_14_24_SGE4r_11_PPO_r3_3530000_1.gif" width="15%">
</p>

</details>

<details>
<summary> <strong>SGE4r_12</strong> </summary>

**Date:** 01/16/24

<details>
<summary> <strong>Observation Function</strong> </summary>

| <div align="center"> 0 </div>  | <div align="center"> 1 </div> | <div align="center"> 2 - 62 </div> | <div align="center"> 63 </div> | <div align="center"> 64 </div> | <div align="center"> 65 </div> | <div align="center"> 66 </div> | <div align="center"> 67 </div> |
| ------------- |:-------------:| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
| apple_pos_x | apple_pos_y | snake_body_components_buffer | snake_body_actual_length | rel_delta_x_to_apple | rel_delta_y_to_apple | vel_x | vel_y |

snake_body_components_buffer **=** { part1_x, part1_y, part2_x, part2_y, **...** , -1, -1 }

rel_delta_to_apple **=** apple_position **-** snake_head

vel_x, vel_y    **=** -10, 0    `if` action **==** 0

vel_x, vel_y    **=** 10, 0     `if` action **==** 1

vel_x, vel_y    **=** 0, 10     `if` action **==** 2

vel_x, vel_y    **=** 0, -10    `if` action **==** 3

</details>

<details>
<summary> <strong>Reward Function</strong> </summary>

<details>
<summary> <strong>Difference</strong> </summary>

{+ else +} \
{+     reward_for_NOT_grbbing_apple = -1 * 0.5 +}

{- Euclid_Dist_to_Apple = np.linalg.norm(np.array(self.snake_head) - np.array(self.apple_position)) -} \
{- Inverted_Euclid_Dist_to_Apple = -1 * Euclid_Dist_to_Apple -} \
{- reward_for_delta_distance_to_apple = Inverted_Euclid_Dist_to_Apple * 0.001 -}

</details>

<details>
<summary> <strong>Code</strong> </summary>

```python
reward_for_grabbing_apple = 0
reward_for_delta_distance_to_apple = 0
reward_for_reaching_max_apples = 0
reward_for_colliding_w_self = 0
reward_for_colliding_w_bound = 0
reward_for_timing_out = 0

# Reward for grabbing apple
if snake_head == apple_position:
    reward_for_grabbing_apple = 50
else
    reward_for_NOT_grbbing_apple = -1 * 0.5

# Reward for reaching max apples
if apple_count >= 30:
    reward_for_reaching_max_apples = 500

# Reward for colliding w self
if collision_with_self(snake_body) == 1:
    reward_for_colliding_w_self = -2 + (-1 * 0.05 * timesteps)

# Reward for colliding w boundary
if collision_with_boundaries(snake_head) == 1:
    reward_for_colliding_w_bound = -2 + (-1 * 0.05 * timesteps)

# Reward for timing out
if timesteps > 16000:
    reward_for_timing_out = -4 + (-1 * 0.05 * timesteps)

reward_for_this_step = reward_for_grabbing_apple + 
            reward_for_delta_distance_to_apple + 
            reward_for_reaching_max_apples + 
            reward_for_colliding_w_bound + 
            reward_for_colliding_w_self + 
            reward_for_timing_out
```

</details>

</details>

<details>
<summary> <strong>Discussion</strong> </summary>

The results for gear 12 were among the worst in this entire research. Unlike past poor performers, gear 12 doesn't even work its way out of the -2 reward trend. It also periodically spikes *down* the way average performers do toward the end of training.

Gear 12 tested out the idea that we should provide a negative reward for taking a step and not grabbing an apple. It makes sense this didn't converge since the agent is basically being punished for moving. Although I did make the punishment very small, like grabbing an apple should compensate for taking 50 or so steps without taking an apple. But I guess the punishment was so bad the agent didn't even have time to learn to grab apples.

</details>

</details>