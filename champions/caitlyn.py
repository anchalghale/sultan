''' Logic of ashe '''
from bot import use_ability
from lvision import Objects

from .utils import Champion


def attack_champion(objects: Objects, abilities):
    ''' Attacks a enemy champion '''
    if abilities.q:
        use_ability(objects.closest_enemy_champion, 'q')
    if abilities.w:
        use_ability(objects.closest_enemy_champion, 'w')
    if abilities.r:
        use_ability(objects.closest_enemy_champion, 'r')


def evade_champion(objects: Objects, abilities):
    ''' Evades a enemy champion '''
    if abilities.e:
        use_ability(objects.closest_enemy_champion, 'e')
    if abilities.w:
        use_ability(objects.player_champion, 'w')


def attack_turret(*_):
    ''' Attacks a enemy turret '''


def attack_minion(objects: Objects, abilities):
    ''' Attacks a enemy minion '''
    if abilities.q:
        use_ability(objects.closest_enemy_minion, 'q')


CAITLYN = Champion(attack_champion, attack_turret, attack_minion)
