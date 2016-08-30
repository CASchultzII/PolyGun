#!/usr/bin/env python3

from enum import Enum

"""
Enum for Types of Shapes:
    - Bullet
    - Target
"""
class ShapeEnum(Enum):
    BULLET = 1
    TARGET = 2

"""
Represents a projectile: any object that moves across the screen from top
to bottom.
"""
class Projectile:
    
    """Update this projectile."""
    def update():
        pass

    """Draw this projectile."""
    def draw():
        pass

"""
Holds projectile objects and is ready to create more on demand.
"""
class ProjectilePool:

    """
    Generates a new projectile at the specified position with provided velocity.
    """
    def generate(shapeEnum, position, velocity):
        pass

    """ Updates all projectiles in the pool. """
    def update():
        pass

    """ Draws all projectiles in the pool. """
    def draw():
        pass
