import os
from weapon import Weapon, WeaponManager

DEFAULT_RUN_OFFSET = (-50, 3)

def create_default_weapon_manager():
    manager = WeaponManager()


    pink_sword = Weapon(
        sheets = {
            'run': ('run_pink.png', 12, DEFAULT_RUN_OFFSET, None),
        },
        default_state = 'run'
    )

    manager.add_weapon('pink_sword', pink_sword)
    manager.equip('pink_sword')
    return manager