import keyboard as kb
import time


if __name__ == '__main__':
    time.sleep(1)
    print('Starting 3!')
    time.sleep(1)
    print('Starting 2!')
    time.sleep(1)
    print('Starting 1!')
    kb.press_and_release('win+d')
    time.sleep(0.5)
    kb.press_and_release('alt+f4')
    time.sleep(0.5)
    kb.press_and_release('enter')
    # time.sleep(0.5)
    # kb.press_and_release('down')
    # time.sleep(0.5)
    # kb.press_and_release('down')
    # time.sleep(0.5)
    # kb.press_and_release('enter')
