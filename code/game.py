"""
Holds the logic for the full game
"""

import pygame as pg

from code.window import Window
from code.level import Level
from code.settings import DEBUG


class Game:
    def __init__(self):
        pg.init()

        self.window = Window(showfps=DEBUG)

        self.level = Level(0, self.window)

    def run(self):
        while True:
            self.window.tick()

            if self.window.has_quit():
                return

            self.level.tick()
