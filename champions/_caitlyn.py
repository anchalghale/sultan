''' Logic of ashe '''
from bot import use_ability, orb_walk, kite, poke, attack, kite_minion, BotContinueException
from lvision import Objects

from .utils import Champion


def attack_champion_cb(objects: Objects, areas, abilities, attack_speed):
    ''' Attacks a enemy champion '''
    tick_interval = orb_walk(areas, objects.closest_enemy_champion, attack_speed)
    use_ability(objects.closest_enemy_champion, abilities, 'q')
    if objects.closest_enemy_champion['distance'] >= 450:
        use_ability(objects.closest_enemy_champion, abilities, 'r')
    raise BotContinueException(tick_interval=(tick_interval, tick_interval))


def kite_champion_cb(objects: Objects, areas, abilities, attack_speed):
    ''' Evades a enemy champion '''
    tick_interval = kite(areas, objects.closest_enemy_champion, attack_speed)
    raise BotContinueException(tick_interval=(tick_interval, tick_interval))


def poke_champion_cb(objects: Objects, areas, abilities, attack_speed):
    ''' Evades a enemy champion '''
    tick_interval = poke(areas, objects.closest_enemy_champion, attack_speed)
    use_ability(objects.closest_enemy_champion, abilities, 'q')
    use_ability(objects.closest_enemy_champion, abilities, 'w')
    raise BotContinueException(tick_interval=(tick_interval, tick_interval))


def attack_turret_cb(objects: Objects, areas, abilities, attack_speed):
    ''' Attacks a enemy turret '''
    attack(objects.closest_turret, attack_speed)


def attack_structure_cb(objects: Objects, areas, abilities, attack_speed):
    ''' Attacks a enemy turret '''
    attack(objects.structure[0], attack_speed)


def attack_minion_cb(objects: Objects, areas, abilities, attack_speed):
    ''' Attacks a enemy minion '''
    use_ability(objects.closest_enemy_minion, abilities, 'q')
    attack(objects.closest_enemy_minion, attack_speed)


def kite_minion_cb(objects: Objects, areas, abilities, attack_speed):
    ''' Attacks a enemy minion '''
    tick_interval = kite_minion(areas, objects.closest_enemy_minion, attack_speed)
    use_ability(objects.closest_enemy_minion, abilities, 'q')
    raise BotContinueException(tick_interval=(tick_interval, tick_interval))


CHAMPION = Champion(attack_champion_cb, poke_champion_cb, kite_champion_cb, attack_turret_cb,
                    attack_minion_cb, kite_minion_cb, attack_structure_cb)
