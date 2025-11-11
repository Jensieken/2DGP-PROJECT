import os
from pico2d import load_image, get_time, load_font, draw_rectangle, close_canvas
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_q, SDLK_w, SDLK_c, SDLK_e, SDLK_r, SDLK_a, SDLK_s, SDLK_d, SDLK_f, SDLK_z, SDLK_x, SDLK_v, SDLK_t, SDLK_y, SDLK_g, SDLK_h, SDLK_b, SDLK_n, SDLK_m, SDLK_j

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

def w_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_w
def w_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_w

def e_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_e
def e_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_e

def r_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_r
def r_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_r

def a_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a
def a_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_a

def s_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_s
def s_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_s

def d_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_d
def d_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_d

def f_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_f
def f_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_f

def z_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_z
def z_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_z

def x_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_x
def x_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_x

def c_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_c
def c_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_c

def v_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_c
def v_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_c

def t_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_c
def t_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_c

def y_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_c
def y_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_c

def g_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_c
def g_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_c

def h_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_c
def h_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_c

def b_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_c
def b_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_c

def n_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_c
def n_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_c

def m_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_c
def m_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_c

def j_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_j
def j_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_j

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
class Normal_Attack:
    IMAGE_KEY = 'normal_attack'

    def __init__(self, girl):
        self.girl = girl
        self.timer = 0.0
        self.playing = False

    def enter(self, e):
        if e and e[0] == 'INPUT':
            event = e[1]
            if event.key == SDLK_RIGHT:
                self.girl.face_dir = 1
            elif event.key == SDLK_LEFT:
                self.girl.face_dir = -1

        self.girl.dir = 0
        self.girl.frame = 0.0
        self.timer = 0.0
        self.playing = True

    def exit(self, e):
        self.playing = False

    def do(self):
        frame_count = 7
        if self.playing:

            self.girl.frame += frame_count * ACTION_PER_TIME * game_framework.frame_time

        if self.girl.frame >= frame_count:

            self.girl.frame = frame_count - 1
            self.playing = False
            self.girl.state_machine.change_state(self.girl.IDLE)

    def draw(self):
        key = self.IMAGE_KEY
        img = self.girl.get_image(key)
        if not img:
            return

        frame_count = 7
        frame_w = img.w // frame_count
        frame_h = img.h

        frame = int(min(self.girl.frame, frame_count - 1))

        if self.girl.face_dir == 1:
            img.clip_draw(frame * frame_w, 0, frame_w, frame_h, self.girl.x, self.girl.y)
        else:
            img.clip_composite_draw(frame * frame_w, 0, frame_w, frame_h, 0, 'h', self.girl.x, self.girl.y, frame_w,
                                    frame_h)
class Strike:
    IMAGE_KEY = 'strike'

    def __init__(self, girl):
        self.girl = girl
        self.timer = 0.0
        self.playing = False

    def enter(self, e):
        if e and e[0] == 'INPUT':
            event = e[1]
            if event.key == SDLK_RIGHT:
                self.girl.face_dir = 1
            elif event.key == SDLK_LEFT:
                self.girl.face_dir = -1

        self.girl.dir = 0
        self.girl.frame = 0.0
        self.timer = 0.0
        self.playing = True

    def exit(self, e):
        self.playing = False

    def do(self):
        frame_count = 7
        if self.playing:
            self.girl.frame += frame_count * ACTION_PER_TIME * game_framework.frame_time

        if self.girl.frame >= frame_count:
            self.girl.frame = frame_count - 1
            self.playing = False
            self.girl.state_machine.change_state(self.girl.IDLE)

    def draw(self):
        key = self.IMAGE_KEY
        img = self.girl.get_image(key)
        if not img:
            return

        frame_count = 7
        frame_w = img.w // frame_count
        frame_h = img.h

        frame = int(min(self.girl.frame, frame_count - 1))

        if self.girl.face_dir == 1:
            img.clip_draw(frame * frame_w, 0, frame_w, frame_h, self.girl.x, self.girl.y)
        else:
            img.clip_composite_draw(frame * frame_w, 0, frame_w, frame_h, 0, 'h', self.girl.x, self.girl.y, frame_w,
                                    frame_h)

