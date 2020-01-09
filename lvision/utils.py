''' Utility functions of lvision package '''
import collections

import cv2

Objects = collections.namedtuple(
    'Objects',
    'player_champion enemy_champion lowest_enemy_champion closest_enemy_champion shield_minion '
    'structure monster ally_minion enemy_minion closest_enemy_minion small_monster turret_aggro '
    'turret plant ')


def lfilter(function, iterable):
    ''' Filters a list and outputs a list value '''
    return list(filter(function, iterable))


def draw_objects(img, objects, wait=True, title=''):
    ''' Draws the object data to the original image '''
    def prepare_objects(objects):
        dobjects = []
        for obj in list(objects):
            if obj is None:
                continue
            if isinstance(obj, dict):
                dobjects.append(obj)
            if isinstance(obj, list):
                dobjects += obj
        return dobjects
    objects = prepare_objects(objects)
    for obj in objects:
        if obj is None:
            continue
        if 'center' in obj:
            img = cv2.circle(img, obj['center'], 7, (0, 0, 255), -1)
    for obj in objects:
        if obj is None:
            continue
        if obj['name'] == 'enemy_minion':
            text = f'''{obj['name']}, {obj['health']}, {obj['aggro']}'''
        elif 'health' in obj and 'level' in obj:
            text = f'''{obj['name']}, {obj['level']}, {obj['health']}'''
        elif 'health' in obj:
            text = f'''{obj['name']}, {obj['health']}'''
        else:
            text = f'''{obj['name']}'''
        img = cv2.putText(img, text, obj['coor'], 1, 0.8, (0, 255, 0))
    cv2.imshow(title, img)
    cv2.moveWindow(title, 0, 0)
    if wait:
        output = cv2.waitKey()
        cv2.destroyWindow(title)
        return output
    output = cv2.waitKey(1)
    cv2.destroyWindow(title)
    return output
