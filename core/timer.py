import time
from OpenGL.GLUT import glutTimerFunc, glutPostRedisplay

class Timer:
    def __init__(self, simulation_state, renderer, solar_system):
        self.state = simulation_state
        self.renderer = renderer
        self.solar_system = solar_system
        
        self.last_clock_time = time.time()
        self.frame_interval_ms = 16  

    def update_scene(self, value: int):
        current_clock = time.time()
        raw_dt = current_clock - self.last_clock_time
        self.last_clock_time = current_clock
        
        scaled_dt = self.state.get_delta_time(raw_dt)
        
        if not self.state.paused:
           
            self.solar_system.update(scaled_dt)
            self.renderer.update(scaled_dt)

        
        glutPostRedisplay()
        glutTimerFunc(self.frame_interval_ms, self.update_scene, 0)

    def start_timer(self):
        self.last_clock_time = time.time()
        glutTimerFunc(self.frame_interval_ms, self.update_scene, 0)