class counter():

    def __init__(self) -> None:
        self.timestep_counter = 0
        self.total_timestep = 0
        self.checkpoint_counter = 0
    
    def counting_function(self, timesteps_to_count):
        for i in range(1, timesteps_to_count + 1):
            self.timestep_counter += 1
            self.total_timestep += 1

        if self.timestep_counter == 10000:
            print (self.total_timestep)
            self.timestep_counter -= 10000
            self.checkpoint_counter += 1
            print (self.checkpoint_counter)

            if self.checkpoint_counter == 500:
                print("END")

        


cnt = counter()

_TIMESTEPS_PER_CHECKPOINT = 10000
_TOTAL_CHECKPOINTS = 501 #Note: Number of executions is _TOTAL_CHECKPOINTS - 1 in reality.
for i in range(1, _TOTAL_CHECKPOINTS):
    cnt.counting_function(_TIMESTEPS_PER_CHECKPOINT)
    if i == 500:
        print("END, END")
    #model.learn(total_timesteps     = _TIMESTEPS_PER_CHECKPOINT, reset_num_timesteps = False, tb_log_name         = date_str + "_" + env_str + "_" + algo_str + "_" + run_str)
    
    #model.save(f"{models_dir}/{_TIMESTEPS_PER_CHECKPOINT * i}")