#!/usr/bin/env python3

from configparser import ConfigParser
from pygame.locals import *
import pygame, sys, os

"""
Holds the configuration options for the game.
"""
class Configuration:
    
    def __init__(self, config):
        self.config = ConfigParser()
        self.config.read(config)
        self.imageCache = {
            "Cannon": self._getImageCache("Cannon"),
            "CircleBullet": self._getImageCache("CircleBullet"),
            "SquareBullet": self._getImageCache("SquareBullet"),
            "TriangleBullet": self._getImageCache("TriangleBullet"),
            "CircleTarget": self._getImageCache("CircleTarget"),
            "SquareTarget": self._getImageCache("SquareTarget"),
            "TriangleTarget": self._getImageCache("TriangleTarget"),
            "Background": self._getBackgroundCache()
        }
        self.generator = {
            "ShapeChance": float(self.config["GENERATOR"]["ShapeChance"]),
            "ShapeDifferential": float(self.config["GENERATOR"]["ShapeDifferential"]),
            "ShapeCooldown": int(self.config["GENERATOR"]["ShapeCooldown"]),
            "ShapeModulus": int(self.config["GENERATOR"]["ShapeModulus"]),
            "DifferentialStep": int(self.config["GENERATOR"]["DifferentialStep"]),
            "DifferentialChance": float(self.config["GENERATOR"]["DifferentialChance"]),
            "DifferentialMax": int(self.config["GENERATOR"]["DifferentialMax"]),
            "TierTwo": float(self.config["GENERATOR"]["TierTwo"]),
            "TierThree": float(self.config["GENERATOR"]["TierThree"]),
            "TierFour": float(self.config["GENERATOR"]["TierFour"]),
            "TierFive": float(self.config["GENERATOR"]["TierFive"]),
            "TierOneMult": float(self.config["GENERATOR"]["TierOneMult"]),
            "TierTwoMult": float(self.config["GENERATOR"]["TierTwoMult"]),
            "TierThreeMult": float(self.config["GENERATOR"]["TierThreeMult"]),
            "TierFourMult": float(self.config["GENERATOR"]["TierFourMult"]),
            "TierFiveMult": float(self.config["GENERATOR"]["TierFiveMult"]),
            "BorderSize": int(self.config["GENERATOR"]["BorderSize"]),
            "Velocity": int(self.config["GENERATOR"]["Velocity"])
        }

    """Gets the image for Game Object"""
    def getGameImage(self, gameObject):
        return self.imageCache[gameObject]
        
    def getGeneratorProperty(self, prop):
        return self.generator[prop]

    def _getImageCache(self, gameObject):
        imageFile = self.config['IMAGES'][gameObject]
        image = pygame.image.load(os.path.join('assets', imageFile)).convert_alpha()
        return image

    def _getBackgroundCache(self):
        imageFile = self.config['IMAGES']["Background"]
        backgroundImage = pygame.image.load(os.path.join("assets", "background.jpg")).convert()
        background = pygame.Surface((600, 900))
        background.blit(backgroundImage, pygame.Rect(0, 0, 600, 900))
        return background
        
    