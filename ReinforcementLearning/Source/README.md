# Source

The source code for this repository is separated by "part" with respect to the [Sentdex tutorial series](https://www.youtube.com/playlist?list=PLQVvvaa0QuDf0O2DWwLZBfJeYY-JOeZB1) and by "experiment" with respect to my individual efforts to solve the Snake Game environment.

**The Active Directory for this Repo:** [exp_3](Source/exp_3)

### Contents

| Part  | Description |
| ------------- |:-------------:|
| [part_1](https://www.youtube.com/watch?v=XbWhJdQgi7E)      | <div align="left"> How to setup gym and stable baselines 3 to train an agent using PPO on the "LunarLander-v2" environment. </div>     |
| [part_2](https://www.youtube.com/watch?v=dLP-2Y6yu70)      | <div align="left"> Shows how to **save** and/or **load** an agent. </div>     |
| [part_3](https://www.youtube.com/watch?v=uKnjGn8fF70)      | <div align="left"> How to take a custom environment and make it compatible with the training methods shown in *the previous parts*. </div>     |
| [part_4](https://www.youtube.com/watch?v=yvwxbkKX9dc)      | <div align="left"> A variant of *part 3* in an attempt to get better performance from the agent. </div>     |
| exp_1 | <div align="left"> The same as *part 4* except the rendering library was translated from cv2 to pygame, which is much more performant during training. </div>     |
| exp_2 | <div align="left"> A series of variants of *exp_1* attempting to solve the Snake Game environment. exp_2 was used to develop the workflow and improve the code-base for the environment and the training scripts. Results were shown in a drop-down format at the end of the landing page. This method for showing results was deprecated since the workflow as causing rollover after every single version. </div> |
| exp_3 | <div align="left"> The latest in Snake-Game-solving agent development. Mainly the difference between this and the previous exp is that in exp_3 we adopt a new workflow for testing different reward functions and reward values which uses tables so that different configurations do not cause a version rollover. This makes it so that the results section in the landing page is more readable and it's easier to try new configurations and document them. </div> |

**Note:**

Parts **1 - 4** strictly follow the source tutorials. You can click the hyperlinks to open the source tutorial directly.