class Spine_Attack:
    IMAGE_KEY = 'spine_attack'

    def __init__(self, girl):
        self.girl = girl
        self.timer = 0.0
        self.playing = False

    def enter(self, e):
        if e and e[0] == 'INPUT':
            event = e[1]
            if event.key == SDLK_RIGHT:
                self.girl.face_dir = 1
            elif event.key == SDLK_LEFT:
                self.girl.face_dir = -1

        self.girl.dir = 0
        self.girl.frame = 0.0
        self.timer = 0.0
        self.playing = True

    def exit(self, e):
        self.playing = False

    def do(self):
        frame_count = 7
        if self.playing:
            self.girl.frame += frame_count * ACTION_PER_TIME * game_framework.frame_time

        if self.girl.frame >= frame_count:
            self.girl.frame = frame_count - 1
            self.playing = False
            self.girl.state_machine.change_state(self.girl.IDLE)

    def draw(self):
        key = self.IMAGE_KEY
        img = self.girl.get_image(key)
        if not img:
            return

        frame_count = 7
        frame_w = img.w // frame_count
        frame_h = img.h

        frame = int(min(self.girl.frame, frame_count - 1))

        if self.girl.face_dir == 1:
            img.clip_draw(frame * frame_w, 0, frame_w, frame_h, self.girl.x, self.girl.y)
        else:
            img.clip_composite_draw(frame * frame_w, 0, frame_w, frame_h, 0, 'h', self.girl.x, self.girl.y, frame_w,
                                    frame_h)

class Fast_Attack:
    IMAGE_KEY = 'fast_attack'

    def __init__(self, girl):
        self.girl = girl
        self.timer = 0.0
        self.playing = False

    def enter(self, e):
        if e and e[0] == 'INPUT':
            event = e[1]
            if event.key == SDLK_RIGHT:
                self.girl.face_dir = 1
            elif event.key == SDLK_LEFT:
                self.girl.face_dir = -1

        self.girl.dir = 0
        self.girl.frame = 0.0
        self.timer = 0.0
        self.playing = True

    def exit(self, e):
        self.playing = False

    def do(self):
        frame_count = 3
        if self.playing:
            self.girl.frame += frame_count * ACTION_PER_TIME * game_framework.frame_time

        if self.girl.frame >= frame_count:
            self.girl.frame = frame_count - 1
            self.playing = False
            self.girl.state_machine.change_state(self.girl.IDLE)

    def draw(self):
        key = self.IMAGE_KEY
        img = self.girl.get_image(key)
        if not img:
            return

        frame_count = 3
        frame_w = img.w // frame_count
        frame_h = img.h

        frame = int(min(self.girl.frame, frame_count - 1))

        if self.girl.face_dir == 1:
            img.clip_draw(frame * frame_w, 0, frame_w, frame_h, self.girl.x, self.girl.y)
        else:
            img.clip_composite_draw(frame * frame_w, 0, frame_w, frame_h, 0, 'h', self.girl.x, self.girl.y, frame_w,
                                    frame_h)

class Stab:
    IMAGE_KEY = 'stab'

    def __init__(self, girl):
        self.girl = girl
        self.timer = 0.0
        self.playing = False

    def enter(self, e):
        if e and e[0] == 'INPUT':
            event = e[1]
            if event.key == SDLK_RIGHT:
                self.girl.face_dir = 1
            elif event.key == SDLK_LEFT:
                self.girl.face_dir = -1

        self.girl.dir = 0
        self.girl.frame = 0.0
        self.timer = 0.0
        self.playing = True

    def exit(self, e):
        self.playing = False

    def do(self):
        frame_count = 10
        if self.playing:
            self.girl.frame += frame_count * ACTION_PER_TIME * game_framework.frame_time

        if self.girl.frame >= frame_count:
            self.girl.frame = frame_count - 1
            self.playing = False
            self.girl.state_machine.change_state(self.girl.IDLE)

    def draw(self):
        key = self.IMAGE_KEY
        img = self.girl.get_image(key)
        if not img:
            return

        frame_count = 10
        frame_w = img.w // frame_count
        frame_h = img.h

        frame = int(min(self.girl.frame, frame_count - 1))

        if self.girl.face_dir == 1:
            img.clip_draw(frame * frame_w, 0, frame_w, frame_h, self.girl.x, self.girl.y)
        else:
            img.clip_composite_draw(frame * frame_w, 0, frame_w, frame_h, 0, 'h', self.girl.x, self.girl.y, frame_w,
                                    frame_h)


class Dash:
    IMAGE_KEY = 'dash'

    def __init__(self, girl):
        self.girl = girl
        self.timer = 0.0
        self.playing = False

    def enter(self, e):
        if e and e[0] == 'INPUT':
            event = e[1]
            if event.key == SDLK_RIGHT:
                self.girl.face_dir = 1
            elif event.key == SDLK_LEFT:
                self.girl.face_dir = -1

        self.girl.dir = 0
        self.girl.frame = 0.0
        self.timer = 0.0
        self.playing = True

    def exit(self, e):
        self.playing = False

    def do(self):
        frame_count = 3
        if self.playing:
            self.girl.frame += frame_count * ACTION_PER_TIME * game_framework.frame_time

        if self.girl.frame >= frame_count:
            self.girl.frame = frame_count - 1
            self.playing = False
            self.girl.state_machine.change_state(self.girl.IDLE)

    def draw(self):
        key = self.IMAGE_KEY
        img = self.girl.get_image(key)
        if not img:
            return

        frame_count = 3
        frame_w = img.w // frame_count
        frame_h = img.h

        frame = int(min(self.girl.frame, frame_count - 1))

        if self.girl.face_dir == 1:
            img.clip_draw(frame * frame_w, 0, frame_w, frame_h, self.girl.x, self.girl.y)
        else:
            img.clip_composite_draw(frame * frame_w, 0, frame_w, frame_h, 0, 'h', self.girl.x, self.girl.y, frame_w,
                                    frame_h)

