"""
Holds the logic for the full game
"""

import pygame as pg

from _code.level import Level
from _code.window import Window


class Game:
    def __init__(self):
        pg.init()

        self.window = Window(showfps=True)

        self.level = Level(self.window)

    def run(self):
        while True:
            self.window.tick()

            if self.window.has_quit():
                return

            self.level.update()

