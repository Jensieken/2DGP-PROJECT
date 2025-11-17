import os
from pico2d import load_image

class Weapon:
    def __init__(self, image_filename, frame_count=1, default_offset=(0, 0), per_frame_offsets=None, visible_in=None):
        base_dir = os.path.dirname(__file__)
        path = os.path.join(base_dir, 'girl_image', image_filename)
        try:
            self.image = load_image(path)
        except Exception as e:
            print(f'[Weapon] 이미지 로드 실패: {path} -> {e}')
            self.image = None

        self.frame_count = max(1, int(frame_count))
        self.default_offset = default_offset
        self.per_frame_offsets = per_frame_offsets or {}
        self.visible_in = set(visible_in) if visible_in is not None else None

    def is_visible_in():

    def _compute_frame():

    def draw():


class WeaponManager:

    def __init__(self):
        self.weapons = {}
        self.equipped = None

    def add_weapon(self, name, weapon: Weapon):
        self.weapons[name] = weapon

    def equip(self, name):
        if name in self.weapons:
            self.equipped = name
        else:
            print(f'[WeaponManager] equip 실패: {name} 없음')

    def unequip(self):
        self.equipped = None

    def ger_equiped(self):
        return self.weapons.get(self.equipped)

    def draw(elf, cx, cy, face_dir, char_frame_index=0, char_frame_count=1, state_name=None):
        w = self.get_equipped()
        if not w:
            return
        w.draw(cx, cy, face_dir, char_frame_index=char_frame_index, char_frame_count=char_frame_count,
               state_name=state_name)