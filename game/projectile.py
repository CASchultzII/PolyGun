#!/usr/bin/env python3

from enum import Enum

"""
Enum for Types of Shapes:
    - Circle
    - Square
    - Triangle
"""
class ShapeEnum(Enum):
    CIRCLE = 1,
    SQUARE = 2,
    TRIANGLE = 3

"""
Enum for Types of Projectiles:
    - Bullet
    - Target
"""
class TypeEnum(Enum):
    BULLET = 1,
    TARGET = 2

"""
Represents a projectile: any object that moves across the screen from top
to bottom.
"""
class Projectile:
    
    """Update this projectile."""
    def update(self):
        pass

    """Draw this projectile."""
    def draw(self):
        pass

"""
Holds projectile objects and is ready to create more on demand.
"""
class ProjectilePool:

    """
    Generates a new projectile at the specified position with provided velocity.
    """
    def generate(self, shapeEnum, typeEnum, position, velocity):
        pass

    """ Updates all projectiles in the pool. """
    def update(self):
        pass

    """ Draws all projectiles in the pool. """
    def draw(self):
        pass
