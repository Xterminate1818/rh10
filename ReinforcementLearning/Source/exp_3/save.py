import os
from stable_baselines3 import PPO as ALGO

from environment.SGE import SnakeGameEnv
from tb_callbacks.Callback_AddLog_PerformancePoints import PerformancePointsCallback

# Note: You should be running this script from a system cmd that has been cd'd into the workspace directory with the appropriate env activated.
out_dir    = "./Source/exp_3/output_data"
date_str    = "01-17-24"    # mod this to specify the model date
env_str     = "SGE-18"         # ... env version
algo_str    = "PPO"         # ... algorithm
run_str     = "r3"          # ... run

log_dir     = out_dir + "/" + "logs"
report_dir  = out_dir + "/" + "eot_reports"
models_dir  = out_dir + "/" + "loadable_models" + "/" + date_str + "/" + env_str + "/" + algo_str + "/" + run_str

# Create directories for checkpoints, logs, and reports
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
if not os.path.exists(report_dir):
    os.makedirs(report_dir)
if not os.path.exists(models_dir):
    os.makedirs(models_dir)

# Create the env
# Note: render_mode="human" will let you see what's happening as it trains, but training will be significantly slower.
env = SnakeGameEnv(
    dbg_report_dir      =   report_dir + "/" + date_str + "_" + env_str + "_" + algo_str + "_" + run_str + ".txt",
    render_run_str      =   run_str, 
    render_mode         =   "human"
)
env.reset()

# Instantiate the engine algorithm
model = ALGO(
    policy             =    "MlpPolicy", 
    env                =    env, 
    verbose            =    1, 
    tensorboard_log    =    log_dir
)

_TIMESTEPS_PER_CHECKPOINT   = 10000
_TOTAL_CHECKPOINTS          = 501       #Note: This is _TOTAL_CHECKPOINTS - 1 in reality.
#Note: Training will last _TIMESTEPS_PER_CHECKPOINT * (_TOTAL_CHECKPOINTS - 1)

for i in range(1, _TOTAL_CHECKPOINTS):
    model.learn(
        total_timesteps     =   _TIMESTEPS_PER_CHECKPOINT,
        callback            =   PerformancePointsCallback(),
        reset_num_timesteps =   False, 
        tb_log_name         =   date_str + "_" + env_str + "_" + algo_str + "_" + run_str
    )
    
    model.save(f"{models_dir}/{_TIMESTEPS_PER_CHECKPOINT * i}")

env.close()