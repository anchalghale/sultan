''' Module to detect the variables related to current state of game '''
import collections

from .utils import lfilter, Objects


State = collections.namedtuple(
    'State',
    'is_shielded is_enemy_turret is_enemy_nexus_turret enemy_minions_dps enemy_champions_dps '
    'player_champions_dps potential_enemy_minions_dps kill_pressure enemy_kill_pressure')


def get_kill_pressure(objects: Objects):
    ''' Returns if the enemy championis under kill pressure '''
    if objects.lowest_enemy_champion is None or objects.player_champion is None:
        return None
    enemy_hp = objects.lowest_enemy_champion['health'] * objects.lowest_enemy_champion['level']
    player_hp = (objects.player_champion['health'] - 40) * objects.player_champion['level']
    return (enemy_hp < player_hp and
            not objects.lowest_enemy_champion['is_turret'] and
            objects.lowest_enemy_champion['distance'] < 300 and
            objects.turret == [])


def get_enemy_kill_pressure(objects: Objects):
    ''' Returns if the enemy championis under kill pressure '''
    if objects.closest_enemy_champion is None or objects.player_champion is None:
        return None
    enemy_hp = (objects.closest_enemy_champion[
        'health'] - 20) * objects.closest_enemy_champion['level']
    player_hp = objects.player_champion['health'] * objects.player_champion['level']
    return (enemy_hp > player_hp and
            objects.closest_enemy_champion['distance'] < 300)


def get_game_state(objects: Objects, areas):
    ''' Returns the variables related to current state of game '''
    shield_minions = objects.shield_minion
    turrets = objects.turret
    is_shielded = (len(shield_minions) > 1 or
                   (len(shield_minions) == 1 and shield_minions[0]['health'] >= 50))
    is_enemy_turret = turrets != [] and areas.is_chaos_side
    is_enemy_nexus_turret = len(turrets) == 2 and areas.is_chaos_side
    single_enemy_minion_dps = 0 if objects.player_champion is None else 20 - \
        objects.player_champion['level']
    potential_enemy_minions_dps = len(objects.enemy_minion) * single_enemy_minion_dps
    enemy_minions_dps = len(
        lfilter(lambda m: m['aggro'], objects.enemy_minion)) * single_enemy_minion_dps
    enemy_champions_dps = sum([20 + c['level'] * 10 for c in objects.enemy_champion])
    player_champions_dps = 0 if objects.player_champion is None else 50 + \
        objects.player_champion['level'] * 10
    kill_pressure = get_kill_pressure(objects)
    enemy_kill_pressure = get_enemy_kill_pressure(objects)
    return State(is_shielded, is_enemy_turret, is_enemy_nexus_turret, enemy_minions_dps,
                 enemy_champions_dps, player_champions_dps, potential_enemy_minions_dps,
                 kill_pressure, enemy_kill_pressure)
