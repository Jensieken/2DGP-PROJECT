import os
from pico2d import load_image

_image_cache = {}

def _load_weapon_image(filename):
    if filename in _image_cache:
        return _image_cache[filename]

    base_dir = os.path.dirname(__file__)
    path = os.path.join(base_dir, 'weapon_image', filename)

    print(f'[Weapon DEBUG] 시도 경로: {path}')
    print(f'[Weapon DEBUG] 존재 여부: {os.path.exists(path)}')

    try:
        img = load_image(path)
    except Exception as e:
        print(f'[Weapon] 이미지 로드 실패: {path} -> {e}')
        img = None

    _image_cache[filename] = img
    return img

class Weapon:
    def __init__(self, sheets: dict, default_state: str):
        self.sheets = {}
        self.default_state = default_state

        for state, sheet in sheets.items():
            filename = sheet[0]
            frame_count = sheet[1] if len(sheet) > 1 else 1
            default_offset = sheet[2] if len(sheet) > 2 else (0, 0)
            per_frame_offsets = sheet[3] if len(sheet) > 3 else None

            img = _load_weapon_image(filename)

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

    def _compute_frame(self, char_frame_index, char_frame_count, weapon_frame_count):
        if weapon_frame_count == char_frame_count:
            return int(char_frame_index) % weapon_frame_count
        ratio = (int(char_frame_index) % max(1, char_frame_count)) / max(1, char_frame_count)
        return int(ratio * weapon_frame_count) % weapon_frame_count

    def draw(self, cx, cy, face_dir, char_frame_index=0, char_frame_count=1, state_name=None):
        sheet = self._choose_sheet(state_name)
        if not sheet:
            return

        img = sheet.get('image')
        if not img:
            return

        fi = self._compute_frame(char_frame_index, char_frame_count, sheet['frame_count'])
        fw = max(1, img.w // sheet['frame_count'])
        fh = img.h
        ox, oy = sheet['per_frame_offsets'].get(fi, sheet['default_offset'])

        if face_dir == 1:
            draw_x = cx + ox
            draw_y = cy + oy
            img.clip_draw(fi * fw, 0, fw, fh, draw_x, draw_y)
        else:
            draw_x = cx - ox
            draw_y = cy + oy
            img.clip_composite_draw(fi * fw, 0, fw, fh, 0, 'h', draw_x, draw_y, fw, fh)

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

    def get_equipped(self):
        return self.weapons.get(self.equipped)

    def draw(self, cx, cy, face_dir, char_frame_index=0, char_frame_count=1, state_name=None):
        w = self.get_equipped()
        if not w:
            return
        w.draw(cx, cy, face_dir, char_frame_index=char_frame_index, char_frame_count=char_frame_count,
               state_name=state_name)