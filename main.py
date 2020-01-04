''' Main module of the script '''
import time

import keyboard
import mouse

from analytics import Analytics
from logger import CliLogger
from screen import Screen
from resources import Resources
from cooldown import Cooldown
from window import find_rect
from lutils import wait_league_window
from ldetect import is_camera_locked, is_level_up, get_minimap_coor, get_minimap_areas, get_objects
from bot import goto_lane, goto_enemy_base, evade, level_up
from constants import LEVEL_UP_SEQUENCE


def filter_objects(objs):
    ''' Filters the objects that are detected '''
    output = {}
    output['enemy_minions'] = filter(lambda o: o['name'] == 'enemy_minion', objs)
    output['ally_minions'] = filter(lambda o: o['name'] == 'ally_minion', objs)
    output['turrets'] = filter(lambda o: o['name'] == 'turret', objs)
    output['shield_minions'] = filter(
        lambda o: o['name'] == 'ally_minion' and not o['is_order_side'], objs)
    for key, value in output.items():
        output[key] = list(value)
    return output


def main():
    '''Main function of the script'''
    logger = CliLogger()
    analytics = Analytics(logger)
    analytics.ignore = ['screenshot', 'get_minimap_coor',
                        'get_minimap_areas', 'get_objects']
    screen = Screen()
    resources = Resources()
    cooldown = Cooldown({'goto_lane': 20, 'goto_enemy_base': 3, 'evade': 0.2})
    resources.load(analytics)

    hwnd = wait_league_window(logger, (0, 0, 1024, 768))
    time.sleep(1)

    logger.log('Press and hold x to exit bot.')
    while True:
        analytics.start_timer()
        if keyboard.is_pressed('x'):
            break
        img = screen.screenshot(analytics, find_rect(hwnd))
        if not is_camera_locked(img):
            keyboard.press_and_release('y')
        level_ups = is_level_up(img)
        level_up(level_ups, LEVEL_UP_SEQUENCE)
        coor = get_minimap_coor(analytics, img)
        areas = get_minimap_areas(analytics, resources.images, coor)
        objs = get_objects(analytics, img, (190, 0, 190), (255, 20, 255))
        objs = filter_objects(objs)
        enemy_minions = objs.get('enemy_minions')
        shield_minions = objs.get('shield_minions')
        turrets = objs.get('turrets')

        if (turrets != [] and
                areas['is_chaos_side'] and
                areas['is_turret'] and len(shield_minions) <= 0):
            evade(cooldown)
            analytics.end_timer()
            time.sleep(1)
            continue
        if turrets != [] and areas['is_chaos_side'] and len(shield_minions) > 0:
            mouse.move(*turrets[0]['coor'])
            mouse.click()
            analytics.end_timer()
            time.sleep(1)
            continue
        if enemy_minions != []:
            enemy_minions.sort(key=lambda o: o['health'])
            mouse.move(*enemy_minions[0]['center'])
            mouse.click()
            analytics.end_timer()
            time.sleep(1)
            continue
        if areas['is_turret']:
            if len(shield_minions) <= 2:
                goto_lane(cooldown)
                analytics.end_timer()
                time.sleep(1)
                continue
        if not (areas['is_chaos_side'] and areas['is_lane']):
            goto_lane(cooldown)
            analytics.end_timer()
            time.sleep(1)
            continue

        if len(shield_minions) > 2:
            goto_enemy_base(cooldown)
        analytics.end_timer()
        time.sleep(1)


if __name__ == "__main__":
    main()
