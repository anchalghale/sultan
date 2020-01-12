'''Module to detect summoner level'''
import cv2

from cutils import crop

MAPPING = [
    'barrier',
    'cooldown',
    'exhaust',
    'flash',
    'ghost',
    'heal',
    'ignite',
    'smite',
    'teleport',
]


def get_summoner_spells(img, knearest):
    '''Finds summoner spell'''
    spells = {}

    def predict(img, rect, key):
        nonlocal spells
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        img = crop(img, rect)
        spell = MAPPING[knearest['summoner_spell'].predict(img)]
        spells[spell] = {'spell': spell, 'key': key}
    predict(img, (534, 707, 19, 16), 'd')
    predict(img, (558, 707, 19, 16), 'f')
    return spells
