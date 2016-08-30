#!/usr/bin/env python3

from configparser import ConfigParser

"""
Holds the configuration options for the game.
"""
class Configuration(ConfigParser):
    
    def __init__(self):
        self.read('settings.ini')
        
    """Gets the Targets per Second"""
    def getTPS(self):        
        return self['DEFAULT']['TargetsPerSecond']
        
    """Gets the Targets per Second Squared (Acceleration)"""
    def getTPS2(self):               
        self['DEFAULT']['TargetsPerSecondSqr']

    """Gets the Bullets per Second (cooldown for firing rate)"""
    def getBPS(self):
        return self['DEFAULT']['BulletsPerSecond']


def main():
    cfg = Configuration()
    cfg.getTPS()

if __name__ == "__main__":
    main()