from OpenGL.GLUT import *

from core.simulation_state import SimulationState
from core.camera import Camera

simulation = SimulationState()
camera = Camera()


def keyboard(key, x, y):
    global simulation

    if key == b' ':
        simulation.paused = not simulation.paused

    elif key == b'+':
        simulation.time_scale *= 2

    elif key == b'-':
        simulation.time_scale /= 2

    elif key == b'r':
        simulation.time_scale *= -1

    elif key == b'\x1b':
        glutLeaveMainLoop()


def special_keys(key, x, y):
    global camera

    if key == GLUT_KEY_LEFT:
        camera.rotate_left()

    elif key == GLUT_KEY_RIGHT:
        camera.rotate_right()

    elif key == GLUT_KEY_UP:
        camera.rotate_up()

    elif key == GLUT_KEY_DOWN:
        camera.rotate_down()

    glutPostRedisplay()