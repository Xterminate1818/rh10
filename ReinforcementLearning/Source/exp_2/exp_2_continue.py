import gymnasium as gym
from stable_baselines3 import PPO as ALGO
import os
from exp_2_env.SGE4r_2 import SnakeGameEnv

#WARNING: This script should only be executed AFTER exp_2_save.py has been executed at least once.

main_dir = "./Source/exp_2/exp_2_data"
#WARNING: The file below is what will be loaded
algo_str = "PPO" #mod this to specify the model algo
date_str = "01_06_24" #mod this to specify the model date
run_str = "r2" #mod this to specify the model run
zip_str = "340000.zip" #mod this to select the model zip

log_dir = main_dir + "/logs"
models_dir = main_dir + "/loadable_models" + "/" + algo_str + "/" + date_str + "/" + run_str
load_dir = main_dir + "/loadable_models" + "/" + algo_str + "/" + date_str + "/" + run_str + "/" + zip_str

env = SnakeGameEnv()
env.reset()

model = ALGO.load(load_dir)
model.set_env(env)

TIMESTEPS = 10000
#WARNING: Make sure you updated this number...
CONTINUE_BOOKMARK = 35
for i in range(CONTINUE_BOOKMARK,51):
    model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name=algo_str + "_" + date_str + "_" + run_str)
    model.save(f"{models_dir}/{TIMESTEPS*i}")

env.close()