
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


