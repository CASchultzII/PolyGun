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
            "TierOne": float(self.config["GENERATOR"]["TierOne"],
            "TierTwo": float(self.config["GENERATOR"]["TierTwo"],
            "TierThree": float(self.config["GENERATOR"]["TierThree"],

            "TierOneMult": float(self.config["GENERATOR"]["TierOneMult"],
            "TierTwoMult": float(self.config["GENERATOR"]["TierTwoMult"],
            "TierThreeMult": float(self.config["GENERATOR"]["TierThreeMult"],

            "EasyPatterns": os.path.join("assets", self.config["GENERATOR"]["EasyPatterns"]),
            "MediPatterns": os.path.join("assets", self.config["GENERATOR"]["MediPatterns"]),
            "HardPatterns": os.path.join("assets", self.config["GENERATOR"]["HardPatterns"],

            "PatternModulus": int(self.config["GENERATOR"]["PatternModulus"]),
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
        backgroundImage = pygame.image.load(os.path.join("assets", imageFile)).convert()
        background = pygame.Surface((600, 900))
        background.blit(backgroundImage, pygame.Rect(0, 0, 600, 900))
        return background
        
    
