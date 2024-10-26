# part_4

This tutorial builds upon the concepts covered in part_3 by making slight modifications to the `part_3_save.py` script around the observation space and reward function that are given to the agent each step.

## Summary

In part_3 we saw the process for gym-ifying a custom environment and also how to define the observation space and the reward function. In this part we modify both the observation space and the reward function in order to show that making changes to these two components has an effect, good or bad, to the agent's performance in solving the environment. The difference in performance can most easily be seen by viewing the "run" metrics graphs on tensorboard.

## part_4_save.py and snakegame_env_2.py

These two scripts are very similar to `part_3_save.py` and `snakegame_env.py` from part_3, the main difference is `snakegame_env_2.py` is modified so that the observation space and the reward function are different, and therefore result in an agent with *different* performance.

## Discussion

After running `part_4_save.py` and inspecting the content of `snakegame_env_2.py` you'll gain more understanding on how to define an observation space and a reward function, as well as see that your method for defining them has a direct impact on the performance and behavior exhibited by your agent. Further, this part opens the door for you to start properly experimenting with RL by defining your own custom environments and then trying to define adequate observation spaces and reward functions so that the agent can solve the environment.