''' Logic of ashe '''
from bot import (use_ability, orb_walk, kite, poke, attack,
                 kite_minion, orb_walk_minion, BotContinueException)
from lvision import Objects

from .utils import Champion


def orb_walk_champion_cb(objects: Objects, areas, abilities, attack_speed):
    ''' Attacks a enemy champion '''
    orb_walk(areas, objects.closest_enemy_champion, attack_speed)
    use_ability(objects.closest_enemy_champion, abilities, 'q')
    use_ability(objects.closest_enemy_champion, abilities, 'w')
    use_ability(objects.closest_enemy_champion, abilities, 'e')
    raise BotContinueException(tick_interval=(0, 0))


def kite_champion_cb(objects: Objects, areas, abilities, attack_speed):
    ''' Evades a enemy champion '''
    kite(areas, objects.closest_enemy_champion, attack_speed)
    use_ability(objects.closest_enemy_champion, abilities, 'q')
    use_ability(objects.closest_enemy_champion, abilities, 'w')
    use_ability(objects.closest_enemy_champion, abilities, 'e')
    use_ability(objects.closest_enemy_champion, abilities, 'r')
    raise BotContinueException(tick_interval=(0, 0))


def poke_champion_cb(objects: Objects, areas, abilities, attack_speed):
    ''' Evades a enemy champion '''
    poke(areas, objects.closest_enemy_champion, attack_speed)
    use_ability(objects.closest_enemy_champion, abilities, 'w')
    raise BotContinueException(tick_interval=(0, 0))


def attack_turret_cb(objects: Objects, areas, abilities, attack_speed):
    ''' Attacks a enemy turret '''
    use_ability(objects.closest_turret, abilities, 'q')
    attack(objects.closest_turret, attack_speed)


def attack_structure_cb(objects: Objects, areas, abilities, attack_speed):
    ''' Attacks a enemy turret '''
    use_ability(objects.structure[0], abilities, 'q')
    attack(objects.structure[0], attack_speed)


def attack_minion_cb(objects: Objects, areas, abilities, attack_speed):
    ''' Attacks a enemy minion '''
    use_ability(objects.closest_enemy_minion, abilities, 'q')
    attack(objects.closest_enemy_minion, attack_speed)


def kite_minion_cb(objects: Objects, areas, abilities, attack_speed):
    ''' Attacks a enemy minion '''
    kite_minion(areas, objects.closest_enemy_minion, attack_speed)
    use_ability(objects.closest_enemy_minion, abilities, 'q')
    raise BotContinueException(tick_interval=(0, 0))


def orb_walk_minion_cb(objects: Objects, areas, abilities, attack_speed):
    ''' Attacks a enemy champion '''
    orb_walk_minion(areas, objects.closest_enemy_minion, attack_speed)
    use_ability(objects.closest_enemy_minion, abilities, 'q')
    raise BotContinueException(tick_interval=(0, 0))


CHAMPION = Champion(orb_walk_champion_cb, poke_champion_cb, kite_champion_cb, attack_turret_cb,
                    attack_minion_cb, kite_minion_cb, orb_walk_minion_cb, attack_structure_cb,
                    ['r', 'q', 'w', 'e'])
