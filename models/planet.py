

import math
from typing import Tuple

try:
    from OpenGL.GL import (
        glPushMatrix, glPopMatrix,
        glRotatef, glTranslatef, glColor3f,
        glMaterialfv, glColorMaterial,
        GL_FRONT, GL_AMBIENT_AND_DIFFUSE,
    )
    from OpenGL.GLU import gluNewQuadric, gluSphere, gluQuadricNormals, GLU_SMOOTH
    _GL_AVAILABLE = True
except ImportError:
    _GL_AVAILABLE = False


class Planet:
   

    def __init__(
        self,
        name: str,
        radius: float,
        distance_from_sun: float,
        color: Tuple[float, float, float],
        orbit_speed: float = 10.0,
        rotation_speed: float = 60.0,
        tilt: float = 0.0,
        slices: int = 32,
        stacks: int = 32,
    ) -> None:
        self.name: str = name
        self.radius: float = radius
        self.distance_from_sun: float = distance_from_sun
        self.color: Tuple[float, float, float] = color
        self.orbit_speed: float = orbit_speed
        self.rotation_speed: float = rotation_speed
        self.tilt: float = tilt
        self.slices: int = slices
        self.stacks: int = stacks

        # Current angles in degrees – updated every frame
        self.orbit_angle: float = 0.0
        self.rotation_angle: float = 0.0

        # Moons attached to this planet (populated externally or by SolarSystem)
        self.moons: list = []

        # GLU quadric – created lazily on first draw so it lives inside a
        # valid OpenGL context.
        self._quadric = None

    # ── Update ────────────────────────────────────────────────────────────────

    def update(self, delta_time: float) -> None:
       
        self.orbit_angle = (self.orbit_angle + self.orbit_speed * delta_time) % 360.0
        self.rotation_angle = (self.rotation_angle + self.rotation_speed * delta_time) % 360.0

        for moon in self.moons:
            moon.update(delta_time)

    # ── Draw ──────────────────────────────────────────────────────────────────

    def draw(self) -> None:
       
        if not _GL_AVAILABLE:
            return

        if self._quadric is None:
            self._quadric = gluNewQuadric()
            gluQuadricNormals(self._quadric, GLU_SMOOTH)

        glPushMatrix()

        # ── Orbit around the Sun ──────────────────────────────────────────────
        # Rotate the whole sub-space around Y so the planet sweeps its orbit.
        glRotatef(self.orbit_angle, 0.0, 1.0, 0.0)
        # Move out to the orbital radius.
        glTranslatef(self.distance_from_sun, 0.0, 0.0)

        # ── Axial tilt ────────────────────────────────────────────────────────
        glRotatef(self.tilt, 0.0, 0.0, 1.0)

        # ── Self-rotation ─────────────────────────────────────────────────────
        glRotatef(self.rotation_angle, 0.0, 1.0, 0.0)

        # ── Material / colour ─────────────────────────────────────────────────
        r, g, b = self.color
        glColor3f(r, g, b)
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [r, g, b, 1.0])

        # ── Sphere ────────────────────────────────────────────────────────────
        gluSphere(self._quadric, self.radius, self.slices, self.stacks)

        # ── Draw attached moons relative to this planet's position ───────────
        for moon in self.moons:
            moon.draw()

        glPopMatrix()

    # ── Helpers ───────────────────────────────────────────────────────────────

    def add_moon(self, moon: "Moon") -> None:  # type: ignore[name-defined]
        """Attach a Moon to this planet."""
        moon.parent_planet = self
        self.moons.append(moon)

    def __repr__(self) -> str:
        return (
            f"Planet(name={self.name!r}, radius={self.radius}, "
            f"distance={self.distance_from_sun}, orbit_angle={self.orbit_angle:.1f}°)"
        )


# Avoid circular-import issues when moon.py imports Planet for type hints.
from models.moon import Moon  # noqa: E402 – intentional deferred import
