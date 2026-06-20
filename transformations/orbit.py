"""
Orbital mechanics primitives. Pure math.
"""

import math
from typing import Tuple

Vec3 = Tuple[float, float, float]


def advance_angle(current_deg: float, speed_deg_per_sec: float, delta_time: float) -> float:
    """Advance an orbital or rotation angle by speed * dt, wrapped to [0, 360)."""
    return (current_deg + speed_deg_per_sec * delta_time) % 360.0


def orbital_position(radius: float, angle_deg: float) -> Vec3:
    """Circular orbit in the XZ plane (Y is up). Returns (x, y, z)."""
    theta = math.radians(angle_deg)
    return (radius * math.cos(theta), 0.0, radius * math.sin(theta))


def distance_vector(a: Vec3, b: Vec3) -> Vec3:
    """Vector from a to b (b minus a)."""
    return (b[0] - a[0], b[1] - a[1], b[2] - a[2])


def vector_magnitude(v: Vec3) -> float:
    """Euclidean length of a 3D vector."""
    return math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])