''' Main module of the get objects function test '''
import cv2

from analytics import Analytics
from logger import CliLogger
from resources import Resources
from ldetect import is_camera_locked, is_level_up, get_minimap_coor, get_objects
from ldetect.utils import draw_objects


def main():
    '''Main function of the script'''
    logger = CliLogger()
    analytics = Analytics(logger)
    analytics.ignore = ['screenshot', 'get_minimap_coor',
                        'get_minimap_areas', 'get_objects']
    resources = Resources()
    resources.load(analytics)

    img_bgr = cv2.imread('screenshots/Screen144.png')
    img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    analytics.start_timer()
    logger.log(f'Camera locked: {is_camera_locked(img)}')
    logger.log(is_level_up(img))
    logger.log(f'Minimap coor: {get_minimap_coor(analytics, img)}')
    objs = get_objects(analytics, img, (190, 0, 190), (255, 20, 255))
    enemy_minions = list(filter(lambda o: o['name'] == 'enemy_minion', objs))
    enemy_minions.sort(key=lambda o: o['health'])
    analytics.end_timer()
    draw_objects(img_bgr, objs)


if __name__ == "__main__":
    main()
