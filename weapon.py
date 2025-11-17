import os
from pico2d import load_image

class Weapon:
    def __init__(self, sheets: dict, default_state: str):
        self.sheets = {}
        self.default_state = default_state

        base_dir = os.path.dirname(__file__)
        for state, sheet in sheets.items():
            filename, frame_count, default_offset, per_frame_offsets = sheet
            path = os.path.join(base_dir, 'girl_image', filename)
            try:
                img = load_image(path)
            except Exception as e:
                print(f'[Weapon] 이미지 로드 실패: {path} -> {e}')
                img = None
            self.sheets[state] = {
                'image': img,
                'frame_count': max(1, int(frame_count)),
                'default_offset': default_offset or (0, 0),
                'per_frame_offsets': per_frame_offsets or {}
            }

    def _choose_sheet(self, state_name):
        if state_name and state_name in self.sheets:
            return self.sheets[state_name]
        return self.sheets.get(self.default_state)

    def _compute_frame(self, char_frame_index, char_frame_count):
        if self.frame_count == char_frame_count:
            return int(char_frame_index) % self.frame_count
        ratio = (int(char_frame_index) % max(1, char_frame_count)) / max(1, char_frame_count)
        return int(ratio * self.frame_count) % self.frame_count

    def draw(self, cx, cy, face_dir, char_frame_index=0, char_frame_count=1, state_name=None):
        if not self.image:
            return

        if not self.is_visible_in(state_name):
            return

        fi = self._compute_frame(char_frame_index, char_frame_count)
        fw = max(1, self.image.w // self.frame_count)
        fh = self.image.h

        ox, oy = self.per_frame_offsets.get(fi, self.default_offset)

        if face_dir == 1:
            draw_x = cx + ox
            draw_y = cy + oy
            self.image.clip_draw(fi * fw, 0, fw, fh, draw_x, draw_y)
        else:
            draw_x = cx - ox
            draw_y = cy + oy
            self.image.clip_composite_draw(fi * fw, 0, fw, fh, 0, 'h', draw_x, draw_y, fw, fh)

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