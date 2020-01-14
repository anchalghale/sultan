''' Utility functions '''

import collections

Champion = collections.namedtuple(
    'Champion',
    'attack_champion poke_champion kite_champion attack_turret attack_minion '
    'kite_minion attack_structure ')
