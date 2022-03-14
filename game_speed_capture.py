import cv2 as cv
import pytesseract
from screen_capture import WindowCapture

WINDOW_NAME = r'RVGL'
TARGET_FPS = 10

spd = {
    '20': 20, 'an': 20,
    '19': 19, '1!': 19,
    '18': 18, '1a': 18,
    '17': 17,
    '15': 16,
    '15': 15,
    '14': 14, 'la': 14,
    '13': 13,
    '12': 12,
    '11': 11,
    '10': 10, '1n': 10,
    '9': 9, '.': 9,
    '8': 8, ':': 8,
    '7': 7,
    '6': 6, '.': 6,
    '5': 5,
    '4': 4, '.': 4,
    '3': 3,
    '2': 2,
    '1': 1,
    '0': 0, 'n': 0
}

pytesseract.pytesseract.tesseract_cmd = \
    r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

wincap = WindowCapture(WINDOW_NAME, TARGET_FPS, False)
data_c = 0

while True:
    wincap.loop_start()
    img = wincap.get_capture()
    size = img.shape
    # print(size)
    img = img[round(size[0]*0.932):round(size[0]*0.932) + round(size[0]*0.04),
              round(size[1]*0.895):round(size[1]*0.895) + round(size[0]*0.04),
              ...]  # (400, 500, 3)
    speed = pytesseract.image_to_string(img, config='-psm 7')
    if speed:
        if speed[:-2] in spd:
            print(spd[speed[:-2]])
        else:
            print(f'new data {speed[:-2]}')
            # cv.imwrite(f'{data_c} {speed[:-2]}.png', img)
            # data_c += 1

    # resize image
    # scale_percent = 500
    # width = int(img.shape[1] * scale_percent / 100)
    # height = int(img.shape[0] * scale_percent / 100)
    # dim = (width, height)
    # img = cv.resize(img, dim, interpolation=cv.INTER_AREA)

    cv.imshow(f'{WINDOW_NAME} {img.shape}', img)
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

    wincap.loop_end()
    # wincap.show_fps()


print('Done.')
