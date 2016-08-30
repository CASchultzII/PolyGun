#!/usr/bin/env python3

from game.projectile import ShapeEnum, TypeEnum
import game.tools.Constants

"""
Contains information on the current player instance.
"""
class PlayerInfo:

    """ Init this Player """
    def __init__(self, sprite, pool): #BAD COUPLING
        self.timeScore = 0L
        self.timeCooldown = 0L
        self.resources = {ShapeEnum.CIRCLE: 10, ShapeEnum.SQUARE: 10, ShapeEnum.TRIANGLE: 10}
        self.position = 100, 100 # TODO create a world coordinate transform
        self.sprite = sprite
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

    """ Draws the player (including resource HUD and time) """
    def draw(self):
        # TODO add drawing of resource HUD and time
        Constants.screen.blit(sprite, position)
