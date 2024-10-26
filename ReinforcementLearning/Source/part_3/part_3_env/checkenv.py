from stable_baselines3.common.env_checker import check_env
from snakegame_env import SnakeGameEnv

env = SnakeGameEnv()

check_env(env)