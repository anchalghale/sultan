''' Main module of the get objects function test '''
import argparse
import glob
import time

import cv2
import keyboard

from analytics import Analytics
from logger import CliLogger
from screen import Screen
from resources import Resources
from window import find_rect

from lutils import wait_league_window
from lvision.utils import draw_objects
from lvision import (is_camera_locked, get_level_ups, get_minimap_coor, get_game_state,
                     get_objects, get_abilities, get_ability_points, get_is_shop, get_champion,
                     get_minimap_areas, get_gold, get_summoner_spells, get_is_loading_screen,
                     get_attack_speed, get_summoner_items, get_game_time, NoCharacterInMinimap)


from constants import ANALYTICS_IGNORE


def tick(logger, analytics, resources, img):
    ''' Simulates a single tick of the bot '''
    analytics.start_timer()
    logger.log(f'Loading screen: {get_is_loading_screen(img)}')
    coor = get_minimap_coor(analytics, img)
    areas = get_minimap_areas(analytics, resources.images, coor)
    objs = get_objects(analytics, img, (190, 0, 190), (255, 20, 255))
    logger.log(f'Camera locked: {is_camera_locked(img)}')
    logger.log(get_abilities(img))
    logger.log(get_ability_points(img))
    logger.log(get_level_ups(img))
    logger.log(areas)
    logger.log(get_game_state(objs, areas))
    logger.log(f'Gold: {get_gold(img, resources.models)}')
    logger.log(f'Attack speed: {get_attack_speed(img, resources.models)}')
    logger.log(get_summoner_spells(img, resources.models))
    logger.log(get_summoner_items(img, resources.models))
    logger.log(f'Time: {get_game_time(img, resources.models)} minute(s)')
    logger.log(f'Minimap coor: {coor}')
    logger.log(f'Is shop: {get_is_shop(img)}')
    logger.log(f'Champion: {get_champion(img, resources.models)}')
    analytics.end_timer()
    return objs


def main():
    '''Main function of the script'''
    parser = argparse.ArgumentParser()
    parser.add_argument('--all', '-a', action='store_true')
    parser.add_argument('--interactive', '-i', action='store_true')

    args = parser.parse_args()

    logger = CliLogger()
    screen = Screen()

    analytics = Analytics(logger)
    resources = Resources()
    analytics.ignore = ANALYTICS_IGNORE
    resources.load(analytics)

    if args.interactive:
        handle = wait_league_window(logger, (0, 0, 1024, 768))
        screen.d3d.capture(target_fps=10, region=find_rect(handle))
        while True:
            if keyboard.is_pressed('x'):
                cv2.destroyAllWindows()
                screen.d3d.stop()
                break
            img = screen.d3d.get_latest_frame()
            if img is None:
                continue
            try:
                img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                objs = tick(logger, analytics, resources, img)
                draw_objects(img_bgr, objs, wait=False, title='League Vision - Interactive')
                logger.log('Press and hold x to exit bot.')
            except NoCharacterInMinimap:
                pass
            logger.log('-'*50)
            time.sleep(1)
        return

    if args.all:
        files = glob.glob('screenshots/*.png')
    else:
        files = glob.glob('screenshots/*.png')[:1]

    for file in files:
        img_bgr = cv2.imread(file)
        img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        try:
            objs = tick(logger, analytics, resources, img)
            logger.log('Press x to exit.')
        except NoCharacterInMinimap:
            pass
        logger.log('-'*50)
        if draw_objects(img_bgr, objs, title=f'League Vision - {file}') == 120:
            break


if __name__ == "__main__":
    main()
    print('exit')
