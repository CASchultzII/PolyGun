#!/usr/bin/env python3

import random
from game.projectile import ShapeEnum, TypeEnum

"""
Contains the generation logic for creating new shapes.
"""
class TargetGenerator():

    def __init__(self, pool):
        self.pool = pool
        
        self.shapeChance = .2

    """ Generator may create new shapes on a call to update. """
    def update(self):
        if (random.random() >= self.shapeChance): # spawn new shape!
            shape = random.choice((ShapeEnum.CIRCLE, ShapeEnum.SQUARE, ShapeEnum.TRIANGLE))
            
            xpos = random.randrange(16, 600-112)
            ypos = -70
            
            velocity = 250
            
            self.pool.generate(shape, TypeEnum.TARGET, [xpos, ypos], velocity, 0)