class Weak_Stab:
    IMAGE_KEY = 'weak_stab'

    def __init__(self, girl):
        self.girl = girl
        self.timer = 0.0
        self.playing = False

    def enter(self, e):
        if e and e[0] == 'INPUT':
            event = e[1]
            if event.key == SDLK_RIGHT:
                self.girl.face_dir = 1
            elif event.key == SDLK_LEFT:
                self.girl.face_dir = -1

        self.girl.dir = 0
        self.girl.frame = 0.0
        self.timer = 0.0
        self.playing = True

    def exit(self, e):
        self.playing = False

    def do(self):
        frame_count = 6
        if self.playing:
            self.girl.frame += frame_count * ACTION_PER_TIME * game_framework.frame_time

        if self.girl.frame >= frame_count:
            self.girl.frame = frame_count - 1
            self.playing = False
            self.girl.state_machine.change_state(self.girl.IDLE)

    def draw(self):
        key = self.IMAGE_KEY
        img = self.girl.get_image(key)
        if not img:
            return

        frame_count = 6
        frame_w = img.w // frame_count
        frame_h = img.h

        frame = int(min(self.girl.frame, frame_count - 1))

        if self.girl.face_dir == 1:
            img.clip_draw(frame * frame_w, 0, frame_w, frame_h, self.girl.x, self.girl.y)
        else:
            img.clip_composite_draw(frame * frame_w, 0, frame_w, frame_h, 0, 'h', self.girl.x, self.girl.y, frame_w,
                                    frame_h)

class Tumble:
    IMAGE_KEY = 'tumble'

    def __init__(self, girl):
        self.girl = girl
        self.timer = 0.0
        self.playing = False

    def enter(self, e):
        if e and e[0] == 'INPUT':
            event = e[1]
            if event.key == SDLK_RIGHT:
                self.girl.face_dir = 1
            elif event.key == SDLK_LEFT:
                self.girl.face_dir = -1

        self.girl.dir = 0
        self.girl.frame = 0.0
        self.timer = 0.0
        self.playing = True

    def exit(self, e):
        self.playing = False

    def do(self):
        frame_count = 4
        if self.playing:
            self.girl.frame += frame_count * ACTION_PER_TIME * game_framework.frame_time

        if self.girl.frame >= frame_count:
            self.girl.frame = frame_count - 1
            self.playing = False
            self.girl.state_machine.change_state(self.girl.IDLE)

    def draw(self):
        key = self.IMAGE_KEY
        img = self.girl.get_image(key)
        if not img:
            return

        frame_count = 4
        frame_w = img.w // frame_count
        frame_h = img.h

        frame = int(min(self.girl.frame, frame_count - 1))

        if self.girl.face_dir == 1:
            img.clip_draw(frame * frame_w, 0, frame_w, frame_h, self.girl.x, self.girl.y)
        else:
            img.clip_composite_draw(frame * frame_w, 0, frame_w, frame_h, 0, 'h', self.girl.x, self.girl.y, frame_w,
                                    frame_h)

class Spine:
    IMAGE_KEY = 'spine'

    def __init__(self, girl):
        self.girl = girl
        self.timer = 0.0
        self.playing = False

    def enter(self, e):
        if e and e[0] == 'INPUT':
            event = e[1]
            if event.key == SDLK_RIGHT:
                self.girl.face_dir = 1
            elif event.key == SDLK_LEFT:
                self.girl.face_dir = -1

        self.girl.dir = 0
        self.girl.frame = 0.0
        self.timer = 0.0
        self.playing = True

    def exit(self, e):
        self.playing = False

    def do(self):
        frame_count = 8
        if self.playing:
            self.girl.frame += frame_count * ACTION_PER_TIME * game_framework.frame_time

        if self.girl.frame >= frame_count:
            self.girl.frame = frame_count - 1
            self.playing = False
            self.girl.state_machine.change_state(self.girl.IDLE)

    def draw(self):
        key = self.IMAGE_KEY
        img = self.girl.get_image(key)
        if not img:
            return

        frame_count = 8
        frame_w = img.w // frame_count
        frame_h = img.h

        frame = int(min(self.girl.frame, frame_count - 1))

        if self.girl.face_dir == 1:
            img.clip_draw(frame * frame_w, 0, frame_w, frame_h, self.girl.x, self.girl.y)
        else:
            img.clip_composite_draw(frame * frame_w, 0, frame_w, frame_h, 0, 'h', self.girl.x, self.girl.y, frame_w,
                                    frame_h)

