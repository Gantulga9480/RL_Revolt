from pygame_base import PyGameBase
from pygame_base import WARNING, ERROR, INFO, DEBUG
from keybindings import *
import pygame
import cv2 as cv
from screen_capture import WindowCapture


class Revolt(PyGameBase):

    WINDOW_NAME = r'RVGL'
    WINDOW_WIDTH = 640
    WINDOW_HEIGHT = 480
    TARGET_FPS = 30

    def __init__(self,
                 title: str = WINDOW_NAME,
                 width: int = WINDOW_WIDTH,
                 height: int = WINDOW_HEIGHT,
                 fps: int = TARGET_FPS,
                 render: bool = True) -> None:
        super().__init__(title, width, height, fps, render)

        self.wincap = WindowCapture(self.WINDOW_NAME, self.TARGET_FPS, True)

    def setup(self):
        ...

    def eventHandler(self):
        ...

    def renderForeground(self):
        game_img = self.wincap.get_capture()
        game_img = cv.cvtColor(game_img.transpose((1, 0, 2)), cv.COLOR_BGR2RGB)
        game_surf = pygame.surfarray.make_surface(game_img) # .convert()
        if game_img.shape[0] != self.WINDOW_WIDTH or game_img.shape[1] != self.WINDOW_HEIGHT:
            self.game_window = self.get_window(game_img.shape[0],
                                               game_img.shape[1])
            self.set_title(f'{self.WINDOW_NAME} {game_img.shape}')
        self.game_window.blit(game_surf, (0, 0))

    def loop_start(self):
        self.wincap.loop_start()
        ...

    def loop_end(self):
        # self.wincap.loop_end()
        self.wincap.show_fps()
        ...
