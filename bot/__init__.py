''' Tasks that bot performs using keyboard and mouse '''
import time

import numpy
import mouse
import keyboard

from cutils import humanize

# DOWN = 509, 477
# UP = 506, 146
# RIGHT = 672, 341
# LEFT = 299, 342
# DOWN_LEFT = 410, 460
# UP_RIGHT = 665, 220

DOWN = numpy.array([0, 1])
UP = numpy.array([0, -1])
RIGHT = numpy.array([1.5, 0])
LEFT = numpy.array([-1.5, 0])
DOWN_LEFT = numpy.array([-1.5, 1])
UP_RIGHT = numpy.array([1.5, -1])

MAX_OFFSET = 25


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


def kite(areas, coor, attack_speed):
    ''' Kite from a coordinate '''
    mouse.move(*coor)
    mouse.click()
    time.sleep(.7/attack_speed)
    evade_relative(coor, areas)
    time.sleep(.2/attack_speed)


def orb_walk(areas, coor, attack_speed):
    ''' Orb walk from a coordinate '''
    mouse.move(*coor)
    mouse.click()
    time.sleep(.7/attack_speed)
    move_forward_relative(coor, areas)
    time.sleep(.2/attack_speed)


def poke(areas, coor, attack_speed):
    ''' Orb walk from a coordinate '''
    mouse.move(*coor)
    mouse.click()
    time.sleep(.7/attack_speed)
    evade_relative((515, 350), areas)
    time.sleep(.2/attack_speed)


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
