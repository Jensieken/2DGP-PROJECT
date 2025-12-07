import os
from pico2d import load_image
import game_framework
import game_world

try:
    from monster import spawn_attack_hit
except Exception:
    spawn_attack_hit = None

_image_cache = None

def _load_magic_frames():
    global _image_cache
    if _image_cache is not None:
        return _image_cache
    base_dir = os.path.dirname(__file__)
    magic_dir = os.path.join(base_dir, 'magic')
    frames = []
    try:
        names = sorted([n for n in os.listdir(magic_dir) if n.lower().endswith('.png')])
        for n in names:
            path = os.path.join(magic_dir, n)
            try:
                img = load_image(path)
            except Exception:
                img = None
            frames.append(img)
    except Exception:
        frames = []
    _image_cache = frames
    return _image_cache

class MagicEffect:

    def __init__(self, x, y, face_dir=1, damage=None, spawn_hit=True, hit_w=120, hit_h=120):

        hand_offset_x = 200
        hand_offset_y = 25

        self.x = x + face_dir * hand_offset_x
        self.y = y + hand_offset_y
        self.face_dir = face_dir
        self.frames = _load_magic_frames()
        self.frame_index = 0.0

        self.fps = 12.0
        self.playing = True
        self.spawn_hit = spawn_hit
        self.damage = damage
        self.hit_w = hit_w
        self.hit_h = hit_h

        if self.spawn_hit and spawn_attack_hit is not None:
            try:
                spawn_x = self.x - self.face_dir * 20
                spawn_attack_hit(spawn_x, self.y, face_dir=self.face_dir,
                                 damage=self.damage, w=self.hit_w * 2, h=self.hit_h * 2)
            except Exception:
                pass

        game_world.add_object(self, 3)

    def update(self):
        if not self.playing:
            return
        import game_framework
        dt = game_framework.frame_time
        if not self.frames:
            self._kill()
            return
        self.frame_index += self.fps * dt
        if int(self.frame_index) >= len(self.frames):
            self._kill()

    def draw(self):
        if not self.frames:
            return
        idx = int(self.frame_index)
        if idx < 0 or idx >= len(self.frames):
            return
        img = self.frames[idx]
        if not img:
            return
        fw = img.w
        fh = img.h

        dw = fw * 3
        dh = fh * 3

        if self.face_dir == 1:
            img.clip_draw(0, 0, fw, fh, self.x, self.y, dw, dh)
        else:
            img.clip_composite_draw(0, 0, fw, fh, 0, 'h', self.x, self.y, dw, dh)

    def _kill(self):
        try:
            game_world.remove_object(self)
        except Exception:
            pass
        self.playing = False

def spawn_magic_effect(x, y, face_dir=1, damage=None, spawn_hit=True, hit_w=120, hit_h=120):

    try:
        return MagicEffect(x, y, face_dir=face_dir, damage=damage, spawn_hit=spawn_hit, hit_w=hit_w, hit_h=hit_h)
    except Exception:
        return None
