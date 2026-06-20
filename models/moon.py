

import math
from typing import Tuple, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from models.planet import Planet

try:
    from OpenGL.GL import (
        glPushMatrix, glPopMatrix,
        glRotatef, glTranslatef, glColor3f,
        glMaterialfv,
        GL_FRONT, GL_AMBIENT_AND_DIFFUSE,
    )
    from OpenGL.GLU import gluNewQuadric, gluSphere, gluQuadricNormals, GLU_SMOOTH
    _GL_AVAILABLE = True
except ImportError:
    _GL_AVAILABLE = False


class Moon:
   

    def __init__(
        self,
        name: str,
        radius: float,
        distance_from_planet: float,
        color: Tuple[float, float, float] = (0.8, 0.8, 0.8),
        orbit_speed: float = 60.0,
        rotation_speed: float = 30.0,
        orbit_inclination: float = 5.0,
        slices: int = 16,
        stacks: int = 16,
    ) -> None:
        self.name: str = name
        self.radius: float = radius
        self.distance_from_planet: float = distance_from_planet
        self.color: Tuple[float, float, float] = color
        self.orbit_speed: float = orbit_speed
        self.rotation_speed: float = rotation_speed
        self.orbit_inclination: float = orbit_inclination
        self.slices: int = slices
        self.stacks: int = stacks

        # Current angles in degrees
        self.orbit_angle: float = 0.0
        self.rotation_angle: float = 0.0

        # Set by Planet.add_moon(); kept as a weak reference (no cycle risk
        # since Planet already holds the list).
        self.parent_planet: Optional["Planet"] = None

        # GLU quadric created lazily on first draw.
        self._quadric = None

    # ── Update ────────────────────────────────────────────────────────────────

    def update(self, delta_time: float) -> None:
       
        self.orbit_angle = (self.orbit_angle + self.orbit_speed * delta_time) % 360.0
        self.rotation_angle = (self.rotation_angle + self.rotation_speed * delta_time) % 360.0

    # ── Draw ──────────────────────────────────────────────────────────────────

    def draw(self) -> None:
        
        if not _GL_AVAILABLE:
            return

        if self._quadric is None:
            self._quadric = gluNewQuadric()
            gluQuadricNormals(self._quadric, GLU_SMOOTH)

        glPushMatrix()

        # Orbital inclination (tilts the orbit plane slightly)
        glRotatef(self.orbit_inclination, 1.0, 0.0, 0.0)

        # Sweep orbit around the planet (Y axis)
        glRotatef(self.orbit_angle, 0.0, 1.0, 0.0)

        # Translate to orbital distance
        glTranslatef(self.distance_from_planet, 0.0, 0.0)

        # Self-rotation
        glRotatef(self.rotation_angle, 0.0, 1.0, 0.0)

        # Material / colour
        r, g, b = self.color
        glColor3f(r, g, b)
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [r, g, b, 1.0])

        # Sphere geometry
        gluSphere(self._quadric, self.radius, self.slices, self.stacks)

        glPopMatrix()

    def __repr__(self) -> str:
        return (
            f"Moon(name={self.name!r}, radius={self.radius}, "
            f"distance={self.distance_from_planet}, orbit_angle={self.orbit_angle:.1f}°)"
        )
