'''Module to find game time'''

import cv2
from cutils import crop


def get_game_time(img, models):
    '''Finds game minutes'''
    img = crop(img, (981, 6, 27, 8))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    minutes = ''
    seconds = ''
    for i in range(2):
        min_crop = crop(img, (i*6, 0, 6, 8))
        min_crop = cv2.resize(min_crop, (7, 9))

        sec_crop = crop(img, (15 + i*6, 0, 6, 8))
        sec_crop = cv2.resize(sec_crop, (7, 9))

        minutes += str(models['gold'].predict(min_crop, threshold=False))
        seconds += str(models['gold'].predict(sec_crop, threshold=False))
    return int(minutes) + int(seconds)/100
