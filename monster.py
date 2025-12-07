import os
import random
from pico2d import load_image, draw_rectangle
import game_framework
import game_world
from state_machine import StateMachine

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm

RUN_SPEED_KMPH = 80.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10.0

class ResourceManager:
    _images = {}\

    def load_image(key, filename):
        if key in ResourceManager._images:
            return ResourceManager._images[key]

        base_dir = os.path.dirname(__file__)
        path = os.path.join(base_dir, 'monster_image', filename)
        if not os.path.exists(path):
            print(f'이미지 파일이 없습니다: {path}')
            ResourceManager._images[key] = None
            return None

        try:
            img = load_image(path)
        except Exception as e:
            print(f'이미지 로드 실패: {path} -> {e}')
            img = None

        ResourceManager._images[key] = img
        return img

class Goblin:
    images = None

    class Idle:
        IMAGE_KEY = 'idle'
        def __init__(self, goblin):
            self.goblin = goblin
            self.timer = 0.0
            self.duration = random.uniform(0.8, 2.5)
        def enter(self, e):
            self.goblin.dir = 0
            self.goblin.frame = 0.0
            self.timer = 0.0
            self.duration = random.uniform(0.8, 2.5)
        def exit(self, e):
            pass
        def do(self):
            import game_framework
            frame_count = 1
            self.goblin.frame = (self.goblin.frame + frame_count * ACTION_PER_TIME * game_framework.frame_time) % frame_count
            self.timer += game_framework.frame_time
            if self.timer >= self.duration:
                self.goblin.state_machine.change_state(self.goblin.RUN)
        def draw(self):
            img = self.goblin.get_image(self.IMAGE_KEY)
            if not img: return
            frame_count = 1
            fw = img.w // frame_count
            fh = img.h
            frame = int(self.goblin.frame) % frame_count
            if self.goblin.face_dir == 1:
                img.clip_draw(frame * fw, 0, fw, fh, self.goblin.x, self.goblin.y)
            else:
                img.clip_composite_draw(frame * fw, 0, fw, fh, 0, 'h', self.goblin.x, self.goblin.y, fw, fh)

    class Run:
        IMAGE_KEY = 'run'
        def __init__(self, goblin):
            self.goblin = goblin
            self.timer = 0.0
        def enter(self, e):
            self.goblin.frame = 0.0
            self.timer = 0.0
            self.goblin.dir = random.choice([-1, 1])
            self.goblin.face_dir = self.goblin.dir
        def exit(self, e):
            pass
        def do(self):
            import game_framework
            frame_count = 4
            self.goblin.frame = (self.goblin.frame + frame_count * ACTION_PER_TIME * game_framework.frame_time) % frame_count
            self.goblin.x += self.goblin.dir * self.goblin.speed * game_framework.frame_time
            if self.goblin.x < 20:
                self.goblin.x = 20; self.goblin.dir = 1; self.goblin.face_dir = 1
            elif self.goblin.x > 1580:
                self.goblin.x = 1580; self.goblin.dir = -1; self.goblin.face_dir = -1
            self.timer += game_framework.frame_time
            if self.timer >= random.uniform(1.0, 3.0):
                if random.random() < 0.25:
                    self.goblin.state_machine.change_state(self.goblin.ATTACK)
                else:
                    self.goblin.state_machine.change_state(self.goblin.IDLE)
        def draw(self):
            img = self.goblin.get_image(self.IMAGE_KEY)
            if not img: return
            frame_count = 4
            fw = img.w // frame_count
            fh = img.h
            frame = int(self.goblin.frame) % frame_count
            if self.goblin.face_dir == 1:
                img.clip_draw(frame * fw, 0, fw, fh, self.goblin.x, self.goblin.y)
            else:
                img.clip_composite_draw(frame * fw, 0, fw, fh, 0, 'h', self.goblin.x, self.goblin.y, fw, fh)

    class Attack:
        IMAGE_KEY = 'attack'
        def __init__(self, goblin):
            self.goblin = goblin
            self.playing = False
        def enter(self, e):
            self.goblin.frame = 0.0
            self.playing = True
        def exit(self, e):
            self.playing = False
        def do(self):
            import game_framework
            frame_count = 3
            if not self.playing: return
            self.goblin.frame += frame_count * ACTION_PER_TIME * game_framework.frame_time
            if self.goblin.frame >= frame_count:
                self.goblin.frame = frame_count - 1
                self.playing = False
                self.goblin.state_machine.change_state(self.goblin.IDLE)
        def draw(self):
            img = self.goblin.get_image(self.IMAGE_KEY)
            if not img: return
            frame_count = 3
            fw = img.w // frame_count
            fh = img.h
            frame = int(min(self.goblin.frame, frame_count - 1))
            if self.goblin.face_dir == 1:
                img.clip_draw(frame * fw, 0, fw, fh, self.goblin.x, self.goblin.y)
            else:
                img.clip_composite_draw(frame * fw, 0, fw, fh, 0, 'h', self.goblin.x, self.goblin.y, fw, fh)

    class Hit:
        IMAGE_KEY = 'hit'
        def __init__(self, goblin):
            self.goblin = goblin
            self.playing = False
            self.timer = 0.0
        def enter(self, e):
            self.goblin.frame = 0.0
            self.playing = True
            self.timer = 0.0
            knockback = 40
            self.goblin.x += -self.goblin.face_dir * knockback
            self.goblin.hp = max(0, getattr(self.goblin, 'hp', 30) - 10)
        def exit(self, e):
            self.playing = False
        def do(self):
            import game_framework
            frame_count = 2
            if not self.playing: return
            self.goblin.frame += frame_count * ACTION_PER_TIME * game_framework.frame_time
            self.timer += game_framework.frame_time
            if self.timer >= 0.4 or self.goblin.frame >= frame_count:
                self.playing = False
                self.goblin.state_machine.change_state(self.goblin.IDLE)
        def draw(self):
            img = self.goblin.get_image(self.IMAGE_KEY)
            if not img: return
            frame_count = 2
            fw = img.w // frame_count
            fh = img.h
            frame = int(min(self.goblin.frame, frame_count - 1))
            if self.goblin.face_dir == 1:
                img.clip_draw(frame * fw, 0, fw, fh, self.goblin.x, self.goblin.y)
            else:
                img.clip_composite_draw(frame * fw, 0, fw, fh, 0, 'h', self.goblin.x, self.goblin.y, fw, fh)


    def __init__(self, x=400, y=40):

        self.images = {
            'idle': ResourceManager.load_image('idle', 'goblin_idle.png'),
            'run': ResourceManager.load_image('run', 'goblin_run.png'),
            'attack': ResourceManager.load_image('attack', 'goblin_attack.png'),
            'hit': ResourceManager.load_image('hit', 'goblin_hit.png'),
        }

        self.x = x
        self.y = y
        self.frame = 0.0
        self.face_dir = -1  # -1 left, 1 right
        self.dir = 0
        self.speed = 100.0  # pixels per second

        self.IDLE = self.__class__.Idle(self)
        self.RUN = self.__class__.Run(self)
        self.ATTACK = self.__class__.Attack(self)
        self.HIT = self.__class__.Hit(self)

        transitions = {
            self.IDLE: {},
            self.RUN: {},
            self.ATTACK: {},
            self.HIT: {}
        }
        self.state_machine = StateMachine(self.IDLE, transitions)

        game_world.add_object(self, 2)

    def get_image(self, key):
        return self.images.get(key)

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()

    def handle_collision(self, group, other):
        try:
            if group == 'weapon_vs_monster':
                self.state_machine.change_state(self.HIT)
        except Exception:
            pass

class MonsterSpawner:
    def __init__(self, count=4, x_range=(200, 1400), y_fixed=40):
        self.count = count
        self.x_range = x_range
        self.y_fixed = y_fixed

        self.spawn_initial()

    def spawn_initial(self):
        for _ in range(self.count):
            x = random.randint(self.x_range[0], self.x_range[1])
            create_goblin(x, self.y_fixed)


def create_goblin(x, y):
    return Goblin(x, y)