class Spine2:
    IMAGE_KEY = 'spine2'

    def __init__(self, girl):
        self.girl = girl
        self.timer = 0.0
        self.playing = False

    def enter(self, e):
        if e and e[0] == 'INPUT':
            event = e[1]
            if event.key == SDLK_RIGHT:
                self.girl.face_dir = 1
            elif event.key == SDLK_LEFT:
                self.girl.face_dir = -1

        self.girl.dir = 0
        self.girl.frame = 0.0
        self.timer = 0.0
        self.playing = True

    def exit(self, e):
        self.playing = False

    def do(self):
        frame_count = 7
        if self.playing:
            self.girl.frame += frame_count * ACTION_PER_TIME * game_framework.frame_time

        if self.girl.frame >= frame_count:
            self.girl.frame = frame_count - 1
            self.playing = False
            self.girl.state_machine.change_state(self.girl.IDLE)

    def draw(self):
        key = self.IMAGE_KEY
        img = self.girl.get_image(key)
        if not img:
            return

        frame_count = 7
        frame_w = img.w // frame_count
        frame_h = img.h

        frame = int(min(self.girl.frame, frame_count - 1))

        if self.girl.face_dir == 1:
            img.clip_draw(frame * frame_w, 0, frame_w, frame_h, self.girl.x, self.girl.y)
        else:
            img.clip_composite_draw(frame * frame_w, 0, frame_w, frame_h, 0, 'h', self.girl.x, self.girl.y, frame_w,
                                    frame_h)

class Attack:
    IMAGE_KEY = 'attack'

    def __init__(self, girl):
        self.girl = girl
        self.timer = 0.0
        self.playing = False

    def enter(self, e):
        if e and e[0] == 'INPUT':
            event = e[1]
            if event.key == SDLK_RIGHT:
                self.girl.face_dir = 1
            elif event.key == SDLK_LEFT:
                self.girl.face_dir = -1

        self.girl.dir = 0
        self.girl.frame = 0.0
        self.timer = 0.0
        self.playing = True

    def exit(self, e):
        self.playing = False

    def do(self):
        frame_count = 11
        if self.playing:
            self.girl.frame += frame_count * ACTION_PER_TIME * game_framework.frame_time

        if self.girl.frame >= frame_count:
            self.girl.frame = frame_count - 1
            self.playing = False
            self.girl.state_machine.change_state(self.girl.IDLE)

    def draw(self):
        key = self.IMAGE_KEY
        img = self.girl.get_image(key)
        if not img:
            return

        frame_count = 11
        frame_w = img.w // frame_count
        frame_h = img.h

        frame = int(min(self.girl.frame, frame_count - 1))

        if self.girl.face_dir == 1:
            img.clip_draw(frame * frame_w, 0, frame_w, frame_h, self.girl.x, self.girl.y)
        else:
            img.clip_composite_draw(frame * frame_w, 0, frame_w, frame_h, 0, 'h', self.girl.x, self.girl.y, frame_w,
                                    frame_h)

class Magic:
    IMAGE_KEY = 'magic'

    def __init__(self, girl):
        self.girl = girl
        self.timer = 0.0
        self.playing = False

    def enter(self, e):
        if e and e[0] == 'INPUT':
            event = e[1]
            if event.key == SDLK_RIGHT:
                self.girl.face_dir = 1
            elif event.key == SDLK_LEFT:
                self.girl.face_dir = -1

        self.girl.dir = 0
        self.girl.frame = 0.0
        self.timer = 0.0
        self.playing = True

    def exit(self, e):
        self.playing = False

    def do(self):
        frame_count = 4
        if self.playing:
            self.girl.frame += frame_count * ACTION_PER_TIME * game_framework.frame_time

        if self.girl.frame >= frame_count:
            self.girl.frame = frame_count - 1
            self.playing = False
            self.girl.state_machine.change_state(self.girl.IDLE)

    def draw(self):
        key = self.IMAGE_KEY
        img = self.girl.get_image(key)
        if not img:
            return

        frame_count = 4
        frame_w = img.w // frame_count
        frame_h = img.h

        frame = int(min(self.girl.frame, frame_count - 1))

        if self.girl.face_dir == 1:
            img.clip_draw(frame * frame_w, 0, frame_w, frame_h, self.girl.x, self.girl.y)
        else:
            img.clip_composite_draw(frame * frame_w, 0, frame_w, frame_h, 0, 'h', self.girl.x, self.girl.y, frame_w,
                                    frame_h)

