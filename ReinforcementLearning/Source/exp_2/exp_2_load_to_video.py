import os
from stable_baselines3 import PPO as ALGO
from stable_baselines3.common.vec_env import VecVideoRecorder, DummyVecEnv

from exp_2_env.SGE4r_11 import SnakeGameEnv

#WARNING: This script has not been tested at all

# Note: You should be running this script from a system cmd that has been cd'd into the workspace directory with the appropriate env activated.
# The parameters here are to select which model to load.
main_dir    = "./Source/exp_2/exp_2_data"
date_str    = "01_12_24"    # mod this to specify the model date
env_str     = "SGE4r_9"     # ... env version
algo_str    = "PPO"         # ... algorithm
run_str     = "r6"          # ... run
time_str    = "3940000"      # ... checkpoint

models_dir = main_dir + "/loadable_models" + "/" + date_str + "/" + env_str + "/" + algo_str + "/" + run_str + "/" + time_str + ".zip"

#Note: Each time you run this script, the model may behave slightly differently...
# The parameters here are to configure where to save the generated video.
video_str         = "1"      # ... video number
video_directory   = main_dir + "/visuals/videos/"
video_length      = 100
video_name        = date_str + "_" + env_str + "_" + algo_str + "_" + run_str + "_" + time_str + "_" + video_str

# Create directories for gifs
if not os.path.exists(video_directory):
    os.makedirs(video_directory)

# Create the vec_env
# Note: render_mode="human" will let you see what's happening as it trains, but training will be significantly slower.
vec_env = DummyVecEnv([lambda: SnakeGameEnv(render_mode="rgb_array")])
obs = vec_env.reset()

#Record...
vec_env = VecVideoRecorder(
    venv                    =    vec_env, 
    video_folder            =    video_directory,
    record_video_trigger    =    lambda x: x == 0,
    video_length            =    video_length,
    name_prefix             =    video_name
)

# Load the algorithm checkpoint
model = ALGO.load(models_dir, env=vec_env)

vec_env.reset()
for ep in range(video_length):
    obs, info = vec_env.reset()
    terminated = False
    while not terminated:
        action, _ = model.predict(obs)
        obs, reward, terminated, trunc, info = vec_env.step(action)

vec_env.close()