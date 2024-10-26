import gymnasium as gym
from stable_baselines3 import PPO as ALGO
import os

main_dir = "./Source/part_2_dir"
algo_str = "A2C" #mod this to select the model algo
date_str = "12_15_23" #mod this to select the model date
run_str = "r2" #mod this to select the model run
zip_str = "40000.zip" #mod this to select the model zip

models_dir = main_dir + "/loadable_models" + "/" + algo_str + "/" + date_str + "/" + run_str + "/" + zip_str

env = gym.make("LunarLander-v2", render_mode="human")
env.reset()

model_path = f"{models_dir}"

model = ALGO.load(model_path, env=env)

episodes = 10

for ep in range(episodes):
    obs, info = env.reset()
    terminated = False
    while not terminated:
        env.render()
        action, _ = model.predict(obs)
        obs, reward, terminated, trunc, info = env.step(action)

env.close()