class Strong_Attack:
    IMAGE_KEY = 'strong_attack'

    def __init__(self, girl):
        self.girl = girl
        self.timer = 0.0
        self.playing = False

    def enter(self, e):
        if e and e[0] == 'INPUT':
            event = e[1]
            if event.key == SDLK_RIGHT:
                self.girl.face_dir = 1
            elif event.key == SDLK_LEFT:
                self.girl.face_dir = -1

        self.girl.dir = 0
        self.girl.frame = 0.0
        self.timer = 0.0
        self.playing = True

    def exit(self, e):
        self.playing = False

    def do(self):
        frame_count = 7
        if self.playing:
            self.girl.frame += frame_count * ACTION_PER_TIME * game_framework.frame_time

        if self.girl.frame >= frame_count:
            self.girl.frame = frame_count - 1
            self.playing = False
            self.girl.state_machine.change_state(self.girl.IDLE)

    def draw(self):
        key = self.IMAGE_KEY
        img = self.girl.get_image(key)
        if not img:
            return

        frame_count = 7
        frame_w = img.w // frame_count
        frame_h = img.h

        frame = int(min(self.girl.frame, frame_count - 1))

        if self.girl.face_dir == 1:
            img.clip_draw(frame * frame_w, 0, frame_w, frame_h, self.girl.x, self.girl.y)
        else:
            img.clip_composite_draw(frame * frame_w, 0, frame_w, frame_h, 0, 'h', self.girl.x, self.girl.y, frame_w,
                                    frame_h)

class Strong_Magic:
    IMAGE_KEY = 'strong_magic'

    def __init__(self, girl):
        self.girl = girl
        self.timer = 0.0
        self.playing = False

    def enter(self, e):
        if e and e[0] == 'INPUT':
            event = e[1]
            if event.key == SDLK_RIGHT:
                self.girl.face_dir = 1
            elif event.key == SDLK_LEFT:
                self.girl.face_dir = -1

        self.girl.dir = 0
        self.girl.frame = 0.0
        self.timer = 0.0
        self.playing = True

    def exit(self, e):
        self.playing = False

    def do(self):
        frame_count = 13
        if self.playing:
            self.girl.frame += frame_count * ACTION_PER_TIME * game_framework.frame_time

        if self.girl.frame >= frame_count:
            self.girl.frame = frame_count - 1
            self.playing = False
            self.girl.state_machine.change_state(self.girl.IDLE)

    def draw(self):
        key = self.IMAGE_KEY
        img = self.girl.get_image(key)
        if not img:
            return

        frame_count = 13
        frame_w = img.w // frame_count
        frame_h = img.h

        frame = int(min(self.girl.frame, frame_count - 1))

        if self.girl.face_dir == 1:
            img.clip_draw(frame * frame_w, 0, frame_w, frame_h, self.girl.x, self.girl.y)
        else:
            img.clip_composite_draw(frame * frame_w, 0, frame_w, frame_h, 0, 'h', self.girl.x, self.girl.y, frame_w,
                                    frame_h)

class Strong_Magic2:
    IMAGE_KEY = 'strong_magic2'

    def __init__(self, girl):
        self.girl = girl
        self.timer = 0.0
        self.playing = False

    def enter(self, e):
        if e and e[0] == 'INPUT':
            event = e[1]
            if event.key == SDLK_RIGHT:
                self.girl.face_dir = 1
            elif event.key == SDLK_LEFT:
                self.girl.face_dir = -1

        self.girl.dir = 0
        self.girl.frame = 0.0
        self.timer = 0.0
        self.playing = True

    def exit(self):
        self.playing = False

    def do(self):
        frame_count = 8
        if self.playing:
            self.girl.frame += frame_count * ACTION_PER_TIME * game_framework.frame_time

        if self.girl.frame >= frame_count:
            self.girl.frame = frame_count - 1
            self.playing = False
            self.girl.state_machine.change_state(self.girl.IDLE)

    def draw(self, e):
        key = self.IMAGE_KEY
        img = self.girl.get_image(key)
        if not img:
            return

        frame_count = 8
        frame_w = img.w // frame_count
        frame_h = img.h

        frame = int(min(self.girl.frame, frame_count - 1))

        if self.girl.face_dir == 1:
            img.clip_draw(frame * frame_w, 0, frame_w, frame_h, self.girl.x, self.girl.y)
        else:
            img.clip_composite_draw(frame * frame_w, 0, frame_w, frame_h, 0, 'h', self.girl.x, self.girl.y, frame_w,
                                    frame_h)

