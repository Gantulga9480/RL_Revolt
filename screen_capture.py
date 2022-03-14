import numpy as np
import win32gui
import win32ui
import win32con
from time import time
from low_level_delay import delay_ms


class WindowCapture:

    border_pixels = 8
    titlebar_pixels = 30

    def __init__(self, window_name, target_fps=30, dynamic=False):
        self.frame_interval = 1000 / target_fps
        self.window_name = window_name
        self.dynamic = dynamic
        self.start = 1
        self.w = 0
        self.h = 0
        self.hwnd = None
        self.cropped_x = 0
        self.cropped_y = 0
        self.offset_x = 0
        self.offset_y = 0
        self.hwnd = win32gui.FindWindow(None, window_name)
        if not self.hwnd:
            raise Exception('Window not found: {}'.format(window_name))
        window_rect = win32gui.GetWindowRect(self.hwnd)
        self.w = window_rect[2] - window_rect[0]
        self.h = window_rect[3] - window_rect[1]
        self.w = self.w - (self.border_pixels * 2)
        self.h = self.h - self.titlebar_pixels - self.border_pixels
        self.cropped_x = self.border_pixels
        self.cropped_y = self.titlebar_pixels
        self.offset_x = window_rect[0] + self.cropped_x
        self.offset_y = window_rect[1] + self.cropped_y

    def get_capture(self):
        if self.dynamic:
            self.hwnd = win32gui.FindWindow(None, self.window_name)
            if not self.hwnd:
                raise Exception('Window not found: {}'.format(self.window_name))
            window_rect = win32gui.GetWindowRect(self.hwnd)
            self.w = window_rect[2] - window_rect[0]
            self.h = window_rect[3] - window_rect[1]
            self.w = self.w - (self.border_pixels * 2)
            self.h = self.h - self.titlebar_pixels - self.border_pixels
            self.cropped_x = self.border_pixels
            self.cropped_y = self.titlebar_pixels
            self.offset_x = window_rect[0] + self.cropped_x
            self.offset_y = window_rect[1] + self.cropped_y

        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (self.w, self.h), dcObj, (self.cropped_x,
                                                     self.cropped_y),
                   win32con.SRCCOPY)
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (self.h, self.w, 4)
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())
        img = img[..., :3]
        img = np.ascontiguousarray(img)
        return img

    def loop_start(self):
        self.start = time()

    def loop_end(self):
        d = (self.frame_interval - (time() - self.start) * 1000)
        if d > 0:
            delay_ms(d)

    def show_fps(self):
        print(f'FPS: {round(1 / (time() - self.start))}')

    def list_window_names(self):
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                print(hex(hwnd), win32gui.GetWindowText(hwnd))
        win32gui.EnumWindows(winEnumHandler, None)

    def get_screen_position(self, pos):
        return (pos[0] + self.offset_x, pos[1] + self.offset_y)
