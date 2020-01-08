''' Module to filter the objects that are detected '''
import collections

from .utils import lfilter

Objects = collections.namedtuple(
    'Objects',
    'ally_minions enemy_minions shield_minions turrets open_structures player_champions '
    'enemy_champions turret_aggros')


def filter_objects(objs, areas):
    ''' Filters the objects that are detected '''

    ally_minions = lfilter(lambda o: o['name'] == 'ally_minion', objs)
    enemy_minions = lfilter(lambda o: o['name'] == 'enemy_minion', objs)
    shield_minions = lfilter(lambda o: o['name'] == 'ally_minion' and o['is_turret'], objs)
    turrets = lfilter(lambda o: o['name'] == 'turret', objs)
    open_structures = [] if len(turrets) > 0 or areas.is_order_side else lfilter(
        lambda o: o['name'] == 'structure', objs)
    player_champions = lfilter(lambda o: o['name'] == 'player_champion', objs)
    enemy_champions = lfilter(lambda o: o['name'] == 'enemy_champion', objs)
    turret_aggros = lfilter(lambda o: o['name'] == 'turret_aggro', objs)
    return Objects(ally_minions, enemy_minions, shield_minions, turrets, open_structures,
                   player_champions, enemy_champions, turret_aggros)
