import random
import math 
from OpenGL.GL import *

class StarField:
    def __init__(self, count: int = 1000, distribution_radius: float = 300.0):
        self.count = count
        self.radius = distribution_radius
        self.stars = []
        self.generate_stars()

    def generate_stars(self):
        """Generates static positions along a celestial spherical boundary."""
        self.stars.clear()
        for _ in range(self.count):
            theta = random.uniform(0, 2.0 * 3.14159265)
            phi = math.acos(random.uniform(-1.0, 1.0))
            
            x = self.radius * math.sin(phi) * math.cos(theta)
            y = self.radius * math.sin(phi) * math.sin(theta)
            z = self.radius * math.cos(phi)
            
            brightness = random.uniform(0.5, 1.0)
            self.stars.append((x, y, z, brightness))

    def draw_stars(self):
        """Renders points inside disabling matrix dependencies safely."""
        glDisable(GL_LIGHTING)
        glPushMatrix()
        glLoadIdentity()
        
        glBegin(GL_POINTS)
        for x, y, z, b in self.stars:
            glColor3f(b, b, b)
            glVertex3f(x, y, z)
        glEnd()
        
        glPopMatrix()
        glEnable(GL_LIGHTING)