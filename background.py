from pico2d import *

class Ground:
    def __init__(self):
        self.image = load_image('ground.png')

    def update(self):
        pass

    def draw(self):
        if self.image:
            try:
                self.image.draw(400, 60)
                self.image.draw(1200, 60)
            except Exception:
                self.image.draw(800, 60)


class Sky:
    def __init__(self):
        self.image = load_image('sky.png')

    def update(self):
        pass

    def draw(self):
        if self.image:
            try:
                self.image.draw(800, 400, 1600, 800)
            except Exception:
                self.image.draw(800, 400)