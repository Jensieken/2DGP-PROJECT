import random
from pico2d import *

import game_framework
import game_world

from girl import Girl

girl = None

def handle_events():


def init():


def update():
    game_world.update()
    game_world.handle_collisions()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def finish():
    game_world.clear()

def pause(): pass

def resume(): pass