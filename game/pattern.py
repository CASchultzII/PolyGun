#!/usr/bin/env python3

# Contains the pattern compiling classes

from game.projectile import ShapeEnum
import random

"""
A node in the pattern.  Contains an x-coordinate and ShapeEnum
"""
class PatternNode:

    def __init__(self, x, shape):
        self.x = x
        self.shape = shape


"""
A collection of PatternNodes.  Used to fire a pattern.
"""
class Pattern:

    def __init__(self, delay, loops, nodes, patternStr):
        self.delay = delay
        self.loops = loops
        self.nodes = nodes
        self.patternStr = patternStr

    def clone(self):
        return compilePattern(self.patternStr)

"""
Constructs a Pattern from a String.
"""
def compilePattern(patternStr):
    pythonStringsAreWeird = patternStr
    delay, loopRange, nodeStr = patternStr.split("|")
    loopMin, loopMax = loopRange.split(",")
    rows = nodeStr.split(";")

    nodes = []
    for rowStr in rows:
        patternStrs = rowStr.split(":")
        row = []
        for patternStr in patternStrs:
            shapeNum, xCoord = patternStr.split(",")
            shape = _getShape(int(shapeNum))
            row.append(PatternNode(float(xCoord), shape))
        nodes.append(row)
    
    loops = random.randint(int(loopMin), int(loopMax))
    return Pattern(int(delay), loops, nodes, pythonStringsAreWeird)

"""
Handles ShapeEnum assignment
"""
shapes = [ShapeEnum.CIRCLE, ShapeEnum.SQUARE, ShapeEnum.TRIANGLE]
def _getShape(shapeNum):
    if (shapeNum >= 0 and shapeNum <= 3):
        
        if (shapeNum == 0):
            return ShapeEnum.RANDOM
        
        random.shuffle(shapes)
        return shapes[shapeNum - 1]

    return ShapeEnum.SQUARE # failsafe
