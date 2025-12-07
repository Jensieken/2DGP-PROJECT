import random
from pico2d import *

import game_framework
import game_world

from girl import Girl
from monster import MonsterSpawner
from background import Ground, Sky

girl = None

game_over = False
game_over_timer = 0.0
_game_over_font = None

game_clear = False
game_clear_timer = 0.0
_game_clear_font = None

def _get_game_over_font():
    global _game_over_font
    if _game_over_font is None:
        try:
            base_dir = os.path.dirname(__file__)
            font_path = os.path.join(base_dir, 'ENCR10B.TTF')
            _game_over_font = load_font(font_path, 72)
        except Exception:
            try:
                _game_over_font = load_font(None, 72)
            except Exception:
                _game_over_font = None
    return _game_over_font

def _get_game_clear_font():
    global _game_clear_font
    if _game_clear_font is None:
        try:
            base_dir = os.path.dirname(__file__)
            font_path = os.path.join(base_dir, 'ENCR10B.TTF')
            _game_clear_font = load_font(font_path, 72)
        except Exception:
            try:
                _game_clear_font = load_font(None, 72)
            except Exception:
                _game_clear_font = None
    return _game_clear_font

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            global game_over
            if not game_over and girl:
                girl.handle_event(event)

def init():
    global girl


    sky = Sky()
    game_world.add_object(sky, 0)

    ground = Ground()
    game_world.add_object(ground, 0)

    girl = Girl()
    game_world.add_object(girl, 1)

    spawner = MonsterSpawner(count=4, x_range=(200, 1400), y_fixed=120)

def update():
    global game_over, game_over_timer
    import game_framework

    if not game_over:
        game_world.update()
        game_world.handle_collisions()

        if girl and getattr(girl, 'hp', 1) <= 0:
            game_over = True
            game_over_timer = 2.5
    else:
        game_over_timer -= game_framework.frame_time
        if game_over_timer <= 0.0:
            game_framework.quit()

def draw():
    clear_canvas()
    game_world.render()

    if game_over:
        try:
            font = _get_game_over_font()
            if font:
                text = 'GAME OVER'
                font.draw(800 - 220, 400, text, (255, 0, 0))
        except Exception:
            pass

    update_canvas()

def finish():
    game_world.clear()

def pause(): pass

def resume(): pass