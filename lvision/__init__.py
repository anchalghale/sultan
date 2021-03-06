''' Object detection module '''
import cv2
import numpy

from cutils import (coor_offset, crop, find_center, get_color_diff, distance,
                    get_nearest, get_nearest_value, inside_rect)

from .abilities import get_level_ups, get_abilities, get_ability_points
from .minimap import get_minimap_areas, get_minimap_coor
from .state import get_game_state
from .stats import get_attack_speed
from .gold import get_gold
from .sums import get_summoner_spells
from .level import get_summoner_level
from .items import get_summoner_items, get_is_shop, get_item
from .time import get_game_time
from .champion import get_champion
from .loading import get_is_loading_screen

from .knearest import KNearest
from .constants import MINIMAP_AREAS, CAMERA_LOCK, LEVEL_Q, LEVEL_W, LEVEL_E, LEVEL_R
from .exceptions import NoCharacterInMinimap
from .utils import lfilter, Objects

LEVEL_OCR = KNearest()
LEVEL_OCR.load_model('lvision/knearest/trained/summoner_level.yml')


def get_small_hp_value(hp_img):
    ''' Calcuates the hp of given image of width 60 '''
    try:
        hp_img = hp_img.reshape((60, 3))
    except ValueError:
        return 60
    reference = hp_img[1]
    for i, value in enumerate(hp_img):
        if get_color_diff(reference, value) > 50:
            return i
    return 60


def get_hp_value(hp_img):
    ''' Calcuates the hp of given image of width 105 '''
    try:
        hp_img = hp_img.reshape((105, 3))
    except ValueError:
        return -1
    reference = hp_img[0]
    for i in range(len(hp_img)-2):
        if all([get_color_diff(reference, hp_img[i+j]) > 50 for j in range(3)]):
            return i
    return 105


def identify_object(img, contour, area):
    ''' Indentify an object from the coordiate '''
    if area != 0:
        return None
    size = img.shape[:2]
    coor = tuple(contour[0][0])
    output = {'coor': coor}
    colors = (0, 255, 0), (255, 0, 0), (255, 255, 0), (0, 0, 255), (0, 0, 134)
    mappings = dict(zip(colors, ('champion', 'structure', 'monster', 'minion', 'small_monster')))
    nearest_color = get_nearest(img[coor_offset(coor, (0, -1), size)], colors, 25)
    if nearest_color is None:
        return None
    if mappings[nearest_color] == 'champion':
        color = img[coor_offset(coor, (1, 0), size)]
        output['name'] = get_nearest_value(
            color,
            ((0, 255, 0), (255, 0, 0), (0, 0, 255)),
            ('player_champion', 'enemy_champion', 'ally_champion'))
        output['center'] = coor[0]+40, coor[1]+100
        hp_bar = img[coor[1]:coor[1]+1, coor[0]+1:coor[0]+106]
        output['health'] = get_hp_value(hp_bar)
        output['level'] = get_summoner_level(
            crop(img, (coor[0]-22, coor[1]-12, 19, 21)), LEVEL_OCR)
        output['is_turret'] = tuple(img[coor_offset(coor, (-2, 0), size)]) == (0, 36, 21)
    elif mappings[nearest_color] == 'structure':
        output['name'] = 'structure'
        output['center'] = coor[0] + 75, coor[1] + 150
    elif mappings[nearest_color] == 'monster':
        output['name'] = 'monster'
    elif mappings[nearest_color] == 'small_monster':
        output['name'] = 'small_monster'
    elif mappings[nearest_color] == 'minion':
        color = img[coor_offset(coor, (1, 0), size)]
        colors = (98, 167, 231), (224, 114, 112), (219, 170, 130)
        mappings = dict(zip(colors, ('ally_minion', 'enemy_minion', 'plant')))
        output['name'] = mappings[get_nearest(color, colors)]
        hp_bar = img[coor[1]:coor[1]+1, coor[0]+1:coor[0]+61]
        output['health'] = get_small_hp_value(hp_bar)
        output['center'] = coor[0]+30, coor[1]+35
        if output['name'] == 'enemy_minion':
            output['aggro'] = get_color_diff(
                img[coor_offset(coor, (28, -16), size)], (255, 0, 0)) < 50
        output['is_order_side'] = output['center'][1] / \
            output['center'][0] > img.shape[0]/img.shape[1]
        try:
            output['is_turret'] = (
                tuple(img[coor_offset(coor, (-1, 0), size)]) == (0, 36, 21) or
                tuple(img[output['center'][::-1]]) == (0, 36, 21)
            )
        except IndexError:
            output['is_turret'] = False
    return output


