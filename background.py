from pico2d import *

class Ground:
    def __init__(self):
        self.image = load_image('ground.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(1600, 120)


class Sky:
    def __init__(self):
        self.image = load_image('sky.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(1600, 800)