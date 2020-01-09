''' Module to filter the objects that are detected '''
import collections

from cutils import distance

from .utils import lfilter

Objects = collections.namedtuple(
    'Objects',
    'ally_minions enemy_minions shield_minions turrets open_structures player_champions '
    'enemy_champions turret_aggros lowest_enemy_champion closest_enemy_champion kill_pressure '
    'enemy_kill_pressure')


def get_kill_pressure(player_champion, enemy_champion, turrets):
    ''' Returns if the enemy championis under kill pressure '''
    return (enemy_champion['health'] < player_champion['health'] + 20 and
            not enemy_champion['is_turret'] and
            enemy_champion['distance'] < 300 and
            len(turrets) <= 0)


def get_enemy_kill_pressure(player_champion, enemy_champion):
    ''' Returns if the enemy championis under kill pressure '''
    return (enemy_champion['health'] > player_champion['health'] + 20 and
            enemy_champion['distance'] < 300)


def filter_objects(objs, areas):
    ''' Filters the objects that are detected '''
    # open_structures = [] if len(turrets) > 0 or areas.is_order_side else lfilter(
    #     lambda o: o['name'] == 'structure', objs)
    
    if len(enemy_champions) > 0:
        enemy_champions.sort(key=lambda o: o['health'])
        lowest_enemy_champion = enemy_champions[0]
        if len(player_champions) > 0:
            for champion in enemy_champions:
                champion['distance'] = distance(champion['center'], player_champions[0]['center'])
            enemy_champions.sort(key=lambda o: o['distance'])
            closest_enemy_champion = enemy_champions[0]
            enemy_kill_pressure = get_enemy_kill_pressure(
                player_champions[0], closest_enemy_champion)
            kill_pressure = get_kill_pressure(player_champions[0], lowest_enemy_champion, turrets)
        else:
            enemy_kill_pressure = None
            kill_pressure = None
            closest_enemy_champion = None
    else:
        lowest_enemy_champion = None
        closest_enemy_champion = None
        enemy_kill_pressure = None
        kill_pressure = None

    return Objects(ally_minions, enemy_minions, shield_minions, turrets, open_structures,
                   player_champions, enemy_champions, turret_aggros, lowest_enemy_champion,
                   closest_enemy_champion, kill_pressure, enemy_kill_pressure)
