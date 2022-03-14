import cv2 as cv
import pytesseract
import matplotlib.pyplot as plt
from screen_capture import WindowCapture

WINDOW_NAME = r'RVGL'
TARGET_FPS = 10

spd = {
    'an': 20,
    '1!': 19,
    '1a': 18,
    '17': 17,
    '15': 16,
    '15': 15,
    '14': 14,
    '13': 13,
    '12': 12,
    '11': 11,
    '1n': 10,
    '.': 9,
    ':': 8,
    '7': 7,
    '.': 6,
    '5': 5,
    '.': 4,
    '3': 3,
    '2': 2,
    '1': 1,
    'n': 0
}

pytesseract.pytesseract.tesseract_cmd = \
    r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

wincap = WindowCapture(WINDOW_NAME, TARGET_FPS, False)

while True:
    wincap.loop_start()
    img = wincap.get_capture()
    size = img.shape

    # img = img[round(size[0]*0.928):round(size[0]*0.928) + round(size[0]*0.04),
    #           round(size[1]*0.918):round(size[1]*0.918) + round(size[0]*0.04),
    #           ...]  # (300, 500, 3)

    img = img[round(size[0]*0.932):round(size[0]*0.932) + round(size[0]*0.04),
              round(size[1]*0.895):round(size[1]*0.895) + round(size[0]*0.04),
              ...]  # (400, 500, 3)
    speed = pytesseract.image_to_string(img, config='-psm 7')  # ('-psm', '8')
    if speed:
        if speed[:-2] in spd:
            print(spd[speed[:-2]])

    # resize image
    # scale_percent = 500
    # width = int(img.shape[1] * scale_percent / 100)
    # height = int(img.shape[0] * scale_percent / 100)
    # dim = (width, height)
    # resized = cv.resize(img, dim, interpolation=cv.INTER_AREA)

    cv.imshow(f'{WINDOW_NAME} {img.shape}', img)
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

    wincap.loop_end()
    # wincap.show_fps()


print('Done.')


"""
20 - an
19 - 1!
18 - 1a
17 - 17
16 - 15
15 - 15
14 - 14
13 - 13
12 - 12
11 - 11
10 - 1n
9 - .
8 - :
7 - 7
6 - .
5 - 5
4 - .
3 - 3
2 - 2
1 - 1
0 - n
"""
