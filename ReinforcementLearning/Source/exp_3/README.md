# exp_3

The goal of this experiment is to solve the Snake Game environment. To do so, we start by building upon the codebase from [exp_2](Source/exp_2). As the solution is developed we update the observation function and the reward function between iterations of exp_3. The workflow consists of utilizing a variant of **SGE** and **exp_3** where SGE is the template for the environment (contains observation and reward functions) and exp_3 is the template for the training activity (save model, load model, etc.). SGE is modified, then deployed using exp_3, then the results are studied in order to make a new modification to SGE before being evaluated again using exp_3. The pattern continues, building upon itself from version to version, until a suitable result is obtained in the context of solving the Snake Game environment.

## Contents

- [Workflow](#workflow)
    - [Training a Model](#training-a-model-and-saving-it)
    - [Loading a Model](#loading-a-model-to-evaluate-it)
    - [Visualizing Model Performance using TensorBoard](#visualizing-model-performance-using-tensorboard)
    - [Visualizing a Model as a .gif File](#loading-a-model-to-evaluate-it-and-save-the-visualization-to-a-gif-file)
- [Results](#results)

## Workflow

**Note:** For organizational purposes, SGE (environment) scripts are in the [environment](Source/exp_3/environment) folder.

**Note:** The [test.py](Source/exp_3/test.py) script isn't really used for training a model, it is meant to be used to output debug messages that should be appearing during run-time from the SGE script, so it is a script meant for debugging/development of the environment rather than actual agent training activities.

### Training a model and saving it

I suggest utilizing system cmd terminals since you can open multiples of them and have each of them train a model, you'd be surprised how model performance can be very different going from one training session to another, even if using the same SGE4r environment and the same exp_2 training activity script. 

**WARNING:** Remember that when training this way with multiple terminals, they're different models from each other. In other words, they're separate agents - they're not sharing experience with each other.

The script used to launch a training session is [save.py](Source/exp_3/save.py)

- Open a CMD terminal, outside of VS Code
- utilizing the ```dir```/```cd``` commands, navigate to the workspace folder
    - i.e. type `cd Desktop/Development/SkillNexus/SentdexRLTutorials` and press enter
- activate the project VENV
    - i.e. type `C:/Users/Mauricio/Desktop/Development/SkillNexus/SentdexRLTutorials/VENV/sentdexrltutorials/Scripts/activate` and press enter
- run the training script
    - i.e. type `C:/Users/Mauricio/Desktop/Development/SkillNexus/SentdexRLTutorials/Source/exp_3/save.py` and press enter

Remember that you should go into [save.py](Source/exp_3/save.py) and update the training details at the top of the script. By updating the training details you can save different agents and differentiate between them.

If you need to stop training click on the CMD terminal to restore focus to it and then press `ctrl + c` many times until the script is interrupted. You CAN continue to train at a later time, see the next section for instructions.

### Continue to train a model and save it after having had to pause training (warning: imperfect solution)

**WARNING - TODO:** The [continue.py](Source/exp_3/continue.py) script needs to be updated to ensure that the instructions in this section work.

**WARNING - TODO:** The instructions here are imperfect: Training will continue and complete but the logs used by tensorboard will be incoherent.

The script used to continue a training session is [continue.py](Source/exp_3/continue.py)

- Open a CMD terminal, outside of VS Code
- utilizing the ```dir```/```cd``` commands, navigate to the workspace folder
    - i.e. type `cd Desktop/Development/SkillNexus/SentdexRLTutorials` and press enter
- activate the project VENV
    - i.e. type `C:/Users/Mauricio/Desktop/Development/SkillNexus/SentdexRLTutorials/VENV/sentdexrltutorials/Scripts/activate` and press enter
- run the continue training script
    - i.e. type `C:/Users/Mauricio/Desktop/Development/SkillNexus/SentdexRLTutorials/Source/exp_3/continue.py` and press enter

Remember that you should go into [continue.py](Source/exp_3/continue.py) and update the training details at the top of the script. By updating the training details you can have the agent pickup where it left off in the previous training session.

### Loading a model to evaluate it

For loading a model and evaluating it, i.e. to look at what an agent does, you don't necessarily need to use a cmd terminal that is external to VS Code.

The script used to launch an evaluation session is [load.py](Source/exp_3/load.py)

- Open a CMD terminal, outside of VS Code
- utilizing the ```dir```/```cd``` commands, navigate to the workspace folder
    - i.e. type `cd Desktop/Development/SkillNexus/SentdexRLTutorials` and press enter
- activate the project VENV
    - i.e. type `C:/Users/Mauricio/Desktop/Development/SkillNexus/SentdexRLTutorials/VENV/sentdexrltutorials/Scripts/activate` and press enter
- run the load checkpoint script
    - i.e. type `C:/Users/Mauricio/Desktop/Development/SkillNexus/SentdexRLTutorials/Source/exp_3/load.py` and press enter

You should go into the [load.py](Source/exp_3/load.py) and update the loading details at the top of the script. The main parameter that needs updating is the time_str parameter since it points to the checkpoint that you wish to load. One thing to remember is that in order for you to know which checkpoint to load you should inspect *tensorboard* to find the checkpoint with the best average reward.

### Visualizing model performance using TensorBoard

- Open a CMD terminal, outside of VS Code
- utilizing the ```dir```/```cd``` commands, navigate to the workspace folder
    - i.e. type `cd Desktop/Development/SkillNexus/SentdexRLTutorials` and press enter
- activate the project VENV
    - i.e. type `C:/Users/Mauricio/Desktop/Development/SkillNexus/SentdexRLTutorials/VENV/sentdexrltutorials/Scripts/activate` and press enter
- utilizing the ```dir```/```cd``` commands, navigate to the appropriate data folder
    - i.e. type `cd Source/exp_3/output_data` and press enter
- run TensorBoard
    - i.e. type `tensorboard --logdir=logs` and press enter

### Loading a model to evaluate it and save the visualization to a gif file

For loading. evaluating, and saving the visualization of a model to a gif file, i.e. to look at what an agent does and save it to a gif, you don't necessarily need to use a cmd terminal that is external to VS Code.

The script used to launch an evaluation session and record it to a gif is [load_to_gif.py](Source/exp_3/load_to_gif.py)

- Open a CMD terminal, outside of VS Code
- utilizing the ```dir```/```cd``` commands, navigate to the workspace folder
    - i.e. type `cd Desktop/Development/SkillNexus/SentdexRLTutorials` and press enter
- activate the project VENV
    - i.e. type `C:/Users/Mauricio/Desktop/Development/SkillNexus/SentdexRLTutorials/VENV/sentdexrltutorials/Scripts/activate` and press enter
- run the load checkpoint to save it to gif script
    - i.e. type `C:/Users/Mauricio/Desktop/Development/SkillNexus/SentdexRLTutorials/Source/exp_3/load_to_gif.py` and press enter

You should go into the [load_to_gif.py](Source/exp_3/load_to_gif.py) and update the loading details at the top of the script. You can also edit the gif parameters that follwo. The main parameter that needs updating is the time_str parameter since it points to the checkpoint that you wish to load. One thing to remember is that in order for you to know which checkpoint to load you should inspect *tensorboard* to find the checkpoint with the best average reward. You can then modify the gif parameters so that you can properly label the agent that you just recorded.

## Results

<details>
<summary> <strong>SGE</strong> </summary>

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

(coming soon)

</details>
