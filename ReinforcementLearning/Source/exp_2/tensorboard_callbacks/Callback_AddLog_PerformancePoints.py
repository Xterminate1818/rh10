from stable_baselines3.common.callbacks import BaseCallback

class PerformancePointsCallback(BaseCallback):
    def _on_step(self) -> bool:
        #Note: "infos" is not misspelled
        #Note: the variable you want to record, in this case "performance_points", should be defined in the "info" dictionary at the end of step/reset in the env script
        #Note: You can group parameters by using the "groupname/parameter" formatting like paths in a file system 

        log_performance_points = self.locals["infos"][0]["performance_points"]
        self.logger.record("custom/performance_points", log_performance_points)
        
        return True