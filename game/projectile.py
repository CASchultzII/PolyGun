#!/usr/bin/env python3

from enum import Enum
import pygame # temporary
import os

from game.tools import Constants

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

    def __init__(self, shapeEnum, position, velocity, acceleration):
        self.position = position
        self.velocity = velocity # Pixels per second
        self.acceleration = acceleration # Pixels per second per second
        self.shape = shapeEnum
        self.sprite = None
    
    """Update this projectile."""
    def update(self):
        
        timeDelta = Constants.clock.get_time() / 1000.0
        self.position[1] += self.velocity * timeDelta
        self.velocity += self.acceleration * timeDelta
        
    """Draw this projectile."""
    def draw(self):
        Constants.screen.blit(self.sprite, self.position)

"""
Holds projectile objects and is ready to create more on demand.
"""
class ProjectilePool:

    def __init__(self):
        self.bullets = []
        self.targets = []
        
        for x in range(50): # Use configuration supplied pool size
            self.bullets.append([False, Projectile(None, [0, 0], 0, 0)])
            self.targets.append([False, Projectile(None, [0, 0], 0, 0)])
    
    def findEmptyProjectile(self, type):
        collection = None
        if type == TypeEnum.BULLET: collection = self.bullets
        else: collection = self.targets
        
        for x in collection:
            if not x[0]:
                x[0] = True
                return x[1]
                
        return None
    
    """
    Generates a new projectile at the specified position with provided velocity.
    """
    def generate(self, shapeEnum, typeEnum, position, velocity, acceleration):
        proj = self.findEmptyProjectile(typeEnum)
        if proj == None: return # Fail silently, all shapes in motion.
        
        proj.shape = shapeEnum
        proj.position = position
        proj.velocity = velocity
        proj.acceleration = acceleration
        
        sprite = None
        # TODO replace sprite assignments with Constants / Configuration access
        if typeEnum == TypeEnum.BULLET:
            if shapeEnum == ShapeEnum.CIRCLE:
                sprite = Constants.config.getGameImage('CircleBullet')
            elif shapeEnum == ShapeEnum.SQUARE:
                sprite = Constants.config.getGameImage('SquareBullet')
            else:
                sprite = Constants.config.getGameImage('TriangleBullet')
        else:
            if shapeEnum == ShapeEnum.CIRCLE:
                sprite = Constants.config.getGameImage('CircleTarget')
            elif shapeEnum == ShapeEnum.SQUARE:
                sprite = Constants.config.getGameImage('SquareTarget')
            else:
                sprite = Constants.config.getGameImage('TriangleTarget')
        proj.sprite = sprite
        
    """ Updates all projectiles in the pool. """
    def update(self):
        for x in self.bullets:
            if x[0]: x[1].update()
            if x[1].position[1] < 0: x[0] = False
            
        for x in self.targets:
            if x[0]: x[1].update()
            if x[1].position[1] > 900: x[0] = False
            
         # TODO generate collision detection code

    """ Draws all projectiles in the pool. """
    def draw(self):
        for x in self.bullets:
            if x[0]: x[1].draw()
            
        for x in self.targets:
            if x[0]: x[1].draw()
