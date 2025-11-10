from pico2d import load_image, get_time, load_font, draw_rectangle, close_canvas
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT

import game_world
import game_framework

from state_machine import StateMachine

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

class Idle:

    def __init__(self, girl):
        self.girl = girl

    def enter(self, e):
        self.girl.dir = 0

    def do(self):
        pass

    def exit(self):
        pass

    def draw(self):
        pass

class Walk:

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

class Run:

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
class Jump:

class Fall:

class Skill_1:

class Skill_2:

class Skill_3:

class Skill_4:

class Skill_5:

class Skill_6:

class Skill_7:

class Skill_8:

class Skill_9:

class Skill_10:

class Skill_11:

class Skill_12:

class Skill_13:

class Skill_14:

class Skill_15:

class Skill_16:

class Skill_17:

class Skill_18:

class Skill_19:

class Skill_20:

class Skill_21:

class Girl:

