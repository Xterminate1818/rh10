from snakegame_env_3 import SnakeGameEnv

env = SnakeGameEnv()
episodes = 50

for episode in range(episodes):
    done = False
    obs = env.reset()
    while True:
        random_action = env.action_space.sample()
        obs, reward, done, trunc, info = env.step(random_action)