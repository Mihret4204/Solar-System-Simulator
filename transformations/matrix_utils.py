
try:
    from OpenGL.GL import glTranslatef, glRotatef, glScalef
    _GL_AVAILABLE = True
except ImportError:
    _GL_AVAILABLE = False


def apply_translation(x: float, y: float, z: float) -> None:
    if _GL_AVAILABLE:
        glTranslatef(x, y, z)


def apply_rotation(angle_deg: float, x: float, y: float, z: float) -> None:
    if _GL_AVAILABLE:
        glRotatef(angle_deg, x, y, z)


def apply_scale(sx: float, sy: float, sz: float) -> None:
    if _GL_AVAILABLE:
        glScalef(sx, sy, sz)


def compute_rotation_matrix_y(angle_deg: float):
    
    import math
    rad = math.radians(angle_deg)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)
    return [
        cos_a,  0.0, -sin_a, 0.0,
        0.0,    1.0,  0.0,   0.0,
        sin_a,  0.0,  cos_a, 0.0,
        0.0,    0.0,  0.0,   1.0
    ]