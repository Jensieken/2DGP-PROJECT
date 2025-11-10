import os
from pico2d import load_image, get_time, load_font, draw_rectangle, close_canvas
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_q

import game_world
import game_framework

from state_machine import StateMachine

last_right_down_time = 0
last_left_down_time = 0
DOUBLE_TAP_TIME = 0.3


def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

def q_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_q

def q_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_q

def right_double_tap(e):
    global last_right_down_time
    if e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT:
        current_time = get_time()
        if current_time - last_right_down_time < DOUBLE_TAP_TIME:
            last_right_down_time = 0
            return True
        last_right_down_time = current_time
    return False

def left_double_tap(e):
    global last_left_down_time
    if e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT:
        current_time = get_time()
        if current_time - last_left_down_time < DOUBLE_TAP_TIME:
            last_left_down_time = 0
            return True
        last_left_down_time = current_time
    return False

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
WALK_SPEED_KMPH = 40.0  # Km / Hour
WALK_SPEED_MPM = (WALK_SPEED_KMPH * 1000.0 / 60.0)
WALK_SPEED_MPS = (WALK_SPEED_MPM / 60.0)
WALK_SPEED_PPS = (WALK_SPEED_MPS * PIXEL_PER_METER)

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 80.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION

class ResourceManager:
    _images = {}\

    def load_image(key, filename):
        if key in ResourceManager._images:
            return ResourceManager._images[key]

        base_dir = os.path.dirname(__file__)
        path = os.path.join(base_dir, 'girl_image', filename)
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

class Idle:
    IMAGE_KEY = 'idle'

    def __init__(self, girl):
        self.girl = girl

    def enter(self, e):
        self.girl.dir = 0
        self.girl.frame = 0.0

    def do(self):
        frame_count = 12
        self.girl.frame = (self.girl.frame + frame_count * ACTION_PER_TIME * game_framework.frame_time) % frame_count

    def exit(self, e):
        pass

    def draw(self):
        key = self.IMAGE_KEY
        img = self.girl.get_image(key)
        if not img:
            return

        frame_count = 12
        frame_w = img.w // frame_count
        frame_h = img.h

        frame = int(self.girl.frame) % frame_count

        if self.girl.face_dir == 1:
            img.clip_draw(frame * frame_w, 0, frame_w, frame_h, self.girl.x, self.girl.y)
        else:
            img.clip_composite_draw(frame * frame_w, 0, frame_w, frame_h, 0, 'h', self.girl.x, self.girl.y, frame_w, frame_h)



class Walk:
    IMAGE_KEY = 'walk'

    def __init__(self, girl):
        self.girl = girl

    def enter(self, e):
        if right_down(e) or left_up(e):
            self.girl.dir = self.girl.face_dir = 1
        elif left_down(e) or right_up(e):
            self.girl.dir = self.girl.face_dir = -1
        self.girl.frame = 0.0

    def exit(self, e):
        pass

    def do(self):
        frame_count = 8
        self.girl.frame = (self.girl.frame + frame_count * ACTION_PER_TIME * game_framework.frame_time) % frame_count
        self.girl.x += self.girl.dir * WALK_SPEED_PPS * game_framework.frame_time

    def draw(self):
        key = self.IMAGE_KEY
        img = self.girl.get_image(key)
        if not img:
            return

        frame_count = 8
        frame_w = img.w // frame_count
        frame_h = img.h

        frame = int(self.girl.frame) % frame_count

        if self.girl.face_dir == 1:
            img.clip_draw(frame * frame_w, 0, frame_w, frame_h, self.girl.x, self.girl.y)
        else:
            img.clip_composite_draw(frame * frame_w, 0, frame_w, frame_h, 0, 'h', self.girl.x, self.girl.y, frame_w, frame_h)

class Run:
    IMAGE_KEY = 'run'

    def __init__(self, girl):
        self.girl = girl

    def enter(self, e):
        if right_double_tap(e) or right_down(e):
            self.girl.dir = self.girl.face_dir = 1
        elif left_double_tap(e) or left_down(e):
            self.girl.dir = self.girl.face_dir = -1
        self.girl.frame = 0.0

    def exit(self, e):
        pass

    def do(self):
        frame_count = 12
        self.girl.frame = (self.girl.frame + frame_count * ACTION_PER_TIME * game_framework.frame_time) % frame_count
        self.girl.x += self.girl.dir * RUN_SPEED_PPS * game_framework.frame_time

    def draw(self):
        key = self.IMAGE_KEY
        img = self.girl.get_image(key)
        if not img:
            return

        frame_count = 12
        frame_w = img.w // frame_count
        frame_h = img.h

        frame = int(self.girl.frame) % frame_count

        if self.girl.face_dir == 1:
            img.clip_draw(frame * frame_w, 0, frame_w, frame_h, self.girl.x, self.girl.y)
        else:
            img.clip_composite_draw(frame * frame_w, 0, frame_w, frame_h, 0, 'h', self.girl.x, self.girl.y, frame_w,
                                    frame_h)