class Strong_Spine:
    IMAGE_KEY = 'strong_spine'

    def __init__(self, girl):
        self.girl = girl
        self.timer = 0.0
        self.playing = False

    def enter(self, e):
        if e and e[0] == 'INPUT':
            event = e[1]
            if event.key == SDLK_RIGHT:
                self.girl.face_dir = 1
            elif event.key == SDLK_LEFT:
                self.girl.face_dir = -1

        self.girl.dir = 0
        self.girl.frame = 0.0
        self.timer = 0.0
        self.playing = True

    def exit(self, e):
        self.playing = False

    def do(self):
        frame_count = 9
        if self.playing:
            self.girl.frame += frame_count * ACTION_PER_TIME * game_framework.frame_time

        if self.girl.frame >= frame_count:
            self.girl.frame = frame_count - 1
            self.playing = False
            self.girl.state_machine.change_state(self.girl.IDLE)

    def draw(self):
        key = self.IMAGE_KEY
        img = self.girl.get_image(key)
        if not img:
            return

        frame_count = 9
        frame_w = img.w // frame_count
        frame_h = img.h

        frame = int(min(self.girl.frame, frame_count - 1))

        if self.girl.face_dir == 1:
            img.clip_draw(frame * frame_w, 0, frame_w, frame_h, self.girl.x, self.girl.y)
        else:
            img.clip_composite_draw(frame * frame_w, 0, frame_w, frame_h, 0, 'h', self.girl.x, self.girl.y, frame_w,
                                    frame_h)

class Strong_Magic3:
    IMAGE_KEY = 'strong_magic3'

    def __init__(self, girl):
        self.girl = girl
        self.timer = 0.0
        self.playing = False

    def enter(self, e):
        if e and e[0] == 'INPUT':
            event = e[1]
            if event.key == SDLK_RIGHT:
                self.girl.face_dir = 1
            elif event.key == SDLK_LEFT:
                self.girl.face_dir = -1

        self.girl.dir = 0
        self.girl.frame = 0.0
        self.timer = 0.0
        self.playing = True

    def exit(self, e):
        self.playing = False

    def do(self):
        frame_count = 13
        if self.playing:
            self.girl.frame += frame_count * ACTION_PER_TIME * game_framework.frame_time

        if self.girl.frame >= frame_count:
            self.girl.frame = frame_count - 1
            self.playing = False
            self.girl.state_machine.change_state(self.girl.IDLE)

    def draw(self):
        key = self.IMAGE_KEY
        img = self.girl.get_image(key)
        if not img:
            return

        frame_count = 13
        frame_w = img.w // frame_count
        frame_h = img.h

        frame = int(min(self.girl.frame, frame_count - 1))

        if self.girl.face_dir == 1:
            img.clip_draw(frame * frame_w, 0, frame_w, frame_h, self.girl.x, self.girl.y)
        else:
            img.clip_composite_draw(frame * frame_w, 0, frame_w, frame_h, 0, 'h', self.girl.x, self.girl.y, frame_w,
                                    frame_h)

class Step:
    IMAGE_KEY = 'step'

    def __init__(self, girl):
        self.girl = girl
        self.timer = 0.0
        self.playing = False

    def enter(self, e):
        if e and e[0] == 'INPUT':
            event = e[1]
            if event.key == SDLK_RIGHT:
                self.girl.face_dir = 1
            elif event.key == SDLK_LEFT:
                self.girl.face_dir = -1

        self.girl.dir = 0
        self.girl.frame = 0.0
        self.timer = 0.0
        self.playing = True

    def exit(self, e):
        self.playing = False

    def do(self):
        frame_count = 10
        if self.playing:
            self.girl.frame += frame_count * ACTION_PER_TIME * game_framework.frame_time

        if self.girl.frame >= frame_count:
            self.girl.frame = frame_count - 1
            self.playing = False
            self.girl.state_machine.change_state(self.girl.IDLE)

    def draw(self):
        key = self.IMAGE_KEY
        img = self.girl.get_image(key)
        if not img:
            return

        frame_count = 10
        frame_w = img.w // frame_count
        frame_h = img.h

        frame = int(min(self.girl.frame, frame_count - 1))

        if self.girl.face_dir == 1:
            img.clip_draw(frame * frame_w, 0, frame_w, frame_h, self.girl.x, self.girl.y)
        else:
            img.clip_composite_draw(frame * frame_w, 0, frame_w, frame_h, 0, 'h', self.girl.x, self.girl.y, frame_w,
                                    frame_h)

