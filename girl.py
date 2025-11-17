import os
from pico2d import load_image, get_time, load_font, draw_rectangle, close_canvas
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_q, SDLK_w, SDLK_c, SDLK_e, SDLK_r, SDLK_a, SDLK_s, SDLK_d, SDLK_f, SDLK_z, SDLK_x, SDLK_v, SDLK_t, SDLK_y, SDLK_g, SDLK_h, SDLK_b, SDLK_n, SDLK_m, SDLK_j

import game_world
import game_framework

from state_machine import StateMachine

right_pressed = False
left_pressed = False

def right_down(e):
    global right_pressed
    if e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT:
        right_pressed = True
        return True
    return False
def right_up(e):
    global right_pressed
    if e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT:
        right_pressed = False
        return True
    return False

def left_down(e):
    global left_pressed
    if e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT:
        left_pressed = True
        return True
    return False
def left_up(e):
    global left_pressed
    if e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT:
        left_pressed = False
        return True
    return False

def no_dir_key_pressed(e):
    return not right_pressed and not left_pressed

def any_dir_key_pressed(e):
    return right_pressed or left_pressed

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE
def space_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_SPACE

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
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_v
def v_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_v

def t_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_t
def t_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_t

def y_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_y
def y_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_y

def g_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_g
def g_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_g

def h_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_h
def h_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_h

def b_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_b
def b_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_b

def n_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_n
def n_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_n

def m_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_m
def m_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_m

def j_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_j
def j_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_j

def finish_to_idle_or_run(girl):
    if right_pressed and not left_pressed:
        girl.face_dir = 1
        girl.dir = 1
        girl.state_machine.change_state(girl.RUN)
    elif left_pressed and not right_pressed:
        girl.face_dir = -1
        girl.dir = -1
        girl.state_machine.change_state(girl.RUN)
    else:
        girl.state_machine.change_state(girl.IDLE)

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


class Run:
    IMAGE_KEY = 'run'

    def __init__(self, girl):
        self.girl = girl

    def enter(self, e):
        if getattr(self.girl, 'stop_after_jump', False):
            self.girl.stop_after_jump = False
            self.girl.dir = 0

            self.girl.state_machine.change_state(self.girl.IDLE)
            return

        if right_pressed:
            self.girl.dir = self.girl.face_dir = 1
        elif left_pressed:
            self.girl.dir = self.girl.face_dir = -1
        else:
            self.girl.dir = 0
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
    IMAGE_KEY_JUMP = 'jump'
    IMAGE_KEY_JUMPING = 'jumping'
    IMAGE_KEY_FALLING = 'falling'

    def __init__(self, girl):
        self.girl = girl
        self.initial_y = 0
        self.velocity_y = 0
        self.gravity = -2000  # 중력 가속도 (픽셀/초^2)
        self.jump_power = 900  # 초기 점프 속도 (픽셀/초)
        self.max_height_reached = False
        self.frame = 0.0
        self.dir_on_jump = 0
        self.started_with_dir = False
        self.released_during_jump = False

    def enter(self, e):
        self.initial_y = self.girl.y
        self.velocity_y = self.jump_power
        self.max_height_reached = False
        self.frame = 0.0

        if right_pressed:
            self.dir_on_jump = 1
            self.girl.face_dir = 1
        elif left_pressed:
            self.dir_on_jump = -1
            self.girl.face_dir = -1
        else:
            self.dir_on_jump = 0

        self.started_with_dir = (self.dir_on_jump != 0)
        self.released_during_jump = False
        self.girl.stop_after_jump = False

    def exit(self, e):
        pass

    def do(self):
        import game_framework

        self.velocity_y += self.gravity * game_framework.frame_time
        self.girl.y += self.velocity_y * game_framework.frame_time

        self.girl.x += self.dir_on_jump * RUN_SPEED_PPS * game_framework.frame_time

        if right_pressed and not left_pressed:
            self.girl.face_dir = 1
        elif left_pressed and not right_pressed:
            self.girl.face_dir = -1

        if self.started_with_dir and not (right_pressed or left_pressed) and self.girl.y > self.initial_y:
            self.released_during_jump = True
            self.girl.stop_after_jump = True

        if self.released_during_jump and (right_pressed or left_pressed):
            self.released_during_jump = False
            self.girl.stop_after_jump = False

        if self.velocity_y <= 0 and not self.max_height_reached:
            self.max_height_reached = True


        if self.girl.y <= self.initial_y:
            self.girl.y = self.initial_y
            self.girl.state_machine.change_state(self.girl.FALL)
            return


        current_image_key = self.get_current_image_key()
        img = self.girl.get_image(current_image_key)
        if img:
            frame_count = self.get_frame_count(current_image_key)
            self.frame = (self.frame + frame_count * ACTION_PER_TIME * 2.0 * game_framework.frame_time) % frame_count

    def get_current_image_key(self):
        if not self.max_height_reached:
            return self.IMAGE_KEY_JUMPING
        else:
            return self.IMAGE_KEY_FALLING

    def get_frame_count(self, image_key):

        frame_counts = {
            'jump': 2,
            'jumping': 1,
            'falling': 1
        }
        return frame_counts.get(image_key, 1)

    def draw(self):
        current_image_key = self.get_current_image_key()
        img = self.girl.get_image(current_image_key)
        if not img:
            return

        frame_count = self.get_frame_count(current_image_key)
        frame_w = img.w // frame_count
        frame_h = img.h

        frame = int(self.frame) % frame_count

        if self.girl.face_dir == 1:
            img.clip_draw(frame * frame_w, 0, frame_w, frame_h, self.girl.x, self.girl.y)
        else:
            img.clip_composite_draw(frame * frame_w, 0, frame_w, frame_h, 0, 'h',
                                    self.girl.x, self.girl.y, frame_w, frame_h)


