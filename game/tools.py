#!/usr/bin/env python3

from pygame.time import Clock

""" Contains useful tools for running a game. """

""" Contains constants used for a single game. """
class Constants():

    """
    Creating a new Constants object merely reinitializes the
    class variables.
    """
    def __init__(self):
        Constants.clock = new Clock()
        Constants.config = None
        Constants.screen = None