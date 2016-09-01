#!/usr/bin/env python3

import random
from game.projectile import ShapeEnum, TypeEnum
from game.tools import Constants

"""
Contains the generation logic for creating new shapes.
"""
class TargetGenerator():

    def __init__(self, pool):
        self.pool = pool
        
        self.shapeChance = .05
        self.shapeCooldown = 500 # ms
        self.differential = 0
        self.shapesDropped = 0

    """ Generator may create new shapes on a call to update. """
    def update(self):
        self.shapeCooldown -= Constants.clock.get_time()
        if self.shapeCooldown < 0: self.shapeCooldown = 0
        
        if (self.shapeCooldown <= 0):
            if (random.random() <= self.shapeChance): # spawn new shape!
                shape = random.choice((ShapeEnum.CIRCLE, ShapeEnum.SQUARE, ShapeEnum.TRIANGLE))
            
                xpos = random.randrange(16, 600-112)
                ypos = 0
            
                velocity = 250
            
                self.pool.generate(shape, TypeEnum.TARGET, [xpos, ypos], velocity, 0)
                self.shapeCooldown = 500 - self.differential
                self.shapesDropped += 1

                # And increase odds of another shape!
                if self.shapesDropped % 3 != 0:
                    return
                
                if self.shapeChance < .2:
                    self.shapeChance *= 1.07
                elif self.shapeChance < .4:
                    self.shapeChance *= 1.05
                elif self.shapeChance < .6:
                    self.shapeChance *= 1.03
                elif self.shapeChance < .8:
                    self.shapeChance *= 1.02
                elif self.shapeChance < 1:
                    self.shapeChance *= 1.01
                else:
                    self.shapeChance = 1

                if self.shapeChance >= .5 and self.differential < 250:
                    self.differential += 25
                    self.shapeChance = .1