class Jump:

    def __init__(self, girl):
        self.girl = girl

    def enter(self, e):
        pass

    def exit(self):
        pass

    def do(self):
        pass

    def draw(self):
        pass
class Fall:

    def __init__(self, girl):
        self.girl = girl

    def enter(self, e):
        pass

    def exit(self):
        pass

    def do(self):
        pass

    def draw(self):
        pass
class Skill_1:
    IMAGE_KEY = 'skill1'

    def __init__(self, girl):
        self.girl = girl
        self.timer = 0.0

    def enter(self, e):
        if q_down(e):
            self.girl.dir = self.girl.face_dir = 1
        self.girl.frame = 0.0
        self.timer = 0.0

    def exit(self, e):
        pass

    def do(self):
        frame_count = 7
        self.girl.frame = (self.girl.frame + frame_count * ACTION_PER_TIME * game_framework.frame_time) % frame_count
        self.timer += game_framework.frame_time

        if self.girl.frame >= frame_count:
            self.girl.state_machine.change_state(self.girl.IDLE)

    def draw(self):
        key = self.IMAGE_KEY
        img = self.girl.get_image(key)
        if not img:
            return

        frame_count = 7
        frame_w = img.w // frame_count
        frame_h = img.h

        frame = int(self.girl.frame) % frame_count

        if self.girl.face_dir == 1:
            img.clip_draw(frame * frame_w, 0, frame_w, frame_h, self.girl.x, self.girl.y)
        else:
            img.clip_composite_draw(frame * frame_w, 0, frame_w, frame_h, 0, 'h', self.girl.x, self.girl.y, frame_w,
                                    frame_h)
class Skill_2:

    def __init__(self, girl):
        self.girl = girl

    def enter(self, e):
        pass

    def exit(self):
        pass

    def do(self):
        pass

    def draw(self):
        pass
class Skill_3:

    def __init__(self, girl):
        self.girl = girl

    def enter(self, e):
        pass

    def exit(self):
        pass

    def do(self):
        pass

    def draw(self):
        pass
class Skill_4:

    def __init__(self, girl):
        self.girl = girl

    def enter(self, e):
        pass

    def exit(self):
        pass

    def do(self):
        pass

    def draw(self):
        pass
class Skill_5:

    def __init__(self, girl):
        self.girl = girl

    def enter(self, e):
        pass

    def exit(self):
        pass

    def do(self):
        pass

    def draw(self):
        pass
class Skill_6:

    def __init__(self, girl):
        self.girl = girl

    def enter(self, e):
        pass

    def exit(self):
        pass

    def do(self):
        pass

    def draw(self):
        pass
class Skill_7:

    def __init__(self, girl):
        self.girl = girl

    def enter(self, e):
        pass

    def exit(self):
        pass

    def do(self):
        pass

    def draw(self):
        pass
class Skill_8:

    def __init__(self, girl):
        self.girl = girl

    def enter(self, e):
        pass

    def exit(self):
        pass

    def do(self):
        pass

    def draw(self):
        pass
class Skill_9:

    def __init__(self, girl):
        self.girl = girl

    def enter(self, e):
        pass

    def exit(self):
        pass

    def do(self):
        pass

    def draw(self):
        pass
class Skill_10:

    def __init__(self, girl):
        self.girl = girl

    def enter(self, e):
        pass

    def exit(self):
        pass

    def do(self):
        pass

    def draw(self):
        pass
class Skill_11:

    def __init__(self, girl):
        self.girl = girl

    def enter(self, e):
        pass

    def exit(self):
        pass

    def do(self):
        pass

    def draw(self):
        pass
class Skill_12:

    def __init__(self, girl):
        self.girl = girl

    def enter(self, e):
        pass

    def exit(self):
        pass

    def do(self):
        pass

    def draw(self):
        pass
class Skill_13:

    def __init__(self, girl):
        self.girl = girl

    def enter(self, e):
        pass

    def exit(self):
        pass

    def do(self):
        pass

    def draw(self):
        pass
class Skill_14:

    def __init__(self, girl):
        self.girl = girl

    def enter(self, e):
        pass

    def exit(self):
        pass

    def do(self):
        pass

    def draw(self):
        pass
