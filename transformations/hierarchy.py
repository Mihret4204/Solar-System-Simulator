
from typing import List, Optional
try:
    from OpenGL.GL import glPushMatrix, glPopMatrix
    _GL_AVAILABLE = True
except ImportError:
    _GL_AVAILABLE = False

from transformations.matrix_utils import apply_translation, apply_rotation, apply_scale


class TransformationNode:
   

    def __init__(self, name: str) -> None:
        self.name: str = name
        self.children: List['TransformationNode'] = []
        
        # Local transformation attributes
        self.translation: list = [0.0, 0.0, 0.0]
        self.rotation_axis_angle: List[list] = []  # List of [angle, x, y, z] rotations sequence
        self.scale: list = [1.0, 1.0, 1.0]

    def add_child(self, child: 'TransformationNode') -> None:
        self.children.append(child)

    def set_translation(self, x: float, y: float, z: float) -> None:
        self.translation = [x, y, z]

    def add_rotation(self, angle_deg: float, x: float, y: float, z: float) -> None:
        self.rotation_axis_angle.append([angle_deg, x, y, z])

    def clear_rotations(self) -> None:
        self.rotation_axis_angle.clear()

    def set_scale(self, sx: float, sy: float, sz: float) -> None:
        self.scale = [sx, sy, sz]

    def execute_transformations(self) -> None:
        # 1. Translate local space
        apply_translation(*self.translation)
        
        # 2. Rotate local space sequentially
        for rot in self.rotation_axis_angle:
            apply_rotation(rot[0], rot[1], rot[2], rot[3])
            
        # 3. Scale local space
        if self.scale != [1.0, 1.0, 1.0]:
            apply_scale(*self.scale)

    def traverse_and_render(self, rendering_callback=None) -> None:
        
        if not _GL_AVAILABLE:
            return

        glPushMatrix()

        #Push down the local transformation frame
        self.execute_transformations()

        #Render geometry bound to this specific space frame
        if rendering_callback:
            rendering_callback(self.name)

        #Cascade transformations to children frames
        for child in self.children:
            child.traverse_and_render(rendering_callback)

        glPopMatrix()


def build_simulation_hierarchy(solar_system) -> TransformationNode:
    # Root node positioned at the Sun
    root = TransformationNode("Sun")
    
    for planet in solar_system.planets:
        planet_node = TransformationNode(planet.name)
        
        #Translate space by the planet's orbital sweep angle, then move outward
        planet_node.add_rotation(planet.orbit_angle, 0.0, 1.0, 0.0)
        planet_node.set_translation(planet.distance_from_sun, 0.0, 0.0)
        
        #Apply axial tilt and self-rotation
        planet_node.add_rotation(planet.tilt, 0.0, 0.0, 1.0)
        planet_node.add_rotation(planet.rotation_angle, 0.0, 1.0, 0.0)
        
        #Add moons relative to this planet
        for moon in planet.moons:
            moon_node = TransformationNode(moon.name)
            # Moons tilt, orbit their parent, and translate outward
            moon_node.add_rotation(moon.orbit_inclination, 1.0, 0.0, 0.0)
            moon_node.add_rotation(moon.orbit_angle, 0.0, 1.0, 0.0)
            moon_node.set_translation(moon.distance_from_planet, 0.0, 0.0)
            moon_node.add_rotation(moon.rotation_angle, 0.0, 1.0, 0.0)
            
            planet_node.add_child(moon_node)
            
        root.add_child(planet_node)
        
    return root