"""
Orbital mechanics primitives. Pure math, no OpenGL.
"""

import math
from typing import Tuple

Vec3 = Tuple[float, float, float]


def advance_angle(current_deg: float, speed_deg_per_sec: float, delta_time: float) -> float:
    """Advance an orbital or rotation angle by speed * dt, wrapped to [0, 360)."""
    return (current_deg + speed_deg_per_sec * delta_time) % 360.0


def period_to_angular_speed(period_seconds: float) -> float:
    """Convert orbital period (seconds per full revolution) to deg/sec."""
    if period_seconds <= 0:
        return 0.0
    return 360.0 / period_seconds


def angular_speed_to_period(speed_deg_per_sec: float) -> float:
    """Inverse of period_to_angular_speed."""
    if speed_deg_per_sec <= 0:
        return float("inf")
    return 360.0 / speed_deg_per_sec


def orbital_position(radius: float, angle_deg: float) -> Vec3:
    """Circular orbit in the XZ plane (Y is up). Returns (x, y, z)."""
    theta = math.radians(angle_deg)
    return (radius * math.cos(theta), 0.0, radius * math.sin(theta))


def inclined_orbital_position(
    radius: float, angle_deg: float, inclination_deg: float
) -> Vec3:
    """Circular orbit tilted about the X axis by inclination_deg."""
    theta = math.radians(angle_deg)
    incl = math.radians(inclination_deg)
    x = radius * math.cos(theta)
    y_flat = 0.0
    z_flat = radius * math.sin(theta)
    y = y_flat * math.cos(incl) - z_flat * math.sin(incl)
    z = y_flat * math.sin(incl) + z_flat * math.cos(incl)
    return (x, y, z)


def distance_vector(a: Vec3, b: Vec3) -> Vec3:
    """Vector from a to b (b minus a)."""
    return (b[0] - a[0], b[1] - a[1], b[2] - a[2])


def vector_magnitude(v: Vec3) -> float:
    """Euclidean length of a 3D vector."""
    return math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])


def distance_between(a: Vec3, b: Vec3) -> float:
    """Scalar distance from a to b."""
    return vector_magnitude(distance_vector(a, b))