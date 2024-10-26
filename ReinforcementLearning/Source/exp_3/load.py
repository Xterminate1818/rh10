from stable_baselines3 import PPO as ALGO

from environment.SGE import SnakeGameEnv

# Note: You should be running this script from a system cmd that has been cd'd into the workspace directory with the appropriate env activated.
# The parameters here are to select which model to load.
main_dir    = "./Source/exp_3/output_data"
date_str    = "01-14-24"    # mod this to specify the model date
env_str     = "SGE-1"     # ... env version
algo_str    = "PPO"         # ... algorithm
run_str     = "r1"          # ... run
time_str    = "4980000"      # ... checkpoint

models_dir = main_dir + "/loadable_models" + "/" + date_str + "/" + env_str + "/" + algo_str + "/" + run_str + "/" + time_str + ".zip"

# Create the env
# Note: render_mode="human" will let you see what's happening as it trains, but training will be significantly slower.
env = SnakeGameEnv(render_mode="human")
env.reset()

# Load the algorithm checkpoint
model = ALGO.load(models_dir, env=env)

_EPISODES_TO_EVALUATE = 300

for ep in range(_EPISODES_TO_EVALUATE):
    obs, info = env.reset()
    terminated = False
    while not terminated:
        action, _ = model.predict(obs)
        obs, reward, terminated, trunc, info = env.step(action)

env.close()