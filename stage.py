# File: `stage.py`
# 클래스: Stage
import random
import game_world

class Stage:
    def __init__(self, config):
        self.config = config
        self._objects = []  # game_world에 추가한 객체들 추적

    def enter(self, girl=None):

        try:
            from background import Sky, Ground
            sky = Sky()
            ground = Ground()
            game_world.add_object(sky, 0)
            game_world.add_object(ground, 0)
            self._objects.extend([sky, ground])
        except Exception:
            pass

        if girl is not None:
            sx, sy = self.config.get('player_start', (girl.x, girl.y))
            girl.x, girl.y = sx, sy

        try:
            from monster import create_goblin
            count = int(self.config.get('monster_count', 0))
            x0, x1 = self.config.get('x_range', (200, 1400))
            y_fixed = self.config.get('y_fixed', 40)
            for _ in range(count):
                x = random.randint(x0, x1)
                m = create_goblin(x, y_fixed)

                self._objects.append(m)
        except Exception:
            pass

    def exit(self):

        for o in list(self._objects):
            try:
                game_world.remove_object(o)
            except Exception:
                pass
        self._objects.clear()