class Cut:
    IMAGE_KEY = 'cut'

    def __init__(self, girl):
        self.girl = girl
        self.timer = 0.0
        self.playing = False

    def enter(self, e):
        if e and e[0] == 'INPUT':
            event = e[1]
            if event.key == SDLK_RIGHT:
                self.girl.face_dir = 1
            elif event.key == SDLK_LEFT:
                self.girl.face_dir = -1

        self.girl.dir = 0
        self.girl.frame = 0.0
        self.timer = 0.0
        self.playing = True

    def exit(self, e):
        self.playing = False

    def do(self):
        frame_count = 2
        if self.playing:
            self.girl.frame += frame_count * ACTION_PER_TIME * game_framework.frame_time

        if self.girl.frame >= frame_count:
            self.girl.frame = frame_count - 1
            self.playing = False
            self.girl.state_machine.change_state(self.girl.IDLE)

    def draw(self):
        key = self.IMAGE_KEY
        img = self.girl.get_image(key)
        if not img:
            return

        frame_count = 2
        frame_w = img.w // frame_count
        frame_h = img.h

        frame = int(min(self.girl.frame, frame_count - 1))

        if self.girl.face_dir == 1:
            img.clip_draw(frame * frame_w, 0, frame_w, frame_h, self.girl.x, self.girl.y)
        else:
            img.clip_composite_draw(frame * frame_w, 0, frame_w, frame_h, 0, 'h', self.girl.x, self.girl.y, frame_w,
                                    frame_h)

class Cut2:
    IMAGE_KEY = 'cut2'

    def __init__(self, girl):
        self.girl = girl
        self.timer = 0.0
        self.playing = False

    def enter(self, e):
        if e and e[0] == 'INPUT':
            event = e[1]
            if event.key == SDLK_RIGHT:
                self.girl.face_dir = 1
            elif event.key == SDLK_LEFT:
                self.girl.face_dir = -1

        self.girl.dir = 0
        self.girl.frame = 0.0
        self.timer = 0.0
        self.playing = True

    def exit(self, e):
        self.playing = False

    def do(self):
        frame_count = 2
        if self.playing:
            self.girl.frame += frame_count * ACTION_PER_TIME * game_framework.frame_time

        if self.girl.frame >= frame_count:
            self.girl.frame = frame_count - 1
            self.playing = False
            self.girl.state_machine.change_state(self.girl.IDLE)

    def draw(self):
        key = self.IMAGE_KEY
        img = self.girl.get_image(key)
        if not img:
            return

        frame_count = 2
        frame_w = img.w // frame_count
        frame_h = img.h

        frame = int(min(self.girl.frame, frame_count - 1))

        if self.girl.face_dir == 1:
            img.clip_draw(frame * frame_w, 0, frame_w, frame_h, self.girl.x, self.girl.y)
        else:
            img.clip_composite_draw(frame * frame_w, 0, frame_w, frame_h, 0, 'h', self.girl.x, self.girl.y, frame_w,
                                    frame_h)



