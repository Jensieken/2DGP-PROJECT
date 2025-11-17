import os
from weapon import Weapon, WeaponManager

RUN_OFFSET = (-50, 3)

IDLE_OFFSETS = {
    0:  (-50,  3),
    1:  (-51,  2),
    2:  (-52,  1),
    3:  (-51,  0),
    4:  (-50,  0),
    5:  (-49,  1),
    6:  (-48,  2),
    7:  (-47,  3),
    8:  (-48,  4),
    9:  (-49,  4),
    10: (-50,  3),
    11: (-51,  2)
}

def create_default_weapon_manager():
    manager = WeaponManager()


    pink_sword = Weapon(
        sheets = {
            'run': ('run_pink.png', 12, RUN_OFFSET, None),
            'idle': ('idle_pink.png', 1, (-50, 3), IDLE_OFFSETS),
        },
        default_state = 'run'
    )

    manager.add_weapon('pink_sword', pink_sword)
    manager.equip('pink_sword')
    return manager