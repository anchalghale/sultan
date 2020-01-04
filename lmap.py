''' Main module of the get objects function test '''
import glob
import cv2

from analytics import Analytics
from logger import CliLogger
from resources import Resources
from cutils import crop
from ldetect import get_minimap_coor

TURRET_LOCATIONS = [(54, 9)]


def get_turret_coors(analytics, img):
    analytics.start_timer()
    map_ = crop(img, (834, 577, 183, 183))
    coor = get_minimap_coor(analytics, img)
    width = 36
    height = 27
    pt1 = (coor[1]-width//2-1, coor[0]-height//2-1)
    pt2 = (coor[1]+width//2-2, coor[0]+height//2-1)
    turret_coor = []
    for turret in TURRET_LOCATIONS:
        if pt1[0] < turret[0] < pt2[0] and pt1[1] < turret[1] < pt2[1]:
            offset = [turret[0]-pt1[0], turret[1]-pt1[1]]
            scale = img.shape[1]/width
            offset = tuple([int(v * scale) for v in offset])
            turret_coor.append(offset)
            print('offset', offset)
    analytics.end_timer()

    for coor in turret_coor:
        img = cv2.circle(img, coor, 7, (0, 0, 255), -1)
    cv2.rectangle(map_, pt1, pt2, (0, 255, 0), 1)
    map_ = cv2.resize(map_, (0, 0), fx=5, fy=5, interpolation=cv2.INTER_NEAREST)
    cv2.imshow('Map', map_)
    cv2.imshow('', img)
    cv2.waitKey()


def main():
    '''Main function of the script'''
    logger = CliLogger()
    analytics = Analytics(logger)
    analytics.ignore = ['screenshot', 'get_minimap_coor',
                        'get_minimap_areas', 'get_objects']
    resources = Resources()
    resources.load(analytics)

    for file in glob.glob('screenshots/*.png'):
        img_bgr = cv2.imread(file)
        img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        get_turret_coors(analytics, img)
        # break


if __name__ == "__main__":
    main()