class Girl:

    def __init__(self):
        self.images = {
            'idle': ResourceManager.load_image('idle', 'stand.png'),
            'walk': ResourceManager.load_image('walk', 'walk.png'),
            'run': ResourceManager.load_image('run', 'run.png'),
            'normal_attack': ResourceManager.load_image('normal_attack', 'normal_attack.png'),
            'strike': ResourceManager.load_image('strike', 'strike.png'),
            'spine_attack': ResourceManager.load_image('spine_attack', 'spine_attack.png'),
            'fast_attack': ResourceManager.load_image('fast_attack', 'fast_attack.png'),
            'stab': ResourceManager.load_image('stab', 'stab.png'),
            'dash': ResourceManager.load_image('dash', 'dash.png'),
            'weak_stab': ResourceManager.load_image('weak_stab', 'weak_stab.png'),
            'tumble': ResourceManager.load_image('tumble', 'tumble.png'),
            'spine': ResourceManager.load_image('spine', 'spine.png'),
            'spine2': ResourceManager.load_image('spine2', 'spine2.png'),
            'attack': ResourceManager.load_image('attack', 'attack.png'),
            'magic': ResourceManager.load_image('magic', 'magic.png'),
            'strong_attack': ResourceManager.load_image('strong_attack', 'strong_attack.png'),
            'strong_magic' : ResourceManager.load_image('strong_magic', 'strong_magic.png'),
            'strong_magic2': ResourceManager.load_image('strong_magic2', 'strong_magic2.png'),
            'strong_spine': ResourceManager.load_image('strong_spine', 'strong_spine.png'),
            'strong_magic3': ResourceManager.load_image('strong_magic3', 'strong_magic3.png'),
            'step': ResourceManager.load_image('step', 'step.png'),
            'cut': ResourceManager.load_image('cut', 'cut.png'),
            'cut2': ResourceManager.load_image('cut2', 'cut2.png'),
        }

        self.x, self.y = 50, 120
        self.frame = 0
        self.face_dir = 1
        self.dir = 0

        self.IDLE = Idle(self)
        self.WALK = Walk(self)
        self.RUN = Run(self)
        self.NORMAL_ATTACK = Normal_Attack(self)
        self.STRIKE = Strike(self)
        self.SPINE_ATTACK = Spine_Attack(self)
        self.FAST_ATTACK = Fast_Attack(self)
        self.STAB = Stab(self)
        self.DASH = Dash(self)
        self.WEAK_STAB = Weak_Stab(self)
        self.TUMBLE = Tumble(self)
        self.SPINE = Spine(self)
        self.SPINE2 = Spine2(self)
        self.ATTACK = Attack(self)
        self.MAGIC = Magic(self)
        self.STRONG_ATTACK = Strong_Attack(self)
        self.STRONG_MAGIC = Strong_Magic(self)
        self.STRONG_MAGIC2 = Strong_Magic2(self)
        self.STRONG_SPINE = Strong_Spine(self)
        self.STRONG_MAGIC3 = Strong_Magic3(self)
        self.STEP = Step(self)
        self.CUT = Cut(self)
        self.CUT2 = Cut2(self)
        self.JUMP = Jump(self)
        self.FALL = Fall(self)


        transitions = {
            self.IDLE: {
                right_double_tap: self.RUN,
                left_double_tap: self.RUN,
                right_down: self.WALK,
                left_down: self.WALK,
                q_down: self.NORMAL_ATTACK,
                w_down: self.STRIKE,
                e_down: self.SPINE_ATTACK,
                r_down: self.FAST_ATTACK,
                t_down: self.STAB,
                y_down: self.DASH,
                a_down: self.WEAK_STAB,
                s_down: self.TUMBLE,
                d_down: self.SPINE,
                f_down: self.SPINE2,
                g_down: self.ATTACK,
                h_down: self.MAGIC,
                z_down: self.STRONG_ATTACK,
                x_down: self.STRONG_MAGIC,
                c_down: self.STRONG_MAGIC2,
                v_down: self.STRONG_SPINE,
                b_down: self.STEP,
                n_down: self.CUT,
                m_down: self.CUT2,
                j_down: self.STRONG_MAGIC3
            },
            self.WALK: {
                right_double_tap: self.RUN,
                left_double_tap: self.RUN,
                right_up: self.IDLE,
                left_up: self.IDLE,
                q_down: self.NORMAL_ATTACK,
                w_down: self.STRIKE,
                e_down: self.SPINE_ATTACK,
                r_down: self.FAST_ATTACK,
                t_down: self.STAB,
                y_down: self.DASH,
                a_down: self.WEAK_STAB,
                s_down: self.TUMBLE,
                d_down: self.SPINE,
                f_down: self.SPINE2,
                g_down: self.ATTACK,
                h_down: self.MAGIC,
                z_down: self.STRONG_ATTACK,
                x_down: self.STRONG_MAGIC,
                c_down: self.STRONG_MAGIC2,
                v_down: self.STRONG_SPINE,
                b_down: self.STEP,
                n_down: self.CUT,
                m_down: self.CUT2,
                j_down: self.STRONG_MAGIC3
            },
            self.RUN: {
                right_up: self.IDLE,
                left_up: self.IDLE,
                q_down: self.NORMAL_ATTACK,
                w_down: self.STRIKE,
                e_down: self.SPINE_ATTACK,
                r_down: self.FAST_ATTACK,
                t_down: self.STAB,
                y_down: self.DASH,
                a_down: self.WEAK_STAB,
                s_down: self.TUMBLE,
                d_down: self.SPINE,
                f_down: self.SPINE2,
                g_down: self.ATTACK,
                h_down: self.MAGIC,
                z_down: self.STRONG_ATTACK,
                x_down: self.STRONG_MAGIC,
                c_down: self.STRONG_MAGIC2,
                v_down: self.STRONG_SPINE,
                b_down: self.STEP,
                n_down: self.CUT,
                m_down: self.CUT2,
                j_down: self.STRONG_MAGIC3
            },
            self.NORMAL_ATTACK: {},
            self.STRIKE: {},
            self.SPINE_ATTACK: {},
            self.FAST_ATTACK: {},
            self.STAB: {},
            self.DASH: {},
            self.WEAK_STAB: {},
            self.TUMBLE: {},
            self.SPINE: {},
            self.SPINE2: {},
            self.ATTACK: {},
            self.MAGIC: {},
            self.STRONG_ATTACK: {},
            self.STRONG_MAGIC: {},
            self.STRONG_MAGIC2: {},
            self.STRONG_SPINE: {},
            self.STRONG_MAGIC3: {},
            self.STEP: {},
            self.CUT: {},
            self.CUT2: {},
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