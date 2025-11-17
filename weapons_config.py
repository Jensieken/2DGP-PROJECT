import os
from weapon import Weapon, WeaponManager

RUN_OFFSET = (-50, 3)

IDLE_OFFSET = (-50, 3)

def create_default_weapon_manager():
    manager = WeaponManager()


    pink_sword = Weapon(
        sheets = {
            'run': ('run_pink.png', 12, RUN_OFFSET, None),
            'idle': ('idle_pink.png', 1, IDLE_OFFSET, None),
        },
        default_state = 'run'
    )

    manager.add_weapon('pink_sword', pink_sword)
    manager.equip('pink_sword')
    return manager