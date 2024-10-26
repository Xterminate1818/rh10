from Source.exp_2.exp_2_env.snakegame_env_4 import SnakeGameEnv

env = SnakeGameEnv()
episodes = 50

for episode in range(episodes):
    done = False
    obs = env.reset()
    while True:
        random_action = env.action_space.sample()
        obs, reward, done, trunc, info = env.step(random_action)