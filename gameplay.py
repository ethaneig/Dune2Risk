import random

TURNS = [1,2,3,4]


def turn_cycle(current):
    if current == 4:
        return 1
    else:
        return current + 1

def attack_victory(attacker:Country, defender:Country):
    if attacker.num_troops() > defender.num_troops():
        if random.uniform(0,1) > 0.5 + (attacker.num_troops() - defender.num_troops() * 0.05):
            return True
    return False







