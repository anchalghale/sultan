''' Module to detect the variables related to current state of game '''
import collections

from .utils import Objects


State = collections.namedtuple(
    'State', 'is_shielded is_enemy_turret is_enemy_structure pressure')


def get_pressure(objects: Objects, areas):
    ''' Returns if the enemy championis under kill pressure '''
    if objects.player_champion is None or objects.closest_enemy_champion is None:
        return None
    level = objects.player_champion['level']
    distance = objects.closest_enemy_champion['distance']
    enemy_level = len(objects.enemy_minion) * 2 / level + \
        sum(map(lambda o: o['level'], objects.enemy_champion))
    level_adv = enemy_level < level
    if level_adv and (objects.turret == [] or areas.is_order_side):
        return 'orb_walk'
    if objects.turret != [] and distance < 150:
        return 'evade'
    if objects.turret == [] and distance < 350:
        return 'kite'
    if objects.turret == [] and distance < 450:
        return 'poke'
    return None


def get_game_state(objects: Objects, areas):
    ''' Returns the variables related to current state of game '''
    shield_minions = objects.shield_minion
    turrets = objects.turret
    is_shielded = (len(shield_minions) > 1 or
                   (len(shield_minions) == 1 and shield_minions[0]['health'] >= 50))
    is_enemy_turret = turrets != [] and areas.is_chaos_side
    is_enemy_structure = objects.structure != [] and areas.is_chaos_side
    pressure = get_pressure(objects, areas)

    return State(is_shielded, is_enemy_turret, is_enemy_structure, pressure)
