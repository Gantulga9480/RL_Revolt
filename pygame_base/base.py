import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'PYGAME_HIDE_SUPPORT_PROMPT'
import pygame as pg   # noqa
from .color import *  # noqa
from .utils import *  # noqa


class PyGameBase:

    def __init__(self,
                 title: str = 'PyGameDemo',
                 width: int = 640,
                 height: int = 480,
                 fps: int = 60,
                 render: bool = True) -> None:
        pg.init()

        # Main window
        self.screen_width: int = width
        self.screen_height: int = height
        self.fps: int = fps
        self.title: str = title
        self.backgroundColor: pg.Color = WHITE
        self.running: bool = True
        self.rendering: bool = render
        self.clock = pg.time.Clock()

        # Event
        self.mouse_x = 0
        self.mouse_y = 0
        self.events = []

        # Render
        self.sprites: list[pg.Rect] = []

        # Class method implementation flags
        self.__is_setup = True
        self.__is_eventHandler = True
        self.__is_renderForeground = True

    def __del__(self):
        pg.quit()

    def mainloop(self):
        self.__highLevelSetup()
        while self.running:
            self.loop_start()
            self.__highLevelEventHandler()
            self.__highLevelRender()
            self.loop_end()

    def loop_start(self):
        """ User should override this method """
        ...

    def loop_end(self):
        """ User should override this method """
        ...

    def __highLevelSetup(self):
        if self.__is_setup:
            try:
                self.setup()
            except NotImplementedError:
                self.__is_setup = False
                self.LOG(WARNING, 'Game setup not implemented!')
        self.__lowLevelSetup()

    def setup(self):
        """ User should override this method """
        raise NotImplementedError

    def __lowLevelSetup(self):
        self.game_window = self.get_window(self.screen_width,
                                           self.screen_height)
        self.set_title(self.title)

    def __highLevelEventHandler(self):
        if self.__lowLevelEventHandler() and self.__is_eventHandler:
            try:
                self.eventHandler()
            except NotImplementedError:
                self.__is_eventHandler = False
                self.LOG(WARNING, 'Game event handler not implemented!')

    def eventHandler(self):
        """ User should override this method """
        raise NotImplementedError

    def __lowLevelEventHandler(self):
        self.events = []
        self.mouse_x, self.mouse_y = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                break
            else:
                self.events.append(event)
        return self.running

    def __highLevelRender(self):
        if self.rendering and self.running:
            self.renderBackground()
            if self.__is_renderForeground:
                try:
                    self.renderForeground()
                except NotImplementedError:
                    self.__is_renderForeground = False
                    self.LOG(WARNING, 'Game rendering nothing!')
            self.__lowLevelRender()

    def renderForeground(self):
        """ User should override this method """
        raise NotImplementedError

    def renderBackground(self):
        self.game_window.fill(self.backgroundColor)

    def __lowLevelRender(self):
        """ TODO flip() or update() """
        if self.sprites.__len__() > 0:
            pg.display.update(self.sprites)
        else:
            pg.display.update()
        self.clock.tick(self.fps)

    @staticmethod
    def set_title(title: str):
        pg.display.set_caption(title)

    @staticmethod
    def get_window(width: int, height: int):
        """ Avoid calling outside of PyGameBase instance """
        return pg.display.set_mode((width, height))

    @staticmethod
    def LOG(level: str, msg: str):
        print(f'[{level}]: {msg}')
