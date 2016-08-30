#!/usr/bin/env python3

import sys
import pygame
pygame.init()

from game import configuration, generator, player, projectile

""" Contains game sensitive information. """
class Game:

    def __init__(self):
        #self.config = new Configuration("path/to/config.cfg")
        size = 1600, 900 # This should be relocated to configuration.py
        self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN|pygame.HWSURFACE|pygame.DOUBLEFUB)

    """ PolyGun setup. """
    def init(self):
        self.player = new player.PlayerInfo()
        self.pool = new projectile.ProjectilePool()
        self.tgen = new generator.TargetGenerator()

    """ Update game. """
    def update(self):
        self.player.update()
        self.pool.update()
        self.tgen.update()

    """ Draw game. """
    def draw(self):
        # draw background first
        self.player.draw()
        self.pool.draw()

Game game = new Game()
game.init()

while (True): # need to add timing controls here using pygame.time.clock
    game.update()
    game.draw()