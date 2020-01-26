'''Module to detect champion'''
import cv2

from cutils import crop

CHAMPIONS_MAPPING = {
    51: 'Caitlyn',
    22: 'Ashe',
    15: 'Sivir',
    17: 'Teemo',
    18: 'Tristana',
    21: 'MissFortune',
}


def get_champion(img, models):
    '''Finds the selected champion'''
    img = crop(img, (330, 720, 20, 20))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    return CHAMPIONS_MAPPING[models['champion'].predict(img)]
