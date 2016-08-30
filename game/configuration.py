#!/usr/bin/env python3

from configparser import ConfigParser

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


def main():
    cfg = Configuration('settings.ini')
    print(cfg.getTPS())

if __name__ == "__main__":
    main()