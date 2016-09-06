#!/usr/bin/env python3

from enum import Enum
import pygame # temporary
import os
import random

from game.tools import Constants

"""
Enum for Types of Shapes:
    - Circle
    - Square
    - Triangle
"""
class ShapeEnum(Enum):
    RANDOM = 0,
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
        self.hitbox = None
        self.collidesPlayer = False
    
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
        self.music_confirmation = pygame.mixer.Sound(os.path.join("assets", os.path.join("sounds", "Confirmation.ogg")))
        self.music_wrong = pygame.mixer.Sound(os.path.join("assets", os.path.join("sounds", "Wrong.ogg")))
        
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

        if shapeEnum == ShapeEnum.RANDOM:
            shapeEnum = random.choice([ShapeEnum.CIRCLE, ShapeEnum.SQUARE, ShapeEnum.TRIANGLE])
      
        proj.shape = shapeEnum
        proj.position = position
        proj.velocity = velocity
        proj.acceleration = acceleration        

        sprite = None
        hitbox = None
        # TODO replace sprite assignments with Constants / Configuration access
        if typeEnum == TypeEnum.BULLET:
            if shapeEnum == ShapeEnum.CIRCLE:
                sprite = Constants.config.getGameImage('CircleBullet')
                hitbox = Constants.config.getHitBox("BulletCircle")
            elif shapeEnum == ShapeEnum.SQUARE:
                sprite = Constants.config.getGameImage('SquareBullet')
                hitbox = Constants.config.getHitBox("BulletSquare")
            else:
                sprite = Constants.config.getGameImage('TriangleBullet')
                hitbox = Constants.config.getHitBox("BulletTriangle")
        else:
            if shapeEnum == ShapeEnum.CIRCLE:
                sprite = Constants.config.getGameImage('CircleTarget')
                hitbox = Constants.config.getHitBox("TargetCircle")
            elif shapeEnum == ShapeEnum.SQUARE:
                sprite = Constants.config.getGameImage('SquareTarget')
                hitbox = Constants.config.getHitBox("TargetSquare")
            else:
                sprite = Constants.config.getGameImage('TriangleTarget')
                hitbox = Constants.config.getHitBox("TargetTriangle")
        proj.sprite = sprite
        proj.hitbox = hitbox
        
    """ Updates all projectiles in the pool. """
    def update(self):

        resources = {ShapeEnum.CIRCLE: 0, ShapeEnum.SQUARE: 0, ShapeEnum.TRIANGLE: 0}

        for bullet in self.bullets:
            if bullet[0]:
                bullet[1].update()
                if bullet[1].position[1] < 0: bullet[0] = False
            
        liveTargets = []
        for target in self.targets:
            if target[0]:
                target[1].update()
                liveTargets.append(target[1])
                if target[1].position[1] > 900 or target[1].collidesPlayer:
                    target[1].position = [0, 0]
                    val = 3 if target[1].collidesPlayer else 1
                    target[0] = target[1].collidesPlayer = False
                    resources[target[1].shape] -= val
    
        for bullet in self.bullets:
            for target in self.targets:
                if not bullet[0] or not target[0]: continue
                
                bulletRect = bullet[1].hitbox.copy().move(bullet[1].position[0], bullet[1].position[1])
                targetRect = target[1].hitbox.copy().move(target[1].position[0], target[1].position[1])
                if bulletRect.colliderect(targetRect):
                    if (bullet[1].shape == target[1].shape):
                        target[0] = False
                        resources[bullet[1].shape] += 2
                        self.music_confirmation.play()
                    else:
                        self.music_wrong.play()
                    bullet[0] = False

        return resources, liveTargets # return resources for addition to player by game.

    """ Draws all projectiles in the pool. """
    def draw(self):
        for x in self.bullets:
            if x[0]: x[1].draw()
            
        for x in self.targets:
            if x[0]: x[1].draw()
