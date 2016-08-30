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
        
    """Gets the Targets per Second"""
    def getTPS(self):        
        return float(self.config['DEFAULT']['TargetsPerSecond'])
        
    """Gets the Targets per Second Squared (Acceleration)"""
    def getTPS2(self):               
        return float(self.config['DEFAULT']['TargetsPerSecondSqr'])

    """Gets the Bullets per Second (cooldown for firing rate)"""
    def getBPS(self):
        return float(self.config['DEFAULT']['BulletsPerSecond'])

    """Gets the image for Game Object"""
    def getGameImage(self, gameObject):
        imageFile = self.config['IMAGES'][gameObject]
        image = pygame.image.load(os.path.join('..', 'assets', imageFile)).convert_alpha()
        return image

def main():
    pygame.init()
    cfg = Configuration(os.path.join('..', 'settings.ini'))
    while (True):
        for event in pygame.event.get():
            if not hasattr(event, 'key'): continue
            elif event.key == K_ESCAPE: sys.exit(0)

        screen = pygame.display.set_mode((1024, 768))
        screen.blit(cfg.getGameImage('Player'), (100, 100))
        pygame.display.flip()
        
if __name__ == "__main__":
    main()