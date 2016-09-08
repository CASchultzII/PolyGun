#!/usr/bin/env python3

from configparser import ConfigParser
from pygame.locals import *
from pygame import Rect
import pygame, sys, os

"""
Holds the configuration options for the game.
"""
class Configuration:
    
    def __init__(self, config):
        self.config = ConfigParser()
        self.config.read(self._getFilePath(config))
        self.imageCache = {
            "Cannon": self._getImageCache("Cannon"),
            "CircleBullet": self._getImageCache("CircleBullet"),
            "SquareBullet": self._getImageCache("SquareBullet"),
            "TriangleBullet": self._getImageCache("TriangleBullet"),
            "CircleTarget": self._getImageCache("CircleTarget"),
            "SquareTarget": self._getImageCache("SquareTarget"),
            "TriangleTarget": self._getImageCache("TriangleTarget"),
            "Background": self._getImageCache("Background"),
            "Banner": self._getImageCache("Banner")
        }
        self.generator = {
            "TierOne": float(self.config["GENERATOR"]["TierOne"]),
            "TierTwo": float(self.config["GENERATOR"]["TierTwo"]),
            "TierThree": float(self.config["GENERATOR"]["TierThree"]),

            "TierOneMult": float(self.config["GENERATOR"]["TierOneMult"]),
            "TierTwoMult": float(self.config["GENERATOR"]["TierTwoMult"]),
            "TierThreeMult": float(self.config["GENERATOR"]["TierThreeMult"]),

            "EasyPatterns": self._getFilePath(self.config["GENERATOR"]["EasyPatterns"], "assets", "data"),
            "MediPatterns": self._getFilePath(self.config["GENERATOR"]["MediPatterns"], "assets", "data"),
            "HardPatterns": self._getFilePath(self.config["GENERATOR"]["HardPatterns"], "assets", "data"),

            "PatternModulus": int(self.config["GENERATOR"]["PatternModulus"]),
            "Velocity": int(self.config["GENERATOR"]["Velocity"]),
            "Delay": int(self.config["GENERATOR"]["Delay"])
        }
        self.hitboxes = {
            "TargetCircle": self._getHitBox(self.config["HITBOXES"]["TargetCircle"]),
            "TargetSquare": self._getHitBox(self.config["HITBOXES"]["TargetSquare"]),
            "TargetTriangle": self._getHitBox(self.config["HITBOXES"]["TargetTriangle"]),
            "BulletCircle": self._getHitBox(self.config["HITBOXES"]["BulletCircle"]),
            "BulletSquare": self._getHitBox(self.config["HITBOXES"]["BulletSquare"]),
            "BulletTriangle": self._getHitBox(self.config["HITBOXES"]["BulletTriangle"]),
            "Player": self._getHitBox(self.config["HITBOXES"]["Player"])
        }
        self.sounds = {
            "Background": self._getFilePath(self.config["SOUNDS"]["Background"], "assets", "sounds"),
            "Fire": self._getFilePath(self.config["SOUNDS"]["Fire"], "assets", "sounds"),
            "Hit": self._getFilePath(self.config["SOUNDS"]["Hit"], "assets", "sounds"),
            "Wrong": self._getFilePath(self.config["SOUNDS"]["Wrong"], "assets", "sounds"),
            "Collision": self._getFilePath(self.config["SOUNDS"]["Collision"], "assets", "sounds")
        }

    """Gets the image for Game Object"""
    def getGameImage(self, gameObject):
        return self.imageCache[gameObject]
        
    def getGeneratorProperty(self, prop):
        return self.generator[prop]

    def getHitBox(self, sprite):
        return self.hitboxes[sprite]
        
    def getSound(self, sound):
        return pygame.mixer.Sound(self.sounds[sound])
        
    def getFontPath(self):
        return self._getFilePath(self.config["OTHER"]["Font"], "assets")

    def _getImageCache(self, gameObject):
        imageFile = self.config['IMAGES'][gameObject]
        path = self._getFilePath(imageFile, "assets", "images")
        image = pygame.image.load(path).convert_alpha()
        return image
        
    def _getHitBox(self, rectString):
        x, y, width, height = rectString.split(",")
        return Rect(int(x), int(y), int(width), int(height))
        
    def _getFilePath(self, file, *args):
        rel = ""
        for part in args:
            rel = os.path.join(rel, part)
        rel = os.path.join(rel, file)
        base = ""
        try:
            base = sys._MEIPASS
        except Exception:
            base = "."
            
        return os.path.join(base, rel)
