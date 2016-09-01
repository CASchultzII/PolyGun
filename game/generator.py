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
        
        self.shapeChance = Constants.config.getGeneratorProperty("ShapeChance")
        self.shapeCooldown = Constants.config.getGeneratorProperty("ShapeCooldown")
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
            
                velocity = Constants.config.getGeneratorProperty("Velocity")
            
                self.pool.generate(shape, TypeEnum.TARGET, [xpos, ypos], velocity, 0)
                self.shapeCooldown = Constants.config.getGeneratorProperty("ShapeCooldown") - self.differential
                self.shapesDropped += 1

                # And increase odds of another shape!
                if self.shapesDropped % Constants.config.getGeneratorProperty("ShapeModulus") != 0:
                    return
                
                if self.shapeChance < Constants.config.getGeneratorProperty("TierTwo"):
                    self.shapeChance *= Constants.config.getGeneratorProperty("TierOneMult")
                elif self.shapeChance < Constants.config.getGeneratorProperty("TierThree"):
                    self.shapeChance *= Constants.config.getGeneratorProperty("TierTwoMult")
                elif self.shapeChance < Constants.config.getGeneratorProperty("TierFour"):
                    self.shapeChance *= Constants.config.getGeneratorProperty("TierThreeMult")
                elif self.shapeChance < Constants.config.getGeneratorProperty("TierFive"):
                    self.shapeChance *= Constants.config.getGeneratorProperty("TierFourMult")
                elif self.shapeChance < 1:
                    self.shapeChance *= Constants.config.getGeneratorProperty("TierFiveMult")
                else:
                    self.shapeChance = 1

                if self.shapeChance >= Constants.config.getGeneratorProperty("DifferentialChance") and \
                        self.differential < Constants.config.getGeneratorProperty("DifferentialMax"):
                    self.differential += Constants.config.getGeneratorProperty("DifferentialStep")
                    self.shapeChance = Constants.config.getGeneratorProperty("ShapeDifferential")
