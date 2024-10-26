import os
from stable_baselines3 import PPO as ALGO
import imageio
import numpy as np

from exp_2_env.SGE4r_12 import SnakeGameEnv

# Note: You should be running this script from a system cmd that has been cd'd into the workspace directory with the appropriate env activated.
# The parameters here are to select which model to load.
main_dir    = "./Source/exp_2/exp_2_data"
date_str    = "01_14_24"    # mod this to specify the model date
env_str     = "SGE4r_11"     # ... env version
algo_str    = "PPO"         # ... algorithm
run_str     = "r3"          # ... run
time_str    = "3530000"      # ... checkpoint

models_dir = main_dir + "/loadable_models" + "/" + date_str + "/" + env_str + "/" + algo_str + "/" + run_str + "/" + time_str + ".zip"

#Note: Each time you run this script, the model may behave slightly differently...
# The parameters here are to configure where to save the generated gif.
gif_str         = "1"      # ... gif number
gif_directory   = main_dir + "/visuals/gifs"
gif_name        = date_str + "_" + env_str + "_" + algo_str + "_" + run_str + "_" + time_str + "_" + gif_str + ".gif"
gif_path        = gif_directory + "/" + gif_name
images          = []        # container for constructing a gif

# Create directories for gifs
if not os.path.exists(gif_directory):
    os.makedirs(gif_directory)

# Create the env
# Note: render_mode="human" will let you see what's happening as it trains, but training will be significantly slower.
env = SnakeGameEnv(render_mode="rgb_array")
env.reset()

# Load the algorithm checkpoint
model = ALGO.load(models_dir, env=env)

_EPISODES_TO_EVALUATE = 30

img = model.env.render(mode="rgb_array")
for ep in range(_EPISODES_TO_EVALUATE):
    obs, info = env.reset()
    terminated = False
    while not terminated:
        images.append(img)
        action, _ = model.predict(obs)
        obs, reward, terminated, trunc, info = env.step(action)
        img = model.env.render(mode="rgb_array")

imageio.mimsave(gif_path, [np.array(img) for i, img in enumerate(images) if i%2 == 0], fps=29)
env.close()