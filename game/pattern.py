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

    def __init__(self, delay, loops, nodes):
        self.delay = delay
        self.loops = loops
        self.nodes = nodes

"""
Constructs a Pattern from a String.
"""
def compilePattern(patternStr):
    delay, loopRange, nodeStr = patternStr.split("|")
    loopMin, loopMax = loopRange.split(",")
    rows = nodeStr.split(";")

    nodes = []
    for rowStr in rows:
        patternStrs = rowStr.split(":")
        row = []
        for patternStr in patternStrs:
            shapeNum, xCoord = patternStr.split(",")
            shape = _getShape(shapeNum)
            row.append(PatternNode(x, shape))
        nodes.append(row)
    
    loops = random.randint(int(loopMin), int(loopMax))
    return Pattern(int(delay), loops, nodes)

"""
Handles ShapeEnum assignment
"""
def _getShape(shapeNum):
    if (shapeNum >= 0 and shapeNum <= 3):
        if (shapeNum == 0):
            return random.choice([ShapeEnum.CIRCLE, ShapeEnum.SQUARE, ShapeEnum.TRIANGLE])

        if (shapeNum == 1):
            return ShapeEnum.CIRCLE
        elif (shapeNum == 2):
            return ShapeEnum.SQUARE
        else: # shapeNum == 3
            return ShapeEnum.TRIANGLE

    return ShapeEnum.SQUARE # failsafe
