'''Module to detect summoner level'''
import collections
import cv2

from cutils import crop

Spells = collections.namedtuple('Spells', 'd f')


def get_summoner_spells(image, knearest):
    '''Finds summoner spell'''
    img = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    img = crop(img, (534, 707, 19, 16))
    spell_d = knearest.predict(img)

    img = crop(image, (558, 707, 19, 16))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    spell_f = knearest.predict(img)
    return Spells(spell_d, spell_f)
