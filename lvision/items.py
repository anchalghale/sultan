'''Module to detect summoner items'''
import cv2

from cutils import crop, get_color_diff

RECTANGLES = [(596, 709, 12, 12),
              (619, 709, 12, 12),
              (642, 709, 12, 12),
              (596, 731, 12, 12),
              (619, 731, 12, 12),
              (642, 731, 12, 12)]

MAPPING = {
    -1: None,
    0: '''Doran's Blade''',
    1: '''Health Potion''',
}

KEY_MAPPING = [1, 2, 3, 5, 6, 7]


def get_summoner_items(image, models):
    '''Finds summoners items'''
    def prepare(image, rect):
        img = crop(image, rect)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        return img
    items = []

    for i, rect in enumerate(RECTANGLES):
        img = prepare(image, rect)
        item = MAPPING[models['summoner_item'].predict(img)]
        items.append({'name': item, 'key': KEY_MAPPING[i]})
    return items


def get_item(items, name):
    ''' Get an item from name return None if not found '''
    return next(filter(lambda i: i['name'] == name, items), None)


def get_is_shop(img):
    ''' Returns if the shop menu is open or not '''
    return get_color_diff(img[5, 906], [136, 123, 60]) < 10
