import cv2 as cv
from screen_capture import WindowCapture

WINDOW_NAME = r'RVGL'
TARGET_FPS = 24

wincap = WindowCapture(WINDOW_NAME, TARGET_FPS, True)

while True:
    wincap.loop_start()
    screenshot = wincap.get_capture()
    size = screenshot.shape
    cv.imshow(f'{WINDOW_NAME} {size}', screenshot)
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

    wincap.loop_end()
    wincap.show_fps()


print('Done.')
