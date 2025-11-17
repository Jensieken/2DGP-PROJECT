import os
import random
from pico2d import load_image, draw_rectangle
import game_framework
import game_world
from state_machine import StateMachine

class ResourceManager:
    _images = {}

    @staticmethod
    def load_image(key, filename):
        if key in ResourceManager._images:
            return ResourceManager._images[key]

        base_dir = os.path.dirname(__file__)
        path = os.path.join(base_dir, 'monster_image', filename)
        if not os.path.exists(path):
            print(f'[Monster] 이미지 파일 없음: {path}')
            ResourceManager._images[key] = None
            return None

        try:
            img = load_image(path)
        except Exception as e:
            print(f'[Monster] 이미지 로드 실패: {path} -> {e}')
            img = None

        ResourceManager._images[key] = img
        return img


class Idle:
    def __init__(self, goblin):
        self.goblin = goblin

    def enter(self, e):
        self.goblin.dir = 0
        self.goblin.frame = 0.0
        # small idle pause before possibly running
        self.wait = random.uniform(0.5, 1.8)
        self.time = 0.0

    def do(self):

        img = self.goblin.get_image('idle')
        frame_count = 1 if not img else 1
        self.goblin.frame = (self.goblin.frame + frame_count * 1.0 * game_framework.frame_time) % max(1, frame_count)

        self.time += game_framework.frame_time
        if self.time >= self.wait:

            if random.random() < 0.6:
                self.goblin.dir = random.choice([-1, 1])
                self.goblin.state_machine.change_state(self.goblin.RUN)
            else:
                self.wait = random.uniform(0.5, 1.8)
                self.time = 0.0

    def exit(self, e):
        pass

    def draw(self):
        img = self.goblin.get_image('idle')
        if not img:
            return
        fw = img.w
        fh = img.h
        frame = 0
        if self.goblin.face_dir == 1:
            img.clip_draw(frame * fw, 0, fw, fh, self.goblin.x, self.goblin.y)
        else:
            img.clip_composite_draw(frame * fw, 0, fw, fh, 0, 'h',
                                    self.goblin.x, self.goblin.y, fw, fh)


class Run:
    def __init__(self, goblin):
        self.goblin = goblin

    def enter(self, e):
        if self.goblin.dir == 0:
            self.goblin.dir = random.choice([-1, 1])
        self.goblin.face_dir = 1 if self.goblin.dir > 0 else -1
        self.goblin.frame = 0.0
        self.run_time = random.uniform(0.6, 2.0)
        self.time = 0.0

    def do(self):
        frame_count = 4
        self.goblin.frame = (self.goblin.frame + frame_count * 2.0 * game_framework.frame_time) % frame_count

        self.goblin.x += self.goblin.dir * self.goblin.speed * game_framework.frame_time
        self.goblin.face_dir = 1 if self.goblin.dir > 0 else -1

        if self.goblin.x < 20:
            self.goblin.x = 20
            self.goblin.dir = 1
        elif self.goblin.x > 1580:
            self.goblin.x = 1580
            self.goblin.dir = -1

        self.time += game_framework.frame_time
        if self.time >= self.run_time:
            self.goblin.state_machine.change_state(self.goblin.IDLE)

    def exit(self, e):
        self.goblin.dir = 0

    def draw(self):
        img = self.goblin.get_image('run')
        if not img:
            return
        frame_count = 4
        fw = max(1, img.w // frame_count)
        fh = img.h
        frame = int(self.goblin.frame) % frame_count
        if self.goblin.face_dir == 1:
            img.clip_draw(frame * fw, 0, fw, fh, self.goblin.x, self.goblin.y)
        else:
            img.clip_composite_draw(frame * fw, 0, fw, fh, 0, 'h',
                                    self.goblin.x, self.goblin.y, fw, fh)


class Goblin:
    def __init__(self, x=400, y=40):

        self.images = {
            'idle': ResourceManager.load_image('idle', 'goblin_idle.png'),
            'run': ResourceManager.load_image('run', 'goblin_run.png'),
        }

        self.x = x
        self.y = y
        self.frame = 0.0
        self.face_dir = -1  # -1 left, 1 right
        self.dir = 0
        self.speed = 100.0  # pixels per second

        self.IDLE = Idle(self)
        self.RUN = Run(self)

        transitions = {
            self.IDLE: {},
            self.RUN: {}
        }
        self.state_machine = StateMachine(self.IDLE, transitions)

        game_world.add_object(self, 2)

    def get_image(self, key):
        return self.images.get(key)

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()

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