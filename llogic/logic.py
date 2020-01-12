''' Logic module of the bot '''
import time

import keyboard
import mouse

from lvision.state import get_game_state
from lvision import (is_camera_locked, get_level_ups, get_ability_points, get_is_shop,
                     get_abilities, get_attack_speed, get_gold, get_summoner_items,
                     get_minimap_coor, get_minimap_areas, get_objects)

from bot import goto_lane, evade, move_forward, level_up, poke, kite, buy_item
from bot.exceptions import BotContinueException
from constants import LEVEL_UP_SEQUENCE


class Logic:
    ''' Logic class of the bot '''

    def __init__(self):
        self.command = None

    def buy_items(self, is_shop, gold, items):
        ''' Buys items '''
        if gold == 500 and all(i is None for i in items):
            self.command = 'buy_items'
        if self.command == 'buy_items':
            if not is_shop:
                keyboard.press_and_release('p')
                time.sleep(1)
                raise BotContinueException
            if gold == 500:
                buy_item(0)
                buy_item(1)
                self.command = None
        if self.command != 'buy_items':
            if is_shop:
                keyboard.press_and_release('p')
                time.sleep(1)

    def tick(self, utility):
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
        attack_speed = get_attack_speed(img, utility.resources.models["gold"])
        gold = get_gold(img, utility.resources.models["gold"])
        items = get_summoner_items(img, utility.resources.models["summoner_item"])
        is_shop = get_is_shop(img)
        objects = get_objects(utility.analytics, img, (190, 0, 190), (255, 20, 255))
        state = get_game_state(objects, areas)
        utility.analytics.end_timer()
        self.buy_items(is_shop, gold, items)
        if areas.is_turret and state.is_enemy_turret and not state.is_shielded:
            evade(utility.cooldown, areas)
            raise BotContinueException
        if len(objects.turret_aggro) > 0:
            evade(utility.cooldown, areas)
            raise BotContinueException
        if state.enemy_minions_dps >= 10 and len(objects.enemy_champion) == 0:
            if objects.closest_enemy_minion:
                kite(areas, objects.closest_enemy_minion['center'], attack_speed)
            else:
                evade(utility.cooldown, areas)
            raise BotContinueException
        if state.enemy_minions_dps + state.enemy_champions_dps > state.player_champions_dps:
            evade(utility.cooldown, areas)
            raise BotContinueException
        if objects.enemy_champion != [] and objects.closest_enemy_champion['distance'] < 300:
            if state.enemy_kill_pressure:
                if abilities.e:
                    mouse.move(*objects.lowest_enemy_champion['center'])
                    keyboard.press_and_release('e')
                if state.is_kitable:
                    kite(areas, objects.lowest_enemy_champion['center'], attack_speed)
                else:
                    evade(utility.cooldown, areas)
                raise BotContinueException
            # if state.kill_pressure:
            #     if abilities.w:
            #         keyboard.press_and_release('w')
            #     if abilities.q:
            #         keyboard.press_and_release('q')
            #     if abilities.e:
            #         mouse.move(*objects.lowest_enemy_champion['center'])
            #         keyboard.press_and_release('e')
            #     orb_walk(areas, objects.lowest_enemy_champion['center'], attack_speed)
            #     raise BotContinueException
            if state.is_pokeable:
                if abilities.e:
                    mouse.move(*objects.closest_enemy_champion['center'])
                    keyboard.press_and_release('e')
                if abilities.w:
                    keyboard.press_and_release('w')
                poke(areas, objects.closest_enemy_champion['center'], attack_speed)
        # if(objects.closest_enemy_champion is not None and
        #    objects.closest_enemy_champion['distance'] < 300 and
        #    len(objects.turret) <= 0 and
        #    state.potential_enemy_minions_dps <= 30):
        #     if not objects.closest_enemy_champion['is_turret']:
        #         poke(areas, objects.closest_enemy_champion['center'], attack_speed)
        #         raise BotContinueException
        #     evade(utility.cooldown, areas)
        #     raise BotContinueException
        # if fobjects.open_structures != []:
        #     if abilities.w:
        #         keyboard.press_and_release('w')
        #     fobjects.enemy_minions.sort(key=lambda o: o['health'])
        #     mouse.move(*fobjects.open_structures[0]['center'])
        #     mouse.click()
        #     raise BotContinueException
        if state.is_enemy_turret and state.is_shielded:
            if abilities.w:
                keyboard.press_and_release('w')
            mouse.move(*objects.turret[0]['center'])
            mouse.click()
            raise BotContinueException
        if objects.closest_enemy_minion:
            if abilities.w:
                keyboard.press_and_release('w')
            mouse.move(*objects.closest_enemy_minion['center'])
            mouse.click()
            raise BotContinueException
        if ((areas.is_lane or (areas.is_base and areas.is_chaos_side)) and
                not state.is_enemy_turret):
            move_forward(utility.cooldown, areas)
            raise BotContinueException
        if not (areas.is_chaos_side and areas.is_lane):
            goto_lane(utility.cooldown)
            raise BotContinueException
