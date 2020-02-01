'''Module to detect champion'''
import cv2

from cutils import crop

CHAMPIONS_MAPPING = {
    51: 'caitlyn',
    22: 'ashe',
    15: 'sivir',
    17: 'teemo',
    18: 'tristana',
    21: 'miss_fortune',
    11: 'master_yi'
}


def get_champion(img, models):
    '''Finds the selected champion'''
    img = crop(img, (330, 720, 20, 20))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    return CHAMPIONS_MAPPING[models['champion'].predict(img)]
