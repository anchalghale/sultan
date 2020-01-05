''' Module to detect the variables related to current state of game '''
import collections

State = collections.namedtuple('State', 'is_shielded is_enemy_turret')


def get_game_state(filtered_objs, areas):
    ''' Returns the variables related to current state of game '''
    shield_minions = filtered_objs.get('shield_minions')
    turrets = filtered_objs.get('turrets')
    is_shielded = (len(shield_minions) > 1 or
                   (len(shield_minions) == 1 and shield_minions[0]['health'] >= 50))
    is_enemy_turret = turrets != [] and areas['is_chaos_side']
    return State(is_shielded, is_enemy_turret)
