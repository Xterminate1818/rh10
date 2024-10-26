import gymnasium as gym
from stable_baselines3 import PPO as ALGO
import os
from exp_1_env.snakegame_env_3 import SnakeGameEnv

main_dir = "./Source/exp_1/exp_1_data"
algo_str = "PPO" #mod this to specify the model algo
date_str = "12_19_23" #mod this to specify the model date
run_str = "r2" #mod this to specify the model run

log_dir = main_dir + "/logs"
models_dir = main_dir + "/loadable_models" + "/" + algo_str + "/" + date_str + "/" + run_str

if not os.path.exists(models_dir):
    os.makedirs(models_dir)

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

env = SnakeGameEnv()
env.reset()

model = ALGO("MlpPolicy", env, verbose=1, tensorboard_log=log_dir)

TIMESTEPS = 10000
for i in range(1,30):
    model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name=algo_str + "_" + date_str + "_" + run_str)
    model.save(f"{models_dir}/{TIMESTEPS*i}")

env.close()