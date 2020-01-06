''' Main module of the get objects function test '''
import argparse
import glob
import time

import cv2
import keyboard

from analytics import Analytics
from logger import CliLogger
from screen import Screen
from window import find_rect

from lutils import wait_league_window
from lvision.utils import draw_objects
from lvision import (is_camera_locked, get_level_ups, get_minimap_coor,
                     get_objects, get_abilities, get_ability_points)
from lvision.ocr import OCR
from lvision.gold import get_gold

from constants import ANALYTICS_IGNORE


def tick(logger, analytics, img, ocr):
    ''' Simulates a single tick of the bot '''
    analytics.start_timer()
    logger.log(f'Camera locked: {is_camera_locked(img)}')
    logger.log(get_abilities(img))
    logger.log(get_ability_points(img))
    logger.log(get_level_ups(img))
    logger.log(get_gold(img, ocr))
    logger.log(f'Minimap coor: {get_minimap_coor(analytics, img)}')
    objs = get_objects(analytics, img, (190, 0, 190), (255, 20, 255))
    enemy_minions = list(filter(lambda o: o['name'] == 'enemy_minion', objs))
    enemy_minions.sort(key=lambda o: o['health'])
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
    ocr = OCR(threshold=200000)
    ocr.load_model('model.yml')
    analytics = Analytics(logger)
    analytics.ignore = ANALYTICS_IGNORE

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
            img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            objs = tick(logger, analytics, img, ocr)
            draw_objects(img_bgr, objs, wait=False)
            logger.log('Press and hold x to exit bot.')
            logger.log('-'*50)
            time.sleep(1)
        return

    if args.all:
        files = glob.glob('screenshots/*.png')
    else:
        files = ['screenshots/Screen144.png']

    for file in files:
        img_bgr = cv2.imread(file)
        img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        objs = tick(logger, analytics, img, ocr)
        logger.log('Press x to exit.')
        logger.log('-'*50)
        if draw_objects(img_bgr, objs) == 120:
            break


if __name__ == "__main__":
    main()
    print('exit')
