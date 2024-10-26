# part_3

This tutorial builds upon the concepts covered in part_2 by explaining how to setup a custom environment so that your agent can interact with it and learn to solve it.

## Summary

In part_1 and in part_2 we utilized existing environments provided by the gym package. Our goal is to learn how to create agents for custom environments. To do that, we utilize an existing game, snake game, and translate it to a syntax that is consistent with gym environments. Once that is done, the environment can be instantiated normally and the agent can interact with it like any other gym environment.

## part_3_save.py

This script is exactly like `part_2_save.py` except it utilizes an instance of our *custom environment* instead of the `LunarLander-v2` environment.

## snakegame_base.py

This script is the actual game that is human-playable which we translate into gym-compatible syntax. If you wanted to see how the game works, you can just run this script and play it yourself.

## snakegame_env.py

This script is the gym-compatible version of `snakegame_base.py`. Notably, this version of the game isn't human-playable, but it is agent-playable.

## checkenv.py and doublecheckenv.py

These are helper scripts that can be ran to verify that the `snakegame_env.py` script is gym-compatible and can be utilized safely in `part_3_save.py`.

## Discussion

After running `part_3_save.py` you'll see in tensorboard that the performance is generally slowly improving but it definitely does not converge to anything meaningful. This means that either your observation space or reward function needs improvement. Essentially, depending on what your providing to the agent as the observation, the Agent will make decisions that can be either good or bad. Similarly, the reward function will define what the agent finds incentivizing as a result of taking any particular action. So the take away for this part is that not only do you have to define your environment but you also have to define good observations and provide adequate rewards so that the environment can be solved.