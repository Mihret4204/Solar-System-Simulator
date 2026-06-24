import math
from OpenGL.GLU import gluLookAt


class Camera:
    def __init__(self):
        self.distance = 60.0

        self.yaw = 45.0
        self.pitch = 20.0

    def apply(self):
        yaw_rad = math.radians(self.yaw)
        pitch_rad = math.radians(self.pitch)

        eye_x = self.distance * math.cos(pitch_rad) * math.sin(yaw_rad)
        eye_y = self.distance * math.sin(pitch_rad)
        eye_z = self.distance * math.cos(pitch_rad) * math.cos(yaw_rad)

        gluLookAt(
            eye_x,
            eye_y,
            eye_z,
            0.0,
            0.0,
            0.0,
            0.0,
            1.0,
            0.0,
        )

    def zoom_in(self):
        self.distance = max(10.0, self.distance - 2)

    def zoom_out(self):
        self.distance = min(150.0, self.distance + 2)

    def rotate_left(self):
        self.yaw -= 5

    def rotate_right(self):
        self.yaw += 5

    def rotate_up(self):
        self.pitch = min(89, self.pitch + 5)

    def rotate_down(self):
        self.pitch = max(-89, self.pitch - 5)