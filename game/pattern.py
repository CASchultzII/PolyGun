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
        self.shapes = None

    def bind(self):
        pureShapes = random.sample([ShapeEnum.CIRCLE, ShapeEnum.SQUARE, ShapeEnum.TRIANGLE], 3)
        self.shapes = [ShapeEnum.RANDOM]
        self.shapes.extend(pureShapes)
        self._bind()

    def _bind(self):
        for row in self.nodes:
            for pattern in row:
                pattern.shape = self.shapes[int(pattern.shape)]

    def clone(self):
        clone = compilePattern(self.patternStr)
        if self.shapes != None:
            clone.shapes = self.shapes
            clone._bind()
        return clone

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
        if patternStrs[0] != '-':
            for patternStr in patternStrs:
                shapeNum, xCoord = patternStr.split(",")
                row.append(PatternNode(float(xCoord), shapeNum))
        nodes.append(row)
    
    loops = random.randint(int(loopMin), int(loopMax))
    return Pattern(int(delay), loops, nodes, pythonStringsAreWeird)
