from OpenGL.GL import *
from OpenGL.GLUT import *

class SimulationUI:
    def __init__(self, simulation_state, solar_system):
        self.state = simulation_state
        self.solar_system = solar_system

    def draw_text(self, x: float, y: float, text: str, color=(1.0, 1.0, 1.0)):
        glColor3f(*color)
        glRasterPos2f(x, y)
        for char in text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

    def render(self, window_width: int, window_height: int):
       
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, window_width, 0, window_height, -1, 1)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        glDisable(GL_LIGHTING)
        glDisable(GL_DEPTH_TEST)

       
        self.draw_text(20, window_height - 30, "🪐 SOLAR SYSTEM SIMULATION", (0.0, 0.9, 1.0))
        
       
        status_str = "PAUSED" if self.state.paused else "RUNNING"
        status_color = (1.0, 0.3, 0.3) if self.state.paused else (0.3, 1.0, 0.3)
        self.draw_text(20, window_height - 60, f"Status: {status_str}", status_color)
        self.draw_text(20, window_height - 85, f"Time Scale: {self.state.time_scale:.2f}x")
        self.draw_text(20, window_height - 110, f"System Time: {self.solar_system.elapsed_time:.1f}s")

        self.draw_text(20, 70, "Controls:", (0.7, 0.7, 0.7))
        self.draw_text(20, 50, "[Space] Pause | [+ / -] Speed Up/Down | [R] Reverse", (0.6, 0.6, 0.6))
        self.draw_text(20, 30, "[Arrows] Rotate Cam | [Mouse Wheel] Zoom", (0.6, 0.6, 0.6))

        
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()