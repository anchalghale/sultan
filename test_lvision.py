''' Main module of the get objects function test '''
import argparse
import glob
import time
import collections

import cv2
import keyboard

from analytics import Analytics
from logger import CliLogger
from screen import Screen
from resources import Resources
from window import find_rect

from lutils import wait_league_window
from lvision.utils import draw_objects
from lvision import (is_camera_locked, get_level_ups, get_minimap_coor,
                     get_objects, get_abilities, get_ability_points,
                     get_minimap_areas, get_gold, get_summoner_spells, get_attack_speed, get_summoner_level)

from lvision.ocr import Ocr

from constants import ANALYTICS_IGNORE


OCR = collections.namedtuple('ocr', 'gold spell level')


def tick(logger, analytics, resources, img, ocr):
    ''' Simulates a single tick of the bot '''
    analytics.start_timer()
    coor = get_minimap_coor(analytics, img)
    areas = get_minimap_areas(analytics, resources.images, coor)
    logger.log(f'Camera locked: {is_camera_locked(img)}')
    logger.log(get_abilities(img))
    logger.log(get_ability_points(img))
    logger.log(get_level_ups(img))
    logger.log(areas)
    logger.log(f'Gold: {get_gold(img, ocr.gold)}')
    logger.log(f'Attack speed: {get_attack_speed(img, ocr.gold)}')
    logger.log(get_summoner_spells(img, ocr.spell))
    logger.log(f'Minimap coor: {coor}')
    objs = get_objects(analytics, img, (190, 0, 190), (255, 20, 255))
    coor = [obj['coor'] for obj in objs if obj['name'] == 'player_champion']
    logger.log(f'Level: {get_summoner_level(img, ocr.level, coor[0])}')
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
    gold_ocr = Ocr(threshold=200000)
    gold_ocr.load_model('lvision/ocr/trained/gold.yml')

    spell_ocr = Ocr()
    spell_ocr.load_model('lvision/ocr/trained/summoner_spell.yml')

    level_ocr = Ocr()
    level_ocr.load_model('lvision/ocr/trained/summoner_level.yml')

    ocr = OCR(gold_ocr, spell_ocr, level_ocr)
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
            img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            objs = tick(logger, analytics, resources, img, ocr)
            draw_objects(img_bgr, objs, wait=False, title='League Vision - Interactive')
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
        objs = tick(logger, analytics, resources, img, ocr)
        logger.log('Press x to exit.')
        logger.log('-'*50)
        if draw_objects(img_bgr, objs, title=f'League Vision - {file}') == 120:
            break


if __name__ == "__main__":
    main()
    print('exit')
