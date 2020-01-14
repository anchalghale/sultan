''' Logic of ashe '''
import time

from bot import use_ability
from lvision import Objects

from .utils import Champion


def attack_champion(objects: Objects, abilities):
    ''' Attacks a enemy champion '''
    if abilities.q:
        use_ability(objects.closest_enemy_champion, 'q')
    if abilities.w:
        use_ability(objects.closest_enemy_champion, 'w')
    if abilities.e:
        use_ability(objects.closest_enemy_champion, 'e')
    if abilities.r:
        use_ability(objects.closest_enemy_champion, 'e')
        use_ability(objects.closest_enemy_champion, 'r')
        time.sleep(5)


def evade_champion(objects: Objects, abilities):
    ''' Evades a enemy champion '''
    if abilities.e:
        use_ability(objects.closest_enemy_champion, 'e')


def attack_turret(objects: Objects, abilities):
    ''' Attacks a enemy turret '''
    if abilities.w:
        use_ability(objects.turret[0], 'w')


def attack_minion(objects: Objects, abilities):
    ''' Attacks a enemy minion '''
    if abilities.w:
        use_ability(objects.closest_enemy_minion, 'w')


MISS_FORTUNE = Champion(attack_champion, attack_turret, attack_minion)
