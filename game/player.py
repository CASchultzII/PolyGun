#!/usr/bin/env python3

import game.projectile.ShapeEnum

"""
Contains information on the current player instance.
"""
class PlayerInfo:

    """ Init this Player """
    def __init__(self, sprite, pool): #BAD COUPLING
        self.timeScore = 0L
        self.timeCooldown = 0L
        self.resources = {ShapeEnum.CIRCLE: 10, ShapeEnum.SQUARE: 10, ShapeEnum.TRIANGLE: 10}
        self.position = 0 # TODO create a world coordinate transform
        self.sprite = sprite
        self.pool = pool # BAD COUPLING

    """ Asks the PlayerInfo to try to fire. """
    def fire(self):
        pass
        
    """ Checks if the player collides with the provided rect. """
    def collides(self, rect):
        pass

    """ Updates the player. """
    def update(self):
        pass

    """ Draws the player (including resource HUD and time) """
    def draw(self):
        pass
