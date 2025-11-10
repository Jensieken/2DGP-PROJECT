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
