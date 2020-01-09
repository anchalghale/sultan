''' Module to detect the variables related to current state of game '''
import collections

from .utils import lfilter


State = collections.namedtuple(
    'State',
    'is_shielded is_enemy_turret is_enemy_nexus_turret enemy_minions_dps enemy_champions_dps '
    'player_champions_dps potential_enemy_minions_dps')


def get_game_state(fobjects, areas):
    ''' Returns the variables related to current state of game '''
    shield_minions = fobjects.shield_minions
    turrets = fobjects.turrets
    is_shielded = (len(shield_minions) > 1 or
                   (len(shield_minions) == 1 and shield_minions[0]['health'] >= 50))
    is_enemy_turret = turrets != [] and areas.is_chaos_side
    is_enemy_nexus_turret = len(turrets) == 2 and areas.is_chaos_side
    potential_enemy_minions_dps = len(fobjects.enemy_minions) * 20
    enemy_minions_dps = len(lfilter(lambda m: m['aggro'], fobjects.enemy_minions)) * 20
    enemy_champions_dps = len(fobjects.enemy_champions) * 20
    player_champions_dps = 50
    return State(is_shielded, is_enemy_turret, is_enemy_nexus_turret, enemy_minions_dps,
                 enemy_champions_dps, player_champions_dps, potential_enemy_minions_dps)
