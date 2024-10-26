import gymnasium as gym
from stable_baselines3 import PPO as ALGO
from environment.SGE import SnakeGameEnv

env = SnakeGameEnv()
env.reset()

model = ALGO("MlpPolicy", env, verbose=1)

TIMESTEPS = 10000
for i in range(1,51):
    model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False)

env.close()