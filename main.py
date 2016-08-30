#!/usr/bin/env python3

import sys
import pygame
from pygame.locals import *
pygame.init()

from game import configuration, generator, player, projectile
from game.tools import Constants

""" Contains game sensitive information. """
class Game:

    def __init__(self):
        # Generate constants for game.
        Constants()
        #Constants.config = new Configuration("path/to/config.cfg")
        size = 600, 900 # This should be relocated to configuration.py
        self.screen = pygame.display.set_mode(size, pygame.HWSURFACE|pygame.DOUBLEBUF)
        pygame.display.set_caption("PolyGun")

    """ PolyGun setup. """
    def init(self):
        self.pool = projectile.ProjectilePool()
        self.player = player.PlayerInfo(self.pool)
        self.tgen = generator.TargetGenerator(self.pool)

    """ Update game. """
    def update(self):
        self.player.update()
        self.pool.update()
        self.tgen.update()

    """ Draw game. """
    def draw(self):
        self.screen.fill((128, 128, 128))
        # draw background first
        self.player.draw()
        self.pool.draw()

game = Game()
game.init()
Constants.screen = game.screen #BAD BAD BAD... but no choice for now

Constants.clock.tick(60)
while (True): # need to add timing controls here using pygame.time.clock
    # INPUT HANDLING
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit(0)
        
        if not hasattr(event, 'key'): continue
        
        down = event.type == KEYDOWN
        if event.key == K_LEFT: game.player.moveLeft = down
        elif event.key == K_RIGHT: game.player.moveRight = down
        
        if event.key == K_a and down: game.player.fire(projectile.ShapeEnum.CIRCLE)
        elif event.key == K_s and down: game.player.fire(projectile.ShapeEnum.SQUARE)
        elif event.key == K_d and down: game.player.fire(projectile.ShapeEnum.TRIANGLE)
        
        if event.key == K_ESCAPE: sys.exit(0)

    game.update()
    game.draw()
    pygame.display.flip()
    Constants.clock.tick(60) # target 60 frames