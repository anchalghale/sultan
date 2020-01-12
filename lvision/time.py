# 981, 6, 6, 8
'''Module to find game time'''

import cv2
from cutils import crop


def get_game_time(img, models):
    '''Finds game minutes'''
    img = crop(img, (981, 6, 12, 8))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    minutes = ''
    for i in range(2):
        cropped = crop(img, (i*6, 0, 6, 8))
        cropped = cv2.resize(cropped, (7, 9))
        minutes += str(models['gold'].predict(cropped, threshold=False))
    return int(minutes)
