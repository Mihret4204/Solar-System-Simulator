import math
from typing import List, Optional, Tuple

try:
    from OpenGL.GL import (
        glEnable, glDisable, glPushMatrix, glPopMatrix,
        glMatrixMode, glLoadIdentity,
        glBegin, glEnd, glVertex3f, glColor3f, glColor4f,
        glTranslatef, glRotatef,
        glLightfv, glLightModelfv, glMaterialfv, glColorMaterial,
        glShadeModel,
        GL_DEPTH_TEST, GL_LIGHTING, GL_LIGHT0, GL_NORMALIZE,
        GL_COLOR_MATERIAL, GL_FRONT, GL_FRONT_AND_BACK,
        GL_AMBIENT, GL_DIFFUSE, GL_SPECULAR, GL_POSITION,
        GL_AMBIENT_AND_DIFFUSE, GL_SHININESS,
        GL_LINE_LOOP, GL_MODELVIEW, GL_SMOOTH,
        GL_LIGHT_MODEL_AMBIENT,
    )
    from OpenGL.GLU import gluNewQuadric, gluSphere, gluQuadricNormals, GLU_SMOOTH
    _GL_AVAILABLE = True
except ImportError:
    _GL_AVAILABLE = False
    print("[WARNING] PyOpenGL not available – Renderer is a no-op stub.")

from models.planet import Planet
from models.moon import Moon

from effect.stars import StarField
from effect.astroid_belt import AsteroidBelt
from effect.saturn_ring import SaturnRings

SUN_RADIUS: float = 2.5
SUN_COLOR: Tuple[float, float, float] = (1.0, 0.9, 0.0)
_PLANET_PARAMS: List[Tuple] = [
    ("Mercury", 0.30,  5.0, (0.72, 0.70, 0.68),  47.9, 10.8,   0.0),
    ("Venus",   0.50,  8.0, (0.90, 0.75, 0.40),  35.0,  6.5, 177.4),
    ("Earth",   0.55, 11.0, (0.20, 0.40, 1.00),  29.8, 360.0,  23.4),
    ("Mars",    0.45, 15.0, (0.85, 0.35, 0.15),  24.1, 350.9,  25.2),
    ("Jupiter", 1.20, 22.0, (0.80, 0.60, 0.40),  13.1, 870.5,   3.1),
    ("Saturn",  1.00, 30.0, (0.90, 0.80, 0.55),   9.7, 810.0,  26.7),
    ("Uranus",  0.80, 37.0, (0.55, 0.85, 0.95),   6.8, 501.6,  97.8),
    ("Neptune", 0.75, 44.0, (0.25, 0.40, 0.90),   5.4, 536.3,  28.3),
]
_ORBIT_SEGMENTS: int = 128

class Renderer:
    def __init__(self) -> None:
        self._planets: List[Planet] = []
        self._sun_quadric = None
        
        self.stars = StarField()
        self.asteroid_belt = AsteroidBelt()
        self.saturn_rings = SaturnRings()

        self._build_default_scene()

    def render(self, solar_system: Optional[object] = None) -> None:
        if not _GL_AVAILABLE: return
        planets, sun = self._resolve_scene(solar_system)

        self.stars.draw_stars()
        self._draw_orbits(planets)
        self.asteroid_belt.draw_asteroids()
        self._draw_sun(sun)
        self._draw_planets(planets)

    def update(self, delta_time: float) -> None:
        for planet in self._planets:
            planet.update(delta_time)
        self.asteroid_belt.update_asteroids(delta_time)

    def _build_default_scene(self) -> None:
        self._planets.clear()
        for (name, radius, dist, color, orb_spd, rot_spd, tilt) in _PLANET_PARAMS:
            p = Planet(name=name, radius=radius, distance_from_sun=dist, color=color, orbit_speed=orb_spd, rotation_speed=rot_spd, tilt=tilt)
            if name == "Earth":
                luna = Moon(name="Luna", radius=0.15, distance_from_planet=1.2, color=(0.80, 0.80, 0.78), orbit_speed=130.0, rotation_speed=130.0, orbit_inclination=5.1)
                p.add_moon(luna)
            self._planets.append(p)

    
    def setup_lighting(self) -> None:
        if not _GL_AVAILABLE: return
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_NORMALIZE)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
        glShadeModel(GL_SMOOTH)
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.05, 0.05, 0.05, 1.0])
        glLightfv(GL_LIGHT0, GL_POSITION, [0.0, 0.0, 0.0, 1.0])
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.10, 0.10, 0.10, 1.0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.00, 1.00, 0.95, 1.0])
        glLightfv(GL_LIGHT0, GL_SPECULAR, [0.80, 0.80, 0.80, 1.0])

    def _resolve_scene(self, solar_system: Optional[object]) -> Tuple[List[Planet], Optional[object]]:
        if solar_system is None: return self._planets, None
        return getattr(solar_system, "planets", self._planets), getattr(solar_system, "sun", None)

    def _draw_sun(self, sun: Optional[object] = None) -> None:
        if not _GL_AVAILABLE: return
        glDisable(GL_LIGHTING)
        if sun is not None and hasattr(sun, "draw"):
            try:
                sun.draw()
                glEnable(GL_LIGHTING)
                return
            except Exception as exc: pass

        if self._sun_quadric is None:
            self._sun_quadric = gluNewQuadric()
            gluQuadricNormals(self._sun_quadric, GLU_SMOOTH)

        glPushMatrix()
        glColor3f(*SUN_COLOR)
        gluSphere(self._sun_quadric, SUN_RADIUS, 48, 48)
        glPopMatrix()
        glEnable(GL_LIGHTING)

    def _draw_orbits(self, planets: List[Planet]) -> None:
        if not _GL_AVAILABLE: return
        glDisable(GL_LIGHTING)
        glColor3f(0.3, 0.3, 0.3)
        for planet in planets:
            dist = planet.distance_from_sun
            glBegin(GL_LINE_LOOP)
            for i in range(_ORBIT_SEGMENTS):
                angle = 2.0 * math.pi * i / _ORBIT_SEGMENTS
                glVertex3f(dist * math.cos(angle), 0.0, dist * math.sin(angle))
            glEnd()
        glEnable(GL_LIGHTING)

    def _draw_planets(self, planets: List[Planet]) -> None:
        for planet in planets:
            try:
                if planet.name == "Saturn":
                    glPushMatrix()
                    glRotatef(planet.orbit_angle, 0.0, 1.0, 0.0)
                    glTranslatef(planet.distance_from_sun, 0.0, 0.0)
                    glRotatef(planet.tilt, 0.0, 0.0, 1.0)
                    self.saturn_rings.draw_ring()
                    glPopMatrix()
                planet.draw()
            except Exception as exc:
                print(f"[WARNING] {planet.name}.draw() failed: {exc}")