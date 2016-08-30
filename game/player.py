#!/usr/bin/env python3

import os
from enum import Enum
import pygame
from game.projectile import ShapeEnum, TypeEnum
from game.tools import Constants

class Direction(Enum):
    NONE = 0,
    LEFT = 1,
    RIGHT = 2

"""
Contains information on the current player instance.
"""
class PlayerInfo:

    """ Init this Player """
    def __init__(self, pool): #BAD COUPLING
        self.timeScore = 0
        self.timeCooldown = 0
        self.resources = {ShapeEnum.CIRCLE: 10, ShapeEnum.SQUARE: 10, ShapeEnum.TRIANGLE: 10}
        self.position = [236, 820] # TODO create a world coordinate transform
        self.sprite = pygame.image.load(os.path.join("assets", "cannon.png")).convert_alpha()
        self.dir = Direction.NONE
        self.pool = pool # BAD COUPLING

    """ Asks the PlayerInfo to try to fire. """
    def fire(self, shapeEnum):
        if (self.timeCooldown <= 0):
            self.pool.generate(shapeEnum, TypeEnum.BULLET, position, 1) # Velocity of bullet should be obtained from config
            self.timeCooldown = 0 # TODO obtain time cooldown from config
        
    """ Checks if the player collides with the provided rect. """
    def collides(self, rect):
        return sprite.get_rect().colliderect(rect)

    """ Updates the player. """
    def update(self):
        self.timeScore += Constants.clock.get_time()
        if (self.timeCooldown > 0):
            self.timeCooldown -= Constants.clock.get_time()
            if (self.timeCooldown < 0):
                self.timeCooldown = 0
                
        mod = 0
        if (self.dir != Direction.NONE):
            mod = -1 if self.dir == Direction.LEFT else 1
        
        velocity = 100 * mod # pixels per second
        self.position[0] = velocity * (Constants.clock.get_time() / 1000.0)
        if self.position[0] < 0:
            self.position[0] = 0
        elif self.position[0] > 600 - 128:
            self.position[0] = 600 - 128

        print("Player Velocity: " + velocity + "\n")
    """ Draws the player (including resource HUD and time) """
    def draw(self):
        # TODO add drawing of resource HUD and time
        Constants.screen.blit(self.sprite, (self.position[0], self.position[1]))
