#!/usr/bin/env python3

import os
from enum import Enum
import pygame
from pygame.font import Font
from pygame import Rect
from game.projectile import ShapeEnum, TypeEnum
from game.tools import Constants

"""
Contains information on the current player instance.
"""
class PlayerInfo:

    """ Init this Player """
    def __init__(self, pool): #BAD COUPLING
        self.timeScore = 0
        self.timeCooldown = 0
        self.resources = {ShapeEnum.CIRCLE: 10, ShapeEnum.SQUARE: 10, ShapeEnum.TRIANGLE: 10}
        self.position = [236, 820] # TODO create a world coordinate transform
        self.sprite = Constants.config.getGameImage("Cannon")
        self.hitbox = Constants.config.getHitBox("Player")
        self.pool = pool # BAD COUPLING
        
        self.moveLeft = False
        self.moveRight = False

        self.gameOver = False
        self.music_botched = pygame.mixer.Sound(os.path.join("assets", os.path.join("sounds", "Botched.ogg")))
        self.music_lazer = pygame.mixer.Sound(os.path.join("assets", os.path.join("sounds", "Lazer.ogg")))

    """ Asks the PlayerInfo to try to fire. """
    def fire(self, shapeEnum):
        if self.gameOver: return
        if (self.resources[shapeEnum] < 1): return # Can't fire anymore
        if (self.timeCooldown <= 0):
            position = [self.position[0], self.position[1]]
            
            width = 0
            height = 0
            if (shapeEnum == ShapeEnum.CIRCLE):
                width = Constants.config.getGameImage("CircleBullet").get_width()
                height = Constants.config.getGameImage("CircleBullet").get_height()
            elif (shapeEnum == ShapeEnum.SQUARE):
                width = Constants.config.getGameImage("SquareBullet").get_width()
                height = Constants.config.getGameImage("SquareBullet").get_height()
            else: # ShapeEnum.TRIANGLE
                width = Constants.config.getGameImage("TriangleBullet").get_width()
                height = Constants.config.getGameImage("TriangleBullet").get_height()
            
            position[0] += (self.sprite.get_width() - width) / 2
            position[1] -= height + 10
            
            self.pool.generate(shapeEnum, TypeEnum.BULLET, position, -500, 0) # Velocity of bullet should be obtained from config
            self.timeCooldown = 100 # TODO obtain time cooldown from config
            self.resources[shapeEnum] -= 1
            self.music_lazer.play()
        
    """ Checks if the player collides with the provided rect. """
    def collides(self, rect):
        return self.hitbox.copy().move(self.position[0], self.position[1]).colliderect(rect)

    """ Increases or decreases the resources accordingly """
    def adjustResources(self, resources, targetRects):
        if self.gameOver: return

        self.resources[ShapeEnum.CIRCLE] += resources[ShapeEnum.CIRCLE]
        self.resources[ShapeEnum.SQUARE] += resources[ShapeEnum.SQUARE]
        self.resources[ShapeEnum.TRIANGLE] += resources[ShapeEnum.TRIANGLE]

        for target in targetRects:
            rect = target.hitbox.copy().move(target.position[0], target.position[1])
            if self.collides(rect):
                target.collidesPlayer = True
                self.music_botched.play()

    """ Updates the player. """
    def update(self):
        if self.resources[ShapeEnum.CIRCLE] < 0 or \
            self.resources[ShapeEnum.SQUARE] < 0 or \
            self.resources[ShapeEnum.TRIANGLE] < 0:
            self.gameOver = True
            
        if self.gameOver: return

        self.timeScore += Constants.clock.get_time()
        if (self.timeCooldown > 0):
            self.timeCooldown -= Constants.clock.get_time()
            if (self.timeCooldown < 0):
                self.timeCooldown = 0
                
        if (not (self.moveLeft or self.moveRight)):
            return
            
        mod = -1 if self.moveLeft else 1
        
        velocity = 600 * mod # pixels per second
        self.position[0] += velocity * (Constants.clock.get_time() / 1000.0)
        if self.position[0] < 0:
            self.position[0] = 0
        elif self.position[0] > 600 - 128:
            self.position[0] = 600 - 128
            
    """ Draws the player (including resource HUD and time) """
    def draw(self):
        # Draw HUD
        Constants.screen.fill((0,0,0), pygame.Rect(0, 0, 600, 120))
        Constants.screen.blit(Constants.config.getGameImage("CircleTarget"), [10, 10])
        Constants.screen.blit(Constants.config.getGameImage("SquareTarget"), [132, 10])
        Constants.screen.blit(Constants.config.getGameImage("TriangleTarget"), [254, 10])
        
        font = Font(os.path.join("assets", "astron boy.ttf"), 48)
        cString = str(self.resources[ShapeEnum.CIRCLE]) if self.resources[ShapeEnum.CIRCLE] >= 0 else "-"
        cPoints = font.render(cString, True, (255,255,255))
        cPos = [10 + 112/2 - cPoints.get_width()/2, 109 - 99/2 - cPoints.get_height()/2 + 30]

        sString = str(self.resources[ShapeEnum.SQUARE]) if self.resources[ShapeEnum.SQUARE] >= 0 else "-"
        sPoints = font.render(sString, True, (255,255,255))
        sPos = [132 + 112/2 - sPoints.get_width()/2, 109 - 99/2 - sPoints.get_height()/2 + 30]

        tString = str(self.resources[ShapeEnum.TRIANGLE]) if self.resources[ShapeEnum.TRIANGLE] >= 0 else "-"
        tPoints = font.render(tString, True, (255,255,255))
        tPos = [254 + 112/2 - tPoints.get_width()/2, 109 - 99/2 - tPoints.get_height()/2 + 30]
        
        Constants.screen.blit(cPoints, cPos)
        Constants.screen.blit(sPoints, sPos)
        Constants.screen.blit(tPoints, tPos)

        # Draw time
        minutes = int(self.timeScore / 1000 / 60)
        seconds = int(self.timeScore / 1000 - minutes * 60)
        timeString = str(minutes) + ":" + str(seconds)

        font = Font(os.path.join("assets", "astron boy.ttf"), 70)
        time = font.render(timeString, True, (255,255,255))
        timeRect = time.get_bounding_rect()
        Constants.screen.blit(time, [600 - timeRect.w - 10, 10])
        
        if self.gameOver:
            font = Font(os.path.join("assets", "astron boy.ttf"), 100)
            game = font.render("GAME", True, (255,255,255))
            over = font.render("OVER", True, (255,255,255))

            gameRect = game.get_bounding_rect()
            overRect = over.get_bounding_rect()
            gamePosition = [(600 - gameRect.w) / 2, 900 / 2 - gameRect.h - 10]
            overPosition = [(600 - overRect.w) / 2, 900 / 2 + 10]

            width = (gameRect.w if gameRect.w > overRect.w else overRect.w) + 40
            height = gameRect.h + overRect.h + 60

            # Create a bounding box and inner blur
            box = pygame.Surface((width + 20, height + 20))
            box.fill((255,255,255))
            box.fill((0,0,0), Rect(10, 10, width, height))
            box.set_colorkey((0,0,0))
            boxPosition = [(600 - box.get_width()) / 2, (900 - box.get_height()) / 2]
            # HACKS
            boxPosition[0] += 4
            boxPosition[1] += 16

            blur = pygame.Surface((width, height))
            blur.set_alpha(128)
            blur.fill((0,0,0))
            blurPosition = [boxPosition[0] + 10, boxPosition[1] + 10]

            # Draw all the things
            Constants.screen.blit(box, boxPosition)
            Constants.screen.blit(blur, blurPosition)
            Constants.screen.blit(game, gamePosition)
            Constants.screen.blit(over, overPosition)

            # Don't draw player...
            return

        # Draw Player
        Constants.screen.blit(self.sprite, self.position)
