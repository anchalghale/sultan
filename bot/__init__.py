''' Tasks that bot performs using keyboard and mouse '''
import mouse
import keyboard

from cutils import humanize

DOWN = 509, 477
UP = 506, 146
RIGHT = 672, 341
LEFT = 299, 342
DOWN_LEFT = 410, 460
UP_RIGHT = 665, 220

MAX_OFFSET = 25


def goto_lane(cooldown):
    ''' Goto a lane '''
    # Currently moves to mid lane only
    if not cooldown.is_available('goto_lane'):
        return
    print('moving to lane')
    mouse.move(*humanize((931, 663)))
    mouse.right_click()
    cooldown.start_timer('goto_lane')


def evade(cooldown, areas):
    ''' Evade '''
    if not cooldown.is_available('evade'):
        return
    if areas.nearest_lane == 'mid':
        mouse.move(*humanize(DOWN_LEFT, max_offset=MAX_OFFSET))
    if areas.nearest_lane == 'top':
        if areas.is_map_divide:
            mouse.move(*humanize(DOWN_LEFT, max_offset=MAX_OFFSET))
        elif areas.is_order_side:
            mouse.move(*humanize(DOWN, max_offset=MAX_OFFSET))
        else:
            mouse.move(*humanize(LEFT, max_offset=MAX_OFFSET))
    if areas.nearest_lane == 'bot':
        if areas.is_map_divide:
            mouse.move(*humanize(DOWN_LEFT, max_offset=MAX_OFFSET))
        elif areas.is_order_side:
            mouse.move(*humanize(LEFT, max_offset=MAX_OFFSET))
        else:
            mouse.move(*humanize(DOWN, max_offset=MAX_OFFSET))
    mouse.right_click()
    cooldown.start_timer('evade')


def move_forward(cooldown, areas):
    ''' Move forward '''
    if not cooldown.is_available('move_forward'):
        return
    if areas.nearest_lane == 'mid':
        mouse.move(*humanize(UP_RIGHT, max_offset=MAX_OFFSET))
    if areas.nearest_lane == 'top':
        if areas.is_map_divide:
            mouse.move(*humanize(UP_RIGHT, max_offset=MAX_OFFSET))
        elif areas.is_order_side:
            mouse.move(*humanize(UP, max_offset=MAX_OFFSET))
        else:
            mouse.move(*humanize(RIGHT, max_offset=MAX_OFFSET))
    if areas.nearest_lane == 'bot':
        if areas.is_map_divide:
            mouse.move(*humanize(UP_RIGHT, max_offset=MAX_OFFSET))
        elif areas.is_order_side:
            mouse.move(*humanize(RIGHT, max_offset=MAX_OFFSET))
        else:
            mouse.move(*humanize(UP, max_offset=MAX_OFFSET))
    mouse.right_click()
    cooldown.start_timer('move_forward')


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
