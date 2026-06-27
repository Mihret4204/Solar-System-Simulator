import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import control.keyboard as kb
import control.mouse as ms
from core.timer import Timer

window_width = 1024
window_height = 768
timer_instance = None
solar_system_ref = None
renderer_ref = None

def display_callback():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    if hasattr(kb, 'camera'):
        kb.camera.apply()
    
    if renderer_ref and solar_system_ref:
        renderer_ref.render(solar_system_ref)
    
    glutSwapBuffers()

def reshape_window(width: int, height: int):
    global window_width, window_height
    window_width = max(1, width)
    window_height = max(1, height)
    
    glViewport(0, 0, window_width, window_height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(window_width) / float(window_height), 0.1, 500.0)
    glMatrixMode(GL_MODELVIEW)

def register_callbacks():
    glutDisplayFunc(display_callback)
    glutReshapeFunc(reshape_window)
    glutKeyboardFunc(kb.keyboard)
    glutSpecialFunc(kb.special_keys)
    glutMouseFunc(ms.mouse)

def initialize_window():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(window_width, window_height)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Solar System Simulation")
    
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

def start_main_loop(solar_system_instance, renderer_instance):
    global timer_instance, solar_system_ref, renderer_ref
    solar_system_ref = solar_system_instance
    renderer_ref = renderer_instance
    
    
    initialize_window()
    renderer_instance.setup_lighting()
    register_callbacks()
    
    timer_instance = Timer(kb.simulation, renderer_instance, solar_system_instance)
    timer_instance.start_timer()
    
    glutMainLoop()