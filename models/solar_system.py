"""
SolarSystem: authoritative scene graph for the simulation.
"""

from typing import List, Tuple

from models.planet import Planet
from models.moon import Moon

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


# (name, radius, distance_from_sun, color, orbit_speed, rotation_speed, tilt)
_PLANET_DATA: List[Tuple] = [
    ("Mercury", 0.30,  5.0, (0.72, 0.70, 0.68),  47.9,  10.8,   0.0),
    ("Venus",   0.50,  8.0, (0.90, 0.75, 0.40),  35.0,   6.5, 177.4),
    ("Earth",   0.55, 11.0, (0.20, 0.40, 1.00),  29.8, 360.0,  23.4),
    ("Mars",    0.45, 15.0, (0.85, 0.35, 0.15),  24.1, 350.9,  25.2),
    ("Jupiter", 1.20, 22.0, (0.80, 0.60, 0.40),  13.1, 870.5,   3.1),
    ("Saturn",  1.00, 30.0, (0.90, 0.80, 0.55),   9.7, 810.0,  26.7),
    ("Uranus",  0.80, 37.0, (0.55, 0.85, 0.95),   6.8, 501.6,  97.8),
    ("Neptune", 0.75, 44.0, (0.25, 0.40, 0.90),   5.4, 536.3,  28.3),
]


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
        self.elapsed_time: float = 0.0
        self._build_scene()

    def _build_scene(self) -> None:
        """Populate self.planets from the canonical data table."""
        self.planets.clear()
        for (name, radius, dist, color, orb_spd, rot_spd, tilt) in _PLANET_DATA:
            planet = Planet(
                name=name,
                radius=radius,
                distance_from_sun=dist,
                color=color,
                orbit_speed=orb_spd,
                rotation_speed=rot_spd,
                tilt=tilt,
            )
            if name == "Earth":
                planet.add_moon(Moon(
                    name="Luna",
                    radius=0.15,
                    distance_from_planet=1.2,
                    color=(0.80, 0.80, 0.78),
                    orbit_speed=130.0,
                    rotation_speed=130.0,
                    orbit_inclination=5.1,
                ))
            self.planets.append(planet)

    def update(self, delta_time: float) -> None:
        """Advance simulation clock and update every body."""
        self.elapsed_time += delta_time
        for planet in self.planets:
            planet.update(delta_time)