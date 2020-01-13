''' Logic of ashe '''
from bot import use_ability


from .utils import Champion


def attack_champion(objects, abilities):
    ''' Attacks a enemy champion '''
    if abilities.q:
        use_ability(objects.lowest_enemy_champion, 'q')
    if abilities.w:
        use_ability(objects.lowest_enemy_champion, 'w')
    if abilities.e:
        use_ability(objects.lowest_enemy_champion, 'e')
    if abilities.r:
        use_ability(objects.lowest_enemy_champion, 'r')


def attack_turret(objects, abilities):
    ''' Attacks a enemy turret '''
    if abilities.q:
        use_ability(objects.turret[0], 'q')


def attack_minion(objects, abilities):
    ''' Attacks a enemy minion '''
    if abilities.q:
        use_ability(objects.closest_enemy_minion, 'q')


ASHE = Champion(attack_champion, attack_turret, attack_minion)