def identify_turret(contour, area):
    ''' Indentify an turret from contour '''
    if area > 3000:
        x, y, w, h = cv2.boundingRect(contour)
        center = x + w//2, y + h - 30
        return {'name': 'turret', 'coor': tuple(contour[0][0]), 'center': center}
    return None


def identify_turret_aggro(contour, area):
    ''' Indentify an turret from contour '''
    if(600 < area < 3000 and
       inside_rect(contour[0][0], (470, 260, 100, 100))):
        return {'name': 'turret_aggro', 'coor': tuple(contour[0][0])}
    return None


def get_dependent_objects(objects):
    ''' Finds the objects from exisiting objects '''
    objects['shield_minion'] = lfilter(lambda o: o['is_turret'], objects['ally_minion'])
    objects['enemy_minion_aggro'] = lfilter(lambda o: o['aggro'], objects['enemy_minion'])
    objects['player_champion'] = (None if objects['player_champion'] ==
                                  [] else objects['player_champion'][0])

    if objects['turret'] != [] and objects['player_champion'] is not None:
        for turret in objects['turret']:
            turret['distance'] = distance(
                turret['center'], objects['player_champion']['center'])
        objects['turret'].sort(key=lambda o: o['distance'])
        objects['closest_turret'] = objects['turret'][0]
    else:
        objects['closest_turret'] = None

    if objects['enemy_minion'] != [] and objects['player_champion'] is not None:
        for minion in objects['enemy_minion']:
            minion['distance'] = distance(
                minion['center'], objects['player_champion']['center'])
        objects['enemy_minion'].sort(key=lambda o: o['distance'])
        objects['closest_enemy_minion'] = objects['enemy_minion'][0]
    else:
        objects['closest_enemy_minion'] = None
    if len(objects['enemy_champion']) > 0:
        objects['enemy_champion'].sort(key=lambda o: o['health'])
        objects['lowest_enemy_champion'] = objects['enemy_champion'][0]
    else:
        objects['lowest_enemy_champion'] = None
    if len(objects['enemy_champion']) > 0 and objects['player_champion'] is not None:
        for champion in objects['enemy_champion']:
            champion['distance'] = distance(
                champion['center'], objects['player_champion']['center'])
        objects['enemy_champion'].sort(key=lambda o: o['distance'])
        objects['closest_enemy_champion'] = objects['enemy_champion'][0]
    else:
        objects['closest_enemy_champion'] = None


def get_objects(analytics, img, start, end):
    ''' Finds the league objects '''
    analytics.start_timer('get_objects', 'Finding objects')
    threshed = cv2.inRange(img, start, end)
    contours, _ = cv2.findContours(
        threshed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    objects = dict(zip(Objects._fields, [[] for _ in range(len(Objects._fields))]))
    for contour in contours:
        area = cv2.contourArea(contour)
        turret_aggro = identify_turret_aggro(contour, area)
        if turret_aggro is not None:
            objects['turret_aggro'].append(turret_aggro)
            continue
        turret = identify_turret(contour, area)
        if turret is not None:
            objects['turret'].append(turret)
            continue
        obj = identify_object(img, contour, area)
        if obj is not None:
            objects[obj['name']].append(obj)
    get_dependent_objects(objects)
    analytics.end_timer('get_objects')
    return Objects(**objects)


def is_camera_locked(img):
    ''' Returns is the camera is locked '''
    return (img[CAMERA_LOCK[::-1]] == [49, 65, 52]).all()
