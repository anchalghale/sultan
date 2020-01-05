''' Utility functions of lvision package '''
import cv2


def draw_objects(img, objects, wait=True):
    ''' Draws the object data to the original image '''
    for obj in objects:
        if 'center' in obj:
            img = cv2.circle(img, obj['center'], 7, (0, 0, 255), -1)
    for obj in objects:
        if 'health' in obj:
            text = f'''{obj['name']}, {obj['health']}, {obj['is_turret']}'''
        else:
            text = f'''{obj['name']}'''
        img = cv2.putText(img, text, obj['coor'], 1, 0.8, (0, 255, 0))
    # img = cv2.line(img, (0, 0), img.shape[:2][::-1], (0, 255, 0))
    cv2.imshow('', img)
    if wait:
        cv2.waitKey()
    else:
        cv2.waitKey(1)
