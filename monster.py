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

    def handle_collision(self, group, other):
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