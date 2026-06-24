from OpenGL.GLUT import *

from control.keyboard import camera


def mouse(button, state, x, y):

    if state != GLUT_DOWN:
        return

    # Mouse wheel up
    if button == 3:
        camera.zoom_in()

    # Mouse wheel down
    elif button == 4:
        camera.zoom_out()

    glutPostRedisplay()