"""
Handles all io
"""

import pygame as pg


class Window:
    """
    Handles all io such as rendering and events
    """

    def __init__(self, width=800, height=600, showfps=False) -> None:
        self.display = pg.display.set_mode((width, height))

        self.clock = pg.time.Clock()

        self.events = pg.event.get()
        self.keys = pg.key.get_pressed()

        self.deltatime = 1
        self.fps = 60
        self.showfps = showfps

        self.debug_font = pg.font.SysFont("consolas.ttf", 48)

    def _draw_fps(self):
        img = self.debug_font.render(f"fps: {self.fps}", True, (0, 0, 0))
        self.display.blit(img, (0, 0))

    def tick(self):
        """
        Updates all io elements:
            - Updates last frame onto display
            - clears the buffer
            - gets events and keypresses
            - ticks the clock
        :return:
        """
        pg.display.update()
        self.display.fill("black")
        self.events = pg.event.get()
        self.keys = pg.key.get_pressed()

        ms_elapsed = self.clock.tick(60)
        self.deltatime = ms_elapsed * 60 / 1000
        try:
            self.fps = int(1000 / ms_elapsed)
        except ZeroDivisionError:
            self.fps = 1000

        if self.showfps:
            self._draw_fps()

        return ms_elapsed

    def get_keys(self):
        return self.keys

    def get_events(self):
        return self.events

    def has_quit(self):
        for e in self.events:
            if e.type == pg.QUIT:
                return True
        return False
