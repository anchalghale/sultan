''' Module to filter the objects that are detected '''
import collections

Objects = collections.namedtuple('Objects', 'ally_minions enemy_minions shield_minions turrets')


def filter_objects(objs):
    ''' Filters the objects that are detected '''
    def lfilter(function, iterable):
        ''' Filters a list and outputs a list value '''
        return list(filter(function, iterable))
    ally_minions = lfilter(lambda o: o['name'] == 'ally_minion', objs)
    enemy_minions = lfilter(lambda o: o['name'] == 'enemy_minion', objs)
    shield_minions = lfilter(lambda o: o['name'] == 'ally_minion' and o['is_turret'], objs)
    turrets = lfilter(lambda o: o['name'] == 'turret', objs)
    return Objects(ally_minions, enemy_minions, shield_minions, turrets)
