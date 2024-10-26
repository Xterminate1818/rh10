from stable_baselines3.common.env_checker import check_env
from Source.exp_2.exp_2_env.snakegame_env_4 import SnakeGameEnv

env = SnakeGameEnv()

check_env(env)