class Fall:
    IMAGE_KEY = 'fall'

    def __init__(self, girl):
        self.girl = girl
        self.timer = 0.0
        self.playing = False

    def enter(self, e):
        self.girl.dir = 0
        self.girl.frame = 0.0
        self.timer = 0.0
        self.playing = True

    def exit(self, e):
        self.playing = False

    def do(self):
        import game_framework

        frame_count = self.get_frame_count()
        if self.playing:
            self.girl.frame += frame_count * ACTION_PER_TIME * 2.0 * game_framework.frame_time

        if self.girl.frame >= frame_count:
            self.girl.frame = frame_count - 1
            self.playing = False

            if getattr(self.girl, 'stop_after_jump', False):
                self.girl.stop_after_jump = False
                self.girl.dir = 0
                self.girl.state_machine.change_state(self.girl.IDLE)
            else:
                if any_dir_key_pressed(None):
                    self.girl.state_machine.change_state(self.girl.RUN)
                else:
                    self.girl.state_machine.change_state(self.girl.IDLE)

    def get_frame_count(self):
        return 2

    def draw(self):
        key = self.IMAGE_KEY
        img = self.girl.get_image(key)
        if not img:
            return

        frame_count = self.get_frame_count()
        frame_w = img.w // frame_count
        frame_h = img.h

        frame = int(min(self.girl.frame, frame_count - 1))

        if self.girl.face_dir == 1:
            img.clip_draw(frame * frame_w, 0, frame_w, frame_h, self.girl.x, self.girl.y)
        else:
            img.clip_composite_draw(frame * frame_w, 0, frame_w, frame_h, 0, 'h',
                                    self.girl.x, self.girl.y, frame_w, frame_h)

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
        frame_count = 14
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

        frame_count = 14
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
            'run': ResourceManager.load_image('run', 'run.png'),
            'jump': ResourceManager.load_image('jump', 'jump.png'),
            'jumping': ResourceManager.load_image('jumping', 'jumping.png'),
            'falling': ResourceManager.load_image('falling', 'falling.png'),
            'fall': ResourceManager.load_image('fall', 'fall.png'),
            'normal_attack': ResourceManager.load_image('normal_attack', 'normal_attack.png'),
            'strike': ResourceManager.load_image('strike', 'strike.png'),
            'spine_attack': ResourceManager.load_image('spine_attack', 'spine_attack.png'),
            'fast_attack': ResourceManager.load_image('fast_attack', 'fast_attack.png'),
            'stab': ResourceManager.load_image('stab', 'stab.png'),
            'weak_stab': ResourceManager.load_image('weak_stab', 'weak_stab.png'),
            'spine': ResourceManager.load_image('spine', 'spine.png'),
            'spine2': ResourceManager.load_image('spine2', 'spine2.png'),
            'attack': ResourceManager.load_image('attack', 'attack.png'),
            'magic': ResourceManager.load_image('magic', 'magic.png'),
            'strong_attack': ResourceManager.load_image('strong_attack', 'strong_attack.png'),
            'strong_magic' : ResourceManager.load_image('strong_magic', 'strong_magic.png'),
            'strong_magic2': ResourceManager.load_image('strong_magic2', 'strong_magic2.png'),
            'strong_spine': ResourceManager.load_image('strong_spine', 'strong_spine.png'),
            'strong_magic3': ResourceManager.load_image('strong_magic3', 'strong_magic3.png'),
            'cut': ResourceManager.load_image('cut', 'cut.png'),
            'cut2': ResourceManager.load_image('cut2', 'cut2.png'),
        }

        self.x, self.y = 50, 120
        self.frame = 0
        self.face_dir = 1
        self.dir = 0
        self.stop_after_jump = False

        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.JUMP = Jump(self)
        self.NORMAL_ATTACK = Normal_Attack(self)
        self.STRIKE = Strike(self)
        self.SPINE_ATTACK = Spine_Attack(self)
        self.FAST_ATTACK = Fast_Attack(self)
        self.STAB = Stab(self)
        self.WEAK_STAB = Weak_Stab(self)
        self.SPINE = Spine(self)
        self.SPINE2 = Spine2(self)
        self.ATTACK = Attack(self)
        self.MAGIC = Magic(self)
        self.STRONG_ATTACK = Strong_Attack(self)
        self.STRONG_MAGIC = Strong_Magic(self)
        self.STRONG_MAGIC2 = Strong_Magic2(self)
        self.STRONG_SPINE = Strong_Spine(self)
        self.STRONG_MAGIC3 = Strong_Magic3(self)
        self.CUT = Cut(self)
        self.CUT2 = Cut2(self)
        self.JUMP = Jump(self)
        self.FALL = Fall(self)


        transitions = {
            self.IDLE: {
                right_down: self.RUN,
                left_down: self.RUN,
                right_up: self.RUN,
                left_up: self.RUN,
                space_down: self.JUMP,
                q_down: self.NORMAL_ATTACK,
                w_down: self.STRIKE,
                e_down: self.SPINE_ATTACK,
                r_down: self.FAST_ATTACK,
                t_down: self.STAB,
                y_down: self.STRONG_MAGIC3,
                a_down: self.WEAK_STAB,
                s_down: self.CUT,
                d_down: self.SPINE,
                f_down: self.SPINE2,
                g_down: self.ATTACK,
                h_down: self.MAGIC,
                z_down: self.STRONG_ATTACK,
                x_down: self.STRONG_MAGIC,
                c_down: self.STRONG_MAGIC2,
                v_down: self.STRONG_SPINE,
                b_down: self.CUT2
            },

            self.RUN: {
                right_up: self.IDLE,
                left_up: self.IDLE,
                right_down: self.IDLE,
                left_down: self.IDLE,
                space_down: self.JUMP,
                q_down: self.NORMAL_ATTACK,
                w_down: self.STRIKE,
                e_down: self.SPINE_ATTACK,
                r_down: self.FAST_ATTACK,
                t_down: self.STAB,
                y_down: self.STRONG_MAGIC3,
                a_down: self.WEAK_STAB,
                s_down: self.CUT,
                d_down: self.SPINE,
                f_down: self.SPINE2,
                g_down: self.ATTACK,
                h_down: self.MAGIC,
                z_down: self.STRONG_ATTACK,
                x_down: self.STRONG_MAGIC,
                c_down: self.STRONG_MAGIC2,
                v_down: self.STRONG_SPINE,
                b_down: self.CUT2
            },
            self.JUMP: {

            },
            self.FALL: {

            },
            self.NORMAL_ATTACK: {},
            self.STRIKE: {},
            self.SPINE_ATTACK: {},
            self.FAST_ATTACK: {},
            self.STAB: {},
            self.WEAK_STAB: {},
            self.SPINE: {},
            self.SPINE2: {},
            self.ATTACK: {},
            self.MAGIC: {},
            self.STRONG_ATTACK: {},
            self.STRONG_MAGIC: {},
            self.STRONG_MAGIC2: {},
            self.STRONG_SPINE: {},
            self.STRONG_MAGIC3: {},
            self.CUT: {},
            self.CUT2: {}
        }

        self.state_machine = StateMachine(self.IDLE, transitions)

    def get_image(self, key):
        return self.images.get(key)

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        global right_pressed, left_pressed
        try:
            if event.type == SDL_KEYDOWN:
                if event.key == SDLK_RIGHT:
                    right_pressed = True
                elif event.key == SDLK_LEFT:
                    left_pressed = True
            elif event.type == SDL_KEYUP:
                if event.key == SDLK_RIGHT:
                    right_pressed = False
                elif event.key == SDLK_LEFT:
                    left_pressed = False
        except Exception:
            pass

        self.state_machine.handle_state_event(('INPUT', event))


    def draw(self):
        self.state_machine.draw()

    def handle_collision(self, group, other):
        pass