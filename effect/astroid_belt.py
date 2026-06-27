import random
import math
from OpenGL.GL import *

class AsteroidBelt:
    def __init__(self, count: int = 400, inner_r: float = 17.0, outer_r: float = 20.0):
        self.asteroids = []
        self.generate_asteroids(count, inner_r, outer_r)

    def generate_asteroids(self, count, inner_r, outer_r):
        """Distributes orbital fragments between Mars and Jupiter bounds."""
        for _ in range(count):
            radius = random.uniform(inner_r, outer_r)
            angle = random.uniform(0.0, 360.0)
            speed = random.uniform(5.0, 15.0)  
            size = random.uniform(0.03, 0.08)
            y_offset = random.uniform(-0.5, 0.5) 
            
            self.asteroids.append({
                'radius': radius,
                'angle': angle,
                'speed': speed,
                'size': size,
                'y_offset': y_offset
            })

    def update_asteroids(self, delta_time: float):
        """Advances positions systematically over intervals."""
        for ast in self.asteroids:
            ast['angle'] = (ast['angle'] + ast['speed'] * delta_time) % 360.0

    def draw_asteroids(self):
        """Renders positions."""
        glDisable(GL_LIGHTING)
        glColor3f(0.55, 0.50, 0.48) 

        glBegin(GL_POINTS)
        for ast in self.asteroids:
            rad = math.radians(ast['angle'])
            x = ast['radius'] * math.cos(rad)
            z = ast['radius'] * math.sin(rad)
            glVertex3f(x, ast['y_offset'], z)
        glEnd()
        
        glEnable(GL_LIGHTING)