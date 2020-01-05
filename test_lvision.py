''' Main module of the get objects function test '''
import argparse
import glob

import cv2

from analytics import Analytics
from logger import CliLogger
from resources import Resources
from lvision.utils import draw_objects
from lvision import (is_camera_locked, get_level_ups, get_minimap_coor,
                     get_objects, get_abilities, get_ability_points)


def main():
    '''Main function of the script'''
    parser = argparse.ArgumentParser()
    parser.add_argument('--all', '-a', action='store_true')
    args = parser.parse_args()

    logger = CliLogger()
    analytics = Analytics(logger)
    analytics.ignore = ['screenshot', 'get_minimap_coor',
                        'get_minimap_areas', 'get_objects']
    resources = Resources()
    resources.load(analytics)
    logger.log('-'*50)

    if args.all:
        files = glob.glob('screenshots/*.png')
    else:
        files = ['screenshots/Screen144.png']

    for file in files:
        img_bgr = cv2.imread(file)
        img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

        analytics.start_timer()
        logger.log(f'Camera locked: {is_camera_locked(img)}')
        logger.log(get_abilities(img))
        logger.log(get_ability_points(img))
        logger.log(get_level_ups(img))
        logger.log(f'Minimap coor: {get_minimap_coor(analytics, img)}')
        objs = get_objects(analytics, img, (190, 0, 190), (255, 20, 255))
        enemy_minions = list(filter(lambda o: o['name'] == 'enemy_minion', objs))
        enemy_minions.sort(key=lambda o: o['health'])
        analytics.end_timer()
        logger.log('Press x to exit.')
        logger.log('-'*50)
        if draw_objects(img_bgr, objs) == 120:
            break


if __name__ == "__main__":
    main()
