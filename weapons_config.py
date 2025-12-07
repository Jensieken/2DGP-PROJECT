import os


from weapon import Weapon, WeaponManager

RUN_OFFSET = (-50, 3)

IDLE_OFFSETS = {
    0:  (-50,  4),
    1:  (-49.5,  3.5),
    2:  (-49.5,  3.5),
    3:  (-50,  4),
    4:  (-50.5,  4.5),
    5:  (-51,  5),
    6:  (-51.5,  5.5),
    7:  (-52,  6),
    8:  (-51.5,  5.5),
    9:  (-51,  5),
    10: (-50.5,  4.5),
}

NORMAL_ATTACK_OFFSET = (0, 20)

STAB_OFFSET = (0, 20)

SPINE_OFFSET = (0, 20)


def create_default_weapon_manager():
    manager = WeaponManager()


    pink_sword = Weapon(
        sheets = {
            'run': ('run_pink.png', 12, RUN_OFFSET, None),
            'idle': ('idle_pink.png', 1, (-50, 3), IDLE_OFFSETS),
            'normal_attack': ('normal_attack_pink.png', 7, NORMAL_ATTACK_OFFSET, None),
        },
        default_state = 'run'
    )

    manager.add_weapon('pink_sword', pink_sword)
    manager.equip('pink_sword')
    return manager