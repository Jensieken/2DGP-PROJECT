from pico2d import load_image

class StageManager:
    def __init__(self, stage_definitions, default_stage='stage1'):

        self.stages = stage_definitions
        self.current = None
        self._images = {}
        self.change_stage(default_stage)

    def _load_img(self, filename):
        if filename in self._images:
            return self._images[filename]
        img = load_image(filename)
        self._images[filename] = img
        return img

    def change_stage(self, name):
        if name not in self.stages:
            raise KeyError(f"stage {name} not found")
        self.current = self.stages[name]

        if 'background' in self.current:
            self.current['_bg_img'] = self._load_img(self.current['background'])
        if 'tilesheet' in self.current:
            self.current['_tiles_img'] = self._load_img(self.current['tilesheet'])

    def update(self, dt=0):
        pass

    def draw(self, camera_x=0, camera_y=0):
        if not self.current:
            return

        bg = self.current.get('_bg_img')
        if bg:
            bg.draw(bg.w // 2 - camera_x, bg.h // 2 - camera_y)

        tiles = self.current.get('_tiles_img')
        if tiles and 'map' in self.current:
            tw = self.current.get('tile_w', 64)
            th = self.current.get('tile_h', 64)
            tile_map = self.current['map']
            cols = tiles.w // tw
            for r, row in enumerate(tile_map):
                for c, tile_idx in enumerate(row):
                    if tile_idx is None or tile_idx < 0:
                        continue
                    sx = (tile_idx % cols) * tw
                    sy = (tile_idx // cols) * th
                    x = c * tw - camera_x + tw // 2
                    y = (len(tile_map) - 1 - r) * th - camera_y + th // 2
                    tiles.clip_draw(sx, sy, tw, th, x, y)

    def get_tile_at(self, col, row):
        m = self.current.get('map')
        if not m:
            return None
        if 0 <= row < len(m) and 0 <= col < len(m[0]):
            return m[row][col]
        return None
