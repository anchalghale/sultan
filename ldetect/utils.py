import cv2


def draw_objects(img, objects):
    for obj in objects:
        if 'health' in obj:
            text = f'''{obj['name']}, {obj['health']}'''
        else:
            text = f'''{obj['name']}'''
        img = cv2.putText(img, text, obj['coor'], 1, 0.8, (0, 255, 0))
    cv2.imshow('', img)
    cv2.waitKey()
