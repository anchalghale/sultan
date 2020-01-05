''' Module for detecting abilities '''
import collections

from cutils import get_nearest

from .constants import (LEVEL_Q, LEVEL_W, LEVEL_E, LEVEL_R, POINT_Q,
                        POINT_W, POINT_E, POINT_R, Q, W, E, R)

Abilities = collections.namedtuple('Abilities', 'q w e r')
AbilityPoints = collections.namedtuple('AbilityPoints', 'q w e r')
LevelUps = collections.namedtuple('LevelUps', 'q w e r')


def get_abilities(img):
    ''' Finds if the abilites are up or not '''
    colors = (0, 0, 0), (228, 192, 121)
    mappings = dict(zip(colors, (False, True)))
    abilities = [mappings[get_nearest(img[Q[::-1]], colors)],
                 mappings[get_nearest(img[W[::-1]], colors)],
                 mappings[get_nearest(img[E[::-1]], colors)],
                 mappings[get_nearest(img[R[::-1]], colors)], ]
    return Abilities(*abilities)


def get_ability_points(img):
    ''' Finds if the first abilites point is unlocked or not '''
    colors = (0, 0, 0), (146, 111, 48)
    mappings = dict(zip(colors, (False, True)))
    abilities = [mappings[get_nearest(img[POINT_Q[::-1]], colors)],
                 mappings[get_nearest(img[POINT_W[::-1]], colors)],
                 mappings[get_nearest(img[POINT_E[::-1]], colors)],
                 mappings[get_nearest(img[POINT_R[::-1]], colors)], ]
    return AbilityPoints(*abilities)


def get_level_ups(img):
    ''' Finds if the abilites level ups are up or not '''

    level_ups = [(img[LEVEL_Q[::-1]] == [255, 251, 173]).all(),
                 (img[LEVEL_W[::-1]] == [255, 251, 173]).all(),
                 (img[LEVEL_E[::-1]] == [255, 251, 173]).all(),
                 (img[LEVEL_R[::-1]] == [255, 251, 173]).all(), ]
    return LevelUps(*level_ups)
