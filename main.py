#!/usr/bin/env python3

import sys, os
import pygame
from pygame.locals import *
pygame.init()
pygame.joystick.init() # JOYSTICKS?!?

from game import configuration, generator, player, projectile
from game.tools import Constants

""" Contains game sensitive information. """
class Game:

    def __init__(self):
        size = 600, 900 # This should be relocated to configuration.py
        self.screen = pygame.display.set_mode(size, pygame.HWSURFACE|pygame.DOUBLEBUF)
        # Generate constants for game.
        Constants()
        Constants.config = configuration.Configuration('settings.ini')       
        pygame.display.set_caption("PolyGun")
        self.music = pygame.mixer.Sound(os.path.join("assets", os.path.join("sounds", "DivideByZero-POL.ogg")))
        self.music.play(-1)

        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            if (self.joystick != None):
                self.joystick.init()

    """ PolyGun setup. """
    def init(self):
        self.pool = projectile.ProjectilePool()
        self.player = player.PlayerInfo(self.pool)
        self.tgen = generator.TargetGenerator(self.pool)

    """ Update game. """
    def update(self):
        self.tgen.update()

        resources, targets = self.pool.update()

        self.player.adjustResources(resources, targets)
        self.player.update()

    """ Draw game. """
    def draw(self):
        self.screen.blit(Constants.config.getGameImage("Background"), [0, 0])
        self.pool.draw()
        self.player.draw()

game = Game()
game.init()
Constants.screen = game.screen #BAD BAD BAD... but no choice for now

Constants.clock.tick(60)
while (True):
    # INPUT HANDLING
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit(0)
        
        if hasattr(event, 'key'):
            down = event.type == KEYDOWN
            if event.key == K_LEFT: game.player.moveLeft = down
            elif event.key == K_RIGHT: game.player.moveRight = down
        
            if event.key == K_a and down: game.player.fire(projectile.ShapeEnum.CIRCLE)
            elif event.key == K_s and down: game.player.fire(projectile.ShapeEnum.SQUARE)
            elif event.key == K_d and down: game.player.fire(projectile.ShapeEnum.TRIANGLE)

            if event.key == K_RETURN and down and game.player.gameOver:
                game.init()
        
            if event.key == K_ESCAPE: sys.exit(0)

        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == 0:
                game.player.fire(projectile.ShapeEnum.CIRCLE)
            elif event.button == 1:
                game.player.fire(projectile.ShapeEnum.SQUARE)
            elif event.button == 4:
                game.player.fire(projectile.ShapeEnum.TRIANGLE)
            elif event.button == 11 and game.player.gameOver:
                game.init()

        if event.type == pygame.JOYAXISMOTION:
            if event.axis == 0 or event.axis == 6:
                if event.value < 0:
                    game.player.moveLeft = True
                    game.player.moveRight = False
                elif event.value > 0:
                    game.player.moveLeft = False
                    game.player.moveRight = True
                else: # event.value == 0
                    game.player.moveLeft = False
                    game.player.moveRight = False
            
    game.update()
    game.draw()
    pygame.display.flip()
    Constants.clock.tick(60) # target 60 frames
