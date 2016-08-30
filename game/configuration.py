#!/usr/bin/env python3

from configparser import ConfigParser

"""
Holds the configuration options for the game.
"""
class Configuration(ConfigParser):
    
    """Gets the Targets per Second"""
    def getTPS(self):
        self.read('settings.ini')
        return self['DEFAULT']['TargetsPerSecond']
        
    """Gets the Targets per Second Squared (Acceleration)"""
    def getTPS2(self):        
        self.read('settings.ini')
        print (self['DEFAULT']['TargetsPerSecondSqr'])

    """Gets the Bullets per Second (cooldown for firing rate)"""
    def getBPS(self):
        self.read('settings.ini')
        return self['DEFAULT']['BulletsPerSecond']


def main():
    cfg = Configuration()
    cfg.getTPS()

main()