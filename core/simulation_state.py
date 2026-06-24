
class SimulationState:
    def __init__(self):
        self.time_scale = 1.0
        self.paused = False

    def get_delta_time(self, dt):
        if self.paused:
            return 0.0

        return dt * self.time_scale