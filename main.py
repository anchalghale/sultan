''' Main module of the script '''
import time
import collections
import traceback
import random

import keyboard
import mouse

from analytics import Analytics
from logger import CliLogger
from screen import Screen
from resources import Resources
from cooldown import Cooldown
from window import find_rect

from lutils import wait_league_window
from lvision.filter import filter_objects
from lvision.state import get_game_state
from lvision.ocr import Ocr
from lvision import (is_camera_locked, get_level_ups, get_ability_points,
                     get_abilities, get_attack_speed,
                     get_minimap_coor, get_minimap_areas, get_objects)


from bot.exceptions import BotContinueException, BotExitException
from bot import goto_lane, goto_enemy_base, evade, move_forward, level_up

from constants import LEVEL_UP_SEQUENCE, ANALYTICS_IGNORE, COOLDOWNS

Utility = collections.namedtuple('Utility', 'logger screen resources analytics cooldown ocr')

TICK_INTERVAL = 50, 150  # ms


def tick(utility):
    ''' Simulates a single tick of the bot '''

    utility.analytics.start_timer()
    img = utility.screen.d3d.get_latest_frame()
    if not is_camera_locked(img):
        keyboard.press_and_release('y')
    level_ups = get_level_ups(img)
    level_up(level_ups, get_ability_points(img), LEVEL_UP_SEQUENCE)
    coor = get_minimap_coor(utility.analytics, img)
    areas = get_minimap_areas(utility.analytics, utility.resources.images, coor)
    abilities = get_abilities(img)
    attack_speed = get_attack_speed(img, utility.ocr)
    objects = get_objects(utility.analytics, img, (190, 0, 190), (255, 20, 255))
    fobjects = filter_objects(objects, areas)
    state = get_game_state(fobjects, areas)
    utility.analytics.end_timer()

    # if len(fobjects.enemy_champions) >= 1:
    #     orb_walk(areas, fobjects.enemy_champions[0]['center'], )
    # return
    if areas.is_turret and state.is_enemy_turret and not state.is_shielded:
        evade(utility.cooldown, areas)
        raise BotContinueException
    if len(fobjects.turret_aggros) > 0:
        evade(utility.cooldown, areas)
        raise BotContinueException
    if state.enemy_minions_dps >= 10 and len(fobjects.enemy_champions) == 0:
        evade(utility.cooldown, areas)
        raise BotContinueException
    if len(fobjects.enemy_champions) >= 1:
        if state.enemy_minions_dps + state.enemy_champions_dps > state.player_champions_dps:
            evade(utility.cooldown, areas)
            raise BotContinueException
        fobjects.enemy_champions.sort(key=lambda o: o['health'])
        if not fobjects.enemy_champions[0]['is_turret']:
            mouse.move(*fobjects.enemy_champions[0]['center'])
            mouse.click()
            raise BotContinueException
        evade(utility.cooldown, areas)
        raise BotContinueException
    if fobjects.open_structures != []:
        if abilities.w:
            keyboard.press_and_release('w')
        fobjects.enemy_minions.sort(key=lambda o: o['health'])
        mouse.move(*fobjects.open_structures[0]['center'])
        mouse.click()
        raise BotContinueException
    if state.is_enemy_turret and state.is_shielded:
        if abilities.w:
            keyboard.press_and_release('w')
        mouse.move(*fobjects.turrets[0]['center'])
        mouse.click()
        raise BotContinueException
    if fobjects.enemy_minions != []:
        if abilities.w:
            keyboard.press_and_release('w')
        fobjects.enemy_minions.sort(key=lambda o: o['health'])
        mouse.move(*fobjects.enemy_minions[0]['center'])
        mouse.click()
        raise BotContinueException
    if (areas.is_chaos_side and
            (areas.is_lane or areas.is_base) and
            not state.is_enemy_turret):
        move_forward(utility.cooldown, areas)
        raise BotContinueException
    if not (areas.is_chaos_side and areas.is_lane):
        goto_lane(utility.cooldown)
        raise BotContinueException
    if len(fobjects.shield_minions) > 2:
        goto_enemy_base(utility.cooldown)
        raise BotContinueException


def main():
    '''Main function of the script'''
    paused = False

    logger = CliLogger()
    screen = Screen()
    resources = Resources()
    analytics = Analytics(logger)
    cooldown = Cooldown(COOLDOWNS)
    analytics.ignore = ANALYTICS_IGNORE
    resources.load(analytics)
    handle = wait_league_window(logger, (0, 0, 1024, 768))
    ocr = Ocr(threshold=200000)
    ocr.load_model('lvision/ocr/trained/gold.yml')

    logger.log('Press and hold x to exit bot.')
    screen.d3d.capture(target_fps=10, region=find_rect(handle))
    while True:
        try:
            if keyboard.is_pressed('x'):
                raise BotExitException
            if keyboard.is_pressed('ctrl+u'):
                paused = False
            if paused:
                time.sleep(0.1)
                continue
            if keyboard.is_pressed('ctrl+p'):
                paused = True
                logger.log('Bot paused. Press ctrl+u to unpause. Press x to exit.')
                continue
            tick(Utility(logger, screen, resources, analytics, cooldown, ocr))
            time.sleep(random.randint(*TICK_INTERVAL)/1000)
        except BotContinueException:
            time.sleep(random.randint(*TICK_INTERVAL)/1000)
        except BotExitException:
            screen.d3d.stop()
            break
        except Exception:  # pylint:disable=broad-except
            traceback.print_exc()
            screen.d3d.stop()
            break


if __name__ == "__main__":
    main()
