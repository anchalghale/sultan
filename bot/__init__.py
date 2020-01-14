''' Tasks that bot performs using keyboard and mouse '''
import time

import numpy
import mouse
import keyboard

from cutils import humanize, distance
from lvision import get_item

from .exceptions import BotContinueException
from .constants import BASING_COOR
from .utils import get_minimap_relative

DOWN = numpy.array([0, 1])
UP = numpy.array([0, -1])
RIGHT = numpy.array([1.5, 0])
LEFT = numpy.array([-1.5, 0])
DOWN_LEFT = numpy.array([-1.5, 1])
UP_RIGHT = numpy.array([1.5, -1])

TELEPORT_LOCATIONS = {
    'top': (848, 631),
    'mid': (907, 681),
    'bot': (961, 746),
}

ITEMS = [(163, 146), (212, 146)]

MAX_OFFSET = 25


def buy_item(item):
    ''' Buys item '''
    if isinstance(item, str):
        keyboard.press_and_release('ctrl+enter')
        time.sleep(1)
        keyboard.write(item)
        time.sleep(1)
        keyboard.press_and_release('enter')
        time.sleep(1)
        keyboard.press_and_release('enter')
    else:
        mouse.move(*ITEMS[item])
        mouse.right_click()
    time.sleep(1)


def use_items(objects, areas, items):
    ''' Uses summoner spells '''
    health_potion = get_item(items, 'Health Potion')
    if (objects.player_champion is not None and objects.player_champion['health'] < 50
            and health_potion is not None and not areas.is_base):
        keyboard.press_and_release(str(health_potion['key']))


def use_spells(objects, areas, spells, level):
    ''' Uses summoner spells '''
    if (objects.player_champion is not None and
            objects.player_champion['health'] < 20 and 'heal' in spells):
        keyboard.press_and_release(spells['heal']['key'])
    if areas.is_base and areas.is_order_side and 'teleport' in spells and level > 1:
        teleport(spells['teleport']['key'])


def base(coor):
    ''' Moves to basing position '''
    distances = [distance(coor[::-1], i) for i in BASING_COOR]
    min_distance = min(distances)
    if min_distance <= 5:
        keyboard.press_and_release('b')
        time.sleep(10)
        return
    index = distances.index(min_distance)
    coor = get_minimap_relative(BASING_COOR[index])
    mouse.move(*humanize(coor, 1))
    mouse.right_click()
    time.sleep(1)


def teleport(key, lane='bot'):
    ''' Teleports to lane '''
    mouse.move(*humanize(TELEPORT_LOCATIONS[lane]))
    time.sleep(0.5)
    keyboard.press_and_release(key)
    time.sleep(1)


def goto_lane(cooldown, lane='bot'):
    ''' Goto a lane '''
    if not cooldown.is_available('goto_lane'):
        return
    if lane == 'mid':
        mouse.move(*humanize((931, 663)))
    else:
        mouse.move(*humanize((993, 730)))
    mouse.right_click()
    cooldown.start_timer('goto_lane')


def evade(cooldown, areas):
    ''' Evade '''
    if not cooldown.is_available('evade'):
        return
    evade_relative((515, 350), areas)
    cooldown.start_timer('evade')
    raise BotContinueException()


def move_forward(cooldown, areas):
    ''' Move forward '''
    if not cooldown.is_available('move_forward'):
        return
    move_forward_relative((515, 350), areas)
    cooldown.start_timer('move_forward')


def evade_relative(coor, areas, size=150):
    ''' Evade forward relative to a coordinate '''
    if areas.nearest_lane == 'mid':
        move = DOWN_LEFT
    if areas.nearest_lane == 'top':
        if areas.is_map_divide:
            move = DOWN_LEFT
        elif areas.is_order_side:
            move = DOWN
        else:
            move = LEFT
    if areas.nearest_lane == 'bot':
        if areas.is_map_divide:
            move = DOWN_LEFT
        elif areas.is_order_side:
            move = LEFT
        else:
            move = DOWN
    mouse.move(*humanize(move * size + coor, 5))
    mouse.right_click()


def move_forward_relative(coor, areas, size=150):
    ''' Move forward relative to a coordinate '''
    if areas.nearest_lane == 'mid':
        move = UP_RIGHT
    if areas.nearest_lane == 'top':
        if areas.is_map_divide:
            move = UP_RIGHT
        elif areas.is_order_side:
            move = UP
        else:
            move = RIGHT
    if areas.nearest_lane == 'bot':
        if areas.is_map_divide:
            move = UP_RIGHT
        elif areas.is_order_side:
            move = RIGHT
        else:
            move = UP
    mouse.move(*humanize(move * size + coor, 5))
    mouse.right_click()


def kite(areas, object_, attack_speed):
    ''' Kite from a coordinate '''
    keyboard.press('`')
    mouse.move(*object_['center'])
    mouse.right_click()
    time.sleep(.5/attack_speed)
    evade_relative(object_['center'], areas)
    keyboard.release('`')
    tick_interval = 300//attack_speed
    raise BotContinueException(tick_interval=(tick_interval, tick_interval))


def kite_minion(areas, object_, attack_speed):
    ''' Kite from a coordinate '''
    mouse.move(*object_['center'])
    mouse.click()
    time.sleep(.5/attack_speed)
    evade_relative(object_['center'], areas)
    tick_interval = 300//attack_speed
    raise BotContinueException(tick_interval=(tick_interval, tick_interval))


def orb_walk(areas, object_, attack_speed):
    ''' Orb walk from a coordinate '''
    keyboard.press('`')
    mouse.move(*object_['center'])
    mouse.right_click()
    time.sleep(.5/attack_speed)
    move_forward_relative(object_['center'], areas, size=50)
    keyboard.release('`')
    tick_interval = 300//attack_speed
    raise BotContinueException(tick_interval=(tick_interval, tick_interval))


def poke(areas, object_, attack_speed):
    ''' Orb walk from a coordinate '''
    keyboard.press('`')
    mouse.move(*object_['center'])
    mouse.right_click()
    time.sleep(.7/attack_speed)
    evade_relative((515, 350), areas)
    keyboard.release('`')
    tick_interval = 300//attack_speed
    raise BotContinueException(tick_interval=(tick_interval, tick_interval))


def goto_enemy_base(cooldown):
    ''' Goto enemy base '''
    if not cooldown.is_available('goto_enemy_base'):
        return
    print('moving to enemy base')
    mouse.move(*humanize((988, 605)))
    mouse.right_click()
    cooldown.start_timer('goto_enemy_base')


def level_up(level_ups, ability_points, sequence):
    ''' Levels up an ability using priority sequence '''
    for ability in sequence:
        if getattr(level_ups, ability) and not getattr(ability_points, ability):
            print(f'leveling up {ability}')
            keyboard.press_and_release(f'ctrl+{ability}')
            return

    for ability in sequence:
        if getattr(level_ups, ability):
            print(f'leveling up {ability}')
            keyboard.press_and_release(f'ctrl+{ability}')
            return


def use_ability(object_, key):
    ''' Uses an ability on an object '''
    mouse.move(*object_['center'])
    keyboard.press_and_release(key)
