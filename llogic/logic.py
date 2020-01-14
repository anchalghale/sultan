''' Logic module of the bot '''
import time
import random

import keyboard

import champions

from lvision import (
    is_camera_locked, get_level_ups, get_ability_points, get_is_shop, get_game_time,
    get_abilities, get_attack_speed, get_gold, get_summoner_items, get_game_state,
    get_minimap_coor, get_minimap_areas, get_objects, get_summoner_spells)
from bot import (
    goto_lane, evade, move_forward, level_up, use_spells, use_items, buy_item, base)
from bot.exceptions import BotContinueException
from constants import LEVEL_UP_SEQUENCE


def goto_lane_logic(utility, areas, objects, gtime):
    ''' Moving to lane logic '''
    if gtime <= 1:
        if not (areas.is_map_divide and areas.is_lane):
            goto_lane(utility.cooldown)
            raise BotContinueException
    else:
        if areas.is_chaos_side and areas.is_base and objects.turret == []:
            move_forward(utility.cooldown, areas)
            raise BotContinueException
        if not (areas.is_chaos_side and areas.is_lane):
            goto_lane(utility.cooldown)
            raise BotContinueException
        if objects.turret == []:
            move_forward(utility.cooldown, areas)


def base_logic(areas, spells, coor, gold, items):
    ''' Basing logic '''
    if (gold >= 2600 and list(map(lambda i: i['name'], items)).count(None) >= 1 and
            not areas.is_base and 'teleport' in spells):
        base(coor)
        raise BotContinueException


class Logic:
    ''' Logic class of the bot '''

    def __init__(self):
        self.command = None
        self.last_health = None
        self.lane = random.choice(['bot', 'mid', 'top'])
        self.champion = champions.ashe

    def get_damage_taken(self, health):
        ''' Calcuates the damage taken in last tick '''
        if self.last_health is None:
            self.last_health = health
            return None
        if health is None:
            return None
        output = health - self.last_health
        self.last_health = health
        return output

    def buy_items(self, areas, is_shop, gold, items):
        ''' Buys items '''
        if gold == 500 and all(i['name'] is None for i in items):
            buyable = 1
        else:
            buyable = min(list(map(lambda i: i['name'], items)).count(None), gold//2600)
        if buyable > 0 and areas.is_platform:
            if not is_shop:
                keyboard.press_and_release('p')
                time.sleep(1)
                raise BotContinueException
            if gold == 500:
                buy_item(0)
                buy_item(1)
                raise BotContinueException
            for _ in range(buyable):
                buy_item('hurr')
            raise BotContinueException
        if is_shop:
            keyboard.press_and_release('p')
            time.sleep(1)
            raise BotContinueException

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
        attack_speed = get_attack_speed(img, utility.resources.models)
        gold = get_gold(img, utility.resources.models)
        items = get_summoner_items(img, utility.resources.models)
        is_shop = get_is_shop(img)
        gtime = get_game_time(img, utility.resources.models)
        spells = get_summoner_spells(img, utility.resources.models)
        objects = get_objects(utility.analytics, img, (190, 0, 190), (255, 20, 255))
        level = -1 if objects.player_champion is None else objects.player_champion['level']
        health = None if objects.player_champion is None else objects.player_champion['health']
        damage_taken = self.get_damage_taken(health)
        state = get_game_state(objects, areas)
        utility.analytics.end_timer()
        self.buy_items(areas, is_shop, gold, items)
        base_logic(areas, spells, coor, gold, items)
        use_spells(objects, areas, spells, level)
        use_items(objects, areas, items)
        if areas.is_turret and state.is_enemy_turret and not state.is_shielded:
            evade(areas)
            time.sleep(0.3)
        if state.pressure == 'orb_walk':
            self.champion.attack_champion(objects, areas, abilities, attack_speed)
        if damage_taken is not None and damage_taken < 0 and objects.turret != []:
            evade(areas)
        if objects.enemy_minion_aggro != [] and objects.enemy_champion == []:
            self.champion.kite_minion(objects, areas, abilities, attack_speed)
        if state.pressure == 'evade':
            evade(areas)
        if state.pressure == 'poke':
            self.champion.poke_champion(objects, areas, abilities, attack_speed)
        if state.pressure == 'kite':
            self.champion.kite_champion(objects, areas, abilities, attack_speed)
        if (state.is_enemy_turret and objects.closest_turret is not None and state.is_shielded and
                objects.closest_turret['distance'] < 550):
            self.champion.attack_turret(objects, areas, abilities, attack_speed)
        if (state.is_enemy_turret and objects.closest_turret is not None and state.is_shielded and
                objects.closest_turret['distance'] < 550):
            self.champion.attack_turret(objects, areas, abilities, attack_speed)
        if state.is_enemy_structure:
            self.champion.attack_structure(objects, areas, abilities, attack_speed)
        if objects.closest_enemy_minion:
            self.champion.attack_minion(objects, areas, abilities, attack_speed)
        goto_lane_logic(utility, areas, objects, gtime)
