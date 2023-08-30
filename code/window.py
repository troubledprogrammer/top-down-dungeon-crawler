import pygame as pg

from code.settings import WINDOW_X, WINDOW_Y


class Window:
    """
    A class to control the window including fps

    Attributes
    ----------
    display: pg.Surface
        A reference to the pygame display to render on
    deltatime: int
        ms passed since last frame
    fps: int
        1000/deltatime -> the fps the game is currently running at

    Methods
    -------
    tick() -> None
        Updates the window
    has_quit() -> bool
        checks if the player has closed the window
    """

    def __init__(self, width=WINDOW_X, height=WINDOW_Y, showfps=False) -> None:
        self.display = pg.display.set_mode((width, height))

        self._clock = pg.time.Clock()

        self.deltatime = 1
        self.fps = 60

        self._showfps = showfps
        self._debug_font = pg.font.SysFont("consolas.ttf", 48)

    def _draw_fps(self):
        pg.display.set_caption(str(self.fps))
        img = self._debug_font.render(f"fps: {self.fps}", True, (255, 255, 255))
        self.display.blit(img, (0, 0))

    def tick(self) -> None:
        """
        Updates all io elements:
            - Updates last frame onto display
            - clears the buffer
            - ticks the clock
        :return: None
        """
        if self._showfps:
            self._draw_fps()
        pg.display.update()
        self.display.fill("black")

        self.deltatime = self._clock.tick(240)
        try:
            self.fps = int(1000 / self.deltatime)
        except ZeroDivisionError:
            self.fps = 1000

    def has_quit(self) -> bool:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
                return True
        return False