class Skill_15:

    def __init__(self, girl):
        self.girl = girl

    def enter(self, e):
        pass

    def exit(self):
        pass

    def do(self):
        pass

    def draw(self):
        pass
class Skill_16:

    def __init__(self, girl):
        self.girl = girl

    def enter(self, e):
        pass

    def exit(self):
        pass

    def do(self):
        pass

    def draw(self):
        pass
class Skill_17:

    def __init__(self, girl):
        self.girl = girl

    def enter(self, e):
        pass

    def exit(self):
        pass

    def do(self):
        pass

    def draw(self):
        pass
class Skill_18:

    def __init__(self, girl):
        self.girl = girl

    def enter(self, e):
        pass

    def exit(self):
        pass

    def do(self):
        pass

    def draw(self):
        pass
class Skill_19:

    def __init__(self, girl):
        self.girl = girl

    def enter(self, e):
        pass

    def exit(self):
        pass

    def do(self):
        pass

    def draw(self):
        pass
class Skill_20:

    def __init__(self, girl):
        self.girl = girl

    def enter(self, e):
        pass

    def exit(self):
        pass

    def do(self):
        pass

    def draw(self):
        pass
class Skill_21:

    def __init__(self, girl):
        self.girl = girl

    def enter(self, e):
        pass

    def exit(self):
        pass

    def do(self):
        pass

    def draw(self):
        pass

class Girl:

    def __init__(self):
        self.images = {
            'idle': ResourceManager.load_image('idle', 'stand.png'),
            'walk': ResourceManager.load_image('walk', 'walk.png'),
            'run': ResourceManager.load_image('run', 'run.png'),
            'skill_1': ResourceManager.load_image('normal_attack', 'normal_attack.png'),
            'skill_2': ResourceManager.load_image('skill2', 'skill2.png'),
            'skill_3': ResourceManager.load_image('skill3', 'skill3.png'),
            'skill_4': ResourceManager.load_image('skill4', 'skill4.png'),
            'skill_5': ResourceManager.load_image('skill5', 'skill5.png'),
            'skill_6': ResourceManager.load_image('skill6', 'skill6.png'),
            'skill_7': ResourceManager.load_image('skill7', 'skill7.png'),
            'skill_8': ResourceManager.load_image('skill8', 'skill8.png'),
            'skill_9': ResourceManager.load_image('skill9', 'skill9.png'),
            'skill_10': ResourceManager.load_image('skill10', 'skill10.png'),
            'skill_11': ResourceManager.load_image('skill11', 'skill11.png'),
            'skill_12': ResourceManager.load_image('skill12', 'skill12.png'),
            'skill_13': ResourceManager.load_image('skill13', 'skill13.png'),
            'skill_14': ResourceManager.load_image('skill14', 'skill14.png'),
            'skill_15': ResourceManager.load_image('skill15', 'skill15.png'),
            'skill_16': ResourceManager.load_image('skill16', 'skill16.png'),
            'skill_17': ResourceManager.load_image('skill17', 'skill17.png'),
            'skill_18': ResourceManager.load_image('skill18', 'skill18.png'),
            'skill_19': ResourceManager.load_image('skill19', 'skill19.png'),
            'skill_20': ResourceManager.load_image('skill20', 'skill20.png'),
            'skill_21': ResourceManager.load_image('skill21', 'skill21.png'),
        }

        self.x, self.y = 50, 120
        self.frame = 0
        self.face_dir = 1
        self.dir = 0

        self.IDLE = Idle(self)
        self.WALK = Walk(self)
        self.RUN = Run(self)
        self.SKILL_1 = Skill_1(self)
        self.JUMP = Jump(self)
        self.FALL = Fall(self)


        transitions = {
            self.IDLE: {
                right_double_tap: self.RUN,
                left_double_tap: self.RUN,
                right_down: self.WALK,
                left_down: self.WALK,
                q_down: self.SKILL_1
            },
            self.WALK: {
                right_double_tap: self.RUN,
                left_double_tap: self.RUN,
                right_up: self.IDLE,
                left_up: self.IDLE,
                q_down: self.SKILL_1
            },
            self.RUN: {
                right_up: self.IDLE,
                left_up: self.IDLE,
                q_down: self.SKILL_1
            },
            self.SKILL_1: {
                lambda e: True: self.IDLE
            },
            self.JUMP: {},
            self.FALL: {}
        }

        self.state_machine = StateMachine(self.IDLE, transitions)

    def get_image(self, key):
        return self.images.get(key)

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))


    def draw(self):
        self.state_machine.draw()

    def handle_collision(self, group, other):
        pass