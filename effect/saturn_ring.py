import math
from OpenGL.GL import *

class SaturnRings:
    def __init__(self, inner_radius: float = 1.4, outer_radius: float = 2.3, segments: int = 64):
        self.inner_radius = inner_radius
        self.outer_radius = outer_radius
        self.segments = segments

    def draw_ring(self):
        glDisable(GL_LIGHTING)
        glColor4f(0.75, 0.68, 0.55, 0.8)
        
        glBegin(GL_TRIANGLE_STRIP)
        for i in range(self.segments + 1):
            angle = (2.0 * math.pi * i / self.segments)
            cos_a = math.cos(angle)
            sin_a = math.sin(angle)
            
            glVertex3f(self.inner_radius * cos_a, 0.0, self.inner_radius * sin_a)
            glVertex3f(self.outer_radius * cos_a, 0.0, self.outer_radius * sin_a)
        glEnd()
        
        glEnable(GL_LIGHTING)