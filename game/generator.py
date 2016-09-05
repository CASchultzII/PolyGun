#!/usr/bin/env python3

import random
from game.pattern import compilePattern
from game.projectile import ShapeEnum, TypeEnum
from game.tools import Constants

"""
Contains the generation logic for creating new shapes.
"""
class TargetGenerator():

    def __init__(self, pool):
        self.pool = pool
        
        self.tierVal = Constants.config.getGeneratorProperty("TierOne")
        self.patternCooldown = 0
        self.differential = 0
        self.patternsDropped = 0
        self.pattern = None
        self.patternD = None
        self._loadPatterns()

    """ Loads a pattern file into an array of pattern strings. """
    def _loadPatternFile(fileString):
        patternStrs = []
        with open(fileString, 'r') as f:
            for line in f:
                patternStrs.append(line.rstrip())
        return patternStrs

    """ Loads patterns into the generator. """
    def _loadPatterns(self):
        easy = TargetGenerator._loadPatternFile(Constants.config.getGeneratorProperty("EasyPatterns"))
        medi = TargetGenerator._loadPatternFile(Constants.config.getGeneratorProperty("MediPatterns"))
        hard = TargetGenerator._loadPatternFile(Constants.config.getGeneratorProperty("HardPatterns"))

        self.easy = []
        self.medi = []
        self.hard = []
        for patternStr in easy:
            self.easy.append(compilePattern(patternStr))
        for patternStr in medi:
            self.medi.append(compilePattern(patternStr))
        for patternStr in hard:
            self.hard.append(compilePattern(patternStr))

    """ Generator may create new shapes on a call to update. """
    def update(self):
        self.patternCooldown -= Constants.clock.get_time()
        if self.patternCooldown < 0: self.patternCooldown = 0
        
        if self.patternCooldown == 0:

            inc = False
            if self.pattern == None:
                self._setNewPattern()
                inc = True
            self._firePattern()

            if self.patternsDropped % Constants.config.getGeneratorProperty("PatternModulus") == 0 and inc:
                # Ramp up difficulty.

                if self.tierVal < Constants.config.getGeneratorProperty("TierTwo"):
                    self.tierVal *= Constants.config.getGeneratorProperty("TierOneMult")
                elif self.tierVal < Constants.config.getGeneratorProperty("TierThree"):
                    self.tierVal *= Constants.config.getGeneratorProperty("TierTwoMult")
                elif self.tierVal < 1:
                    self.tierVal *= Constants.config.getGeneratorProperty("TierThreeMult")
                else:
                    self.tierVal = 1

    """
    Gets a new Pattern and sets it as active.
    """
    def _setNewPattern(self):
        patternArray = None
        tag = None
        if self.tierVal < Constants.config.getGeneratorProperty("TierTwo"):
            patternArray = self.easy
            tag = "(EASY) "
        elif self.tierVal < Constants.config.getGeneratorProperty("TierThree"):
            patternArray = self.medi
            tag = "(MEDI) "
        else:
            patternArray = self.hard
            tag = "(HARD) "

        self.pattern = random.choice(patternArray).clone()
        self.pattern.bind()
        self.patternD = self.pattern.clone()
        print(tag + "PATTERN: " + self.pattern.patternStr)

    """
    Fires the current pattern.
    """
    def _firePattern(self):
        row = self.patternD.nodes.pop(0)
        velocity = Constants.config.getGeneratorProperty("Velocity")
        for node in row:
            self.pool.generate(node.shape, TypeEnum.TARGET, [node.x * 600 - 112/2, 0], velocity, 0)
        self.patternCooldown = self.pattern.delay

        if len(self.patternD.nodes) == 0:
            if self.pattern.loops > 0:
                self.pattern.loops -= 1
                self.patternD = self.pattern.clone()
                print("   Looping...")
            else:
                self.pattern = None
                self.patternsDropped += 1
