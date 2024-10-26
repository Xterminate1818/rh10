# part_1

This tutorial introduces the workflow for implementing reinforcement learning in the context of the stable baselines 3 and gymnasium packages.

## Summary

This tutorial covers how to instantiate a gym environment, minimally initialize it, and close it properly once you're done with it. It also covers how to view actions that are available in any particular environment. Clarity is provided with regard to what really matters with respect to algorithm learning, which is the reward mechanism and the observation space - things like hyperparameters are important but not nearly as much. The benefit of the workflow shown in this tutorial is that you can swap out environments and optimization algorithms on the fly without having to explicitly open up either. This is consistent with the modular nature of the workflows that we use in the professional and hobbyist fields. And of course modularity is beneficial since you can modify things as you like in a plug-and-play fashion, that is to say, if you want a different environmet or algorithm you just "disconnect" or "unplug" the old one and "connect" or "hookup" the new one, without having to modify the rest of your code-base.

One thing to note is that, yes, we're training an agent, but its "brain" isn't being saved anywhere. This means that we made our computer "execute" the agent's learning, but then at the end of the traning, we just delete the agent, and therefore the "learning experience" is lost. This would be like studying for an exam for 2 hours then magically forgetting everything you studied.

There are some terms that you absolutely must be aware of in order to proceed with this tutorial.

### Key Terms

| Term  | Description |
| ------------- |:-------------:|
| Environment | <div align="left"> The *environment* is the reality in which the *agent* finds itself and can be thought of as the "problem" that you are trying to solve, for example cartpole, lunar lander, or some other custom environment. If you're trying to make an AI that plays a game, the game would be the environment. </div> |
| Model | <div align="left"> The *model* is the algorithm that you are using as the agent's optimization policy, for example PPO, SAC, TRPO, TD3, etc... </div> |
| Agent | <div align="left"> The *agent* is the entity that interacts with the environment, for example the cart in cartpole or the lander in lunar lander. </div> |
| Observation | <div align="left"> An *observation*, which is also known as a *state*, is the collection of data representing important details about the *environment* that are fed to the *agent* for the *agent* to make action predictions. An observation can be thought of as the snapshot of information about the *environment* that is perceived by the *agent* at any particular time-step. </div> |
| Action | <div align="left"> An *action* is what the *agent* decides to do, after taking an *observation*, at a particular time-step. "Go left" could be an *action* that the *agent* decides to execute after having made an *observation* on the *environment* at time, t. |
| Step | <div align="left"> A *step* is what occurs after the *agent* has taken an *action*. *Steps* tell the environment to progress which results in the *environment* updating to a new state, from which new subsequent *observations* and *actions* can be made. </div> |
| Discrete | <div align="left"> *Actions* that are constrained to a finite domain, for example "go left" or "go right". Can be thought of as an int-constrained parameter. </div> |
| Continuous | <div align="left"> *Actions* that are not constrained to a finite domain, for example "go 0.02 left" or "go 0.5 right". Can be thought of as a range-constrained parameter. </div> |