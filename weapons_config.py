from weapon import Weapon, WeaponManager

RUN_PER_FRAME_OFFSETS = {
    0: (26, 10),
    1: (28, 9),
    2: (30, 8),
    3: (32, 8),
    4: (34, 7),
    5: (36, 6),
    6: (34, 6),
    7: (32, 7),
    8: (30, 8),
    9: (28, 9),
    10: (26, 10),
    11: (24, 11)
}

def create_default_weapon_manager():
    manager = WeaponManager()


    pink_sword = Weapon(
        sheets = {
            'run': ('run_pink.png', 12, (22, 6), RUN_PER_FRAME_OFFSETS),
        },
        default_state = 'run'
    )

    manager.add_weapon('pink_sword', pink_sword)
    manager.equip('pink_sword')
    return manager