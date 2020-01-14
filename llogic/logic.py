''' Logic module of the bot '''
import time

import keyboard
import mouse

import champions

from lvision.state import get_game_state
from lvision import (
    is_camera_locked, get_level_ups, get_ability_points, get_is_shop, get_game_time,
    get_abilities, get_attack_speed, get_gold, get_summoner_items,
    get_minimap_coor, get_minimap_areas, get_objects, get_summoner_spells)
from bot import (
    goto_lane, evade, move_forward, level_up, kite_minion, use_spells, use_items,
    poke, kite, orb_walk, buy_item, base)
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


def base_logic(areas, coor, gold, items):
    ''' Basing logic '''
    if gold >= 3500 and items.count(None) >= 1 and not areas.is_base:
        base(coor)
        raise BotContinueException


class Logic:
    ''' Logic class of the bot '''

    def __init__(self):
        self.command = None
        self.last_health = None
        self.champion = champions.Caitlyn

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
            self.command = 'buy_items'
        buyable = min(list(map(lambda i: i['name'], items)).count(None), gold//3500)
        if buyable > 0 and areas.is_platform:
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
                raise BotContinueException
            for _ in range(buyable):
                buy_item('bt')
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
        base_logic(areas, coor, gold, items)
        use_spells(objects, areas, spells, level)
        use_items(objects, areas, items)

        if areas.is_turret and state.is_enemy_turret and not state.is_shielded:
            evade(utility.cooldown, areas)
        if len(objects.turret_aggro) > 0:
            evade(utility.cooldown, areas)
        if state.kill_pressure:
            self.champion.attack_champion(objects, abilities)
            orb_walk(areas, objects.lowest_enemy_champion, attack_speed)
        if damage_taken is not None and damage_taken < 0 and objects.turret != []:
            evade(utility.cooldown, areas)
        if state.enemy_minions_dps >= 10 and len(objects.enemy_champion) == 0:
            if objects.closest_enemy_minion:
                kite_minion(areas, objects.closest_enemy_minion, attack_speed)
            else:
                evade(utility.cooldown, areas)
        if state.enemy_minions_dps + state.enemy_champions_dps > state.player_champions_dps:
            evade(utility.cooldown, areas)
        if objects.enemy_champion != [] and objects.closest_enemy_champion['distance'] < 300:
            if state.enemy_kill_pressure:
                kite(areas, objects.closest_enemy_champion, attack_speed)
            if state.is_pokeable:
                poke(areas, objects.closest_enemy_champion, attack_speed)
        if state.is_enemy_turret and state.is_shielded:
            self.champion.attack_turret(objects, abilities)
            mouse.move(*objects.turret[0]['center'])
            mouse.click()
            raise BotContinueException
        if objects.closest_enemy_minion and areas.is_chaos_side:
            self.champion.attack_minion(objects, abilities)
            mouse.move(*objects.closest_enemy_minion['center'])
            mouse.click()
            raise BotContinueException
        goto_lane_logic(utility, areas, objects, gtime)
