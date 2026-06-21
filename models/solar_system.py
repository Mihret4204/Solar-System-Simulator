"""
SolarSystem: authoritative scene graph for the simulation.
"""

from typing import List, Tuple

from models.planet import Planet

try:
    from OpenGL.GL import (
        glPushMatrix, glPopMatrix, glColor3f,
        glDisable, glEnable, GL_LIGHTING,
    )
    from OpenGL.GLU import (
        gluNewQuadric, gluSphere, gluQuadricNormals, GLU_SMOOTH,
    )
    _GL_AVAILABLE = True
except ImportError:
    _GL_AVAILABLE = False


class Sun:
    """Central star, drawn at the origin and always fully bright."""

    def __init__(
        self,
        radius: float = 2.5,
        color: Tuple[float, float, float] = (1.0, 0.9, 0.0),
    ) -> None:
        self.radius: float = radius
        self.color: Tuple[float, float, float] = color
        self._quadric = None

    def draw(self) -> None:
        if not _GL_AVAILABLE:
            return
        if self._quadric is None:
            self._quadric = gluNewQuadric()
            gluQuadricNormals(self._quadric, GLU_SMOOTH)

        glPushMatrix()
        glDisable(GL_LIGHTING)
        glColor3f(*self.color)
        gluSphere(self._quadric, self.radius, 48, 48)
        glEnable(GL_LIGHTING)
        glPopMatrix()


class SolarSystem:
    """Top level scene: Sun and orbiting planets."""

    def __init__(self) -> None:
        self.sun: Sun = Sun()
        self.planets: List[Planet] = []