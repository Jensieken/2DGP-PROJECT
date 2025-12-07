import os
from pico2d import load_image, get_time, load_font, draw_rectangle, close_canvas
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_q, SDLK_w, SDLK_i, SDLK_j, SDLK_g
from weapon import Weapon, WeaponManager
from weapons_config import create_default_weapon_manager


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

def i_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_i
def i_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_i

def j_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_j
def j_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_j

def g_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_g
def g_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_g


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
        frame_count = 11
        self.girl.frame = (self.girl.frame + frame_count * ACTION_PER_TIME * game_framework.frame_time) % frame_count

    def exit(self, e):
        pass

    def draw(self):
        key = self.IMAGE_KEY
        img = self.girl.get_image(key)
        if not img:
            return

        frame_count = 11
        frame_w = img.w // frame_count
        frame_h = img.h

        frame = int(self.girl.frame) % frame_count

        if self.girl.face_dir == 1:
            img.clip_draw(frame * frame_w, 0, frame_w, frame_h, self.girl.x, self.girl.y)
        else:
            img.clip_composite_draw(frame * frame_w, 0, frame_w, frame_h, 0, 'h', self.girl.x, self.girl.y, frame_w, frame_h)

        if hasattr(self.girl, 'weapon_manager'):
            self.girl.weapon_manager.draw(
                self.girl.x, self.girl.y, self.girl.face_dir,
                char_frame_index=self.girl.frame, char_frame_count=12, state_name='idle'
            )

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

        if hasattr(self.girl, 'weapon_manager'):
            self.girl.weapon_manager.draw(
                self.girl.x, self.girl.y, self.girl.face_dir,
                char_frame_index=self.girl.frame, char_frame_count=12, state_name='run'
            )

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
        self.in_air = False

    def enter(self, e):
        if e and e[0] == 'INPUT':
            event = e[1]
            if event.key == SDLK_RIGHT:
                self.girl.face_dir = 1
            elif event.key == SDLK_LEFT:
                self.girl.face_dir = -1

        ground_y = getattr(self.girl, 'ground_y', self.girl.y)
        self.in_air = self.girl.y > ground_y + 1

        if not self.in_air:
            self.girl.dir = 0
        self.girl.frame = 0.0
        self.timer = 0.0
        self.playing = True
        try:
            from monster import spawn_attack_hit
            spawn_attack_hit(self.girl.x, self.girl.y + 10, self.girl.face_dir)
        except Exception:
            pass

    def exit(self, e):
        self.playing = False
        self.in_air = False

    def do(self):
        import game_framework

        frame_count = 7
        if not self.playing:
            return

        if self.in_air:
            # Jump 물리를 위임하기 전 상태를 기록
            prev_state = getattr(self.girl.state_machine, 'current_state', None)
            try:
                self.girl.JUMP.do()
            except Exception:
                pass

            # Jump.do()가 상태를 변경했다면 더 이상 공격 상태에서 위치 덮어쓰지 않음
            curr_state = getattr(self.girl.state_machine, 'current_state', None)
            if curr_state is not None and curr_state is not prev_state and curr_state is not self.girl.NORMAL_ATTACK:
                self.playing = False
                return

            # 착지 허용 오차로 스냅 처리 (소수점/프레임 오차 방지)
            ground_y = getattr(self.girl, 'ground_y', 0)
            LAND_TOLERANCE = 1.0
            if self.girl.y <= ground_y + LAND_TOLERANCE:
                self.girl.y = ground_y
                self.playing = False
                # 착지 후 정상적인 지상 흐름으로 넘김
                self.girl.state_machine.change_state(self.girl.FALL)
                return

            # 공격 애니메이션 진행 (위치 업데이트는 Jump가 담당)
            self.girl.frame += frame_count * ACTION_PER_TIME * game_framework.frame_time
        else:
            # 지상 공격은 기존 로직 유지
            self.girl.frame += frame_count * ACTION_PER_TIME * game_framework.frame_time

        if self.girl.frame >= frame_count:
            self.girl.frame = frame_count - 1
            self.playing = False

            ground_y = getattr(self.girl, 'ground_y', 0)
            if self.girl.y > ground_y + 1:
                self.girl.state_machine.change_state(self.girl.FALL)
            else:
                finish_to_idle_or_run(self.girl)

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
            img.clip_composite_draw(frame * frame_w, 0, frame_w, frame_h, 0, 'h',
                                    self.girl.x, self.girl.y, frame_w, frame_h)

class Normal_Attack:
    IMAGE_KEY = 'normal_attack'

    def __init__(self, girl):
        self.girl = girl
        self.timer = 0.0
        self.playing = False
        self.in_air = False

    def enter(self, e):
        if e and e[0] == 'INPUT':
            event = e[1]
            if event.key == SDLK_RIGHT:
                self.girl.face_dir = 1
            elif event.key == SDLK_LEFT:
                self.girl.face_dir = -1

        ground_y = getattr(self.girl, 'ground_y', self.girl.y)
        self.in_air = self.girl.y > ground_y + 1

        if not self.in_air:
            self.girl.dir = 0

        self.girl.frame = 0.0
        self.timer = 0.0
        self.playing = True

        try:
            from monster import spawn_attack_hit
            spawn_attack_hit(self.girl.x, self.girl.y + 10, self.girl.face_dir)
        except Exception:
            pass

    def exit(self, e):
        self.playing = False
        self.in_air = False

    def do(self):
        import game_framework

        frame_count = 7
        if not self.playing:
            return

        if self.in_air:
            try:
                self.girl.JUMP.do()
            except Exception:
                pass

            ground_y = getattr(self.girl, 'ground_y', 0)
            if self.girl.y <= ground_y:
                self.playing = False
                return

            self.girl.frame += frame_count * ACTION_PER_TIME * game_framework.frame_time
        else:
            self.girl.frame += frame_count * ACTION_PER_TIME * game_framework.frame_time

        if self.girl.frame >= frame_count:
            self.girl.frame = frame_count - 1
            self.playing = False

            ground_y = getattr(self.girl, 'ground_y', 0)
            if self.girl.y > ground_y + 1:
                self.girl.state_machine.change_state(self.girl.FALL)
            else:
                finish_to_idle_or_run(self.girl)

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

        if hasattr(self.girl, 'weapon_manager'):
            self.girl.weapon_manager.draw(
                self.girl.x, self.girl.y, self.girl.face_dir,
                char_frame_index=self.girl.frame, char_frame_count=7, state_name='normal_attack'
            )


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
            finish_to_idle_or_run(self.girl)

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

            'magic': ResourceManager.load_image('magic', 'magic.png')

        }

        self.weapon_manager = create_default_weapon_manager()

        self.x, self.y = 50, 120
        self.ground_y = self.y
        self.frame = 0
        self.face_dir = 1
        self.dir = 0
        self.stop_after_jump = False
        self.hp = 100

        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.JUMP = Jump(self)
        self.FALL = Fall(self)
        self.NORMAL_ATTACK = Normal_Attack(self)
        self.MAGIC = Magic(self)



        transitions = {
            self.IDLE: {
                right_down: self.RUN,
                left_down: self.RUN,
                right_up: self.RUN,
                left_up: self.RUN,
                space_down: self.JUMP,
                q_down: self.NORMAL_ATTACK,
                w_down: self.MAGIC

            },

            self.RUN: {
                right_up: self.IDLE,
                left_up: self.IDLE,
                right_down: self.IDLE,
                left_down: self.IDLE,
                space_down: self.JUMP,
                q_down: self.NORMAL_ATTACK,
                w_down: self.MAGIC

            },
            self.JUMP: {
                q_down: self.NORMAL_ATTACK

            },
            self.FALL: {
                q_down: self.NORMAL_ATTACK

            },
            self.NORMAL_ATTACK: {},

            self.MAGIC